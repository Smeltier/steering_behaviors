import math
import random
import pygame

from src.world import World
from src.entities.moving_entity import MovingEntity
from src.states.seek import Seek
from src.states.separation import Separation
from src.states.blended_steering import BlendedSteering
from src.states.maintain_radius import MaintainRadius
from src.extra.radius_calculator import RadiusCalculator
from src.outputs.behavior_and_weight import BehaviorAndWeight

DEFAULT_CHARACTER_RADIUS = 33.0

def entity_creator() -> MovingEntity:
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)

    separation_threshold = DEFAULT_CHARACTER_RADIUS * 2.5

    entity = MovingEntity(
        x = x,
        y = y,
        world = world,
        max_speed=50,
        max_acceleration=150,
    )

    behaviors = [
        BehaviorAndWeight(Separation(entity, threshold = separation_threshold), weight=2),
        BehaviorAndWeight(MaintainRadius(entity, mouse_entity, radius_calculator), weight=1)
    ]
    
    entity.state_machine.change_state(BlendedSteering(entity, behaviors))
    return entity

pygame.init()

FPS = 60
WIDTH, HEIGHT = 1600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

world = World(screen = SCREEN)

mouse_entity = MovingEntity(x = 0, y = 0, world = world, color='blue')
world.add_entity(mouse_entity)

radius_calculator = RadiusCalculator (
    world = world,
    character_radius = DEFAULT_CHARACTER_RADIUS
)

NUM_AGENTS: int = 10
for _ in range(NUM_AGENTS):
    entity = entity_creator()
    world.add_entity(entity)

running = True
while running:
    delta_time = CLOCK.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                new_entity = entity_creator()
                world.add_entity(new_entity)

            if event.key == pygame.K_w:
                if len(world.entities) > 1: 
                    world.entities.pop()

    mouse_entity.position = pygame.Vector2(pygame.mouse.get_pos())

    SCREEN.fill("black")
    world.update(delta_time)
    pygame.display.flip()

pygame.quit()