import numpy as np
from scipy.odr import ODR, Model
from scipy.odr.odrpack import RealData
import math

class LineDetector:
    def __init__(self):
        self.EPSILON = 25 # maximum distance from any point to the fit line
        self.DELTA = 200 # maximum distance from any point to its predicted location 
        self.SEGMENT_LENGTH = 5 # number of points in seed segment
        self.P_MIN = 5 # minimum number of points in extracted line segment
        self.L_MIN = 200 # minimum length of a detected line segment

    '''Returns a valid seed segment given initialization parameters. 
    Requires that points are ordered counterclockwise around origin.'''
    def Detect(self, points, origin, start_index=0):
        N_P = len(points) # number of points
        for i in range(start_index, 1 + N_P - self.P_MIN):
            flag = True
            j = i + self.SEGMENT_LENGTH
            params = self.fit(points[i:j])

            for k in points[i:j]:
                prediction = self.predict(params, origin, k)

                # break cases
                delta_distance = math.dist(k, prediction)
                epsilon_distance = self.dist_point2line(k, params)
                if delta_distance > self.DELTA or epsilon_distance > self.EPSILON:
                    flag = False
                    break
            
            if flag:
                return [params, points[i:j], (i, j), points, self.get_points(params)]
        return None

    def odr_line(self, parameters, x): # parameters are the line equation parameters in standard form of a line
        a, b, c = parameters
        return x if b == 0 else (- (a * x + c) / b)

    '''uses scipy ODR to find line of best fit in general form'''
    def fit(self, points):
        x = np.array([p[0] for p in points])
        y = np.array([p[1] for p in points])

        linear_model = Model(self.odr_line)
        data = RealData(x, y)
        odr = ODR(data, linear_model, beta0=[1., 1., 1.])
        output = odr.run()

        return output.beta

    '''uses line parameters, origin point, and original point to find the predicted location of a point'''
    def predict(self, params, origin, point):
        return self.intersect(params, self.draw_line(origin, point))
    
    '''calculates intersection of lines with parameters param1 and param2'''
    def intersect(self, params1, params2):
        a, b, c = params1
        j, k, l = params2

        x = (c * k - b * l) / (b * j - a * k)
        y = (a * l - c * j) / (b * j - a * k)
        return x, y
    
    '''finds the parameters of a line going through points p1 and p2'''
    def draw_line(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        a = y1-y2
        b = x2-x1
        c = (x1-x2)*y1 + (y2-y1)*x1
        return a, b, c
    
    def dist_point2line(self, p, params):
        a, b, c = params
        x, y = p
        numerator = abs(a*x+b*y+c)
        denominator = math.sqrt(a**2 + b**2)
        return numerator / denominator

    def get_points(self, params):
        x0, x1 = 10, 1000
        return (x0, self.odr_line(params, x0)), (x1, self.odr_line(params, x1))

    '''grows line segment forwards and backwards until it reaches a point greater than epsilon away'''
    def Grow(self, seed, indices, points):
        N_P = len(points)
        line = self.fit(seed)
        i, j = indices
        L, P = 0, 0
        FRONT, BACK = j, i
        
        while FRONT < N_P and self.dist_point2line(points[FRONT], line) < self.EPSILON:
            line = self.fit(points[BACK:FRONT])
            FRONT += 1
        FRONT -= 1

        while BACK >= 0 and self.dist_point2line(points[BACK], line) < self.EPSILON:
            line = self.fit(points[BACK:FRONT])
            BACK -= 1
        BACK += 1

        P_BACK = self.orthoproject(points[BACK], line)
        P_FRONT = self.orthoproject(points[FRONT], line)

        L = math.dist(P_BACK, P_FRONT)
        P = FRONT - BACK

        # if L >= self.L_MIN and P >= self.P_MIN:
        return [line, points[BACK: FRONT+1], (BACK, FRONT), points, (P_BACK, P_FRONT)]

    '''finds closest point on line params to point p'''
    def orthoproject(self, p, params):
        a, b, c = params
        x, y = p
        a2 = -b
        b2 = a
        c2 = -a * y + b * x
        return self.intersect(params, (a2, b2, c2))

'''helper method that returns multiple valid seeds from a set of points. seeds do not overlap'''
def findSeeds(points, origin):
    seeds = []
    ssd = LineDetector()
    start_index = 0
    while start_index < len(points):
        seed = ssd.Detect(points, origin, start_index=start_index)

        # keep finding seeds until our method returns None
        if not seed:
            break
        
        seed_start, seed_end = seed[2]
        start_index = seed_end

        seeds.append(seed)

    return seeds