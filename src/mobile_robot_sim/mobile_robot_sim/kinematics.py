import math


def update_pose(
    x,
    y,
    theta,
    linear_velocity,
    angular_velocity,
    dt,
):
 
    if dt <= 0.0:
        raise ValueError("dt必须大于0")

    new_x = x + linear_velocity * math.cos(theta) * dt
    new_y = y + linear_velocity * math.sin(theta) * dt
    new_theta = theta + angular_velocity * dt

    return new_x, new_y, new_theta