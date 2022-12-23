import json


class Square:
    def __init__(self, id, node1: int, node2: int, node3: int, node4: int):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.node4 = node4

    def __str__(self):
        string_value = ''
        string_value += f'Id        : {self.id}\n'
        string_value += f'node1    : {self.node1}\n'
        string_value += f'node2    : {self.node2}\n'
        string_value += f'node3    : {self.node3}\n'
        string_value += f'node4    : {self.node3}\n'
        return string_value

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)