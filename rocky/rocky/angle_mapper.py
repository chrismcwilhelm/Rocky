import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

OFFSETS = [0.0, 200.0, 10.0, 0.0, -20.0, 190.0, 0.0, 190.0, 0.0, 0.0, -13.0, 180.0]

FACTORS = [0.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, 0.0, -1.0, -1.0]

MIN = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

MAX = [0.0, 180.0, 180.0, 0.0, 180.0, 180.0, 0.0, 180.0, 180.0, 0.0, 180.0, 180.0]

class AngleMapper(Node):
    def __init__(self):
        super().__init__("convert_angles")
        self.get_logger().info("Initializing Angle Convertor")

        self.sub = self.create_subscription(Float32MultiArray, "/raw_joint_commands", self.callback, 10)
        self.pub = self.create_publisher(Float32MultiArray, "/real_joint_commands", 10)

    def callback(self, msg):
        real = [
            max(min_val, min(max_val, angle * factor + offset))
            for angle, factor, offset, min_val, max_val
            in zip(msg.data, FACTORS, OFFSETS, MIN, MAX)
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