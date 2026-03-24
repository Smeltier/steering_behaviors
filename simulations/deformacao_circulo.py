import random
import math

import pygame

from utils.ellipse import Ellipse
from utils.grid_graph import GridGraph

def random_free_node(graph:GridGraph):
    return random.choice(graph.nodes)

def circle_collides_with_rect(center, radius, rect) -> bool:
    cx, cy = center

    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))

    dist_x = cx - closest_x
    dist_y = cy - closest_y

    dist_sq = (dist_x**2) + (dist_y**2)

    return dist_sq <= (radius**2)
        
pygame.init()
pygame.display.set_caption("Deformação")

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
FPS = 60
BD_COLOR = pygame.Color("black")
SCREEN = pygame.display.set_mode(size=(WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

MAX_A, MAX_B = 100, 100
MIN_A, MIN_B = 10, 10
DA, DB = 50, 50

ellipse = Ellipse(x=0, y=0, a=MAX_A, b=MAX_B)

graph = GridGraph(width=WIDTH//TILE_SIZE, height=HEIGHT//TILE_SIZE)

for _ in range(100):
    graph.obstacles.add(random_free_node(graph))

running = True
while running:
    delta_time = CLOCK.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()

    ellipse_center = (mx, my)
    ellipse.position = ellipse_center

    colliding = False
    for obs in graph.obstacles:
        rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if circle_collides_with_rect(ellipse_center, ellipse.a, rect):
            colliding = True
            break

    if colliding:
        ellipse._a = max(MIN_A, ellipse._a - DA * delta_time)
        ellipse._b = max(MIN_B, ellipse._b - DB * delta_time)
    else:
        ellipse._a = min(MAX_A, ellipse._a + DA * delta_time)
        ellipse._b = min(MAX_B, ellipse._b + DB * delta_time)

    SCREEN.fill(BD_COLOR)

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(SCREEN, (40, 40, 40), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(SCREEN, (40, 40, 40), (0, y), (WIDTH, y))

    for obs in graph.obstacles:
        rect = (obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(SCREEN, "red", rect)

    pygame.draw.circle(
        surface=SCREEN,
        color="white",
        center=(mx, my),
        radius=5
    )

    ellipse.draw(surface=SCREEN)

    pygame.display.flip()

pygame.quit()