"""
UNIVERSITY OF QUEENSLAND TEAM PROJECT 2 2023
Author: Michael Smith 
Student Number: 45838464 
DATE: 06/08/2023
"""

import math, glob, matplotlib.pyplot as plt


class Drawing():

    pass

class Artwork():
    def __init__(self) -> None:
        self.points = []
        self.segments = []
        self.totalDistance = 0
        self.totalSegmentsDistance = 0
        self.totalStrokes = 0
        self.name = None

    def add_segment(self, segment):
        self.segments.append(segment)

    def add_point(self, point):
        self.points.append(point)

    def size(self):
        return len(self.points)
    
    def num_segments(self):
        return len(self.segments)
    
    def update_total_distance(self):
        
        for i in range(self.size()- 1):
            self.totalDistance += math.dist(self.points[i], self.points[i + 1])

    def update_total_segments_distance(self):

        for segment in self.segments:
            for i in range(len(segment) - 1):
                self.totalSegmentsDistance += math.dist(segment[i], segment[i + 1])
    

    def get_total_distance(self):

        return self.totalDistance
    
    def get_total_segments_distance(self):

        return self.totalSegmentsDistance
    
    def get_average_stroke_length(self):

        return self.averageStrokeLength
    
    def get_total_strokes(self):
        for segment in self.segments:
            self.totalStrokes += (len(segment) - 1)
        return self.totalStrokes
    
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
    


# class Line():
#     def __init__(self, start, end) -> None:
#         self.start = start
#         self.end = end
#         self. length =c math.dist(start, end)
        
"""

class Drawer():
    def __init__(self, artworks) -> None:
        self.artworks = artworks

    def draw_artworks(self):
        for i, artwork in enumerate(self.artworks):
            plt.figure(i)
            for segment in self.artworks[artwork]:
                x_coords, y_coords = zip(*segment.points)
                plt.plot(x_coords, y_coords)
            artwork_name = artwork.split('/')[5].split('.')[0]
            plt.title(artwork_name)
            plt.savefig(fname="/home/stiff/tp2-2023/mike/images/"+artwork_name)
        #plt.show()

"""


def read_in_artworks(filename):
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
                # empty line?
                continue
        return artwork


def main():

    pathlucas = "artwork-files/*.txt"
    artworks = {path: read_in_artworks(path) for path in glob.glob(pathlucas)}

    # Print out all the info

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
