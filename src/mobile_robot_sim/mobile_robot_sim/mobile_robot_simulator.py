import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
import math
from nav_msgs.msg import Odometry
import time

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

        self.declare_parameter("command_timeout_sec", 0.5)
        self.command_timeout_sec = self.get_parameter("command_timeout_sec").value

        if self.command_timeout_sec <= 0:
            raise ValueError("command_timeout_sec 必须大于 0")

        self.last_command_time = None

        # 订阅/cmd_vel速度命令
        self.velocity_subscription = self.create_subscription(
            Twist,
            "cmd_vel",
            self.velocity_callback,
            10,
        )

        self.odom_publisher = self.create_publisher(
            Odometry,
            "odom",
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
        self.last_command_time = time.monotonic()

    def update_callback(self):
        """按照固定时间步长更新机器人位姿。"""
        if (
            self.last_command_time is not None
            and time.monotonic() - self.last_command_time >= self.command_timeout_sec
        ):
            if self.linear_velocity != 0.0 or self.angular_velocity != 0.0:
                self.get_logger().warn("速度命令超时，小车停止")

            self.linear_velocity = 0.0
            self.angular_velocity = 0.0
            self.last_command_time = None
            
        self.x, self.y, self.theta = update_pose(
            x=self.x,
            y=self.y,
            theta=self.theta,
            linear_velocity=self.linear_velocity,
            angular_velocity=self.angular_velocity,
            dt=self.update_period,
        )

        self.publish_odometry()

    def publish_odometry(self):
        msg = Odometry()

        # 消息时间和坐标系
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"

        # 位姿：位置
        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.0

        # 平面角 theta 转成绕 z 轴旋转的四元数
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        msg.pose.pose.orientation.w = math.cos(self.theta / 2.0)

        # 速度：Twist 应表达在 child_frame_id，也就是 base_link 坐标系下
        msg.twist.twist.linear.x = self.linear_velocity
        msg.twist.twist.linear.y = 0.0
        msg.twist.twist.linear.z = 0.0
        msg.twist.twist.angular.x = 0.0
        msg.twist.twist.angular.y = 0.0
        msg.twist.twist.angular.z = self.angular_velocity

        self.odom_publisher.publish(msg)

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