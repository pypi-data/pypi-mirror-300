import sys

import pytest

from crypto_connector.base.errors import ExchangeError
from crypto_connector.base.schemas import Order

# cannot currently run tests on github runners (because hosted in the US)
pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="tests for windows only"
)


def test_get_open_orders(exchanges):
    for _, exc in exchanges.items():
        orders = exc.get_open_orders()
        for order in orders:
            assert isinstance(Order.model_validate(order), Order)


class TestPlaceTestOrderFunction:
    def test_insufficient_balance_order(self, exchanges):
        for _, exc in exchanges.items():
            with pytest.raises(ExchangeError):
                exc.place_order(
                    "ETHUSDT", type="limit", side="buy", qty=1000, price=1000
                )

    def test_wrong_precision_order(self, exchanges):
        for _, exc in exchanges.items():
            with pytest.raises(ExchangeError):
                exc.place_order(
                    "ETHUSDT", type="limit", side="buy", qty=1e-09, price=1000
                )


if __name__ == "__main__":
    pytest.main([__file__])
