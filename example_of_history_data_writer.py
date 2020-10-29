from influxdb import InfluxDBClient
import datetime
import pytz

host = "localhost"
port = "8086"
dataBase = "Bonbon_Database"

UTC_timestamp = "modulo"
OpenPrice = 4235.4
HighestPrice = 4240.6
LowestPrice = 4230.0
ClosingPrice = 4230.7
Volume = 37.72941911
client = InfluxDBClient(host=f"{host}", port=f"{port}")

client.create_database("Bonbon_Database")

print(client.get_list_database())

client.switch_database("Bonbon_Database")


class UploadingData:
    def __init__(
            self,
            UTC_timestamp,
            OpenPrice,
            HighestPrice,
            LowestPrice,
            ClosingPrice,
            Volume
    ):
        self.UTC_timestamp = UTC_timestamp
        self.OpenPrice = OpenPrice
        self.HighestPrice = HighestPrice
        self.LowestPrice = LowestPrice
        self.ClosingPrice = ClosingPrice
        self.Volume = Volume

    def composejson(
            self,
            UTC_timestamp,
            OpenPrice,
            HighestPrice,
            LowestPrice,
            ClosingPrice,
            Volume):
        json_body = [
            {
                "measurement": f"{UTC_timestamp}",
                "tags": {
                    "requestName": "Push new data",
                    "requestType": "Push"
                },
                "time": datetime.datetime.now(tz=pytz.UTC),
                "fields": {
                    "(O)pen price, float": OpenPrice,
                    "(H)ighest price, float": HighestPrice,
                    "(L)owest price, float": LowestPrice,
                    "(C)losing price, float": ClosingPrice,
                    "(V)olume (in terms of the base currency)": Volume
                }
            }]
        client.write_points(json_body)


dataUpload = UploadingData(UTC_timestamp, OpenPrice, HighestPrice, LowestPrice, ClosingPrice, Volume)
dataUpload.composeJson(UTC_timestamp, OpenPrice, HighestPrice, LowestPrice, ClosingPrice, Volume)
results = client.query(f'SELECT * FROM {UTC_timestamp}')
print(results)
login_points = list(results.get_points(measurement=f"{UTC_timestamp}", tags={"requestName": "Push"}))
print(login_points)
