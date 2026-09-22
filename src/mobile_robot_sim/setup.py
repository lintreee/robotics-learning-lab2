from setuptools import find_packages, setup

package_name = 'mobile_robot_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lindejun',
    maintainer_email='3189466923@qq.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    "console_scripts": [
        "velocity_publisher = mobile_robot_sim.velocity_publisher:main",
        "velocity_subscriber = mobile_robot_sim.velocity_subscriber:main",
        "mobile_robot_simulator = mobile_robot_sim.mobile_robot_simulator:main",
    ],
},
)
