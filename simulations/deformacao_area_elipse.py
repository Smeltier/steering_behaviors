import random
import math

import pygame as pg

from utils.ellipse import Ellipse
from utils.grid_graph import GridGraph

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
FPS = 60
DA, DB = 100, 100
DR = 100
STRENGTH_GAIN = 2.5

def random_free_node(graph:GridGraph):
    """ Escolhe um nó aleatório de graph.nodes. """
    return random.choice(graph.nodes)

def draw_graph_lines(screen):
    """ Desenha o grid que representa o Grafo """
    for x in range(0, WIDTH, TILE_SIZE):
        pg.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pg.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def draw_obstacles(screen, graph:GridGraph):
    """ Desenha os obstáculos presentes em graph.obstacles em uma superfície. """
    for obs in graph.obstacles:
        rect = (obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(screen, "red", rect)

def ellipse_collision_axes_rotated(center, a, b, theta, rect):
    """ Verifica se a elipse colidiu com algum obstáculo e retorna o quanto 
        ela entrou nele (em caso de colisão). 
    """

    if a <= 0 or b <= 0:
        return False, 0.0, 0.0, 0.0

    cx, cy = center
    ct = math.cos(theta)
    st = math.sin(theta)

    # G: Passa de coordenadas globais para um modelo local que é baseado na deformação da elipse.
    def to_local(px, py):
        dx = px - cx
        dy = py - cy
        lx = ct * dx + st * dy
        ly = -st * dx + ct * dy
        return lx, ly

    corners = [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom)
    ]

    lc = [to_local(x, y) for x, y in corners]
    min_x = min(p[0] for p in lc)
    max_x = max(p[0] for p in lc)
    min_y = min(p[1] for p in lc)
    max_y = max(p[1] for p in lc)

    closest_x = 0.0
    if 0.0 < min_x:
        closest_x = min_x
    elif 0.0 > max_x:
        closest_x = max_x

    closest_y = 0.0
    if 0.0 < min_y:
        closest_y = min_y
    elif 0.0 > max_y:
        closest_y = max_y

    vx = closest_x / a
    vy = closest_y / b
    value = vx*vx + vy*vy

    # G: Verifica se o ponto mais próximo encontrado está dentro da elipse.
    #    Precisa ser <= 1 para estar contido na área da elipse.
    if value > 1.0:
        return False, 0.0, 0.0, 0.0

    # G: Calcula o gradiente da elipse. Usaremos para calcular uma normal
    #    que representa o quanto o bloco entrou na elipse.
    gx = closest_x / (a*a)
    gy = closest_y / (b*b)

    if gx == 0.0 and gy == 0.0:
        dl = abs(0.0 - min_x)
        dr = abs(max_x - 0.0)
        dt = abs(0.0 - min_y)
        db = abs(max_y - 0.0)
        m = min(dl, dr, dt, db)

        if m == dl:
            gx, gy = -1.0, 0.0
        elif m == dr:
            gx, gy = 1.0, 0.0
        elif m == dt:
            gx, gy = 0.0, -1.0
        else:
            gx, gy = 0.0, 1.0

    # G: Normalização da normal.
    glen = math.hypot(gx, gy)
    nx = gx / glen
    ny = gy / glen

    # G: Cálculo da profundidade, ou seja, o quanto o obstáculo entrou na elipse.
    r = math.sqrt(max(value, 1e-12))
    depth = 1.0 - r

    return True, nx, ny, depth

def basic_deformation(ellipse:Ellipse, local_nx:float, local_ny:float, strength:float, dt:float) -> None:
    wx = abs(local_nx)
    wy = abs(local_ny)

    kA = DA * strength * wx
    kB = DB * strength * wy

    ellipse.a = max(MIN_A, ellipse.a - kA * dt)
    ellipse.b = max(MIN_B, ellipse.b - kB * dt)

# def keep_area_deformation(ellipse:Ellipse, local_nx:float, local_ny:float, strength:float, dt:float) -> None:
#     K = ellipse.a * ellipse.b
#     if K <= 0:
#         return
#
#     wx = abs(local_nx)
#     wy = abs(local_ny)
#
#     da = DA * strength * wx * dt
#     db = DB * strength * wy * dt
#
#     new_a = max(MIN_A, ellipse.a - da)
#     new_b = max(MIN_B, ellipse.b - db)
#
#     new_K = new_a * new_b
#     if new_K > 0:
#         s = math.sqrt(K / new_K)
#         ellipse.a = min(MAX_A, max(MIN_A, new_a * s))
#         ellipse.b = min(MAX_B, max(MIN_B, new_b * s))

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Deformação Área')

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    MAX_A, MAX_B = 100, 100
    MIN_A, MIN_B = 10, 10
    ellipse = Ellipse(0, 0, a=MAX_A, b=MAX_B)

    graph = GridGraph(WIDTH//TILE_SIZE, HEIGHT//TILE_SIZE)
    for _ in range(100):
        graph.obstacles.add(random_free_node(graph))

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1_000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        mx, my = pg.mouse.get_pos()

        ellipse_center: tuple[float, float] = (mx, my)
        ellipse.position = pg.Vector2(ellipse_center)

        sum_nx = 0.0
        sum_ny = 0.0
        max_depth = 0.0
        contacts = 0

        for obs in graph.obstacles:
            rect = pg.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            hit, nx, ny, depth = ellipse_collision_axes_rotated(ellipse_center, ellipse.a, ellipse.b, ellipse.rotation, rect)

            if hit:
                sum_nx += nx
                sum_ny += ny
                max_depth += max(max_depth, depth)
                contacts += 1

        if contacts > 0:
            avg_nx = sum_nx / contacts
            avg_ny = sum_ny / contacts
            nlen = math.hypot(avg_nx, avg_ny)

            if nlen > 1e-6:
                avg_nx /= nlen
                avg_ny /= nlen

            strength = min(1.0, max_depth * STRENGTH_GAIN)
            strength = strength ** 0.5

            basic_deformation(ellipse, avg_nx, avg_ny, strength, delta_time)
            # keep_area_deformation(ellipse, avg_nx, avg_ny, strength, delta_time)

        else:
            ellipse.a = min(MAX_A, ellipse.a + DA * delta_time)
            ellipse.b = min(MAX_B, ellipse.b + DB * delta_time)

        screen.fill('black')

        draw_graph_lines(screen)
        draw_obstacles(screen, graph)

        pg.draw.circle(
            surface=screen,
            color="white",
            center=(mx, my),
            radius=2
        )

        ellipse.draw(surface=screen)

        pg.display.flip()

    pg.quit()
