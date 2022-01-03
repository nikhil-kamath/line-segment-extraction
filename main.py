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
def draw_points(Map: pygame.Surface, exit_key = pygame.K_RETURN) -> Set[Tuple[int, int]]:
    running = True
    points = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == exit_key):
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
    # initializing pygame
    pygame.init()
    pygame.display.set_caption("Line Segment Extraction")
    Map = pygame.display.set_mode((1080, 720))

    # colors
    WHITE = (255, 255, 255)
    SEEDCOLOR = (0, 255, 0)
    LINECOLOR = (255, 0, 255)
    origin = (500, 600)

    # filling with white and creating the origin point
    Map.fill(WHITE)
    pygame.draw.circle(Map, (0, 255, 0), origin, 5)


    # find our seeds
    ld = LineDetector()
    while True:
        points = draw_points(Map)
        Map = initialize_map(Map, points)

        output = detectLines(points, origin, ld, overlap=2)
        if output:
            break

        print("invalid points set, no seeds found")

    lines, seeds = output
    print(points)
    print(f"seeds detected: {len(seeds)}")
    print(f"lines extracted: {len(lines)}")
    # print("item we're dealing with: ")
    # print(*lines[0], sep='\n')
    # print("line of best fit found by ld:")
    # print(lines[0][0], lines[0][4])
    # print("line of best fit using these same points with ODR:")
    # test_fit = ld.fit(lines[0][1])
    # print(test_fit)
    # pygame.draw.line(Map, (0, 0, 255), *ld.get_points(test_fit), 9)
    # seed_fit = ld.fit(seeds[0][1])
    # print(seed_fit)
    # pygame.draw.line(Map, (0, 255, 255), *ld.get_points(seed_fit), 9)

    for line in lines:
        display_detected_item(Map, line, LINECOLOR)
    for seed in seeds:
        display_detected_item(Map, seed, SEEDCOLOR, circle_size=5, line_width=2)
    
    endloop()

def endloop() -> None:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                running = False
        
        pygame.display.update()

if __name__ == "__main__":
    main()
