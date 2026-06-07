import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

import math
import time

class GaitController(Node):
    def __init__(self):
        super().__init__("gait_controller")
        self.get_logger().info("Initializing Gait Controller")

        self.pub = self.create_publisher(Float32MultiArray, "/foot_positions", 10)

        self.sub = self.create_subscription(Twist, "/velocity_cmd", self.callback, 10)

        self.linear_x = 0.0

        self.phase = 0.0
        self.timer_period = 0.02
        self.timer = self.create_timer(self.timer_period, self.update_feet)

        self.z0 = -0.18
        self.x0 = -0.02
        self.step_length = 0.08
        self.step_height = 0.04

        

    def callback(self, msg):
        self.linear_x = msg.linear.x
        #msg = Float32MultiArray()
        #msg.data = [self.x0, self.z0, self.x0, self.z0, self.x0, -0.067, self.x0, -0.067]
        #self.pub.publish(msg)

        #time.sleep(5)

        #msg = Float32MultiArray()
        #msg.data = [self.x0, self.z0, self.x0, self.z0, self.x0, self.z0, self.x0, self.z0]
        #self.pub.publish(msg)




    def update_feet(self):
        frequency = 1.5 * self.linear_x

        if abs(self.linear_x) < 0.01:
            msg = Float32MultiArray()
            msg.data = [self.x0, self.z0, self.x0, self.z0, self.x0, self.z0, self.x0, self.z0]
            self.pub.publish(msg)
            return

        self.phase += 2 * math.pi * frequency * self.timer_period

        x_lv, z_lv = self.foot_trajectory(self.phase)

        x_rh, z_rh = self.foot_trajectory(self.phase)

        x_rv, z_rv = self.foot_trajectory(self.phase + math.pi)

        x_lh, z_lh = self.foot_trajectory(self.phase + math.pi)

        msg = Float32MultiArray()

        msg.data = [x_rv, z_rv, x_lv, z_lv, x_rh, z_rh, x_lh, z_lh]

        self.pub.publish(msg)


    def foot_trajectory(self, phase):
        phase = phase % (2 * math.pi)

        if phase < math.pi:
            u = phase / math.pi

            x = self.step_length * (0.5 - u)
            z = self.z0

        else:
            u = (phase - math.pi) / math.pi

            x = self.step_length * (-0.5 + u)
            z = self.z0 + self.step_height * math.sin(math.pi * u)

        return x, z

        
def main(args=None):
    rclpy.init(args=args)
    gc = GaitController()
    rclpy.spin(gc)

    gc.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()