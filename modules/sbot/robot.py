from __future__ import annotations

import math
import random
from os import path, environ
from typing import Optional
from threading import Lock

from sbot import motor, radio, magnet, arduino, compass, encoder
# Webots specific library
from controller import Robot as WebotsRobot
from shared_utils import RobotType


class Robot:
    """
    Primary API for access to robot parts.

    This robot requires that the consumer manage the progession of time manually
    by calling the `sleep` method.
    """

    def __init__(self, quiet: bool = False, init: bool = True) -> None:
        self._initialised = False
        self._quiet = quiet

        self.webot = WebotsRobot()
        # returns a float, but should always actually be an integer value
        self._timestep = int(self.webot.getBasicTimeStep())

        self.mode = environ.get("SR_ROBOT_MODE", "dev")
        self.zone = int(environ.get("SR_ROBOT_ZONE", 0))
        self.type = RobotType(environ.get("SR_ROBOT_TYPE", "forklift"))
        self.arena = "A"
        self.usbkey = path.normpath(path.join(environ["SR_ROBOT_FILE"], "../"))

        # Lock used to guard access to Webot's time stepping machinery, allowing
        # us to safely advance simulation time from *either* the competitor's
        # code (in the form of our `sleep` method) or from our background
        # thread, but not both.
        self._step_lock = Lock()

        if init:
            self.init()
            self.wait_start()

    @classmethod
    def setup(cls) -> Robot:
        return cls(init=False)

    def init(self) -> None:
        self._init_devs()
        self._initialised = True
        self.display_info()

    def _get_user_code_info(self) -> Optional[str]:
        user_version_path = path.join(self.usbkey, '.user-rev')
        if path.exists(user_version_path):
            with open(user_version_path) as f:
                return f.read().strip()

        return None

    def display_info(self) -> None:
        user_code_version = self._get_user_code_info()

        parts = [
            f"Zone: {self.zone}",
            f"Mode: {self.mode}",
            f"Type: {self.type.value}",
        ]

        if user_code_version:
            parts.append(f"User code: {user_code_version}")

        print("Robot Initialized. {}.".format(", ".join(parts)))  # noqa:T001

    def webots_step_and_should_continue(self, duration_ms: int) -> bool:
        """
        Run a webots step of the given duration in milliseconds.

        Returns whether or not the simulation should continue (based on
        Webots telling us whether or not the simulation is about to end).
        """

        if duration_ms <= 0:
            raise ValueError(
                f"Duration must be greater than zero, not {duration_ms!r}",
            )

        with self._step_lock:
            # We use Webots in synchronous mode (specifically
            # `synchronization` is left at its default value of `TRUE`). In
            # that mode, Webots returns -1 from step to indicate that the
            # simulation is terminating, or 0 otherwise.
            result = self.webot.step(duration_ms)
            return result != -1

    def wait_start(self) -> None:
        "Wait for the start signal to happen"

        if self.mode not in ["comp", "dev", "remote-dev"]:
            raise Exception(
                f"mode of '{self.mode}' is not supported -- must be 'comp', "
                "'dev or 'remote-dev'",
            )
        if self.zone < 0 or self.zone > 3:
            raise Exception(
                f"zone must be in range 0-3 inclusive -- value of {self.zone} is invalid",
            )
        if self.arena not in ["A", "B"]:
            raise Exception("arena must be A or B")

        print("Waiting for start signal.")  # noqa:T001

        # Always advance time by a little bit. This simulates the real-world
        # condition that the wait-start mechanism would always wait for the
        # start button.
        self.webots_step_and_should_continue(
            self._timestep * random.randint(8, 20),
        )

        if self.mode in ['comp', 'remote-dev']:
            # Interact with the supervisor "robot" to wait for the start of the match.
            self.webot.setCustomData('ready')
            while (
                self.webot.getCustomData() != 'start' and
                self.webots_step_and_should_continue(self._timestep)
            ):
                pass

        print("Starting")  # noqa:T001

    def _init_devs(self) -> None:
        "Initialise the attributes for accessing devices"

        # Motor boards
        self._init_motors()

        # Ruggeduinos
        self._init_arduino()

        # No camera for SR2021

        # Radio
        self._init_radio()

        # Compass
        self._init_compass()

        # Crane Magnet
        self._init_magnet()

        # Position encoders
        self._init_encoders()

    def _init_motors(self) -> None:
        self.motor_boards = motor.init_motor_array(self.webot, self.type)

    def _init_arduino(self) -> None:
        self.arduino = arduino.init_arduino(self.webot, self.type)

    def _init_radio(self) -> None:
        self.radio = radio.Radio(self.webot, self.zone, self._step_lock)

    def _init_compass(self) -> None:
        if self.type != RobotType.CRANE:  # The crane lacks a compass
            self.compass = compass.Compass(self.webot)

    def _init_magnet(self) -> None:
        if self.type == RobotType.CRANE:
            self.magnet = magnet.Magnet(self.webot)

    def _init_encoders(self) -> None:
        self.encoders = encoder.init_encoder_array(self.webot, self.type)

    def time(self) -> float:
        """
        Roughly equivalent to `time.time` but for simulation time.
        """
        return self.webot.getTime()

    def sleep(self, secs: float) -> None:
        """
        Roughly equivalent to `time.sleep` but accounting for simulation time.
        """
        # Checks that secs is positive or zero
        if secs < 0:
            raise ValueError('sleep length must be non-negative')

        # Ensure the time delay is a valid step increment, while also ensuring
        # that small values remain nonzero.
        n_steps = math.ceil((secs * 1000) / self._timestep)
        duration_ms = n_steps * self._timestep

        # Assume that we're in the main thread here, so we don't really need to
        # do any cleanup if Webots tells us the simulation is terminating. When
        # webots kills the process all the proper tidyup will happen anyway.
        self.webots_step_and_should_continue(duration_ms)

    @property
    def is_competition(self) -> bool:
        return self.mode == 'comp'
