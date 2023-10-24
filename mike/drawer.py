from util import Artwork, greatest_common_divisor
from motor import *
from utime import sleep_us, ticks_us, ticks_diff

class Drawer:
    """
    Class to handle the drawing functionality of the artbot
    """
    def __init__(self, motor_x, motor_y, motor_z, artwork):
        
        self.motor_x: Motor = motor_x
        self.motor_y: Motor = motor_y
        self.motor_z: Motor = motor_z
        self.artwork: Artwork = artwork
    
    def draw_artwork(self):
        print("Drawing :)")
        
        to_start(self.motor_x, self.motor_y, self.motor_z)
        self.motor_x.enable()
        self.motor_y.enable()
        for segment in self.artwork.segments:
            self.move_to_point(segment[0])
            move_canvas(self.motor_z, POS_Z)
            for point in segment:
                self.move_to_point(point)
            move_canvas(self.motor_z, NEG_Z)
        self.move_to_point((0,0))
        self.motor_x.disable()
        self.motor_y.disable()

        
               
    def move_to_point(self, point):
    
        # current position in steps
        x_pos = self.motor_x.get_position() * MICRO_STEP
        y_pos = self.motor_y.get_position() * MICRO_STEP
        
        # target position
        steps_x = (point[0] // LINEAR_STEP_XY) * MICRO_STEP
        steps_y = (point[1] // LINEAR_STEP_XY) * MICRO_STEP
        

        # delta
        delta_x = steps_x - x_pos
        delta_y = steps_y - y_pos
        
        
        print("Moving to point:", point)

        #adjust for negative directions
        if delta_x < 0:
            delta_x = -delta_x
            x_dir = NEG_XY
            x_inc = -(2*x_dir-1) / MICRO_STEP
        else:
            x_dir = POS_XY
            x_inc = -(2*x_dir-1) / MICRO_STEP
        if delta_y < 0:
            delta_y = -delta_y
            y_dir = NEG_XY
            y_inc = -(2*y_dir-1) / MICRO_STEP
        else:
            y_dir = POS_XY
            y_inc = -(2*y_dir-1) / MICRO_STEP
       

        # Find the smoothest path by linking a series of steps together
        hgd = greatest_common_divisor(delta_x, delta_y)
        if hgd == 0:
            hgd = 1
        base = delta_x / hgd  # step in the x direction
        height = delta_y / hgd  # step in the y direction

        # Calculates number of stairs needed to get to the point
        if base >= height:
            if base != 0:
                num_stairs = delta_x // base
            else:
                num_stairs = 1
        elif base < height:
            if height != 0:
                num_stairs = delta_y // height
            else:
                num_stairs = 1
                
        if base == 0 or height == 0:
            ratio = 1
        else:
            ratio = base / height
        
        # Adjusts speed of the motors depending on the x/y ratio to ensure
        # Smooth motion during simultaneous x/y motor movement
        if ratio >= 1:
            x_speed = FINAL_SPEED
            y_speed = FINAL_SPEED / ratio
            
        elif ratio < 1:
            x_speed = FINAL_SPEED * ratio
            y_speed = FINAL_SPEED
            
        
        local_x = 0
        local_y = 0
        
        i = 0 # Stairs counter
        j = 0 # Base counter
        k = 0 # Height counter

        x_time = y_time = accel_timer = ticks_us()

        # Calculate required x/y timer delays
        x_delay = round((1/x_speed)*1e06)
        y_delay = round((1/y_speed)*1e06)

        while (i < num_stairs):
            cur_time = ticks_us()
            if ticks_diff(cur_time, x_time) >= x_delay and j < base:
                self.motor_x.step_motor(x_dir)
                self.motor_x.update_pos(x_inc)
                j += 1
                x_time = cur_time
                
            if ticks_diff(cur_time, y_time) >= y_delay and k < height:
                self.motor_y.step_motor(y_dir)
                self.motor_y.update_pos(y_inc)
                k += 1
                y_time = cur_time

            if j == base and k == height:
                j = 0
                k = 0
                i += 1
        
        