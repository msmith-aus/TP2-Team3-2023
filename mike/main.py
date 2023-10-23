from machine import Pin, freq
from time import sleep, sleep_ms
from motor import *
from util import Artwork
from drawer import Drawer
import stepper_controller as ctrl




if __name__ == "__main__":
    led = Pin(25, Pin.OUT)
    motor_X: Motor = Motor()
    motor_Y: Motor = Motor()
    motor_Z: Motor = Motor()
    init_pins(motor_X, motor_Y, motor_Z)
    motor_X.enable()

    sm = rp2.StateMachine(0, blink, freq=100000, set_base=Pin(21))
    sm.active(1)
    sleep(3)
    sm.active(0)


    motor_X.disable()

    # artwork: Artwork = read_in_artwork(path="./artworks/square.txt")
    # # print(basic_artwork.segments)
    # drawer = Drawer(motor_X, motor_Y, motor_Z, artwork)
    # print(drawer.artwork.segments)

    # # Move from home 

    # # Move up away from ink drip
    # print("Should be at (-1.5, -1.5)mm - (0,0) steps.")
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")

    # motor_Z.enable()
    # print(f"Moving to (0,0)")
    # motor_Z.step_motor(POS_Z, 1200) # pen up 
    # print("PEN UP")
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")
    # sleep_ms(500)

    # print("Move to start of drawing")
    # motor_X.enable()
    # print(f"Moving to (1200,0)")
    # motor_X.step_motor(POS_XY, 1200)
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")
    # sleep_ms(500)
    # motor_Y.enable()
    # motor_Y.step_motor(POS_XY, 1200)
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")
    # sleep_ms(500)
    # # motor_Z.step_motor(NEG_Z, 1200) # pen down
    # # sleep_ms(500)

    # drawer.draw_artwork()

    # # Move back to home
    # print(f"Moving to (1200,1200)")
    # drawer.move_to(0,0)
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps") # home

    # print(f"Moving to (0,1200)")
    # motor_X.step_motor(NEG_XY, 1200)
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")
    # sleep_ms(500)

    # print(f"Moving to (0,0)")
    # motor_Y.step_motor(NEG_XY,1200)
    # print(f"At: ({motor_X._positon},{motor_Y._positon}) steps")
    # sleep_ms(500)

    # motor_Z.step_motor(NEG_Z, 1200) # pen down
    # print("PEN DOWN")
    
    # motor_X.disable()
    # motor_Y.disable()
    # motor_Z.disable()





    
    
    # loop(motor_x, motor_y, motor_z, led)
    # draw_square(motor_x, motor_y, motor_z, led)

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
