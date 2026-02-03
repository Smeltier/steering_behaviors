import heapq
import sys
import math
import random

import pygame

from src.entities.moving_entity import MovingEntity
from simulations.d_star_lite.d_star_lite import DStarLite
from simulations.d_star_lite.d_star_path_follow import DStarPathFollow
from simulations.d_star_lite.grid_graph import GridGraph
from src.world import World

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 15

def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def random_free_node(graph):
    while True:
        node = random.choice(graph.nodes)
        if node not in graph.obstacles:
            return node

def reached_goal(robot, goal_node):
    curr = (
        int(robot.position.x // TILE_SIZE),
        int(robot.position.y // TILE_SIZE)
    )
    return curr == goal_node

def change_goal(planner, new_goal):
    planner.s_goal = new_goal
    
    for node in planner.graph.nodes:
        planner.g[node] = float("inf")
        planner.rhs[node] = float("inf")

    planner.rhs[new_goal] = 0

    planner.U.clear()
    heapq.heappush(planner.U, (planner.calculate_key(new_goal), new_goal))


pygame.init()
pygame.display.set_caption("D* Lite Simulation")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

graph = GridGraph(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE)

#for i in range(1, 100):
#    graph.obstacles.add(random.choice(graph.nodes))

start_node = random_free_node(graph)
goal_node = random_free_node(graph)

planner = DStarLite(graph, start_node, goal_node, heuristic)
planner.compute_shortest_path()

world = World(screen=screen)

robot = MovingEntity(
    x=start_node[0] * TILE_SIZE, 
    y=start_node[1] * TILE_SIZE, 
    world=world, 
    max_speed=50, 
    max_acceleration=50,
    color_name="cyan"
)
world.add_entity(robot)

path_state = DStarPathFollow(
    entity=robot,
    target=MovingEntity(0, 0, world),
    planner=planner,
    graph=graph,
    tile_size=TILE_SIZE,
    waypoint_tolerance=15.0,
    slow_radius=40.0
)

robot.change_state(path_state)

path_state.update_path_from_planner()

while True:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            node = (x // TILE_SIZE, y // TILE_SIZE)
            if event.button == 1:
                path_state.update_obstacle_in_planner(node, True)
            if event.button == 3:
                path_state.update_obstacle_in_planner(node, False)

    screen.fill((20, 20, 20))

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

    for obs in graph.obstacles:
        pygame.draw.rect(
            screen,
            (100, 0, 0),
            (obs[0]*TILE_SIZE, obs[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

    pygame.draw.circle(
        screen,
        "green",
        (goal_node[0]*TILE_SIZE + TILE_SIZE//2,
            goal_node[1]*TILE_SIZE + TILE_SIZE//2),
        8
    )

    for wp in path_state._waypoints:
        pygame.draw.circle(screen, (0, 200, 255), wp, 3)

    if reached_goal(robot, goal_node):
        goal_node = random_free_node(graph)

        change_goal(planner, goal_node)

        planner.compute_shortest_path()
        path_state.update_path_from_planner()

    world.update(dt)

    pygame.display.flip()