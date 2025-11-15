from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
from typing import Dict, List, Optional, Any

class BinanceClient:
    """基于官方 python-binance SDK 的增强客户端"""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = False, using_v2ray: int = 0,
                 v2ray_port: int = 10808):
        """
        初始化客户端
        """
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger = logging.getLogger(__name__)

        # 自动设置 recvWindow 避免 -1021
        self.client.recv_window = 60000  # 60秒宽容窗口

        if using_v2ray == 1:
            # 如果你有代理（强烈推荐！）
            self.client.proxies = {
                'http': f"http://127.0.0.1:{v2ray_port}",  # 你的代理端口
                'https': f"https://127.0.0.1:{v2ray_port}"
            }

        # 关键：强制同步一次服务器时间
        try:
            self.client.futures_time()
            self.logger.info("Binance 时间同步成功")
        except Exception as e:
            self.logger.warning(f"时间同步失败: {e}，但 recv_window 已放宽")

        # 在 Client 初始化后添加
        self.client.timeout = 60  # 增加到 60 秒

    # ========== 基础请求封装（自动处理 202、重试）==========

    def _call(self, func, *args, **kwargs):
        """统一调用，捕获异常"""
        try:
            return func(*args, **kwargs)
        except BinanceAPIException as e:
            raise Exception(f"API错误: {e.code} - {e.message}")
        except Exception as e:
            self.logger.error(f"未知错误: {e}")
            raise

    # ========== 账户信息 ==========

    def get_account_info(self) -> Dict:
        return self._call(self.client.get_account)

    def get_account_balance(self) -> List[Dict]:
        account = self.get_account_info()
        return account.get('balances', [])

    def get_asset_balance(self, asset: str) -> Dict:
        balances = self.get_account_balance()
        for b in balances:
            if b['asset'] == asset:
                return b
        return {'asset': asset, 'free': '0', 'locked': '0'}

    def get_futures_account_info(self) -> Dict:
        return self._call(self.client.futures_account)

    def get_futures_balance(self) -> List[Dict]:
        account = self.get_futures_account_info()
        return account.get('assets', [])

    def get_futures_positions(self) -> List[Dict]:
        return self._call(self.client.futures_position_information)

    def get_active_positions(self) -> List[Dict]:
        positions = self.get_futures_positions()
        return [p for p in positions if float(p.get('positionAmt', 0)) != 0]

    # ========== 市场数据 ==========

    def get_ticker_price(self, symbol: str = None) -> Dict:
        return self._call(self.client.get_symbol_ticker, symbol=symbol)

    def get_24h_ticker(self, symbol: str) -> Dict:
        return self._call(self.client.get_ticker, symbol=symbol)

    def get_klines(self, symbol: str, interval: str, limit: int = 100,
                   startTime: int = None, endTime: int = None) -> List:
        return self._call(self.client.get_klines, symbol=symbol, interval=interval,
                          limit=limit, startTime=startTime, endTime=endTime)

    def get_order_book(self, symbol: str, limit: int = 100) -> Dict:
        return self._call(self.client.get_order_book, symbol=symbol, limit=limit)

    # ========== 现货交易 ==========

    def create_spot_order(self, symbol: str, side: str, order_type: str,
                         quantity: float = None, price: float = None,
                         quote_order_qty: float = None,
                         time_in_force: str = 'GTC', **kwargs) -> Dict:
        return self._call(self.client.create_order,
                          symbol=symbol, side=side, type=order_type,
                          quantity=quantity, price=price,
                          quoteOrderQty=quote_order_qty,
                          timeInForce=time_in_force, **kwargs)

    def cancel_spot_order(self, symbol: str, order_id: int = None,
                         orig_client_order_id: str = None) -> Dict:
        return self._call(self.client.cancel_order,
                          symbol=symbol, orderId=order_id,
                          origClientOrderId=orig_client_order_id)

    def cancel_all_spot_orders(self, symbol: str) -> List[Dict]:
        return self._call(self.client.cancel_open_orders, symbol=symbol)

    def get_spot_order(self, symbol: str, order_id: int) -> Dict:
        return self._call(self.client.get_order, symbol=symbol, orderId=order_id)

    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        return self._call(self.client.get_open_orders, symbol=symbol)

    # ========== 合约交易 ==========

    def set_leverage(self, symbol: str, leverage: int) -> Dict:
        return self._call(self.client.futures_change_leverage,
                          symbol=symbol, leverage=leverage)

    def set_margin_type(self, symbol: str, margin_type: str) -> Dict:
        return self._call(self.client.futures_change_margin_type,
                          symbol=symbol, marginType=margin_type)

    def create_futures_order(self, symbol: str, side: str, order_type: str,
                            quantity: float = None, price: float = None,
                            position_side: str = 'BOTH',
                            reduce_only: bool = False,
                            time_in_force: str = 'GTC', **kwargs) -> Dict:
        if order_type == 'BUY':
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'positionSide': position_side,
                'quantity': quantity,
                'price': price,
                'timeInForce': time_in_force if order_type == 'LIMIT' else None
            }
        else:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'positionSide': position_side,
                'reduceOnly': str(reduce_only).lower(),
                'quantity': quantity,
                'price': price,
                'timeInForce': time_in_force if order_type == 'LIMIT' else None
            }
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)
        return self._call(self.client.futures_create_order, **params)

    def cancel_futures_order(self, symbol: str, order_id: int = None,
                            orig_client_order_id: str = None) -> Dict:
        return self._call(self.client.futures_cancel_order,
                          symbol=symbol, orderId=order_id,
                          origClientOrderId=orig_client_order_id)

    def cancel_all_futures_orders(self, symbol: str) -> Dict:
        return self._call(self.client.futures_cancel_all_open_orders, symbol=symbol)

    def get_futures_order(self, symbol: str, order_id: int) -> Dict:
        return self._call(self.client.futures_get_order, symbol=symbol, orderId=order_id)

    def get_futures_open_orders(self, symbol: str = None) -> List[Dict]:
        return self._call(self.client.futures_get_open_orders, symbol=symbol)

    # ========== 平仓便捷方法 ==========

    def close_position(self, symbol: str, position_side: str = 'BOTH') -> Dict:
        positions = self.get_futures_positions()
        for pos in positions:
            if pos['symbol'] != symbol or float(pos['positionAmt']) == 0:
                continue
            if position_side != 'BOTH' and pos.get('positionSide') != position_side:
                continue
            qty = abs(float(pos['positionAmt']))
            side = 'SELL' if float(pos['positionAmt']) > 0 else 'BUY'
            return self.create_futures_order(
                symbol=symbol, side=side, order_type='MARKET',
                quantity=qty, position_side=pos.get('positionSide', 'BOTH')
            )
        return {'msg': 'No position to close'}

    def close_all_positions(self, symbol: str = None) -> List[Dict]:
        positions = self.get_active_positions()
        results = []
        for pos in positions:
            if symbol and pos['symbol'] != symbol:
                continue
            try:
                self.cancel_all_futures_orders(pos['symbol'])
                close = self.close_position(pos['symbol'], pos.get('positionSide'))
                results.append({'symbol': pos['symbol'], 'result': close})
            except Exception as e:
                results.append({'symbol': pos['symbol'], 'error': str(e)})
        return results

    # ========== 余额 ==========

    def get_usdt_balance(self) -> float:
        bal = self.get_asset_balance('USDT')
        return float(bal.get('free', 0))

    def get_futures_usdt_balance(self) -> float:
        info = self.get_futures_account_info()
        return float(info.get('totalWalletBalance', 0))

    def get_futures_available_balance(self) -> float:
        info = self.get_futures_account_info()
        return float(info.get('availableBalance', 0))

    # ========== 高级功能 ==========

    def get_position_mode(self) -> Dict:
        return self._call(self.client.futures_position_side_dual)

    def set_position_mode(self, dual_side: bool) -> Dict:
        return self._call(self.client.futures_change_position_side_dual,
                          dualSidePosition=dual_side)

    def get_current_funding_rate(self, symbol: str) -> Dict:
        rates = self._call(self.client.futures_funding_rate, symbol=symbol, limit=1)
        return rates[0] if rates else {}

    def get_futures_exchange_info(self, symbol: str = None) -> Dict:
        info = self._call(self.client.futures_exchange_info)
        if symbol:
            return next((s for s in info['symbols'] if s['symbol'] == symbol), {})
        return info