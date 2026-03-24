import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

import ib_async

from trade_crew.agents.execution_agent import execution_agent
from trade_crew.deps import TradingDeps

load_dotenv()


async def main() -> None:
    host = os.getenv("IBKR_HOST", "127.0.0.1")
    port = int(os.getenv("IBKR_PORT", "4002"))
    client_id = int(os.getenv("IBKR_CLIENT_ID", "1"))

    ib = ib_async.IB()

    logger.info("Connecting to IBKR at {}:{} (clientId={}) ...", host, port, client_id)
    await ib.connectAsync(host, port, clientId=client_id)
    logger.info("Connected to IBKR successfully.")

    try:
        deps = TradingDeps(ib=ib)
        result = await execution_agent.run(
            "Buy 10 shares of AAPL",
            deps=deps,
        )
        print(result.output)
    finally:
        ib.disconnect()
        logger.info("Disconnected from IBKR.")


if __name__ == "__main__":
    asyncio.run(main())
