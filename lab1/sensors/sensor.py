import paho.mqtt.client as mqtt
import random
import time

from SensorPayload.SensorPayload import SensorPayload




class sensor():
    name : str
    value : float

    def __init__(self, name:str,host_name:str = "localhost", port : int = 1883, keep_alive: int = 60 ):
        self.name = name
        self.value = 0.0
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"Łączenie z brokerem {host_name}:{port}...")
        self.client.connect(host_name, port, keep_alive)

        self.client.loop_start()


    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"{self.name} Connected successfully to the broker.")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback called when new message is received."""
        print(f"{self.name} Received: {msg.topic} {msg.qos} {msg.payload}")


    def generate_value(self):
        value = random.uniform(1.0, 10.0)
        return value

    def send(self, topic:str ):
            
            self.value = self.generate_value()
            payload = SensorPayload(sensor_name=self.name, value=self.value)
            json_data = payload.model_dump_json()
            self.client.publish(topic, json_data)
            print(f"[{self.name}]Published {topic}: {self.value}")
            time.sleep(2)

    def disconect (self):
         self.client.loop_stop()
         self.client.disconnect()