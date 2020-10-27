from downloader.history_downloader.history_manager import HistoryDownloader
from downloader.history_saver.save_manager import HistorySaver

bitcon_symbol = 'BTC/USDT'
exchange_name = 'binance'
bitcon_history = HistoryDownloader(exchange_name=exchange_name, crypto_symbol=bitcon_symbol).get_history()

# save bitcoin history to csv file
HistorySaver(bitcon_history).save_history_to_csv("test")
