from util import Artwork
from motor import *
from utime import time # Not sure if this is valid for pico?
from utime import sleep_us
from math import sqrt
from drawer import Drawer



# Path to the artwork
path = '~/Desktop/Engineering/METR4810/TP2-Team3-2023/mike/artworks/basic.txt'


def read_artwork(path):
    """
    Reads an artfile and executes it segment by segment
    
    Returns: None
    """
    start = False
    cur_pos = (0,0) # Step value
    with open(path, "r") as file:
        artwork = Artwork()
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
                print("stop")
                artwork.segments.append(segment)
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




def main():
    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    artwork = read_artwork(path)
    drawer = Drawer()
    drawer.draw_artwork(motor_x, motor_y, motor_z, artwork)






if __name__ == '__main__':
    main()