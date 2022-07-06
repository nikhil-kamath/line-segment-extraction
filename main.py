from typing import List, Tuple, Set
import pygame
from Detection import LineDetector, detectLines
from Simulate import Simulator


def draw_points(Map: pygame.Surface, points, color=(255, 0, 0), radius=3):
    for p in points: pygame.draw.circle(Map, color, p, radius)

'''allows user to draw points until enter key is pressed. returns the list of all points user drew'''
def draw_points_loop(Map: pygame.Surface, exit_key = pygame.K_RETURN, BG=(255, 255, 255)) -> Set[Tuple[int, int]]:
    Map.fill(BG)
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

def move_loop(Map: pygame.Surface, points: List[Tuple[int]], exit_key = pygame.K_RETURN, 
              BACKGROUND=(255, 255, 255), SEEDCOLOR=(0, 255, 0), LINECOLOR=(255, 0, 255),
              HIDDENCOLOR=(255, 170, 255), SEENCOLOR=(255, 0, 0)) -> None:
    
    running = True
    ld = LineDetector()
    sim = Simulator()
    clock = pygame.time.Clock()

    while running:
        clock.tick(30) # cap at 30 fps cuz my algorithm slow af
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == exit_key):
                running = False

            # reset with all points pink
            Map.fill(BACKGROUND)
            draw_points(Map, points, color=HIDDENCOLOR, radius=3)
            
            if pygame.mouse.get_focused():
                origin = pygame.mouse.get_pos()
                pygame.draw.circle(Map, (0, 255, 0), origin, 5)
                viewed_points = sim.error(origin, points)
                draw_points(Map, viewed_points, color=SEENCOLOR, radius=4)

                if output := detectLines(viewed_points, origin, ld, overlap=2):
                    lines, seeds = output
                    for line in lines: display_detected_item(Map, line, LINECOLOR)
                    for seed in seeds: display_detected_item(Map, seed, SEEDCOLOR, circle_size=5, line_width=2)
                else:
                    print("invalid origin location?")
            
            pygame.display.update()
                

def display_detected_item(Map: pygame.Surface, item, color, circle_size = 8, line_width = 3) -> None:
    display_points = item[1]
    start, end = item[4]
    for p in display_points:
        pygame.draw.circle(Map, color, p, circle_size)
    pygame.draw.line(Map, color, start, end, line_width)

def end_loop() -> None:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                running = False
        
        pygame.display.update()

def main():
    # initializing pygame
    pygame.init()
    pygame.display.set_caption("Line Segment Extraction")
    Map = pygame.display.set_mode((1080, 720))

    points = draw_points_loop(Map)
    move_loop(Map, points)
    end_loop()
    
    
if __name__ == "__main__":
    main()
