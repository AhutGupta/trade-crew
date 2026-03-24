"""Pydantic models used by the trading crew."""
from pydantic import BaseModel, field_validator


class TradeOrder(BaseModel):
    """Represents a single trade order to be executed."""

    symbol: str
    qty: int
    side: str  # "BUY" or "SELL"

    @field_validator("symbol")
    @classmethod
    def symbol_must_be_valid(cls, v: str) -> str:
        stripped = v.strip().upper()
        if not stripped:
            raise ValueError("symbol must not be empty")
        if not stripped.isalpha():
            raise ValueError(f"symbol must contain only letters, got '{v}'")
        return stripped

    @field_validator("side")
    @classmethod
    def side_must_be_valid(cls, v: str) -> str:
        upper = v.upper()
        if upper not in {"BUY", "SELL"}:
            raise ValueError(f"side must be 'BUY' or 'SELL', got '{v}'")
        return upper

    @field_validator("qty")
    @classmethod
    def qty_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError(f"qty must be a positive integer, got {v}")
        return v
