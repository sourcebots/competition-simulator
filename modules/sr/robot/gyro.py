from typing import cast, Tuple

from controller import Gyro as WebotsGyro, Robot
from sr.robot.utils import get_robot_device
from sr.robot.randomizer import add_jitter


class Gyro:
    def __init__(self, webot: Robot):
        self._gyro = get_robot_device(webot, "robot gyro", WebotsGyro)
        self._gyro.enable(int(webot.getBasicTimeStep()))

    def angular_velocity(self) -> Tuple[float, float, float]:
        raw_velocities = self._gyro.getValues()
        velocities = cast(Tuple[float, float, float], tuple(
            # no actual bounds, should never exceed 100 rad/s
            add_jitter(velocity, -100, 100)
            for velocity in raw_velocities
        ))
        return velocities
