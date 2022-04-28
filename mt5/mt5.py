"""MT5を操作するためのモジュール
"""
from datetime import datetime
import logging

import MetaTrader5


logger = logging.getLogger(__name__)


class Mt5:
    """MT5を使用するためのクラス
    """
    def __init__(self, account_id: int=None, password: str=None) -> None:
        """初期化

        Args:
            account_id (int): アカウントID
            password (str): パスワード
        
        Examples:
            >>> api = Mt5(1111, 'password')
        """
        self.account_id = account_id
        self.password = password
        self.timeframes = {
            'm1': MetaTrader5.TIMEFRAME_M1,
            'm2': MetaTrader5.TIMEFRAME_M2,
            'm3': MetaTrader5.TIMEFRAME_M3,
            'm4': MetaTrader5.TIMEFRAME_M4,
            'm5': MetaTrader5.TIMEFRAME_M5,
            'm6': MetaTrader5.TIMEFRAME_M6,
            'm10': MetaTrader5.TIMEFRAME_M10,
            'm12': MetaTrader5.TIMEFRAME_M12,
            'm15': MetaTrader5.TIMEFRAME_M15,
            'm20': MetaTrader5.TIMEFRAME_M20,
            'm30': MetaTrader5.TIMEFRAME_M30,
            'h1': MetaTrader5.TIMEFRAME_H1,
            'h2': MetaTrader5.TIMEFRAME_H2,
            'h3': MetaTrader5.TIMEFRAME_H3,
            'h4': MetaTrader5.TIMEFRAME_H4,
            'h6': MetaTrader5.TIMEFRAME_H6,
            'h8': MetaTrader5.TIMEFRAME_H8,
            'h12': MetaTrader5.TIMEFRAME_H12,
            'd1': MetaTrader5.TIMEFRAME_D1,
            'w1': MetaTrader5.TIMEFRAME_W1,
            'mn1': MetaTrader5.TIMEFRAME_MN1}

        logger.debug({'success': True})

    @staticmethod
    def connect() -> None:
        """接続

        Examples:
            >>> api.connect()
        """
        if not MetaTrader5.initialize():
            MetaTrader5.shutdown()

            logger.indebugfo({'success': False})
        else:
            logger.debug({'success': True})

    @staticmethod
    def disconnect() -> None:
        """接続解除

        Examples:
            >>> api.disconnect()
        """
        MetaTrader5.shutdown()

        logger.debug({'success': True})
    
    def get_candles(
        self, 
        symbol: str, 
        timeframe: str, 
        from_datetime: datetime, 
        data_count: int):
        """終了日時とデータ数でのローソク足データの取得

        終了日時からデータ数分、以前のデータを取得する

        Args:
            symbol (str): 通貨ペア
            timeframe (str): ローソク足時間
            from_datetime (datetime): 終了日時
            data_count (int): データ数

        Returns:
            List: ローソク足データのリスト

        Examples:
            >>> from_datetime = datetime.now() + timedelta(days=1)
            >>> candles = api.get_candles('USDJPY', 'H1', from_datetime, 20)
        """
        candles = MetaTrader5.copy_rates_from(
            symbol.upper(), 
            self.timeframes[timeframe.lower()], 
            from_datetime, 
            data_count)

        candles = self.create_candles_dict(candles=candles)

        logger.debug({
            'success': True,
            'symbol': symbol,
            'timeframe': timeframe,
            'from_datetime': str(from_datetime),
            'data_count': data_count,
            'candles': {
                'start': candles[0]['time'], 
                'end': candles[-1]['time']}})

        return candles

    @staticmethod
    def create_candles_dict(candles):
        candles = [{
            'time': datetime.utcfromtimestamp(candle[0]),
            'open': candle[1],
            'high': candle[2],
            'low': candle[3],
            'close': candle[4],
            'volume': candle[5],
            'spread': candle[6]}
            for candle in candles]

        return candles

    @staticmethod
    def get_pip(symbol: str):
        """PIPの取得

        Args:
            symbol (str): 通貨ペア

        Return:
            str: PIP

        Examples:
            >>> pip = api.get_pip('USDJPY')
        """
        info = MetaTrader5.symbol_info(symbol)

        pip = info.point

        logger.debug({
            'success': True,
            'symbol': symbol,
            'pip': pip})
        
        return pip

    @staticmethod
    def get_positions(symbol: str=None, ticket: int=None):
        """ポジションの取得

        Args:
            symbol (str): 通貨ペア
            ticket (int): チケット

        Returns:
            Tuple: ポジション

        Examples:
            >>> app.get_positions(symbol='USDJPY')
            >>> app.get_positions(ticket=7873658)
        """
        if symbol:
            positions = MetaTrader5.positions_get(symbol=symbol.upper())
        elif ticket:
            positions = MetaTrader5.positions_get(ticket=ticket)

        logger.debug({
            'success': True,
            'symbol': symbol,
            'ticket': ticket,
            'positions': positions})

        return positions
    
    @staticmethod
    def send_order(
        symbol: str, 
        lot: int, 
        direction: int, 
        magic: int,
        deviation: int=10):
        """発注

        Args:
            symbol (str): 通貨ペア
            lot (int): 注文数
            direction (int): 売買方向
            magic (int): 取引方法のID
            deviation (int): スリッページ
        
        Returns
            OrderSendResult: 発注結果
        
        Examples:
            >>> response = api.send_order('USDJPY', 0.1, 1)
        """
        order_type = MetaTrader5.ORDER_TYPE_BUY if direction == 1 else MetaTrader5.ORDER_TYPE_SELL

        request = {
            'action': MetaTrader5.TRADE_ACTION_DEAL,
            'symbol': symbol.upper(),
            'volume': lot,
            'deviation': deviation,
            'type': order_type,
            'magic': magic,
            'type_time': MetaTrader5.ORDER_TIME_GTC,
            'type_filling': MetaTrader5.ORDER_FILLING_IOC}

        response = MetaTrader5.order_send(request)

        logger.debug({
            'success': True, 
            'symbol': symbol, 
            'lot': lot,
            'direction': direction,
            'magic': magic,
            'deviation': deviation,
            'response': response})

        return response

    def set_profit_and_loss(
        self, ticket: int, profit: int, loss: int):
        """ポジションの指値と逆指値を設定

        Args:
            ticket: チケット
            profit: 利益
            loss: 損失
        
        Returns:
            OrderSendResult: 設定結果

        Examples:
            >>> response = api.send_order('USDJPY', 0.1, 1)
            >>> response = api.set_profit_and_loss(response.order, 100, 100)
        """
        position = self.get_positions(ticket=ticket)

        price = position[0].price_open

        if position[0].type == 0:
            profit_price = price + (profit * 0.01)
            loss_price = price - (loss * 0.01)
        elif position[0].type == 1:
            profit_price = price - (profit * 0.01)
            loss_price = price + (loss * 0.01)
        
        request = {
            'action': MetaTrader5.TRADE_ACTION_SLTP,
            'position': ticket,
            'sl': loss_price,
            'tp': profit_price}

        response = MetaTrader5.order_send(request)

        logger.debug({
            'success': True, 
            'ticket': ticket, 
            'profit': profit,
            'loss': loss,
            'response': response})

        return response
