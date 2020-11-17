import logging
import sys
from threading import Thread, Event
from random import randint
from kafka import KafkaProducer
from json import dumps
import time
import argparse

from zombie import Zombie



def thread_zombie(kill, zombie):
    while not kill.wait(1):
        if zombie.has_moved:
            logging.info("Broadcast to other zombies: %s" % zombie.get_next_broadcast_message())
    logging.info("zombie con ended")


def thread_server_con(kill, zombie, mqtt_server_addr, mqtt_queue):

    # Comment for testing locally
    # producer = KafkaProducer(bootstrap_servers=[mqtt_server_addr],
    #                      value_serializer=lambda x:
    #                      dumps(x).encode('utf-8'))

    while not kill.wait(1):
        if zombie.has_new_contact:

            data = zombie.get_next_server_message()
            logging.info("Sending message to server: %s" % data)

            # Comment for testing locally
            # producer.send(mqtt_queue, value=data)

    logging.info("server con ended")



def main(args):
    ## TODO finish parser

    zombie = Zombie(args['field'], args['position'], False, args['radius'])

    mqtt_server_addr = args['server'][0]
    mqtt_queue = args['server'][1]

    kill = Event()

    zombie_thread = Thread(target=thread_zombie, args=(kill, zombie))

    server_con_thread = Thread(target=thread_server_con, args=(kill, zombie, mqtt_server_addr, mqtt_queue))

    zombie_thread.start()
    server_con_thread.start()

    directions = {'n': 0, 'e': 1, 's': 2, 'w': 3}

    while True:
        command = input('What to do: [a]dd contact, [m]ove, [s]imulate, [q]uit\n')
        try:
            if command[0].startswith('a'):
                aid = input('id? ')
                zombie.update_contacts(aid)
            elif command[0].startswith('m'):
                direction = input('direction: [n]orth, [e]ast, [s]outh, [w]est? ')
                zombie.move(directions[direction])
            elif command[0].startswith('s'):
                for i in range(25):
                    zombie.move(randint(0, 4))
                    time.sleep(1)
            else:
                break
        except Exception as e:
            print(e)

    kill.set()

    zombie_thread.join()
    server_con_thread.join()
    logging.info('program ended')


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.DEBUG,
                        datefmt="%H:%M:%S")

    parser = argparse.ArgumentParser("main.py")
    parser.add_argument('-f', '--field', type=int, nargs=2, metavar=('X', 'Y'), default=[100,100],
                        help='field size in form: x y')
    parser.add_argument('-p', '--position', type=int, nargs=2, metavar=('X', 'Y'), default=[50,50],
                        help='starting position in form: x y')
    #parser.add_argument('-i', '--infected')
    parser.add_argument('-r', '--radius', type=int, nargs=1, metavar='X', default=10,
                        help='radius in which a contact is recognized')
    parser.add_argument('-s', '--server', type=str, nargs=2, metavar=('IP', 'QUEUE'), required=True,
                        help='IP address and QUEUE of the main server')

    args = parser.parse_args()
    logging.debug(args)

    main(vars(args))
