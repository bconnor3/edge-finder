
class Node:
    def __init__(self, id, x_coordinate, y_coordinate):
        self.id = id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def __str__(self):
        string_value = ''
        string_value += f'Id        : {self.id}\n'
        string_value += f'x_coordinate    : {self.x_coordinate}\n'
        string_value += f'y_coordinate : {self.y_coordinate}\n'
        return string_value
