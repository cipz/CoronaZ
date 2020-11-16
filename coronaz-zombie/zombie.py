from threading import Lock


class Zombie:
    def __init__(self):
        self.contacts = list()
        self._new_contact = False
        self._moved = False
        self._lock = Lock()
        self._position = [50, 50]

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

    def update_contacts(self, id):
        with self._lock:
            self.contacts.append(id)
            self.has_new_contact = True

    def move(self, direction):
        with self._lock:
            position = self.position
            if direction[0] == 'n':
                position[0] += 1
            elif direction[0] == 'e':
                position[1] += 1
            elif direction[0] == 's':
                position[0] -= 1
            elif direction[0] == 'w':
                position[1] -= 1
            self.position = position
            self.has_moved = True

    def get_new_contacts(self):
        with self._lock:
            self.has_new_contact = False
            return str(self.contacts)

    def get_new_broadcast_message(self):
        with self._lock:
            self.has_moved = False
            return str(self._position)
