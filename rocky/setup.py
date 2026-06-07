import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rocky'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cwilhelm',
    maintainer_email='cwilhelm@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gait_controller = rocky.gait_controller:main',
            'inverse_kinematics = rocky.inverse_kinematics:main',
            'angle_mapper = rocky.angle_mapper:main',
            'serial_bridge = rocky.serial_bridge:main',
        ],
    },
)
