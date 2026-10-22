# Importujemy wygenerowane klasy z Protobuf
from structure_pb2 import Point, Quaternion, Pose
import zmq

def run_subscriber():
    # Inicjalizacja kontekstu i gniazda ZeroMQ
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    
    # Łączymy się z adresem publishera
    subscriber.connect("tcp://localhost:5555")
    
    # Ustawiamy filtr subskrypcji na temat "telemetry"
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    print("Subscriber uruchomiony. Oczekiwanie na dane...")

    try:
        while True:
            # Odbieranie wiadomości wieloczęściowej
            pos_bytes = subscriber.recv()

            # Tworzenie pustych obiektów struktury
            pos = Pose()
            
            # Deserializacja (parsowanie ze strumienia bajtów)
            pos.ParseFromString(pos_bytes)
            
            # Wyświetlenie odebranych danych
            print(f"  Pose     -> {pos}")
           

    except KeyboardInterrupt:
        print("\nZamykanie subskrybenta...")
    finally:
        subscriber.close()
        context.term()

if __name__ == "__main__":
    run_subscriber()
