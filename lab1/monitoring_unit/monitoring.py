from jsonschema import ValidationError
import paho.mqtt.client as mqtt

from SensorPayload.SensorPayload import SensorPayload

class monitoring():

    def __init__(self, host_name: str = "localhost", port: int = 1883, keep_alive: int = 60):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        print(f"[Monitoring] Łączenie z brokerem {host_name}:{port}...")
        self.client.connect(host_name, port, keep_alive)
        
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("[Monitoring] Połączono pomyślnie z brokerem.")
            self.client.subscribe("#")
            print("[Monitoring] subscribe to : #")
        else:
            print(f"[Monitoring] Connection failed with code: {rc}")

    def on_message(self, client, userdata, msg):
        """Callback called when new message is received."""
        try:
            raw_payload = msg.payload.decode('utf-8')

            data = SensorPayload.model_validate_json(raw_payload)
            

            print(f"[Recived from: {msg.topic}]")
            print(f" -> sensor name: {data.sensor_name}")
            print(f" -> value: {data.value:.2f}")
            print("-" * 30)
            
        except ValidationError as e:
            print(f"[Validate ERROR {msg.topic}]: Dane nie pasują do modelu Pydantic!")
            print(f" Raw value: {msg.payload.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"[EROR]: some error accure: {e}")



    def disconect (self):
         self.client.loop_stop()
         self.client.disconnect()