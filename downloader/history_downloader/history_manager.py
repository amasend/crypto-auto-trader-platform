import ccxt
import time
from datetime import datetime


class HistoryDownloader:

    def __init__(self, exchange_name: str, crypto_symbol: str, year: int, month: int, day: int):
        """ init
            Paramaters
            ------------
            exchange_name: str required - name of cryptocurrency, e.g. 'binance'
            crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
            year: int required - year from which we want to retrieve the data
            month: int required - month from which we want to retrieve the data
            day: int required - day from which we want to retrieve the data
        """
        self.exchange_name = exchange_name.lower()
        self.crypto_symbol = crypto_symbol
        self.year = year
        self.month = month
        self.day = day
        self.exchange = getattr(ccxt, self.exchange_name)()  # creating instance of an exchange

    def get_history(self):
        current_miliseconds = int(round(time.time() * 1000))
        current_miliseconds = current_miliseconds - current_miliseconds % 1000

        now = datetime.now()

        given_date = datetime(self.year, self.month, self.day, now.hour, now.minute, now.second)
        given_miliseconds = int(given_date.timestamp() * 1000)

        days_back = int((current_miliseconds - given_miliseconds) / (3600 * 1000 * 24) * 2)

        if self.exchange.has['fetchOHLCV']:
            historical_data = []
            for i in range(1, days_back + 1):
                start_time = given_miliseconds + (i - 1) * 43200000
                end_time = given_miliseconds + i * 43200000
                candles = self.exchange.fetch_ohlcv(self.crypto_symbol, '1m', limit=720,
                                                    params={'startTime': start_time,
                                                            'endTime': end_time})
                for j in range(len(candles)):
                    candles[j].insert(0, self.crypto_symbol)
                    historical_data.append(candles[j])

        for data in historical_data:
            data[0] = data[0].replace("/", "_")
        return historical_data
