import ccxt

class HistoryDownloader:
    exchange = ccxt.binance() #creating instance of binance exchange
    def __init__(self,crypto_symbol:str)->None:
        self.crypto_symbol = crypto_symbol

    def get_history(self):
        """ downloading cryptocurrency history """
        return self.exchange.fetch_ticker(self.crypto_symbol)

print(type(HistoryDownloader('BTC/USDT').get_history()))