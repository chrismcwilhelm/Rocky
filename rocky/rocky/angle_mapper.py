import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

OFFSETS = [0.0, 80.0, 215.0, 0.0, 80.0, 215.0, 0.0, 80.0, 215.0, 0.0, 80.0, 215.0]

FACTORS = [0.0, 1.0, -1.0, 0.0, 1.0, -1.0, 0.0, 1.0, -1.0, 0.0, 1.0, -1.0]

class AngleMapper(Node):
    def __init__(self):
        super().__init__("convert_angles")
        self.get_logger().info("Initializing Angle Convertor")

        self.sub = self.create_subscription(Float32MultiArray, "/raw_joint_commands", self.callback, 10)
        self.pub = self.create_publisher(Float32MultiArray, "/real_joint_commands", 10)

    def callback(self, msg):
        real = [
            max(0.0, min(180.0, angle * factor + offset))
            for angle, factor, offset
            in zip(msg.data, FACTORS, OFFSETS)
        ]

        out = Float32MultiArray()
        out.data = real

        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    mapper = AngleMapper()
    rclpy.spin(mapper)

    mapper.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()