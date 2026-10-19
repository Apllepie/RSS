from sensors.sensor import sensor
import random

class temperature(sensor):

    def generate_value(self):
        value = random.uniform(0.0, 30.0)
        return value