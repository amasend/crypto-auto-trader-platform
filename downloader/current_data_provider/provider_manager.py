import ccxt
import time
from history_writer.history_writer import setup_manager, upload_data, write_data_from_kafka

# influxdb client
influx_client = setup_manager("localhost", "8086", "crypto-trader")


def provide_current_data(exchange_name: str, crypto_symbol: str):
    exchange = getattr(ccxt, exchange_name)()
    while True:
        current_milliseconds = int(round(time.time() * 1000))
        current_milliseconds = current_milliseconds - current_milliseconds % 1000
        candles = exchange.fetch_ohlcv(crypto_symbol, '1m', limit=1,
                                       params={'startTime': current_milliseconds - 60000,
                                               'endTime': current_milliseconds})
        candles[0].insert(0, crypto_symbol)
        candles[0][0] = candles[0][0].replace("/", "_")
        data = candles[0]
        # save data to influx database
        upload_data(influx_client, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        time.sleep(60)


def download_current_data(exchange_name: str, crypto_symbol: str):
    """ this function downloads current cryptocurrency data """
    crypto_symbol = crypto_symbol.replace("/", "_")
    result = influx_client.query(
        ("select Open_price, Highest_price,Lowest_price,Closing_price, Volume  from {0} order by time DESC").format(
            crypto_symbol))
    return list(result.get_points(measurement=crypto_symbol))[0]


if __name__ == "__main__":
    """ This example code downloasd current crypto data every minute and saves it to database
    provider = CurrentDataProvider("binance")
    provider.provide_current_data('BTC/USDT') """
    provide_current_data("binance", 'BTC/USDT')
