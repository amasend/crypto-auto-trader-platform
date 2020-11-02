import unittest
from downloader.download_manager import DownloadManager
from downloader.history_downloader.history_manager import HistoryDownloader
from downloader.history_saver.save_manager import HistorySaver


class DownloaderTest(unittest.TestCase):

    def test_downloaded_data_type(self):
        history_downloader = HistoryDownloader('binance', 'BTC/USDT', 2020, 10, 10)
        self.assertIsInstance(history_downloader.get_history(), list)

    def test_downloaded_data_length(self):
        cryptocurrency_data = HistoryDownloader('binance', 'BTC/USDT', 2020, 10, 10).get_history()
        for i in range(len(cryptocurrency_data)):
            self.assertTrue(len(cryptocurrency_data[i]) == 720, "Each 12-hour period should 720 data")

    def test_is_data_saved(self):
        cryptocurrency_data = HistoryDownloader('binance', 'BTC/USDT', 2020, 10, 10).get_history()
        self.assertTrue(HistorySaver(cryptocurrency_data).save_history() == 'Data saved',
                        "Data hasn't been saved")


if __name__ == '__main__':
    unittest.main()
