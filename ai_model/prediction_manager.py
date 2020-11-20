import joblib
import numpy as np
from downloader.current_data_provider.provider_manager import download_current_data


class PredictionManager:

    def __init__(self, path: str, crypto_symbol: str):
        """
        path: str  - path to AI model
        crypto_symbol: str - symbol of cryptocurrency
        """
        self.model = joblib.load(path)
        self.crypto_symbol = crypto_symbol

    def predict_action(self):
        """
        predicts action (buy, sell or wait) and returns it
        """
        current_crypto_data = download_current_data(self.crypto_symbol)
        timestamp = current_crypto_data['time']
        open_price = current_crypto_data['Open_price']
        highest_price = current_crypto_data['Highest_price']
        lowest_price = current_crypto_data['Lowest_price']
        closing_price = current_crypto_data['Closing_price']
        volume = current_crypto_data['Volume']
        np_dataset = np.array([[timestamp, open_price, highest_price, lowest_price, closing_price, volume]])
        prediction = self.model.predict(np_dataset)
        return prediction[0]
