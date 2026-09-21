import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class VelocityPublisher(Node):
    def __init__(self):
        super().__init__("velocity_publisher")

        self.publisher = self.create_publisher(
            Twist,
            "cmd_vel",
            10,
        )

        self.timer_period = 0.1
        self.timer = self.create_timer(
            self.timer_period,
            self.publish_velocity,
        )

    def publish_velocity(self):
        message = Twist()

        message.linear.x = 0.5
        message.angular.z = 0.5

        self.publisher.publish(message)

        self.get_logger().info(
            f"Publishing: v={message.linear.x:.2f} m/s, "
            f"omega={message.angular.z:.2f} rad/s"
        )


def main(args=None):
    rclpy.init(args=args)

    node = VelocityPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()