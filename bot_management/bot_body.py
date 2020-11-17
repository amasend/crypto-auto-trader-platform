from time import sleep, ctime
import helpfull_functions
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException


class Bot:

    def __init__(self, bot_id: int):
        self.running = True
        self.bot_id = bot_id

    def bot_inner_working(self,
                 bot_id: int,
                 binance_client: object,
                 influxdb_client: object,
                 amount: int,
                 symbol: str,
                 what_to_do: str = "waiting"):
        """based on information given
            id of the bot: bot_id
            logged with both key's client: binance_client
            amount of money/cryptocurrency: amount
            symbol of the transaction: symbol
            given action: what_to_do
            makes sell/buy request or waits
            and logs, what id did in influx database"""
        # next line connects to the testing servers of binance, should be commented when user usage start
        binance_client.API_URL = 'https://testnet.binance.vision/api'
        json_body = [
            {
                "measurement": "bot_action",
                "tags": {
                    "id": bot_id
                },
                "time": ctime(),
                "fields": {
                    "action": what_to_do,
                    "amount": amount
                }
            }]

        if what_to_do == "invest":
            try:
                buy_order = binance_client.create_order(
                    symbol=f'{symbol}',
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=amount)
                influxdb_client.write_points(json_body)
            except BinanceAPIException as e:
                return e
            except BinanceOrderException as e:
                return e

        elif what_to_do == "sell":
            try:
                buy_order = binance_client.create_order(
                    symbol=f'{symbol}',
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=amount)
                influxdb_client.write_points(json_body)
            except BinanceAPIException as e:
                print(e)
                return "e"
            except BinanceOrderException as e:
                print(e)
                return e

        else:
            influxdb_client.write_points(json_body)

    def start_bot(self, api_key: int, api_secret: int, symbol: str):
        """this function will use
            class object Bot and it's id
            user's not private exchange key: api_key
            user's private exchange key: api_secret
            to every minute start switcher function
            and depending on the decision given from AI(not implemented yet)
            invest/sell/wait. Test variable is only used in tests and not necessary"""

        binance_client = Client(api_key, api_secret)
        influxdb_client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")
        while self.running:
            print(self.bot_id)
            amount_from_AI = 1
            command_from_AI = "invest"
            Bot.bot_inner_working(self,
                                  self.bot_id,
                                  binance_client,
                                  influxdb_client,
                                  amount_from_AI,
                                  symbol,
                                  command_from_AI)
            sleep(60)
