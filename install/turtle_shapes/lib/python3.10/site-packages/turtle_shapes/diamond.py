import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class DiamondDriver(Node):
    def __init__(self):
        super().__init__('diamond_driver')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Parameters
        self.side_length = 2.0  # L
        self.linear_vel = 1.0   # v
        self.angular_vel = 0.5  # ω
        self.angle_target = math.pi / 2  # 90 degrees in radians
        
        # Timing Calculations
        self.move_duration = self.side_length / self.linear_vel
        self.turn_duration = self.angle_target / self.angular_vel
        
        # State Machine Tracking
        self.state = "MOVING" # MOVING, TURNING, STOPPED
        self.count = 0        # 0 to 3 (4 sides total)
        self.start_time = self.get_clock().now()
        
        # Timer at 10Hz
        self.timer = self.create_timer(0.1, self.control_loop)

    def control_loop(self):
        now = self.get_clock().now()
        elapsed = (now - self.start_time).nanoseconds / 1e9
        msg = Twist()

        if self.state == "MOVING":
            if elapsed < self.move_duration:
                msg.linear.x = self.linear_vel
            else:
                self.transition("TURNING")

        elif self.state == "TURNING":
            if elapsed < self.turn_duration:
                msg.angular.z = self.angular_vel
            else:
                self.count += 1
                if self.count < 4:
                    self.transition("MOVING")
                else:
                    self.transition("DONE")

        elif self.state == "DONE":
            self.get_logger().info("Diamond complete!")
            self.timer.cancel() # Stop the loop

        self.publisher_.publish(msg)

    def transition(self, next_state):
        self.state = next_state
        self.start_time = self.get_clock().now()
        self.get_logger().info(f"Transitioning to: {next_state}")

def main(args=None):
    rclpy.init(args=args)
    node = DiamondDriver()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
