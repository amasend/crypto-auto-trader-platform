import unittest
import downloader.global_variables
from downloader.current_data_provider.provider_manager import CurrentDataProvider
from downloader.helpfull_functions import setup_producer, setup_consumer, setup_client
import downloader.current_data_provider.provider_manager
from history_writer.history_writer import write_data_from_kafka


class TestConnection(unittest.TestCase):
    """Set of tests that will provide information about connection between data sources.
        Tests involving Kafka should not be run at the same time and interval between
        Kafka test should last at least 3600ms otherwise results could be inaccurate.
        If Apache Kafka is not running it is advised to comment setUp"""

    def setUp(self):
        self.consumer = setup_consumer('unittest', True)

        self.producer = setup_producer()

    def tearDown(self):
        pass

    def test_downloader_to_kafka(self):
        """Works only if both Binance API is sending information's and Kafka is receiving the same information's
            if test passes Kafka got the same information, which Binance send"""
        CurrentDataProvider(60, 'binance', 'BTC/USDT').provide_current_data(1)
        for message in self.consumer:
            print(message.value)
            print(downloader.global_variables.array_with_my_data[0])
            self.assertEqual(message.value, downloader.global_variables.array_with_my_data[0])
            break

    def test_binance_to_downloader(self):
        """Works only if Binance API is providing data for us to use"""
        downloader.global_variables.array_with_my_data.clear()
        CurrentDataProvider(60, 'binance', 'BTC/USDT').provide_current_data(1)
        self.assertIsNotNone(downloader.global_variables.array_with_my_data[0])

    def influx_db_records(self, client):
        """That Function helps with test_kafka_to_influx and is necessary for it to work"""
        results = client.query('SELECT "Open price" FROM BTC_USDT')
        for measurement in results.get_points(measurement='BTC_USDT'):
            client.query('DELETE FROM BTC_USDT')
            return measurement['Open price']

    def test_kafka_to_influx(self):
        """Works only if both Kafka and InfluxDB database are running and proves their connection"""
        client = setup_client("localhost", "8086", "unittest_database")
        write_data_from_kafka(client, 1)
        self.assertIsNotNone(self.influx_db_records(client))
        pass

# CurrentDataProvider(60, 'binance', 'BTC/USDT').provide_current_data()
# self.assertIsNotNone(message.value)
# downloader.global_variables.array_with_my_data.clear()
# print(downloader.global_variables.array_with_my_data)
# time.sleep(10)
#
# downloader.global_variables.array_with_my_data.clear()
