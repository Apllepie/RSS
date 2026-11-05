import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64 

class Generator(Node):
    def __init__(self):
        super().__init__('generator_node')
        
        # 1. Deklaracja  podstawowych parametrów
        self.declare_parameter('frequency', 10.0)
        self.declare_parameter('amplitude', 2.0)
        
        self.freq = self.get_parameter('frequency').get_parameter_value().double_value
        self.amp = self.get_parameter('amplitude').get_parameter_value().double_value
        
        # 2. SZTYWNE LICZENIE CZĘSTOTLIWOŚCI PRÓBKOWANIA
        points_per_period = 20.0 
        self.pub_rate = self.freq * points_per_period
        
        self.get_logger().info(f'Sygnał: {self.freq}Hz. Próbkowanie: {self.pub_rate}Hz ({points_per_period} pkt/okres)')
        
        self.publisher_ = self.create_publisher(Float64, 'signal_topic', 10)
        self.start_time = self.get_clock().now()
        
        # 3. Timer 
        self.timer_period = 1.0 / self.pub_rate 
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float64()
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9
        
        # Wzór na sinusoidę używa prawdziwej częstotliwości fali (self.freq)
        msg.data = self.amp * math.sin(2.0 * math.pi * self.freq * elapsed_time)
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publikuję: {msg.data:.4f} (czas: {elapsed_time:.2f}s)')

def main(args=None):
    rclpy.init(args=args)
    node = Generator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()