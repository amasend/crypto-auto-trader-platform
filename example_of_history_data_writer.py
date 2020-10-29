from influxdb import InfluxDBClient


def compose_json(
                 host,
                 port,
                 database,
                 crypto_symbol,
                 utc_timestamp,
                 open_price,
                 highest_price,
                 lowest_price,
                 closing_price,
                 volume
                 ):

    client = InfluxDBClient(host=f"{host}", port=f"{port}")
    client.create_database(database)
    client.switch_database(database)
    json_body = [
        {
            "measurement": crypto_symbol,
            "tags": {
                "requestName": "Push new data",
                "requestType": "Push"
            },
            "time": utc_timestamp,
            "fields": {
                "(O)pen price, float": open_price,
                "(H)ighest price, float": highest_price,
                "(L)owest price, float": lowest_price,
                "(C)losing price, float": closing_price,
                "(V)olume (in terms of the base currency)": volume
            }
        }]
    client.write_points(json_body)


#
# example of data that can be used
#
# crypto_symbol= "UTC_USTD"
# UTC_timestamp = 1504541580000
# OpenPrice = 4235.4
# HighestPrice = 4240.6
# LowestPrice = 4230.0
# ClosingPrice = 4230.7
# Volume = 37.72941911

compose_json(
    "localhost",
    "8086",
    "exampleDatabase",
    "UTCUSTD",
    1504541580000,
    4235.4, 4240.6,
    4230.0, 4230.7,
    37.72941911
)
