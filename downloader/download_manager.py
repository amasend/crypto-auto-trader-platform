from downloader.history_downloader.history_manager import HistoryDownloader
from downloader.history_saver.save_manager import HistorySaver


class DownloadManager:
    def __init__(self, exchange_name: str, crypto_symbol: str, year: int, month: int, day: int):
        """ init
            Paramaters
            ------------
            exchange_name: str required - name of cryptocurrency, e.g. 'binance'
            crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
            year: int required - year from which we want to retrieve the data
            month: int required - month from which we want to retrieve the data
            dat: int required - day from which we want to retrieve the data
        """
        self.exchange_name = exchange_name.lower()
        self.crypto_symbol = crypto_symbol
        self.year = year
        self.month = month
        self.day = day

    def download_history(self):
        history_downloader = HistoryDownloader(self.exchange_name, self.crypto_symbol, self.year, self.month, self.day)
        crypto_history = history_downloader.get_history()
        HistorySaver(crypto_history).save_history()



""" Example od downloading data from 2020-10-26 to today
    DownloadManager('binance', 'BTC/USDT', 2020, 10, 26).download_history()
"""
DownloadManager('binance', 'BTC/USDT', 2020, 11, 8).download_history()
