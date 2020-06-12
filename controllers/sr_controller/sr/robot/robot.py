import time
from threading import Lock, Thread

from sr.robot import motor, camera, ruggeduino
from sr.robot.game import stop_after_delay
from sr.robot.settings import TIME_STEP

# Webots specific library
from controller import Robot as WebotsRobot  # isort:skip


class Robot(object):
    """Class for initialising and accessing robot hardware"""

    def __init__(self, quiet=False, init=True):
        self._initialised = False
        self._quiet = quiet

        # TODO set these values dynamically
        self.mode = "dev"
        self.zone = 0
        self.arena = "A"

        self.webot = WebotsRobot()

        # Lock used to guard access to Webot's time stepping machinery, allowing
        # us to safely advance simulation time from *either* the competitor's
        # code (in the form of our `sleep` method) or from our background
        # thread, but not both.
        self._step_lock = Lock()

        if init:
            self.init()
            self.wait_start()
            if self.mode == "comp":
                stop_after_delay()

    @classmethod
    def setup(cls):
        return cls()

    def init(self):
        self.webots_init()
        self._init_devs()
        self._initialised = True

    def webots_init(self):
        # Create a thread which will advance time in the background, so that the
        # competitors' code can ignore the fact that it is actually running in a
        # simulation.
        t = Thread(
            target=self.webot_run_robot,
            # Ensure our background thread alone won't keep the controller
            # process runnnig.
            daemon=True,
        )
        t.start()
        time.sleep(TIME_STEP / 1000)

    def webots_step_and_should_continue(self, duration_ms: int) -> bool:
        """
        Run a webots step of the given duration in milliseconds.

        Returns whether or not Webots is about to terminate the simulation.
        """

        with self._step_lock:
            # We use Webots in synchronous mode (specifically
            # `synchronization` is left at its default value of `TRUE`). In
            # that mode, Webots returns -1 from step to indicate that the
            # simulation is terminating, or 0 otherwise.
            result = self.webot.step(duration_ms)
            return result != -1

    def webot_run_robot(self):
        while self.webots_step_and_should_continue(TIME_STEP):
            pass

    def wait_start(self):
        "Wait for the start signal to happen"

        if self.mode not in ["comp", "dev"]:
            raise Exception(
                "mode of '%s' is not supported -- must be 'comp' or 'dev'" % self.mode,
            )
        if self.zone < 0 or self.zone > 3:
            raise Exception(
                "zone must be in range 0-3 inclusive -- value of %i is invalid" % self.zone,
            )
        if self.arena not in ["A", "B"]:
            raise Exception("arena must be A or B")

    def _init_devs(self):
        "Initialise the attributes for accessing devices"

        # Motor boards
        self._init_motors()

        # Ruggeduinos
        self._init_ruggeduinos()

        # Camera
        self._init_camera()

    def _init_motors(self):
        self.motors = motor.init_motor_array(self.webot)

    def _init_ruggeduinos(self):
        self.ruggeduinos = ruggeduino.init_ruggeduino_array(self.webot)

    def _init_camera(self):
        self.camera = camera.Camera(self.webot)
        self.see = self.camera.see

    def time(self) -> float:
        """
        Roughly equivalent to `time.time` but for simulation time.
        """
        return self.webot.getTime()

    def sleep(self, secs: float) -> None:
        """
        Roughly equivalent to `time.sleep` but accounting for simulation time.
        """

        # Ensure the time delay is a valid step increment
        n_steps = int((secs * 1000) // TIME_STEP)
        duration_ms = n_steps * TIME_STEP

        # We're in the main thread here, so we don't really need to do any
        # cleanup if Webots tells us the simulation is terminating. When webots
        # kills the process all the proper tidyup will happen anyway.
        self.webots_step_and_should_continue(duration_ms)
