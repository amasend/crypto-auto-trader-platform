import ccxt


class HistoryDownloader:

    def __init__(self, exchange_name: str, crypto_symbol: str):
        """ init
            Paramaters
            ------------
            exchange_name: str required - name of cryptocurrency, e.g. 'binance'
            crypto_symbol: str required - symbol of cryptocurrency, e.g. in Bitcoin in Binance is 'BTC/USDT'
        """
        self.exchange_name = exchange_name.lower()
        self.crypto_symbol = crypto_symbol
        self.exchange = getattr(ccxt, self.exchange_name)()  # creating instance of binance exchange

    def get_history(self) -> dict:
        """ downloading cryptocurrency history """
        return self.exchange.fetch_ticker(self.crypto_symbol)
