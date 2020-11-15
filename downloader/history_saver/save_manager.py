from history_writer.history_writer import setup_manager, write_data_from_kafka

# influxdb client
influx_client = setup_manager("localhost", "8086", "crypto-trader")


class HistorySaver:
    def __init__(self, crypto_history: list):
        """ init
            Parameters
            -----------
            crypto_history: list required - list of crypto historical_data
        """
        self.crypto_history = crypto_history

    def save_history(self) -> str:
        """ saving cryptocurrency history from kafka  to database"""
        write_data_from_kafka(influx_client)

        return "Data saved"
