import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class VelocitySubscriber(Node):
    def __init__(self):
        super().__init__("velocity_subscriber")

        self.subscription = self.create_subscription(
            Twist,
            "cmd_vel",
            self.velocity_callback,
            10,
        )

    def velocity_callback(self, message):
        self.get_logger().info(
            f"Received: v={message.linear.x:.2f} m/s, "
            f"omega={message.angular.z:.2f} rad/s"
        )


def main(args=None):
    rclpy.init(args=args)

    node = VelocitySubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()