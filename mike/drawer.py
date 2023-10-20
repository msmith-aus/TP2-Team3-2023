from util import Artwork
from motor import *
from utime import sleep_ms, ticks_us, ticks_diff
from math import sqrt

class Drawer:

    def __init__(self, motor_x, motor_y, motor_z, artwork):
        
        self.motor_x: Motor = motor_x
        self.motor_y: Motor = motor_y
        self.motor_z: Motor = motor_z
        self.artwork: Artwork = artwork
    
    def draw_artwork(self):
        print("Drawing :)")
        to_start(self.motor_x, self.motor_y, self.motor_z)
        for segment in self.artwork.segments:
            self.move_to_point(segment[0])
            move_canvas(self.motor_z, POS_Z)
            for point in segment:
                self.move_to_point(point)
            move_canvas(self.motor_z, NEG_Z)
        self.move_to_point((0,0))
            
            

    def segment_distance(self, segment):
        # Segment distance in number of steps
        x_total = 0
        y_total = 0
        start = segment[0]
        for point in segment:
            x_dist = abs((point[0] - start[0])) // LINEAR_STEP_XY
            y_dist = abs((point[1] - start[1])) // LINEAR_STEP_XY
            print(x_dist)
            print(y_dist)
            x_total += x_dist
            y_total += y_dist
            start = point
        return (x_total, y_total)
               
    def move_to_point(self, point):
    
        # current position in steps
        x_pos = self.motor_x.get_position()
        y_pos = self.motor_y.get_position()
        
        # target position
        steps_x = point[0] / LINEAR_STEP_XY
        steps_y = point[1] / LINEAR_STEP_XY

        # delta
        delta_x = round(steps_x) - x_pos
        delta_y = round(steps_y) - y_pos
        
        print("Moving to point:", point)

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
            
        #acceleration profile
        accel_profile = generate_acceleration_profile(delta_x, delta_y)

        # get required motor speeds for each direction
        if delta_x == 0 or delta_y == 0:
            ratio = 1
        else:
            ratio = delta_x / delta_y
        # Check current motor speeds
        # Set the lower speed motor to match the higher speed motor
        # Then re-calculate the new speeds with the ratio
        #print("Motor speed X:", self.motor_x.get_current_speed())
        #print("Motor speed Y:", self.motor_y.get_current_speed())
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
                x_start = START_SPEED * ratio
            else:
                x_start = self.motor_x.get_current_speed() * ratio
            x_final = FINAL_SPEED * ratio
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
        
        x_time = y_time = accel_timer = ticks_us()
        self.motor_x.set_current_speed(x_start)
        self.motor_y.set_current_speed(y_start)
        self.motor_x.enable()
        self.motor_y.enable()
        #acceleration = (FINAL_SPEED**2 - START_SPEED**2) / 2*acceleration_profile[2]
        local_x = 0
        local_y = 0
        
        while (True):
            cur_time = ticks_us()
            cur_speed_x = self.motor_x.get_current_speed()
            cur_speed_y = self.motor_y.get_current_speed()
            magnitude_travelled = sqrt(local_x**2 + local_y**2)
            #print("Motor speed X:", self.motor_x.get_current_speed())
            #print("Motor speed Y:", self.motor_y.get_current_speed())
            if magnitude_travelled <= accel_profile[0] and \
               (ticks_diff(cur_time, accel_timer)) >= ((1 / ACCEL_UPDATE_RATE)*1e06):
                if ratio > 1:
                    if delta_x > 0 and cur_speed_x < x_final:
                        self.motor_x.accelerate(ACCEL_INC)
                    if delta_y > 0 and cur_speed_y < y_final:
                        self.motor_y.accelerate(ACCEL_INC / ratio)
                elif ratio < 1:
                    if delta_x > 0 and cur_speed_x < x_final:
                        self.motor_x.accelerate(ACCEL_INC * ratio)
                    if delta_y > 0 and cur_speed_y < y_final:
                        self.motor_y.accelerate(ACCEL_INC)
                else:
                    if delta_x > 0 and cur_speed_x < x_final:
                        self.motor_x.accelerate(ACCEL_INC)
                    if delta_y > 0 and cur_speed_y < y_final:
                        self.motor_y.accelerate(ACCEL_INC)
                    
                accel_timer = cur_time
          
                
            if magnitude_travelled >= accel_profile[1] and \
               ticks_diff(cur_time, accel_timer) >= ((1 / ACCEL_UPDATE_RATE)*1e06):
                
                if ratio > 1:
                    if delta_x > 0 and cur_speed_x > x_start:
                        self.motor_x.deccelerate(ACCEL_INC)
                    if delta_y > 0 and cur_speed_y > y_start:
                        self.motor_y.deccelerate(ACCEL_INC / ratio)
                elif ratio < 1:
                    if delta_x > 0 and cur_speed_x > x_start:
                        self.motor_x.deccelerate(ACCEL_INC * ratio)
                    if delta_y > 0 and cur_speed_y > y_start:
                        self.motor_y.deccelerate(ACCEL_INC)
                else:
                    if delta_x > 0 and cur_speed_x > x_start:
                        self.motor_x.deccelerate(ACCEL_INC)
                    if delta_y > 0 and cur_speed_y > y_start:
                        self.motor_y.deccelerate(ACCEL_INC)
        
                accel_timer = cur_time
                

            if ticks_diff(cur_time, x_time) >= ((1 / cur_speed_x)*1e06) and local_x < delta_x:
                x_time = cur_time
                self.motor_x.step_motor(x_dir)
                local_x += 1
                self.motor_x.update_pos(-(2*x_dir-1))
                
            if ticks_diff(cur_time, y_time) >= ((1 / cur_speed_y)*1e06) and local_y < delta_y:
                y_time = cur_time
                self.motor_y.step_motor(y_dir)
                local_y += 1
                self.motor_y.update_pos(-(2*y_dir-1))
                
            if local_x >= delta_x and local_y >= delta_y:
                break
        


def generate_acceleration_profile(total_x_distance, total_y_distance):
    # Returns a tuple (a, b, c)
    # Where a is the number of steps for motors to stop accelerating
    # b is the number of steps for x to start decelerating
    # c it the total distance travelled over the segment

    
    # Try one quarter ratio e.g total steps is 100, finish accelerate by 25 steps and start decelerate at 75 steps
    magnitude = sqrt(total_x_distance**2 + total_y_distance**2)
    return (round(magnitude * 1/5), round(magnitude * 4/5), magnitude)