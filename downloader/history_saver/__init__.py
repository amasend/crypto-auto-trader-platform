import pandas as pd

class HistorySaver:
    def __init__(self,crypto_history:dict):
        self.crypto_history = crypto_history

    def save_history_to_csv(self,csv_name:str):
        """ saving cryptocurrency history to csv file
            Paramaters
            ------------
            csv_name:str required
        """
        crypto_history_csv = pd.DataFrame(self.crypto_history)
        crypto_history_csv.to_csv(f'./crypto_history_csv/{csv_name}.csv',index=False)