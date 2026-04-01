from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'drone_comms'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
      ('share/' + package_name, ['package.xml']),
    ('share/' + package_name + '/launch', ['launch/stack.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mehida',
    maintainer_email='mehidabino@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['altitude_pub = drone_comms.altitude_pub:main',
        'altitude_monitor = drone_comms.altitude_monitor:main',
        ],
    },
)
