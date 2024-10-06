import os
from typing import Any

import pytest
from dotenv import load_dotenv

import crypto_connector as cc

load_dotenv()


@pytest.fixture(scope="session")
def exchanges() -> dict:
    exchanges: dict[str, Any] = {}
    exchanges["binance"] = cc.Binance(
        sub_api_key=os.getenv("BINANCE_SUB_API_KEY_TEST"),
        sub_api_secret=os.getenv("BINANCE_SUB_API_SECRET_TEST"),
        sub_email=os.getenv("BINANCE_SUB_EMAIL"),
        master_api_key=os.getenv("BINANCE_MASTER_API_KEY_TEST"),
        master_api_secret=os.getenv("BINANCE_MASTER_API_SECRET_TEST"),
    )
    exchanges["bybit"] = cc.Bybit(
        os.getenv("BYBIT_API_KEY_TEST"),
        os.getenv("BYBIT_API_SECRET_TEST"),
    )
    exchanges["htx"] = cc.HTX(
        os.getenv("HTX_API_KEY_TEST"),
        os.getenv("HTX_API_SECRET_TEST"),
    )
    return exchanges
