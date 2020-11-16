import logging
import sys
from threading import Thread, Event

from zombie import Zombie


def thread_zombie(kill, zombie):
    while not kill.wait(1):
        if zombie.has_moved:
            logging.info("Broadcast to other zombies: %s" % zombie.get_new_broadcast_message())
    logging.info("zombie con ended")


def thread_server_con(kill, zombie):
    while not kill.wait(1):
        if zombie.has_new_contact:
            logging.info("Message to server: %s" % zombie.get_new_contacts())
    logging.info("server con ended")


threads = list()


def main(argv):
    zombie = Zombie()

    kill = Event()

    zombie_thread = Thread(target=thread_zombie, args=(kill, zombie))
    threads.append(zombie_thread)

    server_con_thread = Thread(target=thread_server_con, args=(kill, zombie))
    threads.append(server_con_thread)

    zombie_thread.start()
    server_con_thread.start()

    while True:
        command = input('What to do: [a]dd, [m]ove, [q]uit\n')

        if command[0].startswith('a'):
            aid = input('id? ')
            zombie.update_contacts(aid)
        elif command[0].startswith('m'):
            direction = input('direction: [n]orth, [e]ast, [s]outh, [w]est? ')
            zombie.move(direction)
        else:
            break

    kill.set()

    zombie_thread.join()
    server_con_thread.join()
    logging.info('programm ended')


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")
    main(sys.argv)
