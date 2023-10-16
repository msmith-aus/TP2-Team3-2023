from util import Artwork
from motor import *

path = '~/Desktop/Engineering/METR4810/TP2-Team3-2023/mike/artworks/basic.txt'

def read_and_execute_artwork(path, motor_x, motor_y, motor_z):
    #artwork = Artwork()
    start = False
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
                draw_segment(segment, motor_x, motor_y, motor_z)
                continue
            else:
                print(line)
                x, y = map(
                    float, line.split(",")
                )  # Split by comma and convert to float
                segment.append((x,y))
                continue


def move_to_start(motor_x, motor_y, motor_z):
    motor_z.enable()
    motor_z.step_motor(NEG_Z, 50, 1500)
    motor_x.enable()
    motor_x.step_motor(POS_XY, 1200, 1000)
    motor_y.enable()
    motor_y.step_motor(POS_XY, 1200, 1000)
    motor_z.step_motor(POS_Z, 50, 1500)
    motor_x.disable()
    motor_y.disable()
    motor_z.disable()


def draw_segment(segment, motor_x, motor_y, motor_z):

    for point in segment:
        if point == (0.0,0.0):
            continue
        
        



        



def main():
    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    read_and_execute_artwork(path, motor_x, motor_y, motor_z)






if __name__ == '__main__':
    main()