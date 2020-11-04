from influxdb import InfluxDBClient
from kafka import KafkaConsumer, KafkaProducer
from json import dumps, loads


def setup_manager(host,
                  port,
                  database):
    """initializing client, have to be called before upload_data"""
    client = InfluxDBClient(host=f"{host}", port=f"{port}")
    client.create_database(database)
    client.switch_database(database)
    return client


def upload_data(client, crypto_symbol, utc_timestamp, open_price, highest_price, lowest_price, closing_price, volume):
    """composes json that will store all necessary data into a point, then writes it into database"""
    json_body = [
        {
            "measurement": crypto_symbol,
            "time": utc_timestamp,
            "fields": {
                "Open price": open_price,
                "Highest price": highest_price,
                "Lowest price": lowest_price,
                "Closing price": closing_price,
                "Volume ": volume
            }
        }]

    client.write_points(json_body)


def write_data_from_kafka(client):
    """consumes data from kafka and uploads it to database"""
    bootstrap_servers = ['localhost:9092']

    consumer = KafkaConsumer(
        'crypto-trader-topic',
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True)

    for kafka_data in consumer:
        data = kafka_data.value
        upload_data(client, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    # few prints to help with test if if it works on the spot
    #
    # results = client.query(f'SELECT * FROM {crypto_symbol}')
    # print(results)
    # print(client.get_list_database())
