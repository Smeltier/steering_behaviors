import random

import pygame

from simulations.hierarquia_no_controle_de_enxames.swarm_state import SwarmState
from simulations.hierarquia_no_controle_de_enxames.ellipse import Ellipse
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
FPS = 60

def create_entity(world: World, ellipse: Ellipse) -> None:
    x = WIDTH / 2
    y = HEIGHT / 2

    entity = MovingEntity(x, y, world, 1, 150, 50)

    states = [
        BehaviorAndWeight(state = SwarmState(entity = entity, ellipse = ellipse, k1 = 5000000000, k2 = 10, gamma = 0.001), weight = 1),
        BehaviorAndWeight(state = Separation(entity = entity), weight = 6),
    ]

    entity.change_state(BlendedSteering(entity = entity, behaviors = states))
    world.add_entity(entity)

def main():
    pygame.init()

    world = World(screen = SCREEN)
    ellipse = Ellipse(WIDTH // 2, HEIGHT // 2, 200, 200, color = 'yellow')

    waypoints = [
        (100, 100),
        (WIDTH - 100, 100),
        (WIDTH - 100, HEIGHT - 100),
        (100, HEIGHT - 100)
    ]

    leader = MovingEntity(WIDTH / 2, HEIGHT / 2, world, 1, 10, 10)
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