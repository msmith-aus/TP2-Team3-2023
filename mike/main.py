from machine import Pin
from time import sleep, sleep_ms
from motor import Motor, init_pins, POS_XY, NEG_XY, STEPS_PER_REV_XY, NEG_Z, POS_Z, STEPS_PER_REV_Z



def draw_square(motor_x: Motor, motor_y: Motor, motor_z: Motor, led):
    x_steps = 0
    y_steps = 0

    motor_z.enable()
    motor_z.step_motor(NEG_Z, 20) # pen up
    sleep_ms(500)

    # Move to start of drawing
    motor_x.enable()
    motor_x.step_motor(POS_XY, 20)
    sleep_ms(500)
    motor_y.enable()
    motor_y.step_motor(POS_XY, 20)
    sleep_ms(500)
    motor_z.step_motor(POS_Z, 20)
    sleep_ms(500)
    # draw square
    motor_x.step_motor(POS_XY, 8000)
    motor_y.step_motor(POS_XY, 8000)
    motor_x.step_motor(NEG_XY, 8000)
    motor_y.step_motor(NEG_XY, 8000)

    sleep_ms(500)
    motor_z.step_motor(NEG_Z, 20)
    sleep_ms(500)
    motor_x.step_motor(NEG_XY, 20)
    sleep_ms(500)
    motor_y.step_motor(NEG_XY,20)

    motor_x.disable()
    motor_y.disable()
    motor_z.disable()



def loop(motor_x: Motor, motor_y: Motor, motor_z: Motor, led):
    while True:
        # Move X Up and Back ###
        # motor_z.enable()
        # motor_z.step_motor(POS_XY, STEPS_PER_REV_XY)
        # motor_z.step_motor(NEG_XY, STEPS_PER_REV_XY)
        # print("Motor X EN: ", motor_x._enable.value(), "Motor Y EN: ", motor_y._enable.value(), "Motor Z EN: ", motor_z._enable.value())
        # motor_z.disable()
        # motor_z.step_motor(POS_XY, STEPS_PER_REV_XY)
        # motor_z.step_motor(NEG_XY, STEPS_PER_REV_XY)
        # print("Motor X EN: ", motor_x._enable.value(), "Motor Y EN: ", motor_y._enable.value(), "Motor Z EN: ", motor_z._enable.value())
        # sleep(1)
        # led.toggle()
        # sleep_ms(200)
        # led.toggle()

        motor_z.enable()
        motor_z.step_motor(POS_Z, STEPS_PER_REV_Z)
        motor_z.step_motor(NEG_Z, STEPS_PER_REV_Z)
        print("Motor X EN: ", motor_x._enable.value(), "Motor Y EN: ", motor_y._enable.value(), "Motor Z EN: ", motor_z._enable.value())
        motor_z.disable()
        motor_z.step_motor(POS_Z, STEPS_PER_REV_Z)
        motor_z.step_motor(NEG_Z, STEPS_PER_REV_Z)
        print("Motor X EN: ", motor_x._enable.value(), "Motor Y EN: ", motor_y._enable.value(), "Motor Z EN: ", motor_z._enable.value())
        sleep(1)
        led.toggle()
        sleep_ms(200)
        led.toggle()


if __name__ == "__main__":
    led = Pin(25, Pin.OUT)
    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    init_pins(motor_x, motor_y, motor_z)
    
    
    # loop(motor_x, motor_y, motor_z, led)
    draw_square(motor_x, motor_y, motor_z, led)

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
