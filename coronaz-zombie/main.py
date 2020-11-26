import logging
from threading import Thread, Event
from random import randint
from kafka import KafkaProducer
from json import dumps
import time
import argparse
import socket as soc

from zombie import Zombie
from movement import step_gen


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
                                 value_serializer=lambda x: dumps(x).encode('utf-8'))
    def send_message():
        data = zombie.get_next_server_message()
        logging.info("Sending message to server: %s" % data)

        if with_kafka:
            producer.send(mqtt_queue, value=data)

    while not kill.wait(1):
        send_message()

    send_message()

    logging.info("server con ended")


def main(args):
    zombie = Zombie(args['field'], args['position'], args['infected'], args['radius'], args['infection_cooldown'])

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
        automatic(zombie, args['lifetime'])

    zombie.alive = False

    kill.set()

    zombie_broadcast.join()
    zombie_listen.join()
    server_con_thread.join()
    logging.info('program ended')


def interactive(zombie):
    logging.info('Interactive mode')
    directions = {'n': 0, 'e': 1, 's': 2, 'w': 3}
    while True:
        command = input('What to do: [c]ontact, [m]ove, [s]imulate, [q]uit\n')
        try:
            if command[0].startswith('m'):
                direction = input('direction: [n]orth, [e]ast, [s]outh, [w]est? ')
                zombie.move(directions[direction])
            elif command[0].startswith('c'):
                position = input('position [x,y]: ')
                zombie.process_message('{"uuid": "test", "position": %s, "infected": false}' % position)
            elif command[0].startswith('s'):
                for i in range(25):
                    zombie.move(randint(0, 3))
                    time.sleep(1)
            else:
                break
        except KeyboardInterrupt:
            logging.info('KeyboardInterrupt.. shutting down')
            return
        except Exception as e:
            print(e)


def automatic(zombie, lifetime):
    logging.info('Automatic mode')
    step = step_gen(zombie)
    try:
        for i in range(lifetime):
            zombie.move(next(step))
            zombie.handle_infection()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt.. shutting down')
        return


if __name__ == '__main__':
    logging.basicConfig(  # format="%(asctime)s: %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S")

    parser = argparse.ArgumentParser("main.py")
    parser.add_argument('-f', '--field', type=int, nargs=2, metavar=('X', 'Y'), default=[100, 100],
                        help='field size in form: x y')
    parser.add_argument('-p', '--position', type=int, nargs=2, metavar=('X', 'Y'), default=[-1, -1],
                        help='Starting position of the client. If one or both values are set to -1, the client will be placed randomly on these axis on the field. Default is "-1 -1". Input form: x y')
    parser.add_argument('-i', '--infected', action='store_true',
                        help='if set the client is infected at startup')
    parser.add_argument('-r', '--radius', type=int, metavar='X', default=10,
                        help='radius in which a contact is recognized')
    parser.add_argument('-s', '--server', type=str, nargs=2, metavar=('IP', 'QUEUE'), required=True,
                        help='IP address and QUEUE of the main server')
    parser.add_argument('-z', '--zombie-port', type=int, metavar='PORT', default=4711,
                        help='Port on which the broadcast messages are send')
    parser.add_argument('--interactive', action='store_true',
                        help='if set the client will be in interactive mode and waits for inputs to move')
    parser.add_argument('--lifetime', type=int, metavar='X', default=120,
                        help='Number of steps to be performed in automatic mode. Default = 120')
    parser.add_argument('--infection-cooldown', type=int, metavar='X', default=15,
                        help='Time it takes to heal and become not infected anymore')
    parser.add_argument('--no-kafka', action='store_true')

    args = parser.parse_args()
    logging.debug(vars(args))

    main(vars(args))
