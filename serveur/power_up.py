
import json

class PowerUp:

    def __init__(self, x, y, power_type):
        self.pos_x = x
        self.pos_y = y
        self.type = power_type

    def to_json(self):
        data = {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'type': self.type.value
        }
        
        json_data = json.dumps(data)
        return json_data
