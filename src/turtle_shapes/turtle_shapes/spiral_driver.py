import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class SpiralDriver(Node):
    def __init__(self):
        super().__init__('spiral_driver')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Constants
        self.v = 1.0        # Constant linear velocity (m/s)
        self.r0 = 0.5       # Starting radius (prevents infinite angular.z)
        self.k = 0.2        # Growth rate (m/rad)
        
        # State tracking
        self.theta = 0.0    # Total rotation in radians
        self.timer_period = 0.05  # 20 Hz
        self.timer = self.create_timer(self.timer_period, self.control_loop)
        
        self.get_logger().info("Starting Archimedean Spiral...")

    def control_loop(self):
        # 1. Calculate current radius based on total theta
        current_r = self.r0 + (self.k * self.theta)
        
        # 2. Calculate required angular velocity: omega = v / r
        omega = self.v / current_r
        
        # 3. Stop after 3 full loops (3 * 2pi)
        if self.theta >= (6 * math.pi):
            self.get_logger().info("Spiral Complete!")
            self.stop_turtle()
            self.timer.cancel()
            return

        # 4. Publish command
        msg = Twist()
        msg.linear.x = self.v
        msg.angular.z = omega
        self.publisher_.publish(msg)
        
        # 5. Update theta for the next iteration
        # Change in theta = omega * change in time
        self.theta += omega * self.timer_period

    def stop_turtle(self):
        msg = Twist()
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SpiralDriver()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
