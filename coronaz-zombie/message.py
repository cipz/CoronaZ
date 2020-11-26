import json
from datetime import datetime

class ZombieMessage:
    def __init__(self, zombie):
        self.message = dict()
        self.message['uuid'] = zombie.uuid
        self.message['position'] = zombie.position
        self.message['infected'] = zombie.infected
        self.message['timestamp'] = str(datetime.now())
        self.message['alive'] = zombie.alive

    def get_dict(self):
        return self.message

    def get_json(self):
        return json.dumps(self.message)


class ServerMessage(ZombieMessage):
    def __init__(self, zombie):
        super().__init__(zombie)
        self.message['contacts'] = zombie.contacts