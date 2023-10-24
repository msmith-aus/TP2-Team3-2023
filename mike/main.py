from machine import Pin
from utime import sleep_ms
from motor import Motor, POS_XY, NEG_XY, STEPS_PER_REV_XY, NEG_Z, POS_Z, STEPS_PER_REV_Z, init_pins, move_canvas, to_start
from util import Artwork
from drawer import Drawer


def read_in_artwork(path):
    """ Method to read the artwork file
    Artworks consist of a list of segments which are a list of points

    Returns:
        Artwork class instantiation
    """
    artwork = Artwork()
    with open(path, "r") as file:
        print("Reading in file")
        content = file.readlines()
        for line in content:
            line = line.strip()
            if line == '':
                print("\n")
                continue=-
            if line == "START":
                print("start")
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
                segment.append((x, y))
                print(x, y)
    return artwork



def main():

    motor_x: Motor = Motor()
    motor_y: Motor = Motor()
    motor_z: Motor = Motor()
    init_pins(motor_x, motor_y, motor_z)
    artwork1 = read_in_artwork('./artworks/basic.txt')
    artwork2 = read_in_artwork('./artworks/beginner.txt')
    artwork3 = read_in_artwork('./artworks/apprentice.txt')
    artwork4 = read_in_artwork('./artworks/journeyman.txt')
    artwork5 = read_in_artwork('./artworks/master.txt')
    artwork6 = read_in_artwork('./artworks/master.txt')
    drawer = Drawer(motor_x, motor_y, motor_z, artwork5)
    drawer.draw_artwork()



if __name__ == "__main__":
    main()