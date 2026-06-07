import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

import serial

NUM_MOTORS = 12

class SerialBridge(Node):
    def __init__(self):
        super().__init__("serial_bridge_node")
        self.get_logger().info("init serial bridge")

        self.serial_vorne = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        self.serial_hinten = serial.Serial("/dev/ttyACM2", 115200, timeout=1)

        self.latest_angles = [90.0] * NUM_MOTORS

        self.sub = self.create_subscription(Float32MultiArray, "/real_joint_commands", self.joint_callback, 10)

        self.timer = self.create_timer(0.02, self.send)

    def joint_callback(self, msg):
        if len(msg.data) == NUM_MOTORS:
            self.latest_angles = [
                max(0.0, min(180.0, float(a))) for a in msg.data
            ]
        else:
            self.get_logger().info("Expected 12 joint values")
    
    def send(self):
        angles_vorne = self.latest_angles[0:NUM_MOTORS//2]
        angles_hinten = self.latest_angles[NUM_MOTORS//2:NUM_MOTORS]
        msg_vorne = ",".join(str(int(a)) for a in angles_vorne) + "\n"
        msg_hinten = ",".join(str(int(a)) for a in angles_hinten) + "\n"

        try:
            self.serial_vorne.write(msg_vorne.encode('utf-8'))
            self.serial_hinten.write(msg_hinten.encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f"Serial write failed: {e}")

def main(args=None):
    rclpy.init(args=args)

    bridge = SerialBridge()

    rclpy.spin(bridge)

    bridge.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()