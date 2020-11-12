import unittest
from bot_management.bot_manager import *
from downloader.global_variables import *
from time import sleep
import sys
import helpfull_functions


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

    def test_02_manager_invest_working(self):
        """tests if manager can send correct data"""
        bot_id = 505
        BotManager().run_bot(bot_id, self.api_key, self.api_secret, 2)
        sleep(1)
        self.assertEqual(array_with_my_data[0], bot_id)

    def test_01_manager_thread_working(self):
        """tests if manager can run multiple threads"""
        BotManager().run_bot(123456789, self.api_key, self.api_secret, 1)
        BotManager().run_bot(123456789, self.api_key, self.api_secret, 1)
        self.assertEqual(3, threading.active_count())

    def test_03_bot_invest(self):
        """tests if Buying works correctly"""
        self.assertEqual(None, Bot().switcher(-1, self.binance_client, 1, 'invest', 3))

    def test_04_bot_sell(self):
        """tests if selling works correctly"""
        self.assertEqual(None, Bot().switcher(-1, self.binance_client, 1, 'sell', 3))

    def test_05_transactions_logs(self):
        """tests if every bot action is logged to database"""
        client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")
        client.query('DELETE FROM bot_action')
        Bot().switcher(-1, self.binance_client, 1, 'invest', 3)
        self.assertEqual(self.influx_db_records(client), 'invest')


    def influx_db_records(self, client):
        """That Function helps with test_05_transactions_logs and is necessary for it to work"""
        results = client.query('SELECT action FROM bot_action')
        for measurement in results.get_points(measurement='bot_action'):
            return measurement['action']






