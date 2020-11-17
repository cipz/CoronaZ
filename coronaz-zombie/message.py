import json

class JsonMessage:
    def __init__(self, json_str):
        self.message = json.loads(json_str)

class ZombieMessage:
    def __init__(self, zombie):
        self.message = dict()
        self.message['uuid'] = str(zombie.uuid)
        self.message['position'] = zombie.position
        self.message['infected'] = zombie.infected

    def get_dict(self):
        return self.message

    def get_json(self):
        return json.dumps(self.message)


class ServerMessage(ZombieMessage):
    def __init__(self, zombie):
        super().__init__(zombie)
        self.message['contacts'] = zombie.contacts