import os
from abc import ABC, abstractmethod


class PricingEngine(ABC):
    @abstractmethod
    def get_price(self, sensor_type: str, quantity: int = 1) -> int:
        """Return price in satoshis."""
        ...


class FlatPricingEngine(PricingEngine):
    """Fixed price per reading, configured via PRICE_SATS env var."""

    def __init__(self, price_sats: int | None = None) -> None:
        if price_sats is not None:
            self._price = price_sats
        else:
            self._price = int(os.environ.get("PRICE_SATS", "150"))

    def get_price(self, sensor_type: str, quantity: int = 1) -> int:
        return self._price * quantity
