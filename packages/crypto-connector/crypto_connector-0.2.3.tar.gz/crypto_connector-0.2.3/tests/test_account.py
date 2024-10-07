import sys

import pytest

from crypto_connector.base.schemas import Balance

# cannot currently run tests on github runners (because hosted in the US)
pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="tests for windows only"
)


def test_get_api_key_info(exchanges):
    for _, exc in exchanges.items():
        info = exc.get_api_key_info()
        assert info["timestamp"] > 0


def test_get_balance(exchanges):
    for _, exc in exchanges.items():
        balance = exc.get_balance()
        assert Balance.model_validate(balance)
        assert balance["equity"] >= 0


def test_get_transfer_history(exchanges):
    for _, exc in exchanges.items():
        transfers = exc.get_transfer_history()
        assert isinstance(transfers, list)


if __name__ == "__main__":
    pytest.main([__file__])
