import math
import pygame

from src.world                     import World
from src.entities.base_game_entity import BaseGameEntity
from src.machines.state_machine    import StateMachine

class MovingEntity (BaseGameEntity):

    def __init__(self, x, y, world: World, mass=1, max_speed=1, max_acceleration=1, max_rotation=math.pi, max_angular_acceleration=math.pi/4, color="white"):
        super().__init__(x, y, world)

        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.angular_acceleration = 0
        self.orientation = 0.0
        self.rotation = 0.0
        self.mass = mass
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration
        self.color = pygame.Color(color)
        self.state_machine = StateMachine(self, None)

    def _limit_entity(self) -> None:
        """ Limita a entidade aos dominios do ambiente. """

        width, height = self.environment.width, self.environment.height
        self.position.x %= width
        self.position.y %= height

    def _apply_force(self, force) -> None:
        """ Aplica a Segunda Lei de Newton para atualizar a aceleração. """
        self.acceleration += force / self.mass

        if self.acceleration.length() > self.max_acceleration:
            self.acceleration.scale_to_length(self.max_acceleration)

    def get_direction(self) -> pygame.Vector2:
        return pygame.Vector2(math.cos(self.orientation), math.sin(self.orientation))

    def draw(self, screen):
        direction = self.get_direction()
        tip = self.position + direction * 15

        pygame.draw.line(screen, 'white',
                        (int(self.position.x), int(self.position.y)),
                        (int(tip.x), int(tip.y)), 2)
        pygame.draw.circle(screen, self.color,
                        (int(self.position.x), int(self.position.y)), 6)


    def change_color(self, color: str) -> None:
        """ Troca a cor da entidade. """
        self.color = pygame.Color(color)

    def update(self, delta_time) -> None:
        """ Atualiza a entidade. """
        
        if self.state_machine:
            self.state_machine.update(delta_time)

    def apply_steering(self, steering, delta_time):
        self.velocity += steering.linear * delta_time

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * delta_time
        self.orientation += steering.angular * delta_time

        self.acceleration = pygame.Vector2(0,0)

        self._limit_entity()