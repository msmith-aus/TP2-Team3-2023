from util import Artwork
from motor import *
from utime import time # Not sure if this is valid for pico?
from utime import sleep_us
from math import sqrt



# Path to the artwork
path = '~/Desktop/Engineering/METR4810/TP2-Team3-2023/mike/artworks/basic.txt'


def read_and_execute_artwork(path, motor_x, motor_y, motor_z):
    """
    Reads an artfile and executes it segment by segment
    
    Returns: None
    """
    start = False
    cur_pos = (0,0) # Step value
    with open(path, "r") as file:
        print("Reading in file")
        content = file.readlines()
        for line in content:
            line = line.strip()
            if line == '':
                print("\n")
                continue
            elif line == "START":
                segment = []
                continue
            elif line == "STOP":
                # End of the segment
                # Draw the segment
                if start == False:
                    move_to_start(motor_x, motor_y, motor_z)
                    start = True
                draw_segment(segment, motor_x, motor_y, motor_z, cur_pos)
                continue
            else:
                print(line)
                x, y = map(
                    float, line.split(",")
                )  # Split by comma and convert to float
                segment.append((x,y)) # x, y in mm
                continue


def move_to_start(motor_x, motor_y, motor_z):
    motor_z.enable()
    motor_x.enable()
    motor_y.enable()
    move_canvas(NEG_Z)
    step_forward(motor_x, motor_y)
    move_canvas(POS_Z)
    motor_x.disable()
    motor_y.disable()
    motor_z.disable()

def move_to_next_segment(motor_x, motor_y):



def move_canvas(motor_z, dir):
    
    for _ in range(200):
        motor_z.step_motor(dir)
        sleep_us(2500)
        
def step_forward(motor_x, motor_y):

    for _ in range(800):
        motor_x.step_motor(POS_XY)
        sleep_us(1500)

    for _ in range(800):
        motor_y.step_motor(POS_XY)
        sleep_us(1500)



def generate_acceleration_profile(total_x_distance, total_y_distance):
    # Returns a tuple (a, b)
    # Where a is the number of steps for motors to stop accelerating
    # b is the number of steps for x to start decelerating
 
    
    # Try one quarter ratio e.g total steps is 100, finish accelerate by 25 steps and start decelerate at 75 steps
    magnitude = sqrt(total_x_distance**2 + total_y_distance**2)
    return (round(magnitude * 1/4), round(magnitude * 3/4))


def draw_segment(segment, motor_x, motor_y, motor_z, cur_pos):

    total_x_distance = 0
    total_y_distance = 0
    x_travelled = 0
    y_travelled = 0
    motor_x.set_current_speed(START_SPEED)
    motor_y.set_current_speed(START_SPEED)
    # Get total number of steps needed to get to end
    # of segment
    # We need this to determine when to start decelerating
    pos = cur_pos
    for point in segment:
        if point == cur_pos:
            continue
        x_dist = point[0] - pos[0]
        y_dist = point[1] - pos[1]
        total_x_distance += x_dist
        total_y_distance += y_dist
        pos = point
    total_x_distance = total_x_distance / LINEAR_STEP_XY # Total steps
    total_y_distance = total_y_distance / LINEAR_STEP_XY # Total steps
    acceleration_profile = generate_acceleration_profile(total_x_distance, total_y_distance)
    if cur_pos != segment[0]:
        # Move to that point to start us off.
        move_to_next_segment(motor_x, motor_y, cur_pos, point)
    for point in segment:
        if point == cur_pos:
            continue
        move_to_point(cur_pos, point, motor_x, motor_y, x_travelled, y_travelled, acceleration_profile)


def move_to_point(cur_pos, point, motor_x, motor_y, x_travelled, y_travelled, acceleration_profile):
    
    # current position in steps
    x_pos = motor_x.get_position()
    y_pos = motor_y.get_position()

    # target position
    steps_x = point[0] / LINEAR_STEP_XY
    steps_y = point[1] / LINEAR_STEP_XY

    # delta
    delta_x = round(steps_x) - x_pos
    delta_y = round(steps_y) - y_pos

    #adjust for negative directions
    if delta_x < 0:
        delta_x = -delta_x
        x_dir = NEG_XY
    else:
        x_dir = POS_XY
    if delta_y < 0:
        delta_y = -delta_y
        y_dir = NEG_XY
    else:
        y_dir = POS_XY

    # get required motor speeds for each direction
    if delta_x == 0 or delta_y == 0:
        ratio = 1
    else:
        ratio = delta_x / delta_y
    # Check current motor speeds
    # Set the lower speed motor to match the higher speed motor
    # Then re-calculate the new speeds with the ratio
    if motor_x.get_current_speed() > motor_y.get_current_speed():
        motor_y.set_current_speed(motor_x.get_current_speed())
    else:
        motor_x.set_current_speed(motor_y.get_current_speed())
    if ratio > 1:
        x_start = motor_x.get_current_speed()
        x_final = FINAL_SPEED
        y_start = motor_y.get_current_speed() / ratio
        y_final = FINAL_SPEED / ratio
    elif ratio < 1:
        x_start = motor_x.get_current_speed() / ratio
        x_final = FINAL_SPEED / ratio
        y_start = motor_y.get_current_speed()
        y_final = FINAL_SPEED
    else:
        x_start = y_start = START_SPEED
        x_final = y_final = FINAL_SPEED
    
    x_time = y_time = accel_timer = time()
    motor_x.set_current_speed(x_start)
    motor_y.set_current_speed(y_start)
    motor_x.enable()
    motor_y.enable()
    while (True):
        cur_time = time()
        cur_speed_x = motor_x.get_current_speed()
        cur_speed_y = motor_y.get_current_speed()
        magnitude_travelled = sqrt(x_travelled**2 + y_travelled**2)
        if cur_speed_x < x_final and \
            cur_speed_y < y_final and \
            (cur_time - accel_timer) >= (1 / ACCEL_UPDATE_RATE) and \
                magnitude_travelled < acceleration_profile[0]:
            accel_timer = cur_time
            # Increment current speed
            motor_x.accelerate(ACCEL_INC)
            motor_y.accelerate(ACCEL_INC)
        if cur_speed_x > 0 and \
            cur_speed_y > 0 and (cur_time - accel_timer) >= (1 / ACCEL_UPDATE_RATE) and \
            magnitude_travelled >= acceleration_profile[1]:
            accel_timer = cur_time
            # Decrement current speed
            motor_x.decelerate(ACCEL_INC)
            motor_y.decelerate(ACCEL_INC)
        if (cur_time - x_time) >= (1 / cur_speed_x) and cur_pos[0] < abs(delta_x):
            x_time = cur_time
            motor_x.step_motor(x_dir)
            x_travelled += 1
            cur_pos[0] += x_dist
            local_x += 1
        if (cur_time - y_time >= (1 / cur_speed_y) and cur_pos[1] < abs(delta_y)):
            y_time = cur_time
            motor_y.step_motor(y_dir)
            y_travelled += 1
            cur_pos[1] += y_dist
            local_y += 1
        if local_x >= abs(delta_x) and local_y >= abs(delta_y):
            break

def main():
    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    read_and_execute_artwork(path, motor_x, motor_y, motor_z)






if __name__ == '__main__':
    main()