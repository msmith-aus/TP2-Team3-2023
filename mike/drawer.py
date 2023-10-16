from util import Artwork
from motor import *
from time import sleep_ms
from util import greatest_common_divisor

class Drawer:

    def __init__(self, motor_x, motor_y, motor_z, artwork):
        
        self.motor_x: Motor = motor_x
        self.motor_y: Motor = motor_y
        self.motor_z: Motor = motor_z
        self.artwork: Artwork = artwork
    
    def draw_artwork(self):
        print("Drawing :)")
        for segment in self.artwork.segments:
            self.motor_z.step_motor(NEG_Z, 600) # pen down
            sleep_ms(500)
            for point in segment:
                self.move_to(point[0], point[1])
            self.motor_z.step_motor(POS_Z, 600)
            self.move_to(0,0)
               
    def move_to(self, x, y):
        # current position in steps
        x_pos = self.motor_x._positon 
        y_pos = self.motor_y._positon
        # target position
        steps_x = x / LINEAR_STEP_XY
        steps_y = y / LINEAR_STEP_XY
        # delta
        delta_x = round(steps_x) - x_pos
        delta_y = round(steps_y) - y_pos

        # adjust for negative directions
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

        # Find the smoothest path by linking a series of steps together
        hgd = greatest_common_divisor(delta_x, delta_y)
        if hgd == 0:
            hgd = 1
        base = delta_x / hgd  # step in the x direction
        height = delta_y / hgd  # step in the y direction

        if base >= height:
            if base != 0:
                num_stairs = delta_x // base
            else:
                num_stairs = 1
            for _ in range(num_stairs):
                self.motor_x.step_motor(x_dir, base)
                self.motor_y.step_motor(y_dir, height)
        elif base < height:
            if height != 0:
                num_stairs = 1
            else:
                num_stairs = delta_y // height
            for _ in range(num_stairs):
                self.motor_x.step_motor(x_dir, base)
                self.motor_y.step_motor(y_dir, height)
    
