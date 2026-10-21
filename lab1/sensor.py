import random
import paho.mqtt.client as mqtt
from pydantic import BaseModel


# Define Pydantic model at the top
class SensorPayload(BaseModel):
    sensor_name: str
    value: float


class Sensor:
    name: str
    value: float

    def __init__(self, name: str, host_name: str = "localhost", port: int = 1883, keep_alive: int = 60):
        self.name = name
        self.value = 0.0

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"[{self.name}] Connecting to broker {host_name}:{port}...")
        self.client.connect(host_name, port, keep_alive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"[{self.name}] Connected successfully to broker.")
        else:
            print(f"[{self.name}] Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"[{self.name}] Received: {msg.topic} {msg.qos} {msg.payload}")

    def generate_value(self) -> float:
        return random.uniform(1.0, 10.0)

    def send(self, topic: str):
        self.value = self.generate_value()
        payload = SensorPayload(sensor_name=self.name, value=self.value)
        json_data = payload.model_dump_json()
        self.client.publish(topic, json_data)
        print(f"[{self.name}] Published to '{topic}': {self.value:.2f}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


class Humidity(Sensor):
    def generate_value(self) -> float:
        return random.uniform(20.0, 100.0)


class Temperature(Sensor):
    def generate_value(self) -> float:
        return random.uniform(0.0, 30.0)