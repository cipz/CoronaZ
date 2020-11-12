import sys
from threading import Thread, Event, Lock
import logging


class Zombie:
    def __init__(self):
        self.contacts = list()
        self._changed = False
        self._lock = Lock()

    def update_contacts(self, id):
        with self._lock:
            self.contacts.append(id)
            self._changed = True

    def get_contacts(self):
        with self._lock:
            self._changed = False
            return str(self.contacts)


def thread_zombie(kill, zombie):
    for i in range(3):
        command = input('What to do: [a]dd, [q]uit\n')

        if command[0].startswith('a'):
            aid = input('id? ')
            zombie.update_contacts(aid)
        else:
            kill.set()
            break
    kill.set()


def thread_server_con(kill, zombie):
    while not kill.wait(1):
        if zombie._changed:
            print("Got new changes: %s" % zombie.get_contacts())
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

    zombie_thread.join()
    server_con_thread.join()
    logging.info('programm ended')


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO,
                        datefmt="%H:%M:%S")
    main(sys.argv)
