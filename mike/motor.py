from machine import Pin, Timer, 
from utime import sleep_us
import rp2

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
LINEAR_STEP_XY = PITCH / STEPS_PER_REV_XY  # 0.00125 mm/step
LINEAR_STEP_Z = PITCH / STEPS_PER_REV_Z  # 0.0025 mm/step

### Direction mapping for postive and negative xyz motion on the canvas
POS_XY = 0 # anticlockwise
NEG_XY = 1 # clockwise
POS_Z = 1 
NEG_Z = 0

XY_CORRECTION = -1

### Pulse definition ###
STEP_PERIOD = 150  # us
MOTOR_PULSE_PERIOD = 600  # us pps


X_POS = 0
Y_POS = 0
Z_POS = 0


class Motor:
    def __init__(self):
        self.steps_to_take = 0
        self.activedir = True
        self.dirchange = True
        self.activeangle = 0.0
        self.DIR_PIN = None
        self.STEP_PIN = None
        self.home_pin = 0
        self.full_step = None
        self.directionchangedelaycounter = 0
        # self.stm_pio = None
        self.stm_sm = None
        self.EN_PIN = None


    def enable(self):
        self.EN_PIN.value(0)

    def disable(self):
        self.EN_PIN.value(1)
    
    # def step(self):
    #     self._step.value(not self._step.value())
    
    # def rotate_motor(self, delay):
    #     self._timer.init()

    # def step_motor(self, direction: int, steps: int):
    #     self._direction.value(direction)

    #     for _ in range(steps):
    #         self._step.value(1)
    #         sleep_us(STEP_PERIOD)
    #         self._step.value(0)
    #         sleep_us(MOTOR_PULSE_PERIOD)
    #         self._positon +=  -(2*direction-1)




def init_pins(motor_x: Motor, motor_y: Motor, motor_z: Motor):
    motor_x.EN_PIN = Pin(MOTOR_X_EN, Pin.OUT)
    motor_x.STEP_PIN = Pin(MOTOR_X_STEP, Pin.OUT)
    motor_x.DIR_PIN = Pin(MOTOR_X_DIR, Pin.OUT)
    motor_x.disable()
    motor_x.full_step = STEPS_PER_REV_XY
    motor_x.stm_sm = 0

    motor_y.EN_PIN = Pin(MOTOR_Y_EN, Pin.OUT)
    motor_y.STEP_PIN = Pin(MOTOR_Y_STEP, Pin.OUT)
    motor_y.DIR_PIN = Pin(MOTOR_Y_DIR, Pin.OUT)
    motor_y.disable()
    motor_y.full_step = STEPS_PER_REV_XY

    motor_z.EN_PIN = Pin(MOTOR_Z_EN, Pin.OUT)
    motor_z.STEP_PIN = Pin(MOTOR_Z_STEP, Pin.OUT)
    motor_z.DIR_PIN = Pin(MOTOR_Z_DIR, Pin.OUT)
    motor_z.disable()
    motor_z.full_step = STEPS_PER_REV_Z

def turn(sm):
  print("irq")

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

def init_pio(motor_x: Motor):
    # motor_x.stm_pio = rp2.PIO(0)
    motor_x.stm_sm = rp2.StateMachine(0, step_counter, freq=10000, sideset_base=motor_x.STEP_PIN)


    


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

