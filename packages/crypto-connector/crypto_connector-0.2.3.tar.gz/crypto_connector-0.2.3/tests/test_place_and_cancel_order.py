import sys

import pytest

pytestmark = pytest.mark.skip("skip this test for now")

# cannot currently run tests on github runners (because hosted in the US)
pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="tests for windows only"
)


def test_place_and_cancel_order(exchanges):
    for _, exc in exchanges.items():
        # delete all open orders first
        orders = exc.cancel_orders()
        assert isinstance(orders, list)

        # place order
        market = "XRPUSDC"
        order = exc.place_order(
            market,
            type="limit",
            side="buy",
            qty=15,
            price=round(exc.get_market_price(market) * 0.95, 2),
        )
        assert order.get("orderId") is not None

        # cancel it
        result = exc.cancel_order(order["orderId"])
        assert result["success"] is True


if __name__ == "__main__":
    pytest.main([__file__])
