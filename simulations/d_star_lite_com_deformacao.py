import heapq
import random as rd

import pygame as pg

from utils.d_star_lite import DStarLite
from utils.ellipse import Ellipse
from utils.grid_graph import GridGraph
from utils.ellipse_collision_checker import ellipse_collision_axes
from utils.d_star_lite import DStarLite
from src.states.d_star_path_follow import DStarPathFollow
from src.entities.moving_entity import MovingEntity
from src.world import World


WIDTH, HEIGHT = 800, 600
TILE_SIZE: int = 20
FPS = 60
MAX_A, MAX_B = 100, 100
MIN_A, MIN_B = 10, 10
DA, DB = 100, 100

def heuristic(a:tuple[int,int], b:tuple[int,int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def random_free_node(graph:GridGraph):
    while True:
        node = rd.choice(graph.nodes)
        if node not in graph.obstacles:
            return node

def reached_goal(agent:MovingEntity, goal_node:tuple[int,int]) -> bool:
    current = (
        int(agent.position.x // TILE_SIZE),
        int(agent.position.y // TILE_SIZE)
    )
    return current == goal_node

def change_goal(planner:DStarLite, new_goal:tuple[int,int]):
    planner.s_goal = new_goal

    for node in planner.graph.nodes:
        planner.g[node] = float("inf")
        planner.rhs[node] = float("inf")

    planner.rhs[new_goal] = 0

    planner.U.clear()
    heapq.heappush(planner.U, (planner.calculate_key(new_goal), new_goal))

pg.init()
pg.display.set_caption("D* Lite com Deformação de Elipse")

screen = pg.display.set_mode(size=(WIDTH, HEIGHT))
clock = pg.time.Clock()

graph = GridGraph(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE)
start_node = random_free_node(graph=graph)
goal_node = random_free_node(graph=graph)
planner = DStarLite(graph=graph, start=start_node, goal=goal_node, heuristic=heuristic)
planner.compute_shortest_path()

for _ in range(100):
    graph.obstacles.add(random_free_node(graph))

ellipse = Ellipse(x=0, y=0, a=MAX_A, b=MAX_B)

world = World(screen=screen)
entity = MovingEntity(
    x=start_node[0] * TILE_SIZE,
    y=start_node[1] * TILE_SIZE,
    world=world,
    max_speed=100,
    max_acceleration=100,
    color_name="red",
)
world.add_entity(entity)

ellipse = Ellipse(
    x=entity.position.x,
    y=entity.position.y,
    a=200,
    b=200,
)

follow_state = DStarPathFollow(
    entity=entity,
    target=MovingEntity(0, 0, world=world),
    planner=planner,
    graph=graph,
    tile_size=TILE_SIZE,
    waypoint_tolerance=15.0,
    slow_radius=40.0
)

entity.change_state(follow_state)
follow_state.update_path_from_planner()

running: bool = True
while running:
    delta_time: float = clock.tick(FPS) / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            node = (x // TILE_SIZE, y // TILE_SIZE)
            if event.button == 1:
                follow_state.update_obstacle_in_planner(node, True)
            if event.button == 3:
                follow_state.update_obstacle_in_planner(node, False)

    ellipse.position = entity.position.copy()

    # G: lógica de deformação da elipse
    colliding_a: bool = False
    colliding_b: bool = False
    for obs in graph.obstacles:
        rect: pg.Rect = pg.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        center: tuple[int, int] = (int(ellipse.position.x), int(ellipse.position.y))

        colliding, hit_a, hit_b = ellipse_collision_axes(center, ellipse.a, ellipse.b, rect)
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

    if reached_goal(entity, goal_node):
        goal_node = random_free_node(graph)
        change_goal(planner, goal_node)
        planner.compute_shortest_path()
        follow_state.update_path_from_planner()

    screen.fill("black")

    for x in range(0, WIDTH, TILE_SIZE):
        pg.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, TILE_SIZE):
        pg.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

    for obs in graph.obstacles:
        rect = pg.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(screen, "red", rect)

    for wp in follow_state._waypoints: # type: ignore
        pg.draw.circle(screen, (0, 200, 255), wp, 3)
        pg.draw.circle(screen, (0, 255, 0), (goal_node[0] * TILE_SIZE + TILE_SIZE // 2, goal_node[1] * TILE_SIZE + TILE_SIZE // 2), 8)

    ellipse.draw(screen)
    world.update(delta_time)

    pg.display.flip()

pg.quit()
