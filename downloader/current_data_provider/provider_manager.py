import ccxt
import time


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

    def provide_current_data(self):
        while True:
            current_miliseconds = int(round(time.time() * 1000))
            current_miliseconds = current_miliseconds - current_miliseconds % 1000
            candles = self.exchange.fetch_ohlcv(self.crypto_symbol, '1m', limit=1,
                                                params={'startTime': current_miliseconds - 60000,
                                                        'endTime': current_miliseconds})  # one minute timeframe
            candles[0].insert(0, self.crypto_symbol)
            # save candles to influx database
            time.sleep(self.interval)
