import sys
import math

import pygame

from src.entities.moving_entity import MovingEntity
from simulations.d_star_lite.d_star_lite import DStarLite
from simulations.d_star_lite.d_star_path_follow import DStarPathFollow
from simulations.d_star_lite.grid_graph import GridGraph
from src.world import World

def heuristic(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def main():
    pygame.init()
    width, height = 800, 600
    tile_size = 20
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    graph = GridGraph(width // tile_size, height // tile_size)
    for i in range(10, 25): graph.obstacles.add((20, i))
    
    start_node = (5, 15)
    goal_node = (35, 15)

    planner = DStarLite(graph, start_node, goal_node, heuristic)
    planner.compute_shortest_path()

    world = World(screen=screen)
    
    robot = MovingEntity(
        x=start_node[0] * tile_size, 
        y=start_node[1] * tile_size, 
        world=world, 
        max_speed=120, 
        max_acceleration=50,
        color_name="cyan"
    )
    world.add_entity(robot)

    path_state = DStarPathFollow(
        entity=robot,
        target=MovingEntity(0, 0, world),
        planner=planner,
        graph=graph,
        tile_size=tile_size,
        waypoint_tolerance=15.0,
        slow_radius=40.0
    )

    robot.change_state(path_state)

    while True:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((20, 20, 20))

        for x in range(0, width, tile_size):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, height))
        for y in range(0, height, tile_size):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (width, y))

        for obs in graph.obstacles:
            pygame.draw.rect(screen, (100, 0, 0), (obs[0]*tile_size, obs[1]*tile_size, tile_size, tile_size))

        pygame.draw.circle(screen, "green", (goal_node[0]*tile_size + 10, goal_node[1]*tile_size + 10), 8)

        world.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    main()