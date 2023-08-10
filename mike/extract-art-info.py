"""
UNIVERSITY OF QUEENSLAND TEAM PROJECT 2 2023
Author: Michael Smith 
Student Number: 45838464 
DATE: 06/08/2023
"""

import math, glob, matplotlib.pyplot as plt

class Drawing():
    pass

class Segment():
    def __init__(self) -> None:
        self.points = []

    def size(self):
        return len(self.points)
    
    def stroke_length(self):
        length = 0
        for i in range(1, len(self.points)):
            length += math.dist(self.points[i-1], self.points[i])
        return length

# class Line():
#     def __init__(self, start, end) -> None:
#         self.start = start
#         self.end = end
#         self. length = math.dist(start, end)
        

class Drawer():
    def __init__(self, artworks) -> None:
        self.artworks = artworks

    def draw_artworks(self):
        for i, artwork in enumerate(self.artworks):
            plt.figure(i)
            for segment in self.artworks[artwork]:
                x_coords, y_coords = zip(*segment.points)
                plt.plot(x_coords, y_coords)
            plt.title(artwork)
            plt.savefig(fname=artwork.split('.')[0])
        plt.show()

def read_in_artworks(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        segments = []
        tmp_segment = None
        for line in content:
            line = line.strip()
            if line == 'START':
                tmp_segment = Segment()
            elif line == 'STOP':
                segments.append(tmp_segment)
                tmp_segment = None
            elif tmp_segment is not None:
                x, y = map(float, line.split(','))  # Split by comma and convert to float
                tmp_segment.points.append((x, y))
            else:
                # empty line?
                continue
        return segments
            



if __name__ == "__main__":
    artworks = {path: read_in_artworks(path) for path in glob.glob("/home/stiff/tp2-2023/*.txt")}

    for artwork in artworks:
        segments = len(artworks[artwork])
        points = sum(artworks[artwork][seg].size() for seg in range(len(artworks[artwork])))
        length = sum(artworks[artwork][seg].stroke_length() for seg in range(len(artworks[artwork])))
        print(f'{artwork}  \n Segments: {segments} \n Points: {points} \n Total stroke length (mm): {length}')
    
    artist = Drawer(artworks)
    artist.draw_artworks()