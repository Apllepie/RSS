import paho.mqtt.client as mqtt
from pydantic import ValidationError

from sensor import SensorPayload


class Monitoring:

    def __init__(self, host_name: str = "localhost", port: int = 1883, keep_alive: int = 60):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"[Monitoring] Connecting to broker {host_name}:{port}...")
        self.client.connect(host_name, port, keep_alive)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("[Monitoring] Connected successfully to broker.")
            self.client.subscribe("#")
            print("[Monitoring] Subscribed to topic: #")
        else:
            print(f"[Monitoring] Connection failed with code: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            raw_payload = msg.payload.decode('utf-8')
            data = SensorPayload.model_validate_json(raw_payload)

            print(f"[Received from: {msg.topic}]")
            print(f" -> Sensor Name: {data.sensor_name}")
            print(f" -> Value: {data.value:.2f}")
            print("-" * 30)

        except ValidationError:
            print(f"[Validation ERROR on {msg.topic}]: Payload standard does not match Pydantic model!")
            print(f" Raw value: {msg.payload.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"[ERROR]: An error occurred: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()



if __name__ == "__main__":
    import time
    monitor = Monitoring()
    print("[Monitoring] Listening for messages. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.disconnect()