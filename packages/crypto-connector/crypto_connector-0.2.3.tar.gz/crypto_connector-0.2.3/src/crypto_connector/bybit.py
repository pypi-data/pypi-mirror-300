import hashlib
import hmac
import json
import time
from datetime import datetime
from typing import Any, Literal

from requests import Response

from crypto_connector.base.errors import (
    BadResponse,
    ExchangeError,
    MissingCredentials,
    OrderNotFound,
)
from crypto_connector.base.exchange import Exchange
from crypto_connector.base.schemas import (
    API,
    Balance,
    BalanceAsset,
    Market,
    Order,
    OrderCancelled,
    OrderStatus,
    TranferStatus,
    Transfer,
)


class Bybit(Exchange):
    base_url = "https://api.bybit.com"
    name = "Bybit"
    order_statuses = {
        # v3 spot
        "NEW": OrderStatus.open,
        "PARTIALLY_FILLED": OrderStatus.open,
        "FILLED": OrderStatus.closed,
        "CANCELED": OrderStatus.canceled,
        "PENDING_CANCEL": OrderStatus.open,
        "PENDING_NEW": OrderStatus.open,
        "REJECTED": OrderStatus.rejected,
        "PARTIALLY_FILLED_CANCELLED": OrderStatus.closed,
        # v3 contract / unified margin / unified account
        "Created": OrderStatus.open,
        "New": OrderStatus.open,
        "Rejected": OrderStatus.rejected,
        "PartiallyFilled": OrderStatus.open,
        "PartiallyFilledCanceled": OrderStatus.closed,
        "Filled": OrderStatus.closed,
        "PendingCancel": OrderStatus.open,
        "Cancelled": OrderStatus.canceled,
        # below self line the status only pertains to conditional orders
        "Untriggered": OrderStatus.open,
        "Deactivated": OrderStatus.canceled,
        "Triggered": OrderStatus.open,
        "Active": OrderStatus.open,
    }
    transfer_statuses = {
        "SUCCESS": TranferStatus.success,
        "PENDING": TranferStatus.pending,
        "FAILED": TranferStatus.failed,
    }
    timeframes = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "1h": 60,
        "4h": 240,
        "1d": "D",
        "1w": "W",
        "1M": "M",
    }

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        headers: bool = False,
        **kwargs,
    ) -> None:
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = headers

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def hash(api_secret: str, query_str: str) -> str:
        hash_obj = hmac.new(
            key=api_secret.encode("utf-8"),
            msg=query_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        return hash_obj.hexdigest()

    @staticmethod
    def _cast_values(params: dict) -> dict:
        string_params = [
            "qty",
            "price",
            "triggerPrice",
            "takeProfit",
            "stopLoss",
        ]
        integer_params = ["positionIdx"]
        upper_params = ["symbol"]
        out: dict[str, Any] = {}
        for key, value in params.items():
            if key in string_params:
                if not isinstance(value, str):
                    out[key] = str(value)
            elif key in integer_params:
                if not isinstance(value, int):
                    out[key] = int(value)
            elif key in upper_params:
                out[key] = value.upper()
            else:
                out[key] = params[key]
        return out

    @staticmethod
    def _prepare_query_string(params: dict) -> str:
        payload = "&".join(
            [str(k) + "=" + str(v) for k, v in params.items() if v is not None]
        )
        return payload

    def _prepare_json_body(self, parameters: dict) -> str:
        cleaned_params = self._clean_none_values(parameters)
        casted_params = self._cast_values(cleaned_params)
        return json.dumps(casted_params)

    def signed_request(
        self,
        http_method: str,
        url_path: str,
        params: dict | None = None,
        data: dict | None = None,
    ) -> dict[str, Any]:
        if (not self.api_key) or (not self.api_secret):
            raise MissingCredentials(
                "To use private endpoints, user must pass credentials."
            )

        if params and data:
            raise ValueError("Can only pass `params` or `data`, but not both.")

        payload = params or data or {}
        if http_method == "GET":
            encoded_payload = self._prepare_query_string(payload)
        else:
            encoded_payload = self._prepare_json_body(payload)

        timestamp = self.get_timestamp()
        to_hash = (
            f"{self.get_timestamp()}"
            f"{self.api_key}"
            f"{self.recv_window}"
            f"{encoded_payload}"
        )
        signature = self.hash(self.api_secret, query_str=to_hash)  # type: ignore[arg-type]  # noqa: E501
        self.session.headers.update(
            {
                "X-BAPI-API-KEY": self.api_key,
                "X-BAPI-SIGN": signature,
                "X-BAPI-SIGN-TYPE": "2",
                "X-BAPI-TIMESTAMP": str(timestamp),
                "X-BAPI-RECV-WINDOW": str(self.recv_window),
            }
        )
        if http_method == "GET":
            url_path += "?" + encoded_payload
            return self.request(http_method, url_path=url_path, params=None)
        else:
            return self.request(http_method, url_path=url_path, data=encoded_payload)

    def handle_exception(self, r: Response) -> None:
        try:
            rjson = r.json()
        except json.JSONDecodeError:
            raise BadResponse(f"Could not decode response text: {r.text}")

        if (rjson.get("retMsg") == "OK") or (rjson.get("retCode") == 0):
            return

        error = {}
        error["error_code"] = rjson["retCode"]
        error["msg"] = rjson["retMsg"]
        if self.headers:
            error["headers"] = r.headers
        raise ExchangeError(error)

    ###############################
    # EXCHANGE SPECIFIC ENDPOINTS #
    ###############################
    @property
    def _account_id(self) -> int:
        return self.get_api_key_info()["info"]["userID"]

    #################
    # EXCHANGE INFO #
    #################
    def get_server_time(self) -> int:
        """
        Fetch the current timestamp in millisecondsfrom the exchange server.
        :see: https://bybit-exchange.github.io/docs/v5/market/time
        """
        r = self.request("GET", "/v5/market/time")
        # {
        #     "retCode": 0,
        #     "retMsg": "OK",
        #     "result": {
        #         "timeSecond": "1688639403",
        #         "timeNano": "1688639403423213947"
        #     },
        #     "retExtInfo": {},
        #     "time": 1688639403423
        # }
        return r.get("time", -1)

    # ###########
    # # ACCOUNT #
    # ###########
    def _parse_api_key_info(self, api_info: dict[str, Any]) -> dict[str, Any]:
        api_obj = API(
            created=api_info["createdAt"],
            timestamp=int(self.str_to_dt(api_info["createdAt"]).timestamp()),
            spot_enabled="SpotTrade" in api_info["permissions"]["Spot"],
            ip_restricted=len(api_info["ips"]) > 0,
            ips=api_info["ips"],
            info=api_info,
        )
        return api_obj.model_dump()

    def get_api_key_info(self) -> dict[str, Any]:
        """
        Return API KEY info of the current user.
        :see: https://bybit-exchange.github.io/docs/v5/user/apikey-info
        """
        r = self.signed_request("GET", "/v5/user/query-api")
        # {
        #     'result': {'affiliateID': 0,
        #               'apiKey': 'HLQISKDNRIKEFQJKJB',
        #               'createdAt': '2023-07-02T16:39:51Z',
        #               'deadlineDay': -2,
        #               'expiredAt': '1970-01-01T00:00:00Z',
        #               'id': '22879041',
        #               'inviterID': 0,
        #               'ips': [],
        #               'isMaster': False,
        #               'kycLevel': 'LEVEL_DEFAULT',
        #               'kycRegion': '',
        #               'mktMakerLevel': '0',
        #               'note': 'BYBIT_APIKEY',
        #               'parentUid': '00000000',
        #               'permissions': {'Affiliate': [],
        #                               'BlockTrade': [],
        #                               'ContractTrade': ['Order', 'Position'],
        #                               'CopyTrading': [],
        #                               'Derivatives': ['DerivativesTrade'],
        #                               'Exchange': ['ExchangeHistory'],
        #                               'NFT': [],
        #                               'Options': ['OptionsTrade'],
        #                               'Spot': ['SpotTrade'],
        #                               'Wallet': ['AccountTransfer',
        #                                          'SubMemberTransferList']},
        #               'readOnly': 0,
        #               'rsaPublicKey': '',
        #               'secret': '',
        #               'type': 1,
        #               'unified': 0,
        #               'userID': 00000000,
        #               'uta': 1,
        #               'vipLevel': 'No VIP'},
        #     'retCode': 0,
        #     'retExtInfo': {},
        #     'retMsg': '',
        #     'time': 1716587467392
        #  }
        api_key_info = self._parse_api_key_info(r["result"])
        return api_key_info

    def _get_balance_value(self):
        """Get balance value in dollars.
        :see: https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        params = {"accountType": "UNIFIED"}
        r = self.signed_request("GET", "/v5/account/wallet-balance", params=params)
        balance_usd = r["result"]["list"][0]["totalEquity"]
        return float(balance_usd)

    @staticmethod
    def _parse_balance_asset(asset: dict[str, Any]) -> BalanceAsset:
        return BalanceAsset(
            coin=asset["coin"],
            free=asset["transferBalance"],
            total=asset["walletBalance"],
        )

    def get_balance(self) -> dict:
        """Query for balance and get the amount of funds available for trading
        or funds locked in orders.
        :see: https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        params = {"accountType": "UNIFIED"}
        r = self.signed_request(
            "GET",
            "/v5/asset/transfer/query-account-coins-balance",
            params=params,
        )
        balance_assets = []
        for raw_asset in r["result"]["balance"]:
            asset = self._parse_balance_asset(raw_asset)
            if asset.total == 0:
                continue
            balance_assets.append(asset)
        balance_usd = self._get_balance_value()
        balance = Balance(equity=balance_usd, assets=balance_assets)
        return balance.model_dump()

    def _parse_transfer(self, transfer: dict[str, Any]) -> dict[str, Any]:
        tr = Transfer(
            date=transfer["timestamp"],
            status=self.transfer_statuses[transfer["status"]],
            from_id=transfer["fromMemberId"],
            to_id=transfer["toMemberId"],
            direction=("in" if transfer["toMemberId"] == self._account_id else "out"),
            coin=transfer["coin"],
            qty=transfer["amount"],
            info=transfer,
        )
        return tr.model_dump()

    def get_transfer_history(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        Return transfer history (in and out) of the current account.
        :see: https://bybit-exchange.github.io/docs/v5/asset/unitransfer-list
        """
        params = {**kwargs}
        if start_date:
            params.update({"startTime": self.dt_to_unix(start_date)})
        if end_date:
            params.update({"endTime": self.dt_to_unix(end_date)})
        r = self.signed_request(
            "GET",
            "/v5/asset/transfer/query-universal-transfer-list",
            params=params,
        )
        # {'result': {'list': [{'amount': '30',
        #                       'coin': 'USDT',
        #                       'fromAccountType': 'FUND',
        #                       'fromMemberId': '01234567',
        #                       'status': 'SUCCESS',
        #                       'timestamp': '1716993775000',
        #                       'toAccountType': 'UNIFIED',
        #                       'toMemberId': '012345678',
        #                       'transferId': 'uni_trans_xxx'}],
        #             'nextPageCursor': 'eyxxxxxxxx=='},
        #  'retCode': 0,
        #  'retExtInfo': {},
        #  'retMsg': 'success',
        #  'time': 1718118312302}
        transfers = [self._parse_transfer(tr) for tr in r["result"]["list"]]
        return transfers

    # ###########
    # # MARKETS #
    # ###########
    def _parse_market(self, market) -> dict[str, Any]:
        market_obj = Market(
            name=market["symbol"],
            active=market["status"] == "Trading",
            base=market["baseCoin"],
            info=market,
            min_amt=market["lotSizeFilter"]["minOrderAmt"],
            min_qty=market["lotSizeFilter"]["minOrderQty"],
            precision=self.decimal_places(
                float(market["lotSizeFilter"]["basePrecision"])
            ),
            quote=market["quoteCoin"],
            spot=True,
        )
        return market_obj.model_dump()

    def get_markets(self, **kwargs) -> list[dict]:
        """
        Retrieves data on all SPOT markets.
        :see: https://bybit-exchange.github.io/docs/v5/market/instrument
        """
        params = {"category": "SPOT", **kwargs}
        r = self.request("GET", "/v5/market/instruments-info", params=params)
        # {
        #     "retCode": 0,
        #     "retMsg": "OK",
        #     "result": {
        #         "category": "spot",
        #         "list": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "baseCoin": "BTC",
        #                 "quoteCoin": "USDT",
        #                 "innovation": "0",
        #                 "status": "Trading",
        #                 "marginTrading": "both",
        #                 "lotSizeFilter": {
        #                     "basePrecision": "0.000001",
        #                     "quotePrecision": "0.00000001",
        #                     "minOrderQty": "0.000048",
        #                     "maxOrderQty": "71.73956243",
        #                     "minOrderAmt": "1",
        #                     "maxOrderAmt": "2000000"
        #                 },
        #                 "priceFilter": {
        #                     "tickSize": "0.01"
        #                 }
        #                 "riskParameters": {
        #                     "limitParameter": "0.05",
        #                     "marketParameter": "0.05"
        #                 }
        #             }
        #         ]
        #     },
        #     "retExtInfo": {},
        #     "time": 1672712468011
        # }
        markets = [self._parse_market(market) for market in r["result"]["list"]]
        return markets

    def get_market_info(self, market: str, **kwargs) -> dict[str, Any]:
        """
        Retrieves data on a specific market.
        :see: https://bybit-exchange.github.io/docs/v5/market/instrument
        """
        if not market:
            raise ValueError(f"`market` cannot be empty, value passed: '{market}'")

        params = {"category": "SPOT", "symbol": market, **kwargs}
        r = self.request("GET", "/v5/market/instruments-info", params=params)
        # {'result': {'category': 'SPOT',
        #             'list': [{'baseCoin': 'ETH',
        #                       'innovation': '0',
        #                       'lotSizeFilter': {'basePrecision': '0.00001',
        #                                         'maxOrderAmt': '4000000',
        #                                         'maxOrderQty': '1229.2336343',  # noqa: E501
        #                                         'minOrderAmt': '1',
        #                                         'minOrderQty': '0.00062',
        #                                         'quotePrecision': '0.0000001'},  # noqa: E501
        #                       'marginTrading': 'both',
        #                       'priceFilter': {'tickSize': '0.01'},
        #                       'quoteCoin': 'USDT',
        #                       'riskParameters': {'limitParameter': '0.03',
        #                                          'marketParameter': '0.03'},
        #                       'status': 'Trading',
        #                       'symbol': 'ETHUSDT'}]},
        #  'retCode': 0,
        #  'retExtInfo': {},
        #  'retMsg': 'OK',
        #  'time': 1717591248436}
        rslt = r["result"]["list"]
        if not rslt:
            raise ExchangeError("Empty response, make sure this market exists")

        parsed_market = self._parse_market(r["result"]["list"][0])
        return parsed_market

    def get_market_price(self, market: str) -> float:
        """
        Return the current price of a market.
        :see: https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        params = {"category": "spot", "symbol": market}
        r = self.request("GET", "/v5/market/tickers", params=params)
        # {
        #     "retCode": 0,
        #     "retMsg": "OK",
        #     "result": {
        #         "category": "spot",
        #         "list": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "bid1Price": "20517.96",
        #                 "bid1Size": "2",
        #                 "ask1Price": "20527.77",
        #                 "ask1Size": "1.862172",
        #                 "lastPrice": "20533.13",
        #                 "prevPrice24h": "20393.48",
        #                 "price24hPcnt": "0.0068",
        #                 "highPrice24h": "21128.12",
        #                 "lowPrice24h": "20318.89",
        #                 "turnover24h": "243765620.65899866",
        #                 "volume24h": "11801.27771",
        #                 "usdIndexPrice": "20784.12009279"
        #             }
        #         ]
        #     },
        #     "retExtInfo": {},
        #     "time": 1673859087947
        # }
        return float(r["result"]["list"][0]["lastPrice"])

    @staticmethod
    def _parse_ohlcv(data: list[list]) -> list[list]:
        return [
            [
                int(x[0]),
                float(x[1]),
                float(x[2]),
                float(x[3]),
                float(x[4]),
                float(x[5]),
            ]
            for x in data[::-1]
        ]

    def get_ohlcv(
        self,
        market: str,
        timeframe: str = "1d",
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        **kwargs,
    ) -> list[list]:
        """
        Fetch historical candlestick data containing
        the open, high, low, and close price, and the volume of a market.
        :see: https://bybit-exchange.github.io/docs/v5/market/kline
        """
        params = {
            "category": "spot",
            "symbol": market,
            "interval": self.timeframes[timeframe],
            **kwargs,
        }
        if start_date:
            params.update({"start": self.dt_to_unix(start_date)})
        if end_date:
            params.update({"end": self.dt_to_unix(end_date)})

        r = self.request("GET", "/v5/market/kline", params=params)
        # [
        #   [
        #     1499040000000,      // Kline open time
        #     "0.01634790",       // Open price
        #     "0.80000000",       // High price
        #     "0.01575800",       // Low price
        #     "0.01577100",       // Close price
        #     "148976.11427815",  // Volume
        #     1499644799999,      // Kline Close time
        #     "2434.19055334",    // Quote asset volume
        #     308,                // Number of trades
        #     "1756.87402397",    // Taker buy base asset volume
        #     "28.46694368",      // Taker buy quote asset volume
        #     "0"                 // Unused field, ignore.
        #   ]
        # ]
        ohlcv = self._parse_ohlcv(r["result"]["list"])
        return ohlcv

    #########
    # ORDER #
    #########
    def _parse_order(self, order: dict[str, Any]) -> dict[str, Any]:
        order_obj = Order(
            amount=order["qty"],
            dt=order["createdTime"],
            orderId=order["orderId"],
            info=order,
            fee=None,
            filled=order["cumExecQty"],
            last_update_timestamp=order["updatedTime"],
            market=order["symbol"],
            price=order["price"],
            reduce_only=order["reduceOnly"],
            remaining=None,
            side=order["side"].lower(),
            status=self.order_statuses[order["orderStatus"]],
            time_in_force=order["timeInForce"],
            timestamp=order["createdTime"],
            type=order["orderType"].lower(),
        )
        return order_obj.model_dump()

    def get_order(self, id: str, market: str, **kwargs) -> dict[str, Any]:
        """
        Get information on an order made by the user.
        :see: https://bybit-exchange.github.io/docs/v5/order/order-list
        :see: https://bybit-exchange.github.io/docs/v5/order/open-order
        """
        params = {
            "category": "spot",
            "orderId": id,
            "symbol": market,
            **kwargs,
        }
        r = self.signed_request("GET", "/v5/order/history", params=params)
        if r["result"]["list"]:
            order = self._parse_order(r["result"]["list"][0])
            return order

        r = self.signed_request("GET", "/v5/order/realtime", params=params)
        if r["result"]["list"]:
            order = self._parse_order(r["result"]["list"][0])
            return order

        return {}

    def place_order(
        self,
        market: str,
        type: Literal["limit", "market"],
        side: Literal["buy", "sell"],
        qty: float,
        price: float | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Place an order.
        :see: https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        # the unit of qty is quote for market buy order, for others, it is base
        if (type.lower() == "market") and (side.lower() == "buy"):
            qty = self.compute_quote_qty(qty, market=market)

        data = {
            "category": "spot",
            "symbol": market,
            "side": side,
            "orderType": type,
            "qty": qty,
            "price": price,
            **kwargs,
        }
        r = self.signed_request("POST", "/v5/order/create", data=data)
        order = self.get_order(id=r["result"]["orderId"], market=market)
        return order

    # def _get_order_history(self, **kwargs) -> dict:
    #     """Query order history."""
    #     orders = []
    #     next_page_cursor = ""
    #     while True:
    #         r = self.client.get_order_history(
    #             category="spot", cursor=next_page_cursor, **kwargs
    #         )
    #         orders.extend(r["result"]["list"])
    #         next_page_cursor = r["result"]["nextPageCursor"]
    #         if not next_page_cursor:
    #             break
    #     return orders

    def get_open_orders(self, market: str | None = None, **kwargs) -> list[dict]:
        """
        Get all currently unfilled open orders.
        :see: https://bybit-exchange.github.io/docs/v5/order/open-order
        """
        params = {
            "category": "spot",
            "symbol": market,
            "openOnly": 0,
            **kwargs,
        }
        r = self.signed_request("GET", "/v5/order/realtime", params=params)
        # {'result': {'category': 'spot',
        #             'list': [{'activationPrice': '0',
        #                       'avgPrice': '0.00',
        #                       'basePrice': '3777.21',
        #                       'blockTradeId': '',
        #                       'cancelType': 'UNKNOWN',
        #                       'closeOnTrigger': False,
        #                       'createdTime': '1717150476055',
        #                       'cumExecFee': '0',
        #                       'cumExecQty': '0.00000',
        #                       'cumExecValue': '0.0000000',
        #                       'isLeverage': '0',
        #                       'lastPriceOnCreated': '',
        #                       'leavesQty': '0.01000',
        #                       'leavesValue': '10.0000000',
        #                       'marketUnit': '',
        #                       'orderId': '0123456789012345678',
        #                       'orderIv': '',
        #                       'orderLinkId': '0123454567812345678',
        #                       'orderStatus': 'New',
        #                       'orderType': 'Limit',
        #                       'placeType': '',
        #                       'positionIdx': 0,
        #                       'price': '1000.00',
        #                       'qty': '0.01000',
        #                       'reduceOnly': False,
        #                       'rejectReason': 'EC_NoError',
        #                       'side': 'Buy',
        #                       'slLimitPrice': '0',
        #                       'slTriggerBy': '',
        #                       'smpGroup': 0,
        #                       'smpOrderId': '',
        #                       'smpType': 'None',
        #                       'stopLoss': '0',
        #                       'stopOrderType': '',
        #                       'symbol': 'ETHUSDT',
        #                       'takeProfit': '0',
        #                       'timeInForce': 'GTC',
        #                       'tpLimitPrice': '0',
        #                       'tpTriggerBy': '',
        #                       'trailingPercentage': '0',
        #                       'trailingValue': '0',
        #                       'triggerBy': '',
        #                       'triggerDirection': 0,
        #                       'triggerPrice': '0.00',
        #                       'updatedTime': '1717150476057'}],
        #             'nextPageCursor': '01561561056165156156XXXXXX'},
        #  'retCode': 0,
        #  'retExtInfo': {},
        #  'retMsg': 'OK',
        #  'time': 1717150481105}
        orders = [self._parse_order(order) for order in r["result"]["list"]]
        return orders

    def cancel_order(self, id: str, **kwargs) -> dict[str, Any]:
        """
        Cancel an open order.
        :see: https://bybit-exchange.github.io/docs/v5/order/cancel-order
        """
        orders = self.get_open_orders()
        market = [order["market"] for order in orders if order["orderId"] == id]
        if not market:
            raise OrderNotFound(f"Could not find an open order with this id '{id}'")

        data = {
            "category": "spot",
            "orderId": id,
            "symbol": market[0],
            **kwargs,
        }
        r = self.signed_request("POST", "/v5/order/cancel", data=data)
        # {'result': {'orderId': '1700955526680286976',
        #             'orderLinkId': '1700955526680286977'},
        #  'retCode': 0,
        #  'retExtInfo': {},
        #  'retMsg': 'OK',
        #  'time': 1717505721947}
        order_obj = OrderCancelled(
            orderId=r["result"]["orderId"], success=(r["retMsg"] == "OK")
        )
        return order_obj.model_dump()

    def cancel_orders(
        self, market: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """
        Cancel all open orders.
        :see: https://bybit-exchange.github.io/docs/v5/order/cancel-all
        """
        data = {"category": "spot", "symbol": market, **kwargs}
        r = self.signed_request("POST", "/v5/order/cancel-all", data=data)
        # {'result': {'list': [{'orderId': '1700979197050361600',
        #                       'orderLinkId': '1700979197050361601'},
        #                      {'orderId': '1700977632994400000',
        #                       'orderLinkId': '1700977632994400001'},
        #                      {'orderId': '1700979427216987904',
        #                       'orderLinkId': '1700979427225376512'}],
        #             'success': '1'},
        #  'retCode': 0,
        #  'retExtInfo': {},
        #  'retMsg': 'OK',
        #  'time': 1717512055774}
        cancelled_orders = []
        for order in r["result"]["list"]:
            cancelled_orders.append(
                OrderCancelled(
                    orderId=order["orderId"], success=r["result"]["success"]
                ).model_dump()
            )
        return cancelled_orders
