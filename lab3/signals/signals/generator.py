import math # Potrzebne do obliczenia funkcji sinus
import rclpy
from rclpy.node import Node
# Importujemy standardowy typ wiadomości dla liczb zmiennoprzecinkowych
from std_msgs.msg import Float64 

class Generator(Node): # Dobra praktyka: nazwy klas z wielkiej litery
    def __init__(self):
        super().__init__('generator_node')
        
        # 1. Deklaracja i pobranie parametrów
        self.declare_parameter('frequency', 1.0)
        self.declare_parameter('amplitude', 1.0)
        
        self.freq = self.get_parameter('frequency').get_parameter_value().double_value
        self.amp = self.get_parameter('amplitude').get_parameter_value().double_value
        
        self.get_logger().info(f'Uruchomiono generator. Amplituda: {self.amp}, Częstotliwość: {self.freq} Hz')
        
        # 2. Tworzenie Publikatora
        self.publisher_ = self.create_publisher(Float64, 'signal_topic', 10)
        
        # [ZMIANA]: Zamiast licznika '0.0', zapisujemy dokładny czas startu węzła
        self.start_time = self.get_clock().now()
        
        # 4. Timer
        self.timer_period = 1.0 / self.freq  # T = 1/f
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float64()
        
        # [ZMIANA]: Pobieramy aktualny czas systemowy ROS i obliczamy ile sekund upłynęło od startu
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9  # Konwersja nanosekund na sekundy
        
        # Obliczamy wartość sinusa na podstawie realnego upływu czasu
        msg.data = self.amp * math.sin(2.0 * math.pi * self.freq * elapsed_time)
        
        # Publikujemy wiadomość
        self.publisher_.publish(msg)
        
        # Logujemy w terminalu wartość oraz czas, aby widzieć zmiany
        self.get_logger().info(f'Publikuję: {msg.data:.4f} (czas: {elapsed_time:.2f}s)')

def main(args=None):
    rclpy.init(args=args)
    node = Generator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
