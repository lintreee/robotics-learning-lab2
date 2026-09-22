import math


def update_pose(
    x,
    y,
    theta,
    linear_velocity,
    angular_velocity,
    dt,
):
    """使用前向欧拉法更新二维移动机器人位姿。

    Args:
        x: 世界坐标系中的x坐标，单位m。
        y: 世界坐标系中的y坐标，单位m。
        theta: 机器人朝向，单位rad。
        linear_velocity: 机器人前进速度，单位m/s。
        angular_velocity: 机器人角速度，单位rad/s。
        dt: 积分时间步长，单位s。

    Returns:
        更新后的(new_x, new_y, new_theta)。
    """
    if dt <= 0.0:
        raise ValueError("dt must be greater than zero")

    new_x = x + linear_velocity * math.cos(theta) * dt
    new_y = y + linear_velocity * math.sin(theta) * dt
    new_theta = theta + angular_velocity * dt

    return new_x, new_y, new_theta

