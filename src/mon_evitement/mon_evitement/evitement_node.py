#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class EvitementObstacles(Node):
    def __init__(self):
        super().__init__('evitement_obstacles_node')
        # Éditeur pour envoyer des commandes de vitesse
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # Abonné pour recevoir les données du Lidar
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        
        # Paramètres de contrôle
        self.distance_securite = 0.5  # Distance minimale avant de tourner (en m)
        self.vitesse_lineaire = 0.2   # Vitesse d'avancement normale (m/s)
        self.vitesse_angulaire = 0.5  # Vitesse de rotation lors de l'évitement
        self.get_logger().info("Nœud d'évitement d'obstacles démarré.")

    def scan_callback(self, msg):
        # On extrait un sous-ensemble des mesures à l'avant (-30° à +30°)
        ranges_avant = msg.ranges[0:30] + msg.ranges[-30:]
        
        # Filtrer les valeurs 'inf' et 'NaN' pour trouver la distance minimale
        distances_valides = [r for r in ranges_avant if r > 0.0 and r < float('inf')]
        
        if not distances_valides:
            distance_min_avant = float('inf')
        else:
            distance_min_avant = min(distances_valides)

        # Créer le message de commande de vitesse
        twist = Twist()

        # Logique d'évitement simple
        if distance_min_avant < self.distance_securite:
            # Obstacle détecté !
            self.get_logger().info(f"Obstacle détecté à {distance_min_avant:.2f}m")
            twist.linear.x = 0.0
            twist.angular.z = self.vitesse_angulaire
        else:
            # Voie libre
            twist.linear.x = self.vitesse_lineaire
            twist.angular.z = 0.0

        # Publier la commande
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    evitement_node = EvitementObstacles()
    try:
        rclpy.spin(evitement_node)
    except KeyboardInterrupt:
        pass
    finally:
        evitement_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
