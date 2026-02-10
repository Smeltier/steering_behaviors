import random

import pygame

from utils.ellipse import Ellipse
from src.outputs.behavior_and_weight import BehaviorAndWeight
from src.states.blended_steering import BlendedSteering
from src.entities.moving_entity import MovingEntity
from src.states.swarm_state import SwarmState
from src.states.separation import Separation
from src.world import World

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
ROTATION_SPEED = 50.0
NUM_ENTITIES = 20
FPS = 60

def create_entity(world: World, ellipse: Ellipse) -> None:
    x = random.randint(1, WIDTH - 1)
    y = random.randint(1, HEIGHT - 1)

    entity = MovingEntity(x, y, world, 1, 150, 50)

    states = [
        BehaviorAndWeight(state = SwarmState(entity = entity, ellipse = ellipse, k1 = 5000, k2 = 10, gamma = 0.001), weight = 2),
        BehaviorAndWeight(state = Separation(entity = entity), weight = 5),
    ]

    entity.change_state(BlendedSteering(entity = entity, behaviors = states))
    world.add_entity(entity)

def main():
    pygame.init()

    world = World(screen = SCREEN)
    ellipse = Ellipse(WIDTH // 2, HEIGHT // 2, 500, 800, color = 'yellow')

    for _ in range(NUM_ENTITIES):
        create_entity(world = world, ellipse = ellipse)

    running = True
    while running:
        SCREEN.fill('black')

        delta_time = CLOCK.tick(FPS) / 1000.0
        ellipse.update(delta_time)

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

        mouse_position = pygame.Vector2(pygame.mouse.get_pos())

        dx = mouse_position.x - ellipse.position.x
        dy = mouse_position.y - ellipse.position.y

        ellipse.update(delta_time, dx, dy)

        ellipse.draw(SCREEN)
        world.update(delta_time)
        pygame.display.flip()

    pygame.quit()

main()