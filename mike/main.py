### Imports ###
import utime
from machine import Pin
import math
from fractions import Fraction

### Constants ###
STEPS_PER_REV = 400 # 0.9 degress
PITCH = 1 # 1mm
LINEAR_STEP = PITCH / STEPS_PER_REV # 0.0025 mm/step

FORWARD = 1
BACKWARD = 0

STEP_DELAY = 100 # us
MOTOR_SPEED = 2000 # us

### Pins ###
MOTOR_X_EN = 13
MOTOR_X_M0 = 12
MOTOR_X_M1 = 11
MOTOR_X_M2 = 10
MOTOR_X_STEP = 9
MOTOR_X_DIR = 8
X_POS = 0

MOTOR_Y_EN = 28
MOTOR_Y_M0 = 27
MOTOR_Y_M1 = 26
MOTOR_Y_M2 = 22
MOTOR_Y_STEP = 21
MOTOR_Y_DIR = 20
Y_POS = 0

MOTOR_Z_EN = 2
MOTOR_Z_M0 = 3
MOTOR_Z_M1 = 4
MOTOR_Z_M2 = 5
MOTOR_Z_STEP = 6
MOTOR_Z_DIR = 7

# Initialise Pins #
X_dir = Pin(MOTOR_X_DIR, Pin.OUT)
X_step = Pin(MOTOR_X_STEP, Pin.OUT)
X_en = Pin(MOTOR_X_EN, Pin.OUT)

Y_dir = Pin(MOTOR_Y_DIR, Pin.OUT)
Y_step = Pin(MOTOR_Y_STEP, Pin.OUT)
Y_en = Pin(MOTOR_Y_EN, Pin.OUT)

Z_dir = Pin(MOTOR_Z_DIR, Pin.OUT)
Z_step = Pin(MOTOR_Z_STEP, Pin.OUT)
Z_en = Pin(MOTOR_Z_EN, Pin.OUT)

def enable_motors():
    X_en.value(0)
    Y_en.value(0)
    Z_en.value(0)

def disable_motors():
    X_en.value(1)
    Y_en.value(1)
    Z_en.value(1)

def step_motor(motor, dir):
    if motor == "X":
        X_dir.value(dir)
        X_step.value(0)
        X_step.value(1)        
    elif motor == "Y":
        Y_dir.value(dir)
        Y_step.value(0)
        Y_step.value(1)  
    elif motor == "Z":
        Z_dir.value(dir)
        Z_step.value(0)
        Z_step.value(1)  

def move_to(x, y):
    # current position
    global X_POS, Y_POS
    # target position
    steps_x = x/LINEAR_STEP
    steps_y = y/LINEAR_STEP
    # delta
    delta_x = round(steps_x) - X_POS
    delta_y = round(steps_y) - Y_POS

    X_POS += delta_x
    Y_POS += delta_y
    
    # adjust for negative directions
    if delta_x < 0:
        delta_x = -delta_x
        x_dir = 1
    else:
        x_dir = 0
    if delta_y < 0:
        delta_y = -delta_y
        y_dir = 1
    else: y_dir = 0

    # Find the smoothest path by linking a series of steps together
    gcd = math.gcd(delta_x, delta_y)
    base = delta_x/gcd # step in the x direction
    height = delta_y/gcd # step in the y direction
    
    if base >= height:
        num_stairs = delta_x/base
        for _ in range(num_stairs):
            for _ in range(base):
                step_motor("X", x_dir)
            for _ in range(height):
                step_motor("Y", y_dir)
    elif base < height:
        num_stairs = delta_x/height
        for _ in range(num_stairs):
            for _ in range(base):
                step_motor("X", x_dir)
            for _ in range(height):
                step_motor("Y", y_dir)

def main():
    
    # Initialise Pins #
    X_dir = Pin(MOTOR_X_DIR, Pin.OUT)
    X_step = Pin(MOTOR_X_STEP, Pin.OUT)
    X_en = Pin(MOTOR_X_EN, Pin.OUT)

    Y_dir = Pin(MOTOR_Y_DIR, Pin.OUT)
    Y_step = Pin(MOTOR_Y_STEP, Pin.OUT)
    Y_en = Pin(MOTOR_Y_EN, Pin.OUT)

    Z_dir = Pin(MOTOR_Z_DIR, Pin.OUT)
    Z_step = Pin(MOTOR_Z_STEP, Pin.OUT)
    Z_en = Pin(MOTOR_Z_EN, Pin.OUT)
    
    # Enable motors
    enable_motors()

    

if __name__ == "__main__":
    main()






    
