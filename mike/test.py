from util import Artwork
from motor import *
from time import sleep
from time import time
from math import sqrt

usleep = lambda x: sleep(x*10E-06)



path = '~/Desktop/Engineering/METR4810/TP2-Team3-2023/mike/artworks/basic.txt'

def read_and_execute_artwork(path, motor_x, motor_y, motor_z):
    #artwork = Artwork()
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
    motor_z.step_motor(NEG_Z, 100, 2000)
    motor_x.enable()
    motor_x.step_motor(POS_XY, 1200, 1000)
    motor_y.enable()
    motor_y.step_motor(POS_XY, 1200, 1000)
    motor_z.step_motor(POS_Z, 100, 2000)
    motor_x.disable()
    motor_y.disable()
    motor_z.disable()

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
    # Get total number of steps needed to get to end
    # of segment
    # We need this to determine when to start decelerating
    for point in segment:
        if point == cur_pos:
            continue
        x_dist = point[0] - cur_pos[0]
        y_dist = point[1] - cur_pos[1]
        total_x_distance += x_dist
        total_y_distance += y_dist
        cur_pos = point
    total_x_distance = total_x_distance / LINEAR_STEP_XY # Total steps
    total_y_distance = total_y_distance / LINEAR_STEP_XY # Total steps
    acceleration_profile = generate_acceleration_profile(total_x_distance, total_y_distance)
    for point in segment:
        if point == cur_pos:
            continue
        move_to_point(cur_pos, point, motor_x, motor_y, x_travelled, y_travelled, acceleration_profile)


def move_to_point(cur_pos, point, motor_x, motor_y, x_travelled, y_travelled, acceleration_profile):
    
    delta_x = (point[0] - cur_pos[0]) // LINEAR_STEP_XY # No. of steps
    delta_y = (point[1] - cur_pos[1]) // LINEAR_STEP_XY # No. of steps
    if delta_x < 0:
        x_dir = NEG_XY
    elif delta_x > 0:
        x_dir = POS_XY
    if delta_y < 0:
        y_dir = NEG_XY
    elif delta_y > 0:
        y_dir = POS_XY
   
    # get required motor speeds for each direction
    if delta_x == 0 or delta_y == 0:
        ratio = 1
    else:
        ratio = abs(delta_x / delta_y)
    if ratio > 1:
        x_start = START_SPEED
        x_final = FINAL_SPEED
        y_start = START_SPEED / ratio
        y_final = FINAL_SPEED / ratio
    elif ratio < 1:
        x_start = START_SPEED / ratio
        x_final = FINAL_SPEED / ratio
        y_start = START_SPEED
        y_final = FINAL_SPEED
    else:
        x_start = y_start = START_SPEED
        x_final = y_final = FINAL_SPEED
    
    accel_update_rate = ACCELERATION / ACCEL_INC # I.e. 1000 PPS/s divided by 20 = 50Hz
    x_start = y_start = accel_timer = time()
    motor_x.set_current_speed(x_start)
    motor_y.set_current_speed(y_start)
    motor_x.enable()
    motor_y.enable()
    while (True):
        cur_time = time()
        cur_speed_x = motor_x.get_current_speed()
        cur_speed_y = motor_y.get_current_speed()
        if cur_speed_x < x_final and \
            cur_speed_y < y_final and \
            (cur_time - accel_timer) >= (1 / accel_update_rate) and:
            accel_timer = cur_time
            # Increment current speed
            motor_x.set_current_speed(cur_speed_x + ACCEL_INC)
            motor_y.set_current_speed(cur_speed_y + ACCEL_INC)
        if (cur_time - x_start) >= (1 / cur_speed_x) and cur_pos[0] < delta_x:
            x_start = cur_time
            motor_x.step_motor(x_dir)
            cur_pos[0] += x_dist
        if (cur_time - y_start) >= (1 / cur_speed_y):
            y_start = cur_time
            motor_y.step_motor(y_dir)
            cur_pos[1] += y_dist
        if cur_pos[0] == point[0] and cur_pos[1] == point[1]:
            break
        

def main():
    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    read_and_execute_artwork(path, motor_x, motor_y, motor_z)






if __name__ == '__main__':
    main()