import helpfull_functions


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


def write_data_from_kafka(client, test_variable=0):
    """consumes data from kafka and uploads it to database
    test variable defaults to 0 but is used in tests if set to 1"""
    consumer = helpfull_functions.setup_consumer('unittest', True)
    for kafka_data in consumer:
        # data = bytes_to_array_conversion(kafka_data.value)
        data = kafka_data.value
        upload_data(client, data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6])
        if test_variable == 1:
            break