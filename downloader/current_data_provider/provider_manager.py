import ccxt
import time


class CurrentDataProvider:

    def __init__(self, interval: int, exchange_name: str, crypto_symbol: str):
        """ Paramaters
            ------------
            timeframe: int required - interval between downloading data in seconds
            exchange_name: str required - name of cryptocurrency, e.g. 'binance'
            crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
        """
        self.interval = interval
        self.exchange_name = exchange_name.lower()
        self.exchange = getattr(ccxt, self.exchange_name)()  # creating instance of an exchange
        self.crypto_symbol = crypto_symbol

    def provide_current_data(self):
        while True:
            current_milliseconds = int(round(time.time() * 1000))
            current_milliseconds = current_milliseconds - current_milliseconds % 1000
            candles = self.exchange.fetch_ohlcv(self.crypto_symbol, '1m', limit=1,
                                                params={'startTime': current_milliseconds - 60000,
                                                        'endTime': current_milliseconds})
            candles[0].insert(0, self.crypto_symbol)
            candles[0][0] = candles[0][0].replace("/", "_")
            # save candles to influx database
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
