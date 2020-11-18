from influxdb import InfluxDBClient
from kafka import KafkaConsumer, KafkaProducer
from json import dumps, loads


def setup_client(host,
                  port,
                  database):
    """initializing client, have to be called before upload_data"""
    client = InfluxDBClient(host=f"{host}", port=f"{port}")
    client.create_database(database)
    client.switch_database(database)
    return client


def setup_consumer(topic, autocomit: bool,offset='earliest'):
    """initializing consumer, have to be called before 'for x in consumer:'"""
    bootstrap_servers = ['localhost:9092']
    consumer = KafkaConsumer(
        f'{topic}',
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset=f'{offset}',
        enable_auto_commit=autocomit,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    return consumer


def setup_producer():
    """initializing consumer, have to be called  'producer.send(database, value=x)'"""
    bootstrap_servers=['localhost:9092']
    value_serializer= lambda x: dumps(x).encode('utf-8')
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=value_serializer)
    return producer


def bytes_to_array_conversion(convertable_bytes):
    """possibly useful function used in previous builds, right now not needed but ready for future use"""
    convertable_bytes = convertable_bytes.decode().split(",")
    new = []
    for elem in convertable_bytes:
        elem = elem.replace("[", "")
        elem = elem.replace("]", "")
        elem = elem.replace('"', "")
        elem = elem.replace(" ", "")
        elem.rstrip()
        elem.lstrip()
        new.append(elem)
    # for i in range(1,7):
    #     new[i] = float(new[i])
    return new


def reading_influxdb_query(client, object_of_intrest="*", name_of_database='BTC_USDT'):
    """"""
    results = client.query(f'SELECT {object_of_intrest} FROM {name_of_database}')
    # print(client.get_list_database())
    return results
