#include <memory>

#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"

class OdomMonitor : public rclcpp::Node
{
public:
  OdomMonitor()
  : Node("odom_monitor")
  {
    subscription_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "/odom",
      10,
      [this](nav_msgs::msg::Odometry::ConstSharedPtr msg) {
        const double x = msg->pose.pose.position.x;
        const double y = msg->pose.pose.position.y;
        const double v = msg->twist.twist.linear.x;

        RCLCPP_INFO(
          this->get_logger(),
          "position: x=%.3f m, y=%.3f m | linear velocity=%.3f m/s",
          x, y, v);
      });
  }

private:
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomMonitor>());
  rclcpp::shutdown();
  return 0;
}