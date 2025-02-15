from __future__ import annotations

from typing import List, Tuple, NewType, Optional, Sequence


class Device:
    def getModel(self) -> str: ...


# Note: we don't actually know if webots offers up tuples or lists.

class CameraRecognitionObject:
    def get_id(self) -> int: ...
    def get_position(self) -> Tuple[float, float, float]: ...
    def get_orientation(self) -> Tuple[float, float, float, float]: ...
    def get_size(self) -> Tuple[float, float]: ...
    def get_position_on_image(self) -> Tuple[int, int]: ...
    def get_size_on_image(self) -> Tuple[int, int]: ...
    def get_number_of_colors(self) -> int: ...
    def get_colors(self) -> Sequence[float]: ...
    def get_model(self) -> bytes: ...


class Camera(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...

    def getType(self) -> int: ...

    def getFov(self) -> float: ...
    def getMinFov(self) -> float: ...
    def getMaxFov(self) -> float: ...
    def setFov(self, fov: float) -> None: ...

    def getFocalLength(self) -> float: ...
    def getFocalDistance(self) -> float: ...
    def getMaxFocalDistance(self) -> float: ...
    def getMinFocalDistance(self) -> float: ...
    def setFocalDistance(self, focalDistance: float) -> None: ...

    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...

    def getNear(self) -> float: ...

    def getImage(self) -> bytes: ...

    @staticmethod
    def imageGetRed(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGreen(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetBlue(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def imageGetGray(image: bytes, width: int, x: int, y: int) -> int: ...
    @staticmethod
    def pixelGetRed(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGreen(pixel: int) -> int: ...
    @staticmethod
    def pixelGetBlue(pixel: int) -> int: ...
    @staticmethod
    def pixelGetGray(pixel: int) -> int: ...

    def hasRecognition(self) -> bool: ...
    def recognitionEnable(self, samplingPeriod: int) -> None: ...
    def recognitionDisable(self) -> None: ...
    def getRecognitionSamplingPeriod(self) -> int: ...
    def getRecognitionNumberOfObjects(self) -> int: ...
    def getRecognitionObjects(self) -> List[CameraRecognitionObject]: ...


class Compass(Device):
    def enable(self, samplingPeriod: int) -> None: ...
    def getValues(self) -> Tuple[float, float, float]: ...


class DistanceSensor(Device):
    GENERIC, INFRA_RED, SONAR, LASER = range(4)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...

    def getType(self) -> int: ...

    def getMaxValue(self) -> float: ...
    def getMinValue(self) -> float: ...
    def getAperture(self) -> float: ...


class Emitter(Device):
    CHANNEL_BROADCAST = -1

    def setChannel(self, channel: int) -> None: ...
    def getChannel(self) -> int: ...

    def send(self, data: bytes) -> int: ...

    def setRange(self, range: float) -> None: ...
    def getRange(self) -> float: ...

    def getBufferSize(self) -> int: ...


class LED(Device):
    def get(self) -> int: ...
    def set(self, value: int) -> None: ...  # noqa:A003


class Motor(Device):
    def setPosition(self, position: float) -> None: ...
    def setVelocity(self, velocity: float) -> None: ...
    def setAcceleration(self, acceleration: float) -> None: ...
    def setAvailableForce(self, force: float) -> None: ...
    def setAvailableTorque(self, torque: float) -> None: ...
    def setControlPID(self, p: float, i: float, d: float) -> None: ...
    def getTargetPosition(self) -> float: ...
    def getMinPosition(self) -> float: ...
    def getMaxPosition(self) -> float: ...
    def getVelocity(self) -> float: ...
    def getMaxVelocity(self) -> float: ...
    def getAcceleration(self) -> float: ...
    def getAvailableForce(self) -> float: ...
    def getMaxForce(self) -> float: ...
    def getAvailableTorque(self) -> float: ...
    def getMaxTorque(self) -> float: ...


class Receiver(Device):
    CHANNEL_BROADCAST = -1

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...

    def getQueueLength(self) -> int: ...
    def nextPacket(self) -> None: ...

    def getData(self) -> bytes: ...
    def getDataSize(self) -> int: ...

    def getSignalStrength(self) -> float: ...
    def getEmitterDirection(self) -> List[float]: ...

    def setChannel(self, channel: int) -> None: ...
    def getChannel(self) -> int: ...


class TouchSensor(Device):
    BUMPER, FORCE, FORCE3D = range(3)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...
    def getValues(self) -> List[float]: ...

    def getType(self) -> int: ...


class Keyboard(Device):
    (
        END,
        HOME,
        LEFT,
        UP,
        RIGHT,
        DOWN,
        PAGEUP,
        PAGEDOWN,
        NUMPAD_HOME,
        NUMPAD_LEFT,
        NUMPAD_UP,
        NUMPAD_RIGHT,
        NUMPAD_DOWN,
        NUMPAD_END,
        KEY,
        SHIFT,
        CONTROL,
        ALT,
    ) = range(18)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getKey(self) -> int: ...


class Display(Device):
    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...
    def setColor(self, color: int) -> None: ...
    def setAlpha(self, alpha: float) -> None: ...
    def setOpacity(self, opacity: float) -> None: ...
    def setFont(self, font: str, size: int, antiAliasing: bool) -> None: ...

    def drawPixel(self, x: int, y: int) -> None: ...
    def drawLine(self, x1: int, y1: int, x2: int, y2: int) -> None: ...
    def drawRectangle(self, x: int, y: int, width: int, height: int) -> None: ...
    def drawOval(self, cx: int, cy: int, a: int, b: int) -> None: ...
    def drawPolygon(self, x: int, y: int) -> None: ...
    def drawText(self, text: str, x: int, y: int) -> None: ...
    def fillRectangle(self, x: int, y: int, width: int, height: int) -> None: ...
    def fillOval(self, cx: int, cy: int, a: int, b: int) -> None: ...
    def fillPolygon(self, x: int, y: int) -> None: ...

    # (RGB, RGBA, ARGB, BGRA, ABGR) = range(5)

    # def imageNew(
    #     self,
    #     data,
    #     format,
    #     width: Optional[int] = None,
    #     height: Optional[int] = None,
    # ): ...
    # def imageLoad(self, filename: str): ...
    # def imageCopy(self, x: int, y: int, width: int, height: int): ...
    # def imagePaste(self, ir, x: int, y: int, blend: bool = False) -> None: ...
    # def imageSave(self, ir, filename: str) -> None: ...
    # def imageDelete(self, ir) -> None: ...


class Connector(Device):
    def enablePresence(self, samplingPeriod: int) -> None: ...
    def disablePresence(self) -> None: ...
    def getPresenceSamplingPeriod(self) -> int: ...
    def getPresence(self) -> int: ...  # -1 returned if connector is passive
    def isLocked(self) -> bool: ...
    def lock(self) -> None: ...
    def unlock(self) -> None: ...


class PositionSensor (Device):
    ROTATIONAL, LINEAR = range(2)

    def enable(self, samplingPeriod: int) -> None: ...
    def disable(self) -> None: ...
    def getSamplingPeriod(self) -> int: ...
    def getValue(self) -> float: ...
    def getType(self) -> int: ...
    # def getBrake(self) -> Brake: ...
    def getMotor(self) -> Motor: ...


class Field:
    def getSFBool(self) -> bool: ...
    def getSFInt32(self) -> int: ...
    def getSFFloat(self) -> float: ...
    def getSFVec2f(self) -> List[float]: ...
    def getSFVec3f(self) -> List[float]: ...
    def getSFRotation(self) -> List[float]: ...
    def getSFColor(self) -> List[float]: ...
    def getSFString(self) -> str: ...
    def getSFNode(self) -> Node: ...
    def getMFBool(self, index: int) -> bool: ...
    def getMFInt32(self, index: int) -> int: ...
    def getMFFloat(self, index: int) -> float: ...
    def getMFVec2f(self, index: int) -> List[float]: ...
    def getMFVec3f(self, index: int) -> List[float]: ...
    def getMFColor(self, index: int) -> List[float]: ...
    def getMFRotation(self, index: int) -> List[float]: ...
    def getMFString(self, index: int) -> str: ...
    def getMFNode(self, index: int) -> Node: ...

    def setSFBool(self, value: bool) -> None: ...
    def setSFInt32(self, value: int) -> None: ...
    def setSFFloat(self, value: float) -> None: ...
    def setSFVec2f(self, values: List[float]) -> None: ...
    def setSFVec3f(self, values: List[float]) -> None: ...
    def setSFRotation(self, values: List[float]) -> None: ...
    def setSFColor(self, values: List[float]) -> None: ...
    def setSFString(self, value: str) -> None: ...
    def setMFBool(self, index: int, value: bool) -> None: ...
    def setMFInt32(self, index: int, value: int) -> None: ...
    def setMFFloat(self, index: int, value: float) -> None: ...
    def setMFVec2f(self, index: int, values: List[float]) -> None: ...
    def setMFVec3f(self, index: int, values: List[float]) -> None: ...
    def setMFRotation(self, index: int, values: List[float]) -> None: ...
    def setMFColor(self, index: int, values: List[float]) -> None: ...
    def setMFString(self, index: int, value: str) -> None: ...


class Node:
    def getField(self, fieldName: str) -> Field: ...
    def getProtoField(self, fieldName: str) -> Field: ...

    def remove(self) -> None: ...

    def restartController(self) -> None: ...

    def setVelocity(self, velocity: List[float]) -> None: ...
    def resetPhysics(self) -> None: ...


class Robot:
    def __init__(self) -> None: ...
    def __del__(self) -> None: ...
    def step(self, duration: int) -> int: ...
    def getTime(self) -> float: ...
    def getBasicTimeStep(self) -> float: ...

    def getCustomData(self) -> str: ...
    def setCustomData(self, data: str) -> None: ...

    def getCamera(self, name: str) -> Camera: ...
    def getDistanceSensor(self, name: str) -> DistanceSensor: ...
    def getEmitter(self, name: str) -> Emitter: ...
    def getLED(self, name: str) -> LED: ...
    def getMotor(self, name: str) -> Motor: ...
    def getReceiver(self, name: str) -> Receiver: ...
    def getTouchSensor(self, name: str) -> TouchSensor: ...
    def getCompass(self, name: str) -> Compass: ...
    def getDisplay(self, name: str) -> Display: ...

    def getDevice(self, name: str) -> Optional[Device]: ...


# Beware: this type doesn't actually exist in Webots. It's just here for type
# safety.
SimulationMode = NewType('SimulationMode', int)


class Supervisor(Robot):
    SIMULATION_MODE_PAUSE: SimulationMode
    SIMULATION_MODE_REAL_TIME: SimulationMode
    SIMULATION_MODE_RUN: SimulationMode
    SIMULATION_MODE_FAST: SimulationMode

    def getRoot(self) -> Node: ...
    def getSelf(self) -> Node: ...
    def getFromDef(self, name: str) -> Optional[Node]: ...
    def getFromId(self, id: int) -> Optional[Node]: ...
    def getSelected(self) -> Optional[Node]: ...

    def animationStartRecording(self, file: str) -> bool: ...
    def animationStopRecording(self) -> bool: ...

    def movieStartRecording(
        self,
        file: str,
        width: int,
        height: int,
        quality: int,
        codec: int,
        acceleration: int,
        caption: bool,
    ) -> bool: ...
    def movieStopRecording(self) -> bool: ...
    def movieIsReady(self) -> bool: ...
    def movieFailed(self) -> bool: ...

    def simulationQuit(self, status: int) -> None: ...
    def simulationReset(self) -> None: ...
    def simulationGetMode(self) -> SimulationMode: ...
    def simulationSetMode(self, mode: SimulationMode) -> None: ...

    def worldLoad(self, file: str) -> None: ...
    def worldSave(self, file: Optional[str] = None) -> bool: ...
    def worldReload(self) -> None: ...
