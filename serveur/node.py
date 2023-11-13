import json


class Node:

    parent = None
    weight = None
    direction = 1

    def __init__(self, px, py, reach, base_weight, value):
        self.x = px
        self.y = py
        self.reach = reach
        self.base_weight = base_weight
        self.value = value

    def to_json(self):
        data = {
            'x': self.x,
            'y': self.y,
            'reach': self.reach,
            'base_weight': self.base_weight,
            'value': self.value,
            'parent': self.parent,
            'weight': self.weight,
            'direction': self.direction
        }

        json_data = json.dumps(data)
        return json_data

