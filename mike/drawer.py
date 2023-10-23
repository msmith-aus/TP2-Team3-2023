from util import Artwork
from machine import *
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
            print(f"Moving to ({segment[0][0]},{segment[0][1]})")
            self.move_to(segment[0][0], segment[0][1])  # move to start of segment
            print(f"At: ({self.motor_x._positon},{self.motor_y._positon}) steps")

            self.motor_z.step_motor(NEG_Z, 1200) #  pen down
            print("PEN DOWN")
            for p in range(1, len(segment)):
                print(f"Moving to ({segment[p][0]},{segment[p][1]})")
                self.move_to(segment[p][0], segment[p][1])
                print(f"At: ({self.motor_x._positon},{self.motor_y._positon}) steps")
            self.motor_z.step_motor(POS_Z, 1200) #  pen up
            print("PEN UP")
               
    def move_to(self, x, y):
        # current position in steps
        x_pos = self.motor_x._positon 
        y_pos = self.motor_y._positon
        # target position
        target_x = x / LINEAR_STEP_XY + 1200
        target_y = y / LINEAR_STEP_XY + 1200
        # delta
        delta_x = round(target_x) - x_pos
        delta_y = round(target_y) - y_pos

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
        
        # if purely x or y 
        if delta_x == 0:
            self.motor_y.step_motor(y_dir, delta_y)
            return
        elif delta_y == 0:
            self.motor_x.step_motor(x_dir, delta_x)
            return

        ### We're diagonal baby ###

        # Find the smoothest path by linking a series of staircases together
        hgd = greatest_common_divisor(delta_x, delta_y)
        # if hgd == 0:
        #     hgd = 1
        base = delta_x / hgd  # step in the x direction
        height = delta_y / hgd  # step in the y direction

        if base >= height:
            num_stairs = round(delta_x / base)
            for _ in range(num_stairs):
                self.motor_x.step_motor(x_dir, base)
                self.motor_y.step_motor(y_dir, height)
        elif base < height:
            num_stairs = round(delta_y / height)
            for _ in range(num_stairs):
                self.motor_x.step_motor(x_dir, base)
                self.motor_y.step_motor(y_dir, height)
    
