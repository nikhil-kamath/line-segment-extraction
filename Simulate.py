'''class that simulates a robot which can only see to a certain range and adds
error to the point locations on each measurement'''
import math
import random


class Simulator:
    def __init__(self) -> None:
        self.RANGE = 300
        self.ERROR = 5
    
    def error(self, location, points):
        viewed_points = []
        for point in points:
            if math.dist(point, location) > self.RANGE:
                continue
            
            x, y = point
            x += random.uniform(-self.ERROR, self.ERROR)
            y += random.uniform(-self.ERROR, self.ERROR)
            viewed_points.append((x, y))
        return viewed_points
            