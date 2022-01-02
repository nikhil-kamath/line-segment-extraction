from typing import List, Tuple, Set
import pygame
from Detection import LineDetector, findSeeds

'''initializes a white map with red points'''
def initialize_map(Map: pygame.Surface, points: List[Tuple[int, int]]) -> pygame.Surface:
    Map.fill((255, 255, 255))
    for point in points:
        pygame.draw.circle(Map, (0, 0, 0), point, 3)
    return Map

'''allows user to draw points until enter key is pressed. returns the list of all points user drew'''
def draw_points(Map: pygame.Surface) -> Set[Tuple[int, int]]:
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
    # colors
    WHITE = (255, 255, 255)
    SEEDCOLOR = (0, 255, 0)
    LINECOLOR = (255, 0, 255)

    pygame.init()
    pygame.display.set_caption("Line Segment Extraction")
    Map = pygame.display.set_mode((1080, 720))
    Map.fill(WHITE)

    origin = (500, 600)
    pygame.draw.circle(Map, (0, 255, 0), origin, 5)

    # find our seeds
    seeds = []
    while True:
        points = draw_points(Map)
        Map = initialize_map(Map, points)
        seeds = findSeeds(points, origin)

        if seeds:
            break

        print("invalid points set, no seeds found")


    for seed in seeds:
        seed_params, seed_points, indices, _, helper_points = seed
        print(indices, seed_points)
        for index in range(*indices):
            pygame.draw.circle(Map, SEEDCOLOR, points[index], 8)
        pygame.draw.line(Map, SEEDCOLOR, *helper_points, 3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        pygame.display.update()

if __name__ == "__main__":
    main()
