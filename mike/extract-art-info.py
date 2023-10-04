"""
UNIVERSITY OF QUEENSLAND TEAM PROJECT 2 2023
Author: Michael Smith 
Student Number: 45838464 
DATE: 06/08/2023
"""

import math, glob, matplotlib.pyplot as plt

class Artwork():
    def __init__(self):
        self.points = []
        self.segments = []
        self.total_distance = 0
        self.total_segments_distance = 0
        self.total_strokes = 0
        self.name = None
    
    def add_point(self, point):
        self.points.append(point)

    def add_segment(self, segment):
        self.segments.append(segment)
    
    def size(self):
        return len(self.points)
    
    def num_segments(self):
        return len(self.segments)
    
    def update_total_distance(self):
        for i in range(self.size() - 1):
            self.total_distance += math.dist(self.points[i], self.points[i + 1])
    
    def update_total_segments_distance(self):

        for segment in self.segments:
            for i in range(len(segment) - 1):
                self.total_segments_distance += math.dist(segment[i], segment[i + 1])

    def get_total_distance(self):
        return self.total_distance
    
    def get_total_segments_distance(self):

        return self.total_segments_distance
      
    def get_total_strokes(self):
        for segment in self.segments:
            self.total_strokes += (len(segment) - 1)
        return self.total_strokes
    
    def get_minimum_stroke(self):
    
        total_min = 10000
        for segment in self.segments:
            min = math.dist(segment[0], segment[1])
            for i in range(len(segment) - 1):
                dist = math.dist(segment[i], segment[i + 1])
                if dist <= min and dist != 0:
                    min = dist
            if min < total_min:
                total_min = min
        return total_min

    def add_name(self, name):
        self.name = name

    def get_name(self):
        return self.name       

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
    data = str(filename).split('/')
    name = data[1]
    with open(filename, 'r') as file:
        artwork = Artwork()
        artwork.add_name(name)
        content = file.readlines()
        for line in content:
            line = line.strip()
            if line == 'START':
                segment = []
            elif line == 'STOP':
                artwork.add_segment(segment)
                segment = None
            elif segment is not None:
                x, y = map(float, line.split(','))  # Split by comma and convert to float
                artwork.add_point((x, y))
                segment.append((x, y))
            else:
                # empty line
                continue
        return artwork

def main():
    artwork_path = "H:/tp2-2023/TP2-Team3-2023/mike/artwork-files/*.txt"
    artworks = {path: parse_artwork_file(path) for path in glob.glob(artwork_path)}

    for artwork in artworks:
        artworks[artwork].update_total_distance()
        artworks[artwork].update_total_segments_distance()
        totalStrokes = artworks[artwork].get_total_strokes()
        segments = artworks[artwork].num_segments()
        points = artworks[artwork].size()
        totalDistance = artworks[artwork].get_total_distance()
        totalSegmentsDist = artworks[artwork].get_total_segments_distance()
        averageStrokeLength = totalSegmentsDist / totalStrokes
        minimumStroke = artworks[artwork].get_minimum_stroke()
        
        print(f'\n\n {artwork} \n \
            Segments: {segments} \n \
            Points: {points} \n \
            Total strokes: {totalStrokes} \n \
            Total Distance Travelled (mm): {totalDistance} \n \
            Total Segments Distance (mm): {totalSegmentsDist} \n \
            Minimum Stroke Length (mm): {minimumStroke} \n \
            Average Stroke Length (mm): {averageStrokeLength} \n \
            Total Non-writing Distance (mm): {totalDistance - totalSegmentsDist} \n')
   

if __name__ == "__main__":
    main()
