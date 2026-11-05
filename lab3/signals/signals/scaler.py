import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class Scaler(Node):
    def __init__(self):
        super().__init__('scaler_node')

        self.declare_parameter('scale', 1.0)
        self.scale = self.get_parameter('scale').get_parameter_value().double_value

        self.subscription = self.create_subscription(
            Float64,
            'signal_topic',
            self.listener_callback,
            10
        )
        self.publisher_ = self.create_publisher(Float64, 'scaled_signal_topic', 10)

    def listener_callback(self, msg):
        scaled_msg = Float64()
        scaled_msg.data = msg.data * self.scale
        self.publisher_.publish(scaled_msg)
        self.get_logger().info(f'Skaluję: {msg.data:.4f} -> {scaled_msg.data:.4f}')

def main(args=None):
    rclpy.init(args=args)
    node = Scaler()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()