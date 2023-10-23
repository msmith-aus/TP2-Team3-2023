from machine import Pin
from utime import sleep_us


### PIN MAPPINGS ###

### X ###
MOTOR_X_EN = 28  # Motor enable pin
MOTOR_X_STEP = 21  # Pin to pulse for each step
MOTOR_X_DIR = 20  # Clockwise/ anit-clockwise ()
MOTOR_X_MS0 = 27
MOTOR_X_MS1 = 26
MOTOR_X_MS2 = 22
### Y ###

MOTOR_Y_EN = 13
MOTOR_Y_STEP = 9
MOTOR_Y_DIR = 8
MOTOR_Y_MS0 = 12
MOTOR_Y_MS1 = 11
MOTOR_Y_MS2 = 10
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
STEP_PERIOD = 5 # us
MOTOR_PULSE_PERIOD = 600  # us pps
START_SPEED = 1500 #PPS
FINAL_SPEED = 10000 #PPS
ACCEL_INC = 10 #PPS
ACCELERATION = 2000 #PPSPS
ACCEL_UPDATE_RATE = ACCELERATION / ACCEL_INC
MICRO_STEP = 2 # HALF




X_POS = 0
Y_POS = 0
Z_POS = 0


class Motor:
    def __init__(self):
        self._enable = None
        self._step = None
        self._direction = None
        self._position = 0 # Position in Steps
        self._cur_speed = 0 # PPS
        self._MSO = 0
        self._MS1 = 0
        self._MS2 = 0

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
    
    def deccelerate(self, increment):
        self._cur_speed -= increment

    def update_pos(self, steps):
        self._position += steps
    
    def get_position(self):
        return self._position
    


def init_pins(motor_x: Motor, motor_y: Motor, motor_z: Motor):
    motor_x._enable = Pin(MOTOR_X_EN, Pin.OUT)
    motor_x._step = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_x._direction = Pin(MOTOR_X_DIR, Pin.OUT)
    motor_x._MS0 = Pin(MOTOR_X_MS0, Pin.OUT)
    motor_x._MS1 = Pin(MOTOR_X_MS1, Pin.OUT)
    motor_x._MS2 = Pin(MOTOR_X_MS2, Pin.OUT)
    motor_x._MS0.value(1)
    motor_x._MS1.value(0)
    motor_x._MS2.value(0)
    motor_y._enable = Pin(MOTOR_Y_EN, Pin.OUT)
    motor_y._step = Pin(MOTOR_Y_STEP, Pin.OUT)
    motor_y._direction = Pin(MOTOR_Y_DIR, Pin.OUT)
    motor_y._MS0 = Pin(MOTOR_Y_MS0, Pin.OUT)
    motor_y._MS1 = Pin(MOTOR_Y_MS1, Pin.OUT)
    motor_y._MS2 = Pin(MOTOR_Y_MS2, Pin.OUT)
    motor_y._MS0.value(1)
    motor_y._MS1.value(0)
    motor_y._MS2.value(0)
    motor_z._enable = Pin(MOTOR_Z_EN, Pin.OUT)
    motor_z._step = Pin(MOTOR_Z_STEP, Pin.OUT)
    motor_z._direction = Pin(MOTOR_Z_DIR, Pin.OUT)
    motor_x.disable()
    motor_y.disable()
    motor_z.disable()

def move_canvas(motor_z, dir):
    
    motor_z.enable()
    print("Moving z stage")
    for _ in range(200):
        motor_z.step_motor(dir)
        sleep_us(2500)
    motor_z.disable()
        
def step_forward(motor_x, motor_y):

    motor_x.enable()
    motor_y.enable()
    for _ in range(800 * MICRO_STEP):
        motor_x.step_motor(POS_XY)
        sleep_us(500)

    for _ in range(800 * MICRO_STEP):
        motor_y.step_motor(POS_XY)
        sleep_us(500)
        
    motor_x.disable()
    motor_y.disable()
        
def to_start(motor_x, motor_y, motor_z):
    move_canvas(motor_z, NEG_Z)
    sleep_us(5000)
    step_forward(motor_x, motor_y)
    sleep_us(5000)


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







