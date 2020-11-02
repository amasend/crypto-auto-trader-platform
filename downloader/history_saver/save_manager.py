class HistorySaver:
    def __init__(self, crypto_history: list):
        """ init
            Parameters
            -----------
            crypto_history: list required - list of crypto historical_data
        """
        self.crypto_history = crypto_history

    def save_history(self) -> str:
        """ saving cryptocurrency history to database """
        # here will be db saving method
        return "Data saved"
