import logging
from threading import Thread, Event
from kafka import KafkaProducer
from json import dumps
import time

from zombie import Zombie
from cli_parser import get_cli_arguments
from zombie_modes import interactive, automatic
from zombie_threads import thread_zombie_broadcast, thread_zombie_listen, thread_server_con


def main(args):
    zombie = Zombie(args['field'], args['position'], args['infected'], args['infection_radius'],
                    args['infection_cooldown'])

    mqtt_server_addr = args['server'][0]
    mqtt_queue = args['server'][1]
    with_kafka = not args['no_kafka']

    if with_kafka:
        producer_connection = False
        while not producer_connection:
            try:
                producer = KafkaProducer(bootstrap_servers=[mqtt_server_addr],
                                         value_serializer=lambda x:
                                         dumps(x).encode('utf-8'))
                producer_connection = True
                logging.info("producer online")
                producer.close()
            except:
                logging.info("producer not yet online")
                time.sleep(10)

    kill = Event()

    zombie_broadcast = Thread(target=thread_zombie_broadcast, args=(kill, zombie, args['zombie_port']))
    zombie_listen = Thread(target=thread_zombie_listen, args=(kill, zombie, args['zombie_port']))

    server_con_thread = Thread(target=thread_server_con, args=(kill, zombie, mqtt_server_addr, mqtt_queue, with_kafka))

    zombie_broadcast.start()
    zombie_listen.start()
    server_con_thread.start()

    if args['interactive']:
        interactive(zombie)
    else:
        automatic(zombie, args['zombie_lifetime'])

    zombie.alive = False

    kill.set()

    zombie_broadcast.join()
    zombie_listen.join()
    server_con_thread.join()
    logging.info('program ended')


if __name__ == '__main__':
    logging.basicConfig(  # format="%(asctime)s: %(message)s",
        # level=logging.DEBUG,
        level=logging.INFO,
        datefmt="%H:%M:%S")

    args = get_cli_arguments()
    logging.debug(args)

    main(args)
