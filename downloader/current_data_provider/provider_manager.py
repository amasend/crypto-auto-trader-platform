import ccxt
import time
import downloader.global_variables
from helpfull_functions import setup_producer


class CurrentDataProvider:

    def __init__(self, interval: int, exchange_name: str, crypto_symbol: str):
        """ init
            Paramaters
            ------------
            timeframe: int required - interval between downloading data in seconds
            exchange_name: str required - name of cryptocurrency, e.g. 'binance'
            crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
            year: int required - year from which we want to retrieve the data
        """
        self.interval = interval
        self.exchange_name = exchange_name.lower()
        self.exchange = getattr(ccxt, self.exchange_name)()  # creating instance of an exchange
        self.crypto_symbol = crypto_symbol

    def provide_current_data(self, test=0):
        """test variable defaults to 0 but is used in tests if set to 1"""
        while True:
            current_miliseconds = int(round(time.time() * 1000))
            current_miliseconds = current_miliseconds - current_miliseconds % 1000
            candles = self.exchange.fetch_ohlcv(self.crypto_symbol, '1m', limit=1,
                                                params={'startTime': current_miliseconds - 60000,
                                                        'endTime': current_miliseconds})

            candles[0].insert(0, self.crypto_symbol)
            candles[0][0] = candles[0][0].replace("/", "_")

            producer = setup_producer()

            producer.send('unittest', value=candles)
            if test == 1:
                downloader.global_variables.array_with_my_data.append(candles)
                return (downloader.global_variables.array_with_my_data)
            else:
                time.sleep(self.interval)


def download_current_data(exchange_name: str, crypto_symbol: str):
    """ this function downloads current cryptocurrency data
        Paramaters
        ------------
        exchange_name: str required - name of cryptocurrency, e.g. 'binance'
        crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
    """
    exchange = getattr(ccxt, exchange_name)()
    current_milliseconds = int(round(time.time() * 1000))
    current_milliseconds = current_milliseconds - current_milliseconds % 1000
    candles = exchange.fetch_ohlcv(crypto_symbol, '1m', limit=1,
                                   params={'startTime': current_milliseconds - 60000,
                                           'endTime': current_milliseconds})
    candles[0].insert(0, crypto_symbol)
    # save candles to influx database
    return candles[0]
    # time.sleep(self.interval)
