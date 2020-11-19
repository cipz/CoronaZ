from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from time import sleep

sleep(30)

print("Starting db-consumer.py")

consumer = KafkaConsumer(
    'coronaz',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    # group_id='my-group',
    group_id=None,
    value_deserializer=lambda x: loads(x.decode('utf-8')))

print("connected to consumer")

client = MongoClient('localhost:27017', username='admin', password='pass')
collection = client.coronaz.coronaz

print("connected to mongo")

print(consumer)

for message in consumer:
    print("Waiting for a new message ... ")
    message = loads(message.value)
    print(message)
    collection.insert_one(message)
    print('{} added to {}'.format(message, collection))

print("consumer out")