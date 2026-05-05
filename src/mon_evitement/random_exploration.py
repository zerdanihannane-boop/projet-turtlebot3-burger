import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import random

class RandomExplorer(Node):
    def __init__(self):
        super().__init__('random_explorer')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriber = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.timer = self.create_timer(0.5, self.move_random)
        self.obstacle_detected = False

    def scan_callback(self, msg):
        # Vérifie si un obstacle est proche devant
        min_distance = min(msg.ranges[0:30] + msg.ranges[-30:])
        if min_distance < 0.5:  # seuil de 50 cm
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False

    def move_random(self):
        twist = Twist()
        if self.obstacle_detected:
            # Tourner aléatoirement
            twist.angular.z = random.uniform(-1.0, 1.0)
        else:
            # Avancer tout droit
            twist.linear.x = 0.2
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = RandomExplorer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
