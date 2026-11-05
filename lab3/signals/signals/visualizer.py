import collections
import importlib
import threading
import time

import matplotlib.pyplot as plt
import rclpy
from rclpy.node import Node


class Visualizer(Node):
    def __init__(self):
        super().__init__('visualizer')

        self.declare_parameter('topic_name', 'signal_topic')
        self.declare_parameter('msg_type', 'std_msgs/msg/Float64')
        self.declare_parameter('field_name', 'data')

        self.topic_name = self.get_parameter('topic_name').value
        self.msg_type_str = self.get_parameter('msg_type').value
        self.field_name = self.get_parameter('field_name').value

        msg_class = self._import_msg_class(self.msg_type_str)

        self.subscriber = self.create_subscription(
            msg_class,
            self.topic_name,
            self.listener_callback,
            10
        )

        self.max_points = 100
        self.y_data = collections.deque(maxlen=self.max_points)
        self.x_data = collections.deque(maxlen=self.max_points)
        self.start_time = time.time()

        #  Tworzymy mechanizm blokady wątków
        self.lock = threading.Lock()

        self.get_logger().info(
            f'Start wizualizacji: topic="{self.topic_name}", '
            f'typ="{self.msg_type_str}", pole="{self.field_name}"'
        )

    def _import_msg_class(self, type_str: str):
        parts = type_str.split('/')
        module_path = f"{parts[0]}.{parts[1]}"
        class_name = parts[2]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def _get_field_value(self, msg, field_path: str):
        val = msg
        for attr in field_path.split('.'):
            val = getattr(val, attr)
        return float(val)

    def listener_callback(self, msg):
        try:
            val = self._get_field_value(msg, self.field_name)
            current_time = time.time() - self.start_time
            
            # Zamykamy kłódkę na czas dodawania danych, 
            # by Matplotlib nie przerwał nam w połowie pracy.
            with self.lock:
                self.x_data.append(current_time)
                self.y_data.append(val)
                
        except AttributeError:
            self.get_logger().error(
                f'Pole "{self.field_name}" nie istnieje w wiadomości!'
            )


def main(args=None):
    rclpy.init(args=args)
    node = Visualizer()

    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    plt.ion()
    fig, ax = plt.subplots()
    (line,) = ax.plot([], [], 'r-', label=f"{node.topic_name} -> {node.field_name}")
    ax.set_title(f'Wykres dynamiczny: {node.topic_name}')
    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Wartość')
    ax.grid(True)
    ax.legend()

    try:
        while rclpy.ok():
            #  Kopiujemy listy będąc "pod kluczem", 
            # co gwarantuje nam, że x_lst i y_lst będą mieć ZAWSZE tę samą długość.
            with node.lock:
                x_lst = list(node.x_data)
                y_lst = list(node.y_data)

            # Rysowanie odbywa się już poza kłódką (żeby nie blokować działania ROSa, bo rysowanie trwa wolno)
            if x_lst and y_lst:
                line.set_xdata(x_lst)
                line.set_ydata(y_lst)
                ax.relim()
                ax.autoscale_view()
                fig.canvas.draw()
                fig.canvas.flush_events()
            plt.pause(0.05)
            
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()