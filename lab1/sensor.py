import random
import time
import paho.mqtt.client as mqtt
from pydantic import BaseModel


class SensorPayload(BaseModel):
    sensor_name: str
    value: float


class Sensor:
    name: str
    value: float

    def __init__(self, name: str, host_name: str = "localhost", port: int = 1883, keep_alive: int = 60):
        self.name = name
        self.host_name = host_name
        self.port = port
        self.keep_alive = keep_alive
        self.value = 0.0
        self.client = None

    def connect(self):
        """Creates client and connects INSIDE child process space."""
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"[{self.name}] Connecting to broker {self.host_name}:{self.port}...")
        self.client.connect(self.host_name, self.port, self.keep_alive)
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
        if not self.client:
            raise RuntimeError("Sensor is not connected to MQTT broker.")
        self.value = self.generate_value()
        payload = SensorPayload(sensor_name=self.name, value=self.value)
        json_data = payload.model_dump_json()
        self.client.publish(topic, json_data)
        print(f"[{self.name}] Published to '{topic}': {self.value:.2f}")

    def disconnect(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def run(self, topic: str, interval: float = 2.0):
        """Main loop executed inside the child process."""
        self.connect()
        try:
            while True:
                self.send(topic)
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
        finally:
            self.disconnect()


class Humidity(Sensor):
    def generate_value(self) -> float:
        return random.uniform(20.0, 100.0)


class Temperature(Sensor):
    def generate_value(self) -> float:
        return random.uniform(0.0, 30.0)