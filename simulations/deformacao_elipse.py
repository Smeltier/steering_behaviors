import random

import pygame

from utils.ellipse import Ellipse
from utils.grid_graph import GridGraph


def random_free_node(graph:GridGraph):
    return random.choice(graph.nodes)


def ellipse_collision_axes(center:tuple[int,int], a:float, b:float, rect:pygame.Rect):
    if a <= 0 or b <= 0:
        return False, False, False

    cx, cy = center

    left = (rect.left - cx) / a
    right = (rect.right - cx) / a
    top = (rect.top - cy) / b
    bottom = (rect.bottom - cy) / b

    closest_x = max(left, min(0.0, right))
    closest_y = max(top, min(0.0, bottom))

    dist_sq = (closest_x**2) + (closest_y**2)

    colliding = dist_sq <= 1.0
    if not colliding:
        return False, False, False

    abs_x = abs(closest_x)
    abs_y = abs(closest_y)
    collide_a = abs_x >= abs_y
    collide_b = abs_y >= abs_x

    return True, collide_a, collide_b


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
DA, DB = 100, 100

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

    ellipse_center: tuple[float, float] = (mx, my)
    ellipse.position = pygame.Vector2(ellipse_center)

    colliding_a = False
    colliding_b = False
    for obs in graph.obstacles:
        rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        colliding, hit_a, hit_b = ellipse_collision_axes(ellipse_center, ellipse.a, ellipse.b, rect)
        if colliding:
            colliding_a = colliding_a or hit_a
            colliding_b = colliding_b or hit_b
            if colliding_a and colliding_b:
                break

    if colliding_a:
        ellipse.a = max(MIN_A, ellipse.a - DA * delta_time)
    else:
        ellipse.a = min(MAX_A, ellipse.a + DA * delta_time)

    if colliding_b:
        ellipse.b = max(MIN_B, ellipse.b - DB * delta_time)
    else:
        ellipse.b = min(MAX_B, ellipse.b + DB * delta_time)

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
