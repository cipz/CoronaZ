from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads

print("Starting db-consumer.py")

# TODO add try catch until consumer finishes booting

consumer_connection = False

while not consumer_connection:
    try:
        consumer = KafkaConsumer(
            'coronaz',
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        consumer_connection = True

    except:
        print("consumer not yet online")

print("connected to consumer")

client = MongoClient('mongo:27017', username='admin', password='pass')
collection = client.coronaz.coronaz

print("connected to mongo")

for message in consumer:
    print("Waiting for a new message ... ")
    message = loads(message.value)
    print(message)
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))

print("consumer out")