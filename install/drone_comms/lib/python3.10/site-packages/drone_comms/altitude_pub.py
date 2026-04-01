import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class AltitudePublisher(Node):

    def __init__(self):
        super().__init__('altitude_publisher')

        self.publisher_ = self.create_publisher(Float32, '/altitude', 10)

        timer_period = 1.0  # 1 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.altitude = 0.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.altitude

        self.publisher_.publish(msg)

        self.get_logger().info(f'Altitude: {msg.data}')

        self.altitude += 1.0


def main(args=None):
    rclpy.init(args=args)

    node = AltitudePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
