import downloader.global_variables
import downloader.helpfull_functions


def upload_data(
        client,
        crypto_symbol,
        utc_timestamp,
        open_price,
        highest_price,
        lowest_price,
        closing_price,
        volume):
    """composes json that will store all necessary data into a point, then writes it into database"""
    json_body = [
        {
            "measurement": crypto_symbol,
            "tag"
            "time": utc_timestamp,
            "fields": {
                "Open price": open_price,
                "Highest price": highest_price,
                "Lowest price": lowest_price,
                "Closing price": closing_price,
                "Volume": volume
            }
        }]
    client.write_points(json_body)


def write_data_from_kafka(client,test_variable):
    """consumes data from kafka and uploads it to database"""
    consumer = downloader.helpfull_functions.setup_consumer('unittest',  True)

    for kafka_data in consumer:
        print(kafka_data.value)
        # data = bytes_to_array_conversion(kafka_data.value)
        data = kafka_data.value
        upload_data(client, data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6])
        if test_variable==1:
            break

