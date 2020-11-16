import logging
import sys
from threading import Thread, Event
from random import randint
import time

from zombie import Zombie



def thread_zombie(kill, zombie):
    while not kill.wait(1):
        if zombie.has_moved:
            logging.info("Broadcast to other zombies: %s" % zombie.get_next_broadcast_message())
    logging.info("zombie con ended")


def thread_server_con(kill, zombie):
    while not kill.wait(1):
        if zombie.has_new_contact:
            logging.info("Message to server: %s" % zombie.get_next_server_message())
    logging.info("server con ended")


threads = list()


def main(argv):
    logging.debug(argv)
    field_size = (int(argv[1]), int(argv[2]))
    position = (int(argv[3]), int(argv[4]))
    if argv[5].lower() == 'false' or argv[5].lower() == '0':
        infected = False
    else:
        infected = True
    radius = int(argv[6])
    zombie = Zombie(field_size, position, infected, radius)

    kill = Event()

    zombie_thread = Thread(target=thread_zombie, args=(kill, zombie))
    threads.append(zombie_thread)

    server_con_thread = Thread(target=thread_server_con, args=(kill, zombie))
    threads.append(server_con_thread)

    zombie_thread.start()
    server_con_thread.start()

    directions = {'n': 0, 'e': 1, 's': 2, 'w': 3}

    while True:
        command = input('What to do: [a]dd, [m]ove, [s]imulate, [q]uit\n')
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

    if len(sys.argv) != 7:
        print('usage: python %s field_size_x field_size_y position_x position_y infected radius' % sys.argv[0])
    else:
        main(sys.argv)
