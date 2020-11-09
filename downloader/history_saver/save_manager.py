import downloader.global_variables
from downloader.helpfull_functions import setup_producer


class HistorySaver:

    def __init__(self, crypto_history: list):
        """ init
            Parameters
            -----------
            crypto_history: list required - list of crypto historical_data
        """
        self.crypto_history = crypto_history

    def save_history(self) -> str:
        """ saving cryptocurrency history to kafka """
        producer = setup_producer()

        for data in self.crypto_history:
            producer.send('unittest', value=data)
            downloader.global_variables.array_with_my_data.append(data)
            # this array will help with testing however isn't necessary for the code to work
        return "Data saved"
