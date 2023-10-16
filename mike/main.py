#from machine import Pin
from time import sleep
from motor import Motor, POS_XY, NEG_XY, STEPS_PER_REV_XY, NEG_Z, POS_Z, STEPS_PER_REV_Z
from util import Artwork
from drawer import Drawer

sleep_ms = lambda x: sleep(x*10E-06)





def draw_square(motor_x: Motor, motor_y: Motor, motor_z: Motor, led):
    x_steps = 0
    y_steps = 0

    # Move up away from ink drip

    motor_z.enable()
    motor_z.step_motor(POS_Z, 600) # pen up
    sleep_ms(500)

    # Move to start of drawing
    motor_x.enable()
    motor_x.step_motor(POS_XY, 1200)
    sleep_ms(500)
    motor_y.enable()
    motor_y.step_motor(POS_XY, 1200)
    sleep_ms(500)
    motor_z.step_motor(NEG_Z, 600) # pen down
    sleep_ms(500)
    # draw square
    motor_x.step_motor(POS_XY, 8000)
    motor_y.step_motor(POS_XY, 8000)
    motor_x.step_motor(NEG_XY, 8000)
    motor_y.step_motor(NEG_XY, 8000)

    # sleep_ms(500)
    motor_z.step_motor(NEG_Z, 600) # pen up
    sleep_ms(500)
    motor_x.step_motor(NEG_XY, 1200)
    sleep_ms(500)
    motor_y.step_motor(NEG_XY,1200)
    motor_z.step_motor(NEG_Z, 600) # pen down
    sleep_ms(500)

    motor_x.disable()
    motor_y.disable()
    motor_z.disable()

def read_in_artwork(path):
    artwork = Artwork()
    with open(path, "r") as file:
        print("Reading in file")
        content = file.readlines()
        segment = []
        for line in content:
            line = line.strip()
            if line == '':
                print("\n")
                continue
            if line == "START":
                print("start")
                segment = []
                continue
            elif line == "STOP":
                print("stop")
                artwork.segments.append(segment)
                segment = []
                continue
            else:
                print(line)
                x, y = map(
                    float, line.split(",")
                )  # Split by comma and convert to float
                artwork.segments.append((x, y))
                print(x, y)
                continue
    return artwork



def main():

    #led = Pin(25, Pin.OUT)
    motor_X: Motor = Motor()
    motor_Y: Motor = Motor()
    motor_Z: Motor = Motor()
    #init_pins(motor_X, motor_Y, motor_Z)

    basic_artwork: Artwork = read_in_artwork(path="./artworks/training_basic.txt")
    print(basic_artwork.segments)
    # drawer = Drawer(motor_X, motor_Y, motor_Z, basic_artwork)
    # drawer.draw_artwork()
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


if __name__ == "__main__":
    main()