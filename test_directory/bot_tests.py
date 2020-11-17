import unittest
from bot_management.bot_manager import *
from time import sleep
import sys
import helpfull_functions
from test_directory.my_keys import api_test_key,api_test_secret_key,binance_client


class TestConnection(unittest.TestCase):
    """Set of tests that will provide information about valorous parts of bot management and inner bot work"""

    def setUp(self):
        if not sys.warnoptions:
            """because of unresolved bug in python there were unnecessary warnings, documented online"""
            import warnings
            warnings.simplefilter("ignore")
        self.api_key = api_test_key()

        self.api_secret = api_test_secret_key()

        self.binance_client = binance_client()

        self.influxdb_client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")

    def test_01_manager_thread_working(self):
        """tests if manager can run multiple threads"""
        BotManager().run_bot(123456789, self.api_key, self.api_secret, 'BTCUSDT')
        BotManager().run_bot(12345678, self.api_key, self.api_secret, 'BTCUSDT')
        self.assertEqual(3, threading.active_count())
        BotManager().stop_bot(123456789)
        BotManager().stop_bot(12345678)

    def test_02_stopping_bot(self):
        """tests manager stop_bot function"""
        BotManager().run_bot(19, self.api_key, self.api_secret, 'BTCUSDT')
        BotManager().stop_bot(19)
        sleep(5)
        self.assertEqual(1, threading.active_count())

    def test_03_bot_invest(self):
        """tests if Buying works correctly"""
        my_bot = Bot(-1)
        self.assertEqual(None, my_bot.bot_inner_working(-1, self.binance_client, self.influxdb_client, 10, 'BTCUSDT',
                                                        'invest'))

    def test_04_bot_sell(self):
        """tests if selling works correctly"""
        my_bot = Bot(-1)
        try:
            self.assertEqual(None,
                         my_bot.bot_inner_working(-1, self.binance_client, self.influxdb_client, 1, 'BTCUSDT', 'sell'))
        except:
            self.assertEqual("e",
                             my_bot.bot_inner_working(-1, self.binance_client, self.influxdb_client, 1, 'BTCUSDT',
                                                      'sell'))

    def test_05_transactions_logs(self):
        """tests if every bot action is logged to database"""
        my_bot = Bot(-1)
        client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")
        client.query('DELETE FROM bot_action')
        my_bot.bot_inner_working(-1, self.binance_client, self.influxdb_client, 1, 'BTCUSDT', 'invest')
        self.assertEqual(self.influx_db_records(client), 'invest')

    def influx_db_records(self, client):
        """That Function helps with test_05_transactions_logs and is necessary for it to work"""
        results = client.query('SELECT action FROM bot_action')
        for measurement in results.get_points(measurement='bot_action'):
            return measurement['action']
