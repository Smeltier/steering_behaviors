import pygame
import random

from src.world import World
from src.entities.moving_entity import MovingEntity
from src.states.cohesion import Cohesion
from src.states.separation import Separation
from src.states.alignment import Alignment
from src.states.wander import Wander
from src.states.blended_steering import BlendedSteering
from src.outputs.behavior_and_weight import BehaviorAndWeight

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    world = World(screen)

    NUM_AGENTS = 20

    agents = []

    for _ in range(NUM_AGENTS):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        entity = MovingEntity(
            x=x,
            y=y,
            world=world,
            max_speed=50,
            max_acceleration=150,
        )

        world.add_entity(entity)
        agents.append(entity)

    for agent in agents:
        wander_target = MovingEntity(0, 0, world) 

        behaviors = [
            BehaviorAndWeight(Separation(agent),            weight=2.0),
            BehaviorAndWeight(Alignment(agent),             weight=1.2),
            BehaviorAndWeight(Cohesion(agent, threshold=100),              weight=1.0),
            BehaviorAndWeight(Wander(agent, wander_target), weight=0.2)
        ]

        blended = BlendedSteering(agent, behaviors)
        agent.state_machine.change_state(blended)

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        world.update(delta_time)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()