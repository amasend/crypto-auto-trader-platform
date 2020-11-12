from time import sleep, ctime
import helpfull_functions
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from downloader.global_variables import *


class Bot:

    def switcher(self, bot_id, binance_client, amount, what_to_do="waiting", test="0"):
        """bot function that does all what bot does"""
        client = helpfull_functions.setup_client("localhost", "8086", "test_bot_logs")
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
            if test == 2:
                # only needed for tests
                array_with_my_data.append(bot_id)
            elif test == 3:
                try:
                    buy_order = binance_client.create_test_order(
                        symbol='BNBUSDT',
                        side=SIDE_BUY,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount)
                    client.write_points(json_body)
                except BinanceAPIException as e:
                    # error handling goes here
                    return e
                except BinanceOrderException as e:
                    # error handling goes here
                    return e
            else:
                try:
                    buy_order = binance_client.create_order(
                        symbol='BTCSDT',
                        side=SIDE_BUY,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount)
                    client.write_points(json_body)
                except BinanceAPIException as e:
                    # error handling goes here
                    print(e)
                    return 'insuficeint_funds'
                except BinanceOrderException as e:
                    # error handling goes here
                    print(e)
                    return 'command is writen wrong'

        elif what_to_do == "sell":
            if test == 3:
                # only needed for tests
                try:
                    buy_order = binance_client.create_test_order(
                        symbol='LTCUSDT',
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount)
                    client.write_points(json_body)
                except BinanceAPIException as e:
                    # error handling goes here
                    return e
                except BinanceOrderException as e:
                    # error handling goes here
                    return e
            else:
                try:
                    buy_order = binance_client.create_order(
                        symbol='BTCUSDT',
                        side=SIDE_SELL,
                        type=ORDER_TYPE_MARKET,
                        quantity=amount)
                    client.write_points(json_body)
                except BinanceAPIException as e:
                    # error handling goes here
                    return e
                except BinanceOrderException as e:
                    # error handling goes here
                    return e

        else:
            client.write_points(json_body)
            print("waiting")

    def start_bot(self, bot_id, api_key, api_secret, test):
        """bot function that loops it's work till told otherwise(not implemented yet)"""
        if test == 1:
            # only needed for tests
            sleep(5)
        elif test == 2:
            # only needed for tests
            binance_client = Client(api_key, api_secret)
            Bot.switcher(self, bot_id, binance_client, 1, "invest", test)
        else:
            binance_client = Client(api_key, api_secret)
            while True:
                amount_from_AI = 1
                command_from_AI = "invest"
                Bot.switcher(self, bot_id, binance_client, amount_from_AI, command_from_AI)
                sleep(30)

# on the spot starting bot for testing
# Bot().start_bot(11, 3)
# on the spot testing if influxdb got the logs about what bot have done
# print(helpfull_functions.reading_influxdb_query(
#     client=helpfull_functions.setup_client("localhost", "8086", "test_bot_logs"),
#     name_of_database="bot_action"))
