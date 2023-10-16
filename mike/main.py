from machine import Pin
from time import sleep, sleep_ms
from motor import Motor, init_pins, POS_XY, NEG_XY, STEPS_PER_REV_XY


# def loop(motor_x: Motor, motor_y: Motor, motor_z: Motor, led):
#     while True:
#         # Move X Up and Back ###
#         motor_x.step_motor(POS_XY, STEPS_PER_REV_XY)
#         motor_x.step_motor(NEG_XY, STEPS_PER_REV_XY)
#         sleep(1)
#         led.toggle()
#         sleep_ms(200)
#         led.toggle()


# if __name__ == "__main__":
#     led = Pin(25, Pin.OUT)
#     motor_x: Motor = Motor()
#     motor_y: Motor = Motor()
#     motor_z: Motor = Motor()
#     init_pins(motor_x, motor_y, motor_z)
#     motor_x.enable()

#     loop(motor_x, motor_y, motor_z, led)

    # # Enable motors
    # enable_motors()

    # # Draw a line
    # for i in range(1500):
    #     if i % 500 == 0:
    #         led.toggle()
    #     X_step.value(1)
    #     utime.sleep_ms(20)
    #     X_step.value(0)
    #     utime.sleep_ms(STEP_DELAY)

    # move_to(0,0)
    # led.value(1) # pen down
    # utime.sleep_ms(250)
    # led.toggle() # pen up

    # move_to(10, 0)
    # led.value(1) # pen down
    # utime.sleep_ms(250)
    # led.toggle()

    # move_to(10,10)
    # led.value(1) # pen down
    # utime.sleep_ms(250)
    # led.toggle()

    # move_to(0,10)
    # led.value(1) # pen down
    # utime.sleep_ms(250)
    # led.toggle()

    # move_to(0,0)
    # led.value(1) # pen down
    # utime.sleep_ms(250)
    # led.toggle()

from machine import Pin, Timer
import utime
 
dir_pin = Pin(20, Pin.OUT)
step_pin = Pin(21, Pin.OUT)
steps_per_revolution = 400
 
# Initialize timer
tim = Timer()
 
def step(t):
    global step_pin
    step_pin.value(not step_pin.value())
 
def rotate_motor(delay):
    # Set up timer for stepping
    tim.init(freq=1000000//delay, mode=Timer.PERIODIC, callback=step)
 
def loop():
    while True:
        # Set motor direction clockwise
        dir_pin.value(0)
 
        # Spin motor slowly
        rotate_motor(2000)
        utime.sleep_ms(steps_per_revolution)
        tim.deinit()  # stop the timer
        utime.sleep(1)
 
        # Set motor direction counterclockwise
        dir_pin.value(0)
 
        # Spin motor quickly
        rotate_motor(1000)
        utime.sleep_ms(steps_per_revolution)
        tim.deinit()  # stop the timer
        utime.sleep(1)
 
if __name__ == '__main__':
    loop()