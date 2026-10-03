#include <chrono>
#include <cmath>
#include <cstddef>
#include <memory>

#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"

class OdomMonitor : public rclcpp::Node
{
public:
  OdomMonitor()
  : Node("odom_monitor"),
    last_odom_time_(std::chrono::steady_clock::now())
  {
    subscription_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "/odom",
      10,
      [this](nav_msgs::msg::Odometry::ConstSharedPtr msg) {
        this->odom_callback(msg);
      });

    check_timer_ = this->create_wall_timer(
      std::chrono::milliseconds(200),
      [this]() {
        this->check_odom_timeout();
      });
  }

private:
  void odom_callback(nav_msgs::msg::Odometry::ConstSharedPtr msg)
  {
    last_odom_time_ = std::chrono::steady_clock::now();

    if (odom_missing_) {
      RCLCPP_INFO(this->get_logger(), "/odom 已恢复，开始新的统计段");
      odom_missing_ = false;
      has_previous_pose_ = false;
      total_distance_ = 0.0;
      message_count_ = 0;
    }

    const double x = msg->pose.pose.position.x;
    const double y = msg->pose.pose.position.y;

    if (!std::isfinite(x) || !std::isfinite(y)) {
      RCLCPP_WARN(this->get_logger(), "收到无效位置，本条不计入路程");
      return;
    }

    if (!has_previous_pose_) {
      start_x_ = x;
      start_y_ = y;
      has_previous_pose_ = true;
    } else {
      const double step = std::hypot(x - previous_x_, y - previous_y_);
      total_distance_ += step;
    }

    previous_x_ = x;
    previous_y_ = y;

    const double displacement = std::hypot(x - start_x_, y - start_y_);
    const double v = msg->twist.twist.linear.x;
    const double omega = msg->twist.twist.angular.z;

    ++message_count_;
    if (message_count_ % 10 == 1) {
      RCLCPP_INFO(
        this->get_logger(),
        "x=%.3f y=%.3f | v=%.3f omega=%.3f | path=%.3f m "
        "displacement=%.3f m",
        x, y, v, omega, total_distance_, displacement);
    }
  }

  void check_odom_timeout()
  {
    const auto now = std::chrono::steady_clock::now();
    const auto elapsed = now - last_odom_time_;

    if (!odom_missing_ && elapsed >= std::chrono::seconds(1)) {
      odom_missing_ = true;
      RCLCPP_WARN(
        this->get_logger(),
        "超过 1 秒没有收到 /odom；这与小车速度为零不同");
    }
  }

  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
  rclcpp::TimerBase::SharedPtr check_timer_;

  std::chrono::steady_clock::time_point last_odom_time_;
  bool odom_missing_ = false;
  bool has_previous_pose_ = false;

  double start_x_ = 0.0;
  double start_y_ = 0.0;
  double previous_x_ = 0.0;
  double previous_y_ = 0.0;
  double total_distance_ = 0.0;
  std::size_t message_count_ = 0;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomMonitor>());
  rclcpp::shutdown();
  return 0;
}