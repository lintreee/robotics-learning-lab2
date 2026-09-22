import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

from mobile_robot_sim.kinematics import update_pose


class MobileRobotSimulator(Node):
    def __init__(self):
        super().__init__("mobile_robot_simulator")

        # 机器人当前位姿
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # 最近一次收到的速度命令
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        # 订阅/cmd_vel速度命令
        self.velocity_subscription = self.create_subscription(
            Twist,
            "cmd_vel",
            self.velocity_callback,
            10,
        )

        # 模拟器以50 Hz更新状态
        self.update_period = 0.02
        self.update_timer = self.create_timer(
            self.update_period,
            self.update_callback,
        )

        # 避免每秒输出50行日志
        self.update_count = 0
        self.log_every_n_updates = 25

        self.get_logger().info(
            "Mobile robot simulator started. "
            "Waiting for velocity commands on /cmd_vel."
        )

    def velocity_callback(self, message):
        """收到速度消息时，保存最新的速度命令。"""
        self.linear_velocity = message.linear.x
        self.angular_velocity = message.angular.z

    def update_callback(self):
        """按照固定时间步长更新机器人位姿。"""
        self.x, self.y, self.theta = update_pose(
            x=self.x,
            y=self.y,
            theta=self.theta,
            linear_velocity=self.linear_velocity,
            angular_velocity=self.angular_velocity,
            dt=self.update_period,
        )

        self.update_count += 1

        if self.update_count % self.log_every_n_updates == 0:
            self.get_logger().info(
                f"pose: x={self.x:.3f} m, "
                f"y={self.y:.3f} m, "
                f"theta={self.theta:.3f} rad | "
                f"command: v={self.linear_velocity:.3f} m/s, "
                f"omega={self.angular_velocity:.3f} rad/s"
            )


def main(args=None):
    rclpy.init(args=args)

    node = MobileRobotSimulator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()