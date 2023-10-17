from util import Artwork
from motor import *
from time import sleep_ms
from time import time
from math import sqrt

class Drawer:

    def __init__(self, motor_x, motor_y, motor_z, artwork):
        
        self.motor_x: Motor = motor_x
        self.motor_y: Motor = motor_y
        self.motor_z: Motor = motor_z
        self.artwork: Artwork = artwork
    
    def draw_artwork(self):
        print("Drawing :)")
        for segment in self.artwork.segments:
            x_travelled = 0
            y_travelled = 0
            segment_distance = self.segment_distance(segment)
            accel_profile = self.generate_acceleration_profile(segment_distance[0], segment_distance[1])
            move_canvas(self.motor_z, NEG_Z)
            sleep_ms(500)
            for point in segment:
                self.move_to_point(point, x_travelled, y_travelled, accel_profile)
            move_canvas(self.motor_z, POS_Z)
            self.move_to_point(0,0)

    def segment_distance(self, segment):
        # Segment distance in number of steps
        x_total = 0
        y_total = 0
        start = segment[0]
        for point in segment:
            if start == segment[0]:
                continue
            x_dist = (point[0] - start[0]) // LINEAR_STEP_XY
            y_dist = (point[1] - start[1]) // LINEAR_STEP_XY
            x_total += x_dist
            y_total += y_dist
            start = point
        return (x_total, y_total)
               
    def move_to_point(self, point, x_travelled, y_travelled, acceleration_profile):
    
        # current position in steps
        x_pos = self.motor_x.get_position()
        y_pos = self.motor_y.get_position()

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
        if self.motor_x.get_current_speed() > self.motor_y.get_current_speed():
            self.motor_y.set_current_speed(self.motor_x.get_current_speed())
        else:
            self.motor_x.set_current_speed(self.motor_y.get_current_speed())
        if ratio > 1:
            if self.motor_x.get_current_speed() == 0:
                x_start = START_SPEED
            else:
                x_start = self.motor_x.get_current_speed()
            x_final = FINAL_SPEED
            if self.motor_y.get_current_speed() == 0:
                y_start = START_SPEED / ratio
            else:
                y_start = self.motor_y.get_current_speed() / ratio
            y_final = FINAL_SPEED / ratio
        elif ratio < 1:
            if self.motor_x.get_current_speed() == 0:
                x_start = START_SPEED / ratio
            else:
                x_start = self.motor_x.get_current_speed() / ratio
            x_final = FINAL_SPEED / ratio
            if self.motor_y.get_current_speed() == 0:
                y_start = START_SPEED
            else:
                y_start = self.motor_y.get_current_speed()
            y_final = FINAL_SPEED
        else:
            if self.motor_x.get_current_speed() == 0:
                x_start = START_SPEED
            else:
                x_start = self.motor_x.get_current_speed()
            if self.motor_y.get_current_speed() == 0:
                y_start = START_SPEED
            else: 
                y_start = self.motor_y.get_current_speed()
            x_final = y_final = FINAL_SPEED
        
        x_time = y_time = accel_timer = time()
        self.motor_x.set_current_speed(x_start)
        self.motor_y.set_current_speed(y_start)
        self.motor_x.enable()
        self.motor_y.enable()
        acceleration = (FINAL_SPEED**2 - START_SPEED**2) / 2*acceleration_profile[2]
        accel_update_rate = acceleration / ACCEL_INC
        while (True):
            cur_time = time()
            cur_speed_x = self.motor_x.get_current_speed()
            cur_speed_y = self.motor_y.get_current_speed()
            magnitude_travelled = sqrt(x_travelled**2 + y_travelled**2)
            if cur_speed_x < x_final and cur_speed_y < y_final and \
                (cur_time - accel_timer) >= (1 / accel_update_rate):
                accel_timer = cur_time
                # Increment current speed
                self.motor_x.accelerate(ACCEL_INC)
                self.motor_y.accelerate(ACCEL_INC)
            if cur_speed_x > 0 and \
                cur_speed_y > 0 and (cur_time - accel_timer) >= (1 / accel_update_rate) and \
                magnitude_travelled >= acceleration_profile[1]:
                accel_timer = cur_time
                # Decrement current speed
                self.motor_x.decelerate(ACCEL_INC)
                self.motor_y.decelerate(ACCEL_INC)
            if (cur_time - x_time) >= (1 / cur_speed_x) and cur_pos[0] < abs(delta_x):
                x_time = cur_time
                self.motor_x.step_motor(x_dir)
                x_travelled += 1
                self.motor_x._positon +=  -(2*x_dir-1)
            if (cur_time - y_time >= (1 / cur_speed_y) and cur_pos[1] < abs(delta_y)):
                y_time = cur_time
                self.motor_y.step_motor(y_dir)
                y_travelled += 1
                self.motor_y._positon +=  -(2*y_dir-1)
            if self.motor_x._positon >= steps_x and self.motor_y._positon >= steps_y:
                break


    def generate_acceleration_profile(total_x_distance, total_y_distance):
        # Returns a tuple (a, b, c)
        # Where a is the number of steps for motors to stop accelerating
        # b is the number of steps for x to start decelerating
        # c it the total distance travelled over the segment
    
        
        # Try one quarter ratio e.g total steps is 100, finish accelerate by 25 steps and start decelerate at 75 steps
        magnitude = sqrt(total_x_distance**2 + total_y_distance**2)
        return (round(magnitude * 1/4), round(magnitude * 3/4), magnitude)