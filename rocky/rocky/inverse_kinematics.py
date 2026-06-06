import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray
import math

class InverseKinematics(Node):
    def __init__(self):
        super().__init__('inverse_kinematics')

        self.L1 = 0.108
        self.L2 = 0.135

        self.sub = self.create_subscription(Float32MultiArray, "/foot_positions", self.foot_callback, 10)

        self.pub = self.create_publisher(Float32MultiArray, "/raw_joint_commands", 10)

        self.get_logger().info("Initialized inverse kinematics")

    def compute_kinematics(self, x, z):
        r = math.sqrt(x*x + z*z)
        r = min(max(r, 0.02), self.L1 + self.L2 - 0.02)

        knee = math.acos((r*r - self.L1*self.L1 - self.L2*self.L2) / (2*self.L1 * self.L2))

        hip = math.atan2(z, x) - math.acos((r*r + self.L1*self.L1 - self.L2*self.L2) / (2*self.L1 * r))

        return knee, hip
    
    def foot_callback(self, msg):
        output = []

        for i in range(0, 8, 2):
            x = msg.data[i]
            z = msg.data[i+1]

            hip, knee = self.compute_kinematics(x, z)

            yaw = 120.0

            output.extend([math.degrees(yaw), math.degrees(hip), math.degrees(knee)])

        out = Float32MultiArray()
        out.data = output
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    ik = InverseKinematics()
    rclpy.spin(ik)

    ik.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()