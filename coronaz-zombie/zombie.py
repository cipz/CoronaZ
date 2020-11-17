import logging
from threading import Lock
import uuid
import json
import math
from message import ZombieMessage, ServerMessage
from datetime import datetime

class Zombie:
    def __init__(self, field_size, position, infected, radius):
        self.uuid = str(uuid.uuid1())

        self.contacts = list()

        self._new_contact = False
        self._moved = False
        self._lock = Lock()

        self.field_size = field_size
        self.position = position
        self.infected = infected
        self.radius = radius

    @property
    def has_new_contact(self):
        return self._new_contact

    @has_new_contact.setter
    def has_new_contact(self, value):
        self._new_contact = value

    @property
    def has_moved(self):
        return self._moved

    @has_moved.setter
    def has_moved(self, value):
        self._moved = value

    @property
    def position(self):
        return self._position.copy()

    @position.setter
    def position(self, new_pos):
        self._position = new_pos

    def process_message(self, message):
        with self._lock:
            m = json.loads(message)
            logging.debug(m)

            if m['uuid'] == self.uuid:
                return

            m_pos = m['position']
            dist = math.hypot(m_pos[0] - self.position[0], m_pos[1] - self.position[1])
            if dist > self.radius:
                return

            if m['infected']:
                self.infected = True
                logging.info('!!! Got infected !!!')
            self.update_contacts(m['uuid'])

    def update_contacts(self, contact):
        self.contacts.append(contact)
        self.has_new_contact = True

    def move(self, direction):
        with self._lock:
            position = self.position
            if direction == 0:
                position[0] += 1
            elif direction == 1:
                position[1] += 1
            elif direction == 2:
                position[0] -= 1
            elif direction == 3:
                position[1] -= 1
            self.position = position
            self.has_moved = True

    def get_next_server_message(self):
        with self._lock:
            self.has_new_contact = False
            return ServerMessage(self).get_json()

    def get_next_broadcast_message(self):
        with self._lock:
            self.has_moved = False
            return ZombieMessage(self).get_json()
