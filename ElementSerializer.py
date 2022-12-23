from json import JSONEncoder


class ElementSerializer(JSONEncoder):
    def default(self, o):
        return o.__dict__
