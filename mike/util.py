"""
UNIVERSITY OF QUEENSLAND TEAM PROJECT 2 2023
Author: Michael Smith 
Student Number: 45838464 
DATE: 06/08/2023
"""

import math

class Artwork:
    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

        


# class BloatedArtwork:
#     def __init__(self):
#         self.points = []
#         self.segments = []
#         self.total_distance = 0
#         self.total_segments_distance = 0
#         self.total_strokes = 0
#         self.name = None

#     def add_point(self, point):
#         self.points.append(point)

#     def add_segment(self, segment):
#         self.segments.append(segment)

#     def size(self):
#         return len(self.points)

#     def num_segments(self):
#         return len(self.segments)
    
#     def distance(self, a, b):
#         return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)  

#     def update_total_distance(self):
#         for i in range(self.size() - 1):
#             self.total_distance += self.distance(self.points[i], self.points[i + 1])

#     def update_total_segments_distance(self):
#         for segment in self.segments:
#             for i in range(len(segment) - 1):
#                 self.total_segments_distance += self.distance(segment[i], segment[i + 1])

#     def get_total_distance(self):
#         return self.total_distance

#     def get_total_segments_distance(self):
#         return self.total_segments_distance

#     def get_total_strokes(self):
#         for segment in self.segments:
#             self.total_strokes += len(segment) - 1
#         return self.total_strokes

#     def get_minimum_stroke(self):
#         total_min = 10000
#         for segment in self.segments:
#             min = self.distance(segment[0], segment[1])
#             for i in range(len(segment) - 1):
#                 dist = self.distance(segment[i], segment[i + 1])
#                 if dist <= min and dist != 0:
#                     min = dist
#             if min < total_min:
#                 total_min = min
#         return total_min

#     def add_name(self, name):
#         self.name = name

#     def get_name(self):
#         return self.name
    

    


# class Drawer():
#     def __init__(self, artworks) -> None:
#         self.artworks = artworks


#     def draw_artworks(self):
#         for i, artwork in enumerate(self.artworks):
#             plt.figure(i)
#             for segment in self.artworks[artwork]:
#                 x_coords, y_coords = zip(*segment.points)
#                 plt.plot(x_coords, y_coords)
#             plt.title(artwork)
#             plt.savefig(fname=artwork.split('.')[0])
#         plt.show()

def parse_artwork_file(filename):
    data = str(filename).split("/")
    name = data[1]
    with open(filename, "r") as file:
        artwork = Artwork()
        artwork.add_name(name)
        content = file.readlines()
        for line in content:
            line = line.strip()
            if line == "START":
                segment = []
            elif line == "STOP":
                artwork.add_segment(segment)
                segment = None
            elif segment is not None:
                x, y = map(
                    float, line.split(",")
                )  # Split by comma and convert to float
                artwork.add_point((x, y))
                segment.append((x, y))
            else:
                # empty line
                continue
        return artwork
    
def greatest_common_divisor(a, b):
    while b:
        a, b = b, a % b
    return a

def draw_square(motor_x: Motor, motor_y: Motor, motor_z: Motor, led):
    x_steps = 0
    y_steps = 0

    # Move up away from ink drip

    motor_z.enable()
    motor_z.step_motor(POS_Z, 600) # pen up
    sleep_ms(500)

    # Move to start of drawing
    motor_x.enable()
    motor_x.step_motor(POS_XY, 1200)
    sleep_ms(500)
    motor_y.enable()
    motor_y.step_motor(POS_XY, 1200)
    sleep_ms(500)
    motor_z.step_motor(NEG_Z, 600) # pen down
    sleep_ms(500)
    # draw square
    motor_x.step_motor(POS_XY, 8000)
    motor_y.step_motor(POS_XY, 8000)
    motor_x.step_motor(NEG_XY, 8000)
    motor_y.step_motor(NEG_XY, 8000)

    # sleep_ms(500)
    motor_z.step_motor(NEG_Z, 600) # pen up
    sleep_ms(500)
    motor_x.step_motor(NEG_XY, 1200)
    sleep_ms(500)
    motor_y.step_motor(NEG_XY,1200)
    motor_z.step_motor(NEG_Z, 600) # pen down
    sleep_ms(500)

    motor_x.disable()
    motor_y.disable()
    motor_z.disable()

    
def read_in_artwork(path):
    artwork = Artwork()
    with open(path, "r") as file:
        artwork = Artwork()
        content = file.readlines()
        for line in content:
            line = line.strip()
            if line == "START":
                segment = []
            elif line == "STOP":
                artwork.add_segment(segment)
                segment = None
            elif segment is not None:
                x, y = map(
                    float, line.split(",")
                )  # Split by comma and convert to float
                segment.append((x, y))
            else:
                # empty line
                continue
        return artwork





# def main():
#     # Artworks
#     artwork_paths = [
#         "C:/Users/micha/Desktop/tp2-2023/mike/artworks/training_apprentice.txt",
#         "C:/Users/micha/Desktop/tp2-2023/mike/artworks/training_basic.txt",
#         "C:/Users/micha/Desktop/tp2-2023/mike/artworks/training_beginner.txt",
#         "C:/Users/micha/Desktop/tp2-2023/mike/artworks/training_journeyman.txt",
#         "C:/Users/micha/Desktop/tp2-2023/mike/artworks/training_master.txt",
#     ]
#     artworks = {path: parse_artwork_file(path) for path in artwork_paths}

#     for artwork in artworks:
#         artworks[artwork].update_total_distance()
#         artworks[artwork].update_total_segments_distance()
#         totalStrokes = artworks[artwork].get_total_strokes()
#         segments = artworks[artwork].num_segments()
#         points = artworks[artwork].size()
#         totalDistance = artworks[artwork].get_total_distance()
#         totalSegmentsDist = artworks[artwork].get_total_segments_distance()
#         averageStrokeLength = totalSegmentsDist / totalStrokes
#         minimumStroke = artworks[artwork].get_minimum_stroke()

#         print(
#             f"\n\n {artwork} \n \
#             Segments: {segments} \n \
#             Points: {points} \n \
#             Total strokes: {totalStrokes} \n \
#             Total Distance Travelled (mm): {totalDistance} \n \
#             Total Segments Distance (mm): {totalSegmentsDist} \n \
#             Minimum Stroke Length (mm): {minimumStroke} \n \
#             Average Stroke Length (mm): {averageStrokeLength} \n \
#             Total Non-writing Distance (mm): {totalDistance - totalSegmentsDist} \n"
#         )


# if __name__ == "__main__":
#     main()
