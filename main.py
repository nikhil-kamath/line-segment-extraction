import typing
from numpy.core.fromnumeric import partition
import pygame
from Detection import LineDetector

'''initializes a white map with red points'''
def initialize_map(Map: pygame.Surface, points: typing.List[typing.Tuple[int, int]]) -> pygame.Surface:
    Map.fill((255, 255, 255))
    for point in points:
        pygame.draw.circle(Map, (0, 0, 0), point, 3)
    return Map

'''allows user to draw points until enter key is pressed. returns the list of all points user drew'''
def draw_points(Map: pygame.Surface) -> typing.Set[typing.Tuple[int, int]]:
    running = True
    points = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                running = False

        focused = pygame.mouse.get_focused()
        pressed = pygame.mouse.get_pressed()[0]
        if focused and pressed:
            position = pygame.mouse.get_pos()
            pygame.draw.circle(Map, (255, 0, 0), position, 3)
            if position not in points: 
                points.append(position)

        pygame.display.update()
    
    return points


def main():
    WHITE = (255, 255, 255)
    pygame.init()
    pygame.display.set_caption("Line Segment Extraction")
    Map = pygame.display.set_mode((1080, 720))
    Map.fill(WHITE)

    origin = (500, 600)
    pygame.draw.circle(Map, (0, 255, 0), origin, 5)

    seedcolor = (0, 255, 0)
    linecolor = (255, 0, 255)

    ssd = LineDetector()

    # find our seed
    valid = False
    while not valid:
        points = draw_points(Map)
        print(points)
        Map = initialize_map(Map, points)

        seed = ssd.Detect(points, origin)
        if seed is not None:
            seed_params, seed_points, indices, points, helper_points = seed
            valid = True
        else:
            valid = False
            print("seed not found")
            continue

        segment = ssd.Grow(seed_points, indices, points)
        if segment is not None:
            params, fit_points, indices, points, endpoints = segment
            valid = True
        else:
            valid = False
            print("seed couldn't grow")
            continue

    for point in seed_points:
        pygame.draw.circle(Map, seedcolor, point, 8)
    pygame.draw.line(Map, seedcolor, *helper_points, 3)

    for point in fit_points:
        pygame.draw.circle(Map, linecolor, point, 5)
    pygame.draw.line(Map, linecolor, *endpoints, 3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        pygame.display.update()

if __name__ == "__main__":
    main()
