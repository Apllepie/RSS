from sensors.sensor import sensor
import random

class humidity(sensor):

    def generate_value(self):
        value = random.uniform(20.0, 100.0)
        return value