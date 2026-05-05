#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class EvitementSimple(Node):
    def __init__(self):
        super().__init__('evitement_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.callback, 10)

    def callback(self, msg):
        cmd = Twist()
        # Si rien devant à moins de 0.5m, on avance
        if min(msg.ranges[0:20] + msg.ranges[340:360]) > 0.5:
            cmd.linear.x = 0.2
        else:
            cmd.angular.z = 0.5 # Sinon on tourne
        self.publisher_.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(EvitementSimple())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
