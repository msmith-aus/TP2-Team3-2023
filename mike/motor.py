from machine import Pin
from utime import sleep_us

### PIN MAPPINGS ###

### X ###
MOTOR_X_EN = 28  # Motor enable pin
MOTOR_X_STEP = 21  # Pin to pulse for each step
MOTOR_X_DIR = 20  # Clockwise/ anit-clockwise ()
### Y ###

MOTOR_Y_EN = 28
MOTOR_Y_STEP = 21
MOTOR_Y_DIR = 20
### Z ###

MOTOR_Z_EN = 5
MOTOR_Z_STEP = 1
MOTOR_Z_DIR = 0

### CONSTANTS ###
STEPS_PER_REV_XY = 400  # 0.9 degress
STEPS_PER_REV_Z = 200
PITCH = 1  # 1mm
LINEAR_STEP_XY = PITCH / STEPS_PER_REV_XY  # 0.0025 mm/step
LINEAR_STEP_Z = PITCH / STEPS_PER_REV_Z  # 0.005 mm/step

### Direction mapping for postive and negative xyz motion on the canvas
POS_XY = 0 
NEG_XY = 1
POS_Z = 1
NEG_Z = 0

### Pulse definition ###
STEP_PERIOD = 500  # us
MOTOR_PULSE_PERIOD = 1000  # us pps


X_POS = 0
Y_POS = 0
Z_POS = 0


class Motor:
    def __init__(self):
        self._enable = None
        self._step = None
        self._direction = None
        self._positon = None

    def enable(self):
        self._enable.value(0)
        self._step.value(0)
        self._direction.value(0)

    def disable(self):
        self._enable.value(1)
        self._enable.value(1)
        self._enable.value(1)

    def step_motor(self, direction: int, steps: int):
        self._direction.value(direction)
        for _ in range(steps):
            self._step.value(1)
            sleep_us(STEP_PERIOD)
            self._step.value(0)
            sleep_us(MOTOR_PULSE_PERIOD)


def init_pins(motor_x: Motor, motor_y: Motor, motor_z: Motor):
    motor_x._enable = Pin(MOTOR_X_EN, Pin.OUT)
    motor_x._step = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_x._direction = Pin(MOTOR_X_DIR, Pin.OUT)
    motor_y._enable = Pin(MOTOR_X_EN, Pin.OUT)
    motor_y._step = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_y._direction = Pin(MOTOR_X_DIR, Pin.OUT)
    motor_z._enable = Pin(MOTOR_X_EN, Pin.OUT)
    motor_z._step = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_z._direction = Pin(MOTOR_X_DIR, Pin.OUT)
