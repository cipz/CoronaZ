from kafka import KafkaConsumer
from json import loads
from time import sleep
import os
import pymongo

print("Starting db-consumer.py")

consumer_connection = False

while not consumer_connection:

    try:

        consumer = KafkaConsumer(
            'coronaz',
            # Linux
            bootstrap_servers=['kafka:9092'],
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

# Linux
client = pymongo.MongoClient('mongo:27019', username='telerik', password='123')
# Windows
# client = pymongo.MongoClient('host.docker.internal:27017', username='admin', password='pass')
collection = client.coronaz.coronaz

print("connected to mongo")

print(consumer)

aggregation_interval = 10
state = {}
counter = 1
aggregation_id = 0
for message in consumer:
    message = loads(message.value)
    print('Received {}'.format(message))

    state[message['uuid']] = (message['position'], message['infected'], message['timestamp'])

    counter = counter + 1
    # Aggregate based if aggregation interval is reached
    if(counter == aggregation_interval):
        counter = 1
        collection.update({'_id' : aggregation_id}, state, upsert = True)
        aggregation_id = aggregation_id + 1
        print('{} added to {}'.format(state, collection))

print("consumer out")