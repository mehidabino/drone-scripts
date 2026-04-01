import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

THRESHOLD = 5.0

class AltitudeMonitor(Node):

    def __init__(self):
        super().__init__('altitude_monitor')

        self.subscription = self.create_subscription(
            Float32,
            '/altitude',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        altitude = msg.data

        if altitude > THRESHOLD:
            self.get_logger().warn(f'WARNING! Altitude too high: {altitude}')
        else:
            self.get_logger().info(f'Altitude safe: {altitude}')


def main(args=None):
    rclpy.init(args=args)

    node = AltitudeMonitor()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
