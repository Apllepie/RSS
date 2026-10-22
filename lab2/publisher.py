import time
import random
# Importujemy wygenerowane klasy z Protobuf
# Zakładam nazwę pliku structure_pb2.py w tym samym katalogu. 
# Jeśli importujesz z pakietu lab2, użyj: from lab2.structure_pb2 import Point, Quaternion
from structure_pb2 import Point, Quaternion, Pose
import zmq

def run_publisher():
    # Inicjalizacja kontekstu i gniazda ZeroMQ
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    
    # Wiążemy publishera do portu 5555
    publisher.bind("tcp://*:5555")
    print("Publisher uruchomiony na porcie 5555... Wysyłam dane.")

    try:
        while True:
            # 1. Tworzenie i uzupełnianie struktury Point
            point = Point()
            point.x = round(random.uniform(-10.0, 10.0), 2)
            point.y = round(random.uniform(-10.0, 10.0), 2)
            point.z = round(random.uniform(-10.0, 10.0), 2)

            # 2. Tworzenie i uzupełnianie struktury Quaternion
            quat = Quaternion()
            quat.x = 0.0
            quat.y = 0.0
            quat.z = round(random.uniform(-1.0, 1.0), 3)
            quat.w = 1.0

            pos = Pose()
            pos.pos.CopyFrom(point)
            pos.quat.CopyFrom(quat)
            # 3. Serializacja obiektów Protobuf do tablicy bajtów
            pos_bytes = pos.SerializeToString()
            

            # 4. Wysyłanie wiadomości przez ZeroMQ
            # Używamy wiadomości wieloczęściowych (multipart):
            # Część 1: Temat (Topic)
            # Część 2: Zserializowany Point
            # Część 3: Zserializowany Quaternion
            publisher.send(pos_bytes)
            
            print(f"Wysłano -> Pose({pos})")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nZamykanie publishera...")
    finally:
        publisher.close()
        context.term()

if __name__ == "__main__":
    run_publisher()
