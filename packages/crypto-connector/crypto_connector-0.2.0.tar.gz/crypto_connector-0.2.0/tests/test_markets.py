import sys

import pytest

from crypto_connector.base.errors import ExchangeError, NotSupported
from crypto_connector.base.schemas import Market

# cannot currently run tests on github runners (because hosted in the US)
pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="tests for windows only"
)


def test_get_markets(exchanges):
    for _, exc in exchanges.items():
        markets = exc.get_markets()
        for market in markets[:10]:
            assert isinstance(Market.model_validate(market), Market)


def test_get_market_price(exchanges):
    for _, exc in exchanges.items():
        assert exc.get_market_price("BTCUSDT") > 0


class TestGetMarketInfoFunction:
    def test_get_market_info(self, exchanges):
        for _, exc in exchanges.items():
            market = exc.get_market_info("ETHUSDT")
            assert isinstance(Market.model_validate(market), Market)

    def test_get_market_info_lowercase_symbol(self, exchanges):
        for _, exc in exchanges.items():
            market = exc.get_market_info("ethusdt")
            assert isinstance(Market.model_validate(market), Market)

    def test_get_market_info_wrong_symbol(self, exchanges):
        for _, exc in exchanges.items():
            with pytest.raises(ExchangeError):
                exc.get_market_info("bababibi")

    def test_get_market_info_empty_symbol(self, exchanges):
        for _, exc in exchanges.items():
            with pytest.raises(ValueError):
                exc.get_market_info("")


def test_get_ohlcv(exchanges):
    ohlcv = exchanges["binance"].get_ohlcv("ETHUSDT")
    assert len(ohlcv) > 0

    ohlcv = exchanges["bybit"].get_ohlcv("ETHUSDT")
    assert len(ohlcv) > 0

    with pytest.raises(NotSupported):
        exchanges["htx"].get_ohlcv("ETHUSDT")


if __name__ == "__main__":
    pytest.main([__file__])
