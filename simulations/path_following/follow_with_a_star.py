import math
import random

import pygame

from simulations.hierarquia_no_controle_de_enxames.swarm_state import SwarmState
from simulations.hierarquia_no_controle_de_enxames.ellipse import Ellipse
from simulations.path_following.grid_adapter import GridAdapter
from simulations.path_following.path_follow import PathFollow
from src.outputs.behavior_and_weight import BehaviorAndWeight
from src.states.blended_steering import BlendedSteering
from src.entities.moving_entity import MovingEntity
from src.states.separation import Separation
from src.world import World

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
ROTATION_SPEED = 50.0
NUM_ENTITIES = 20
TILE_SIZE = 10
SPAWN_POS = (WIDTH / 3, HEIGHT / 2)
FPS = 60

def heuristic_factory(cols): 
    def heuristic(u, v): 
        c1, r1 = u % cols, u // cols 
        c2, r2 = v % cols, v // cols 
        return math.sqrt((c1 - c2)**2 + (r1 - r2)**2) 
    return heuristic

def create_entity(world: World, ellipse: Ellipse) -> None:
    x = SPAWN_POS[0] + random.randint(-20, 20)
    y = SPAWN_POS[1] + random.randint(-20, 20)

    entity = MovingEntity(x, y, world, 1, 150, 50)

    states = [
        BehaviorAndWeight(state = SwarmState(entity = entity, ellipse = ellipse, k1 = 50000000, k2 = 10, gamma = 0.001), weight = 1),
        BehaviorAndWeight(state = Separation(entity = entity), weight = 10),
    ]

    entity.change_state(BlendedSteering(entity = entity, behaviors = states))
    world.add_entity(entity)

def main():
    pygame.init()

    world = World(screen = SCREEN)
    ellipse = Ellipse(WIDTH // 2, HEIGHT // 2, 200, 200, color = 'yellow')

    grid = GridAdapter(WIDTH, HEIGHT, TILE_SIZE)
    start_pos = (SPAWN_POS[0], SPAWN_POS[1]) 
    end_pos = (700, 700)
    waypoints = grid.get_path_waypoints(start_pos, end_pos, heuristic_factory(WIDTH // TILE_SIZE))

    leader = MovingEntity(SPAWN_POS[0], SPAWN_POS[1], world, 1, 10, 10)
    leader.change_state(PathFollow(leader, MovingEntity(0, 0, world), waypoints=waypoints, waypoint_tolerance=20))
    world.add_entity(leader)

    for _ in range(NUM_ENTITIES):
        create_entity(world = world, ellipse = ellipse)

    running = True
    while running:
        SCREEN.fill('black')

        delta_time = CLOCK.tick(FPS) / 1000.0
        ellipse.update(delta_time)

        ellipse.position.x = leader.position.x
        ellipse.position.y = leader.position.y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for x in range(0, WIDTH, TILE_SIZE):
            pygame.draw.line(SCREEN, (30, 30, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pygame.draw.line(SCREEN, (30, 30, 30), (0, y), (WIDTH, y))
            
        if waypoints:
            pygame.draw.lines(SCREEN, 'green', False, waypoints, 2)
            for wp in waypoints:
                pygame.draw.circle(SCREEN, 'red', wp, 3)


        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            ellipse._a += ROTATION_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            ellipse._b += ROTATION_SPEED * delta_time
        if keys[pygame.K_DOWN]:
            ellipse._a -= ROTATION_SPEED * delta_time
        if keys[pygame.K_LEFT]:
            ellipse._b -= ROTATION_SPEED * delta_time
        if keys[pygame.K_q]:
            ellipse._rotation -= ROTATION_SPEED * delta_time
        if keys[pygame.K_e]:
            ellipse._rotation += ROTATION_SPEED * delta_time

        ellipse.draw(SCREEN)
        world.update(delta_time)
        pygame.display.flip()

    pygame.quit()

main()