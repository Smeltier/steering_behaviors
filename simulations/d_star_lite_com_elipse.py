import heapq
import sys
import math
import random

import pygame
from pygame.transform import threshold

from src.outputs.behavior_and_weight import BehaviorAndWeight
from src.states.priority_steering import PrioritySteering
from src.states.d_star_path_follow import DStarPathFollow
from src.states.blended_steering import BlendedSteering
from src.entities.moving_entity import MovingEntity
from src.states.swarm_state import SwarmState
from src.states.separation import Separation
from src.states.cohesion import Cohesion
from utils.d_star_lite import DStarLite
from utils.grid_graph import GridGraph
from utils.ellipse import Ellipse
from src.world import World

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
FPS = 60

def heuristic(a:tuple[int,int], b:tuple[int,int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def random_free_node(graph:GridGraph):
    while True:
        node = random.choice(graph.nodes)
        if node not in graph.obstacles:
            return node

def reached_goal(agent, goal_node):
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

def entity_maker(world, start_node, ellipse):
    entity = MovingEntity(
        x=start_node[0] * TILE_SIZE + random.randint(-20, 20),
        y=start_node[1] * TILE_SIZE + random.randint(-20, 20),
        world=world,
        max_speed=60,
        max_acceleration=160,
        color_name="blue",
    )

    flocking_state = BlendedSteering(entity,[
        BehaviorAndWeight(Separation(entity, threshold=30), weight=5.5),
        BehaviorAndWeight(SwarmState(entity, ellipse, k1=50, k2=5), weight=1.0),
        BehaviorAndWeight(Cohesion(entity, threshold=250), weight=2.0),
    ])
    entity.change_state(flocking_state)

    world.add_entity(entity)
    return entity
    

def run():
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()

    # G: Ajustes iniciais para o D* Lite.
    graph = GridGraph(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE)
    start_node = random_free_node(graph=graph)
    goal_node = random_free_node(graph=graph)
    planner = DStarLite(graph=graph, start=start_node, goal=goal_node, heuristic=heuristic)
    planner.compute_shortest_path()

    # G: Ajustes iniciais para a entidade principal.
    world = World(screen=SCREEN)
    entity = MovingEntity(
        x=start_node[0] * TILE_SIZE,
        y=start_node[1] * TILE_SIZE,
        world=world,
        max_speed=20,
        max_acceleration=20,
        color_name="red",
    )
    world.add_entity(entity)

    # G: Estado mesclado para a entidade.
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

    # G: criando as entidades auxiliares.
    for _ in range(10):
        entity_maker(world, start_node, ellipse)

    while True:
        delta_time = CLOCK.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        SCREEN.fill((20, 20, 20))

        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(SCREEN, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(SCREEN, (40, 40, 40), (0, y), (WIDTH, y)) 

        for obs in graph.obstacles:
            pygame.draw.rect(
                surface=SCREEN,
                color="red",
                rect=(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

        ellipse.position = entity.position.copy()

        if reached_goal(entity, goal_node):
            goal_node = random_free_node(graph)
            change_goal(planner, goal_node)
            planner.compute_shortest_path()
            follow_state.update_path_from_planner()

        for wp in follow_state._waypoints:
            pygame.draw.circle(SCREEN, (0, 200, 255), wp, 3)
        pygame.draw.circle(SCREEN, (0, 255, 0), (goal_node[0] * TILE_SIZE + TILE_SIZE // 2, goal_node[1] * TILE_SIZE + TILE_SIZE // 2), 8)

        ellipse.draw(surface=SCREEN)
        ellipse.update(delta_time=delta_time)
        world.update(delta_time=delta_time)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("D* Lite")
    run()
