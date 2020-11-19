from time import sleep
from json import dumps
from kafka import KafkaProducer
import logging

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'coronaz' : e}
    producer.send('coronaz', value=data)
    print("Sending", str(data))
    sleep(3)