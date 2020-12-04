import logging
from threading import Lock
import uuid
import json
import math
from message import ZombieMessage, ServerMessage
from datetime import datetime
from random import randint


class Zombie:
    def __init__(self, field_size, position, infected, radius, infection_cooldown):
        self.uuid = str(uuid.uuid1())

        self.contacts = list()
        self.contacts_hist = list()

        self._new_contact = False
        self._moved = False
        self._lock = Lock()

        self.field_size = field_size

        self.position = position
        self.infected = infected
        self.radius = radius
        self.infection_cooldown = infection_cooldown +1

        if self.infected:
            self.infection_remaining = self.infection_cooldown
        else:
            self.infection_remaining = 0

        self.alive = True

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
        """
        Setter for the property positon.
        If a -1 is given it will be replaced with a random position on the board.
        """
        for i in range(len(new_pos)):
            if new_pos[i] == -1:
                new_pos[i] = randint(0, self.field_size[i])
        self._position = new_pos

    def process_message(self, message):
        with self._lock:
            m = json.loads(message)

            if m['uuid'] == self.uuid:
                return

            m_pos = m['position']
            dist = math.hypot(m_pos[0] - self.position[0], m_pos[1] - self.position[1])
            if dist > self.radius:
                return
            logging.info('Met other zombie: %s' % m['uuid'])

            if m['infected']:
                self.infected = True
                self.infection_remaining = self.infection_cooldown
                logging.info('!!! Got infected !!!')
            self.update_contacts(m['uuid'])

    def handle_infection(self):
        with self._lock:
            if not self.infected:
                return

            self.infection_remaining -= 1
            if self.infection_remaining <= 0:
                self.infection_remaining = 0
                self.infected = False

    def update_contacts(self, contact):
        self.contacts.append({'uuid': contact, 'timestamp': str(datetime.now())})
        self.has_new_contact = True

    def move(self, direction):
        with self._lock:
            position = self.position
            if direction == 0:
                position[1] += 1
            elif direction == 1:
                position[0] += 1
            elif direction == 2:
                position[1] -= 1
            elif direction == 3:
                position[0] -= 1

            if position[0] < 0 or self.field_size[0] < position[0] or position[1] < 0 or self.field_size[1] < position[
                1]:
                raise Exception('walked out of bounds')
            self.position = position
            self.has_moved = True

    def get_next_server_message(self):
        with self._lock:
            self.has_new_contact = False
            message = ServerMessage(self).get_json()
            self.contacts_hist.extend(self.contacts)
            self.contacts = list()
            return message

    def get_next_broadcast_message(self):
        with self._lock:
            self.has_moved = False
            return ZombieMessage(self).get_json()
