from typing import List, Tuple, Set
import pygame
from Detection import LineDetector, detectLines

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

def display_detected_item(Map: pygame.Surface, item, color, circle_size = 8, line_width = 3) -> None:
    display_points = item[1]
    start, end = item[4]
    for p in display_points:
        pygame.draw.circle(Map, color, p, circle_size)
    pygame.draw.line(Map, color, start, end, line_width)

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
    ld = LineDetector()
    ld.P_MIN = 5
    while True:
        points = draw_points(Map)
        Map = initialize_map(Map, points)

        output = detectLines(points, origin, ld)
        if output:
            break

        print("invalid points set, no seeds found")

    lines, seeds = output
    for line in lines:
        display_detected_item(Map, line, LINECOLOR)
    for seed in seeds:
        display_detected_item(Map, seed, SEEDCOLOR, circle_size=5, line_width=2)
    
    endloop()

def endloop() -> None:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

if __name__ == "__main__":
    main()
