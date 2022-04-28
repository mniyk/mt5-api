"""mt5.pyのunittest
"""
from datetime import datetime, timedelta
import logging
import unittest

from mt5.mt5 import Mt5


logging.basicConfig(
    level=logging.DEBUG,
    format='\t'.join([
        '%(asctime)s',
        '%(levelname)s',
        '%(filename)s',
        '%(funcName)s',
        '%(processName)s',
        '%(process)d',
        '%(threadName)s',
        '%(thread)d',
        '%(message)s']))

logger = logging.getLogger(__name__)


class TestMt5(unittest.TestCase):
    def setUp(self) -> None:
        self.api = Mt5()

        self.api.connect()

    def test_get_candles(self) -> None:
        from_datetime = datetime.now() + timedelta(days=1)

        candles = self.api.get_candles('USDJPY', 'H1', from_datetime, 10)

        logger.debug(candles)

    def test_get_pip(self) -> None:
        self.api.get_pip('EURUSD')

    def test_get_positions(self) -> None:
        self.api.get_positions('USDJPY')

    def test_send_order(self) -> None:
        response = self.api.send_order('USDJPY', 0.1, 1, 20)

    def test_set_profit_and_loss(self) -> None:
        response = self.api.send_order('USDJPY', 0.1, -1, 99)
        response = self.api.set_profit_and_loss(response.order, 100, 100)

    def tearDown(self) -> None:
        self.api.disconnect()
