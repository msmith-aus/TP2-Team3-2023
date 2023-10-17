from machine import Pin
from utime import sleep_us

### PIN MAPPINGS ###

### X ###
MOTOR_X_EN = 28  # Motor enable pin
MOTOR_X_STEP = 21  # Pin to pulse for each step
MOTOR_X_DIR = 20  # Clockwise/ anit-clockwise ()
### Y ###

MOTOR_Y_EN = 13
MOTOR_Y_STEP = 9
MOTOR_Y_DIR = 8
### Z ###

MOTOR_Z_EN = 5
MOTOR_Z_STEP = 1
MOTOR_Z_DIR = 0

### CONSTANTS ###
STEPS_PER_REV_XY = 400  # 0.9 degress
STEPS_PER_REV_Z = 200
PITCH = 0.5  # 0.5 mm
LINEAR_STEP_XY = PITCH / STEPS_PER_REV_XY  # 0.000125 mm/step
LINEAR_STEP_Z = PITCH / STEPS_PER_REV_Z  # 0.0025 mm/step

### Direction mapping for postive and negative xyz motion on the canvas
POS_XY = 0 
NEG_XY = 1
POS_Z = 1
NEG_Z = 0

XY_CORRECTION = -1

### Pulse definition ###
STEP_PERIOD = 150  # us
MOTOR_PULSE_PERIOD = 600  # us pps
START_SPEED = 200 #PPS
ACCELERATION = 1000 #PPSPS
FINAL_SPEED = 5000 #PPS
ACCEL_INC = 20 #PPS
ACCEL_UPDATE_RATE = ACCELERATION / ACCEL_INC # Updates per second




X_POS = 0
Y_POS = 0
Z_POS = 0


class Motor:
    def __init__(self):
        self._enable = None
        self._step = None
        self._direction = None
        self._positon = 0
        self._cur_speed = 0

    def enable(self):
        self._enable.value(0)
        self._step.value(0)
        self._direction.value(0)

    def disable(self):
        self._enable.value(1)
        self._enable.value(1)
        self._enable.value(1)

    def step_motor(self, direction: int):

        self._direction.value(direction)

        self._step.value(1)
        sleep_us(STEP_PERIOD)
        self._step.value(0)

    def set_current_speed(self, speed: int):
        self._cur_speed = speed

    def get_current_speed(self) -> None:
        return self._cur_speed
    
    def accelerate(self, increment):
        self._cur_speed += increment
    
    def decelerate(self, increment):
        self._cur_speed -= increment

    def update_pos(self, steps):
        self._position += steps
    
    def get_position(self):
        return self._position
    


def init_pins(motor_x: Motor, motor_y: Motor, motor_z: Motor):
    motor_x._enable = Pin(MOTOR_X_EN, Pin.OUT)
    motor_x._step = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_x._direction = Pin(MOTOR_X_DIR, Pin.OUT)
    motor_y._enable = Pin(MOTOR_Y_EN, Pin.OUT)
    motor_y._step = Pin(MOTOR_Y_STEP, Pin.OUT)
    motor_y._direction = Pin(MOTOR_Y_DIR, Pin.OUT)
    motor_z._enable = Pin(MOTOR_Z_EN, Pin.OUT)
    motor_z._step = Pin(MOTOR_Z_STEP, Pin.OUT)
    motor_z._direction = Pin(MOTOR_Z_DIR, Pin.OUT)
    motor_x.disable()
    motor_y.disable()
    motor_z.disable()


def out_and_back(motor: Motor, led):
    while True:
        # Move X Up and Back ###
        motor.enable()
        motor.step_motor(POS_XY, STEPS_PER_REV_Z)
        motor.step_motor(NEG_XY, STEPS_PER_REV_Z)
        print("Motor EN: ", motor._enable.value())
        motor.disable()
        motor.step_motor(POS_XY, STEPS_PER_REV_Z)
        motor.step_motor(NEG_XY, STEPS_PER_REV_Z)
        print("Motor EN: ", motor._enable.value())
        sleep(1)
        led.toggle()
        sleep_ms(200)
        led.toggle()

