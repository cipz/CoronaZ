from kafka import KafkaConsumer
from json import loads
from time import sleep
import pymongo
import logging

print("Starting db-consumer.py")


def get_consumer_connection():
    consumer_connection = False
    consumer = None

    while not consumer_connection:
        try:
            consumer = KafkaConsumer(
                'coronaz',
                # Linux
                bootstrap_servers=['kafka:9094'],
                # Windows
                # bootstrap_servers=['host.docker.internal:9092'],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                # group_id='my-group',
                group_id=None,
                value_deserializer=lambda x: loads(x.decode('utf-8')))

            consumer_connection = True
        except:
            print("consumer not yet online")
            sleep(10)

    print("connected to consumer")
    return consumer


# Linux
client = pymongo.MongoClient('mongo', username='admin', password='pass')
collection = client.coronaz.coronaz

print("connected to mongo")

consumer = get_consumer_connection()

print(consumer)

aggregation_interval = 10
state = {}
counter = 1
aggregation_id = 0
for message in consumer:
    message = loads(message.value)
    print('Received {}'.format(message))

    state[message['uuid']] = {
        "position": message['position'],
        "timestamp": message['timestamp'],
        "infected": message['infected'],
        "alive": message['alive']
    }

    # If a node dies, trigger a new state
    if (message['alive']):
        counter = counter + 1
    else:
        counter = aggregation_interval

    # Aggregate based if aggregation interval is reached
    if (counter == aggregation_interval):
        counter = 1
        try:
            client.server_info()
        except:
            mongo_connection = False
            while not mongo_connection:
                try:
                    client = pymongo.MongoClient('mongo', username='admin', password='pass')
                    client.server_info()
                    collection = client.coronaz.coronaz
                    mongo_connection = True
                    logging.debug('reconnected to mongo')
                except:
                    logging.debug('Mongo not reachable')
        collection.update({'_id': aggregation_id}, state, upsert=True)
        aggregation_id = aggregation_id + 1
        print('{} added to {}'.format(state, collection))

    if not consumer.bootstrap_connected():
        consumer = get_consumer_connection()

print("consumer out")
