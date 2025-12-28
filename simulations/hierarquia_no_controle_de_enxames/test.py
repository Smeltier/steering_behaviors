import random

import pygame

from src.world import World
from src.states.seek import Seek
from src.states.separation import Separation
from src.entities.moving_entity import MovingEntity
from src.states.blended_steering import BlendedSteering
from src.outputs.behavior_and_weight import BehaviorAndWeight
from simulations.hierarquia_no_controle_de_enxames.ellipse import Ellipse
from simulations.hierarquia_no_controle_de_enxames.swarm_state import SwarmState

FPS = 60
DEFAULT_CHARACTER_RADIUS = 33.0
WIDTH, HEIGHT = 1600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

ENTITIES_NUMBER = 20
ROTATION_SPEED = 90.0
SCALE_SPEED = 50.0

def main():
    pygame.init()

    world = World(SCREEN)
    ellipse = Ellipse(400, 300, 150, 80, rotation=0)
    mouse_entity = MovingEntity(x = 0, y = 0, world = world, color='blue')

    world.add_entity(mouse_entity)
    for _ in range(ENTITIES_NUMBER):
        x = random.randint(1, WIDTH - 1)
        y = random.randint(1, HEIGHT - 1)

        entity = MovingEntity(x = x, y = y, world = world, color = "cyan", mass = 1, max_speed = 300, max_acceleration = 300)

        states = [
            BehaviorAndWeight(state = SwarmState(entity, ellipse, k1=500, k2=5), weight = 5),
            BehaviorAndWeight(state = Seek(entity, mouse_entity), weight = 1),
            BehaviorAndWeight(state = Separation(entity), weight = 2),
        ]

        entity.change_state(BlendedSteering(entity, states))
        world.add_entity(entity)

    running = True
    while running:
        SCREEN.fill("black")
        delta_time = CLOCK.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mx, my = pygame.mouse.get_pos()
        dx = (mx - ellipse.position.x)
        dy = (my - ellipse.position.y)
        keys = pygame.key.get_pressed()

        dtheta = 0
        if keys[pygame.K_q]:
            dtheta = -ROTATION_SPEED * delta_time
        if keys[pygame.K_e]:
            dtheta = ROTATION_SPEED * delta_time

        if keys[pygame.K_LEFT]:
            ellipse._a -= SCALE_SPEED * delta_time
        if keys[pygame.K_RIGHT]:
            ellipse._a += SCALE_SPEED * delta_time
        if keys[pygame.K_UP]:
            ellipse._b += SCALE_SPEED * delta_time
        if keys[pygame.K_DOWN]:
            ellipse._b -= SCALE_SPEED * delta_time

        ellipse._a = max(10, ellipse._a)
        ellipse._b = max(10, ellipse._b)

        ellipse.update(delta_time, dx, dy, dtheta)

        mouse_entity.position = pygame.Vector2((mx, my))
        ellipse.draw(SCREEN)

        world.update(delta_time)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()