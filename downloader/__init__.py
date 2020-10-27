from downloader.history_downloader import HistoryDownloader
from downloader.history_saver import HistorySaver
bitcon_symbol = 'BTC/USDT'
bitcon_history = HistoryDownloader(bitcon_symbol).get_history()

#save bitcoin history to csv file
HistorySaver(bitcon_history).save_history_to_csv("test")
