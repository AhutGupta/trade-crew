"""Dependency injection containers for the trading crew."""
from dataclasses import dataclass

import ib_async


@dataclass
class TradingDeps:
    """Dependencies shared across trading agents."""

    ib: ib_async.IB
