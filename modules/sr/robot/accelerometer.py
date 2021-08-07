from typing import cast, Tuple

from controller import Robot, Accelerometer as WebotsAccelerometer
from sr.robot.utils import get_robot_device
from sr.robot.randomizer import add_jitter


class Accelerometer:
    def __init__(self, webot: Robot):
        self._accelerometer = get_robot_device(
            webot,
            "robot accelerometer",
            WebotsAccelerometer,
        )
        self._accelerometer.enable(int(webot.getBasicTimeStep()))

    def accelerations(self) -> Tuple[float, float, float]:
        raw_accelerations = self._accelerometer.getValues()
        accelerations = cast(Tuple[float, float, float], tuple(
            # no actual bounds, should never exceed 10G
            add_jitter(acceleration, -98.1, 98.1)
            for acceleration in raw_accelerations
        ))
        return accelerations
