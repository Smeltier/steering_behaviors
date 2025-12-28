import pygame

from src.world import World
from src.entities.moving_entity import MovingEntity

from src.states.seek import Seek
from src.states.arrive import Arrive
from src.states.flee  import Flee
from src.states.wander import Wander

def main():
    pygame.init()

    FPS = 60
    WIDTH, HEIGHT = 800, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock  = pygame.time.Clock()

    world: World = World(screen)

    entity_one = MovingEntity(
        x = WIDTH  // 2,
        y = HEIGHT // 2,
        world = world, 
        max_speed = 300,
        max_acceleration = 500,
    )

    entity_two = MovingEntity(
        x = WIDTH // 4, 
        y = HEIGHT // 4, 
        world = world, 
        max_speed = 300,
        max_acceleration = 500,
    )

    entity_one.change_state(Arrive(entity_one, entity_two))
    entity_two.change_state(Wander(entity_two, MovingEntity(0, 0, world)))

    world.add_entity(entity_one)
    world.add_entity(entity_two)

    running = True
    while running:
        screen.fill('black')

        delta_time: float = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update(delta_time)

        pygame.display.flip()
        
    pygame.quit()

if __name__ == '__main__':
    main()