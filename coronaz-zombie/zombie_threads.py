import logging
import socket as soc
from kafka import KafkaProducer
import json
import time


def thread_zombie_broadcast(kill, zombie, port):
    def send_message(to, message):
        s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        s.setsockopt(soc.SOL_SOCKET, soc.SO_BROADCAST, 1)
        s.sendto(message, (to, port))

    while not kill.wait(1):
        if zombie.has_moved:
            m = zombie.get_next_broadcast_message()

            send_message('255.255.255.255', bytes(m, 'utf-8'))

            logging.info("Broadcast to other zombies: %s" % m)

    send_message('127.0.0.1', b'stop')
    logging.debug('Contacted zombie listener to stop')

    logging.info("zombie broadcast ended")


def thread_zombie_listen(kill, zombie, port):
    while not kill.is_set():
        try:
            s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
            s.bind(('', port))
            m = s.recvfrom(1024)
            logging.info('Got message: %s' % str(m))
            if m[0] == b'stop':
                break
            zombie.process_message(m[0])
        except soc.timeout:
            pass
    logging.info("zombie listen ended")


def thread_server_con(kill, zombie, mqtt_server_addr, mqtt_queue, with_kafka):
    if with_kafka:
        producer = KafkaProducer(bootstrap_servers=[mqtt_server_addr],
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def send_message():
        data = zombie.get_next_server_message()
        logging.info("Sending message to server: %s" % data)

        if with_kafka:
            if not producer.bootstrap_connected():
                get_producer_connection(mqtt_server_addr, 20)

            producer.send(mqtt_queue, value=data)

    while not kill.wait(1):
        send_message()

    send_message()

    logging.info("server con ended")

def get_producer_connection(mqtt_server_addr, tries):
    counter = tries
    producer_connection = False
    while not producer_connection and counter >= 0:
        try:
            producer = KafkaProducer(bootstrap_servers=[mqtt_server_addr],
                                     value_serializer=lambda x:
                                     json.dumps(x).encode('utf-8'))
            producer_connection = True
            logging.info("producer online")
            producer.close()
        except:
            logging.info("producer not yet online")
            counter -= 1
            time.sleep(10)
    if not producer_connection:
        logging.info("Kafka not reachable!")
