"""Execution agent: places trade orders via IBKR with a human-in-the-loop gate."""
import asyncio

from loguru import logger
from pydantic_ai import Agent, RunContext

import ib_async

from trade_crew.deps import TradingDeps
from trade_crew.models import TradeOrder

execution_agent: Agent[TradingDeps, str] = Agent(
    "openai:gpt-4o",
    deps_type=TradingDeps,
    system_prompt=(
        "You are a trading execution agent. "
        "When asked to trade, call the execute_order tool with the correct symbol, "
        "quantity, and side (BUY or SELL)."
    ),
)


@execution_agent.tool
async def execute_order(ctx: RunContext[TradingDeps], order: TradeOrder) -> str:
    """Execute a trade order after receiving explicit human approval.

    Args:
        ctx: The run context containing the IBKR connection.
        order: The trade order to execute.

    Returns:
        A string describing the outcome of the order.
    """
    logger.info(
        "Pending order: {} {} shares of {}",
        order.side,
        order.qty,
        order.symbol,
    )

    confirmation = (
        await asyncio.to_thread(
            input,
            f"Confirm order: {order.side} {order.qty} shares of {order.symbol}? [y/N]: ",
        )
    ).strip()

    if confirmation.lower() != "y":
        logger.warning("Order rejected by user: {} {} {}", order.side, order.qty, order.symbol)
        return f"Order cancelled: {order.side} {order.qty} {order.symbol}"

    contract = ib_async.Stock(order.symbol, "SMART", "USD")
    ib_order = ib_async.MarketOrder(order.side, order.qty)

    trade = ctx.deps.ib.placeOrder(contract, ib_order)
    logger.success(
        "Order placed | orderId={} | {} {} {}",
        trade.order.orderId,
        order.side,
        order.qty,
        order.symbol,
    )
    return (
        f"Order placed successfully: orderId={trade.order.orderId} "
        f"| {order.side} {order.qty} {order.symbol}"
    )
