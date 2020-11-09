import unittest
from api.database.database_manager import create_user, DatabaseClient, authenticate_user, get_user_trades
import requests


class MyTestCase(unittest.TestCase):
    def test_is_user_created(self):
        client = DatabaseClient("users", "admin", "zaq1@WSX", "localhost")
        create_user_res = requests.post("http://localhost:5000/users",
                                        headers={"content-type": "text", "username": "test", "password": "test"})
        result = create_user_res.headers["result"]
        self.assertEqual(result, "User created", "Create user request should return 'User created'")

    def test_authenticate_user(self):
        client = DatabaseClient("crypto-trader", "admin", "zaq1@WSX", "localhost")
        user = authenticate_user(client.cursor, "wrong_username", 'wrong_password')
        self.assertEqual(user, "Username or password is incorrect",
                         "When user puts wrong data, the result should be 'Username or password is incorrect'")

    def test_is_user_trades_list(self):
        client = DatabaseClient("crypto-trader", "admin", "zaq1@WSX", "localhost")
        create_user_res = requests.post("http://localhost:5000/trades",
                                        headers={"content-type": "text", "username": "test", "password": "test"})
        user_trades = get_user_trades(client.cursor, "siema", "siema", "binance", "BTC/USDT")
        self.assertIsInstance(user_trades, list, "User trades should be type of list")

    def test_current_prices_code(self):
        params = {"crypto_symbol": "BTC_USDT", "exchange_name": "binance"}
        current_prices_res = requests.get("http://localhost:5000/current-prices", params=params)
        self.assertEqual(current_prices_res.status_code == 200, "Current prices should return code 200")


if __name__ == '__main__':
    unittest.main()
