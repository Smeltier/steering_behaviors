import math
from typing import TYPE_CHECKING

import pygame

from src.machines.state_machine import StateMachine
from src.outputs.steering_output import SteeringOutput
from src.entities.base_game_entity import BaseGameEntity

if TYPE_CHECKING:
    from src.world import World
    from src.states.state import State

class MovingEntity(BaseGameEntity):

    _velocity: pygame.Vector2
    _acceleration: pygame.Vector2
    _angular_acceleration: int
    _orientation: float
    _rotation: float
    _mass: float
    _max_speed: float
    _max_acceleration: float
    _max_rotation: float
    _max_angular_acceleration: float
    _color: pygame.Color
    _state_machine: StateMachine

    def __init__(self, x: float, y: float, world: 'World', mass=1.0, max_speed=1.0, max_acceleration=1.0, max_rotation=math.pi, max_angular_acceleration=math.pi/4, color_name="white"):
        super().__init__(x, y, world)

        self._mass = mass
        self._max_speed = max_speed
        self._max_acceleration = max_acceleration
        self._max_rotation = max_rotation
        self._max_angular_acceleration = max_angular_acceleration
        
        self._velocity = pygame.Vector2()
        self._acceleration = pygame.Vector2()
        self._color = pygame.Color(color_name)
        self._state_machine = StateMachine(self, None)
        
        self._angular_acceleration = 0
        self._orientation = 0.0
        self._rotation = 0.0

    def update(self, delta_time: float) -> None:
        if self._state_machine:
            self._state_machine.update(delta_time)

    def draw(self, screen: pygame.Surface) -> None:
        if self._velocity.length() > 0:
            direction = self._velocity.normalize()        
            line_length = 15  
            line_end = self._position + direction * line_length

            pygame.draw.line(screen, "white",  
                            (int(self._position.x), int(self._position.y)),
                            (int(line_end.x), int(line_end.y)), 2) 

            direction = pygame.math.Vector2(math.cos(self._orientation), math.sin(self._orientation))
            line_length = 10
            line_end = self._position + direction * line_length

            pygame.draw.line(screen, "grey",  
                            (int(self._position.x), int(self._position.y)),
                            (int(line_end.x), int(line_end.y)), 2)

        pygame.draw.circle(screen, self.color, 
                           (int(self._position.x), int(self._position.y)), 8)

    def apply_steering(self, steering: SteeringOutput, delta_time: float):
        self._velocity += steering.linear * delta_time

        if self._velocity.length() > self._max_speed:
            self._velocity.scale_to_length(self._max_speed)

        self._position += self._velocity * delta_time
        self._orientation += steering.angular * delta_time

        self._acceleration = pygame.Vector2(0,0)

        self._limit_entity()

    def change_color(self, color_name: str) -> None:
        """ Troca a cor da entidade. """
        self.color = pygame.Color(color_name)

    def change_state(self, new_state: 'State') -> None:
        self._state_machine.change_state(new_state)

    def get_direction(self) -> pygame.Vector2:
        return pygame.Vector2(math.cos(self._orientation), math.sin(self._orientation))
    
    def _limit_entity(self) -> None:
        """ Limita a entidade aos dominios do ambiente. """

        width, height = self._environment.width, self._environment.height
        self._position.x %= width
        self._position.y %= height

    def _apply_force(self, force: pygame.Vector2) -> None:
        """ Aplica a Segunda Lei de Newton para atualizar a aceleração. """

        if self._mass > 0:
            self._acceleration += force / self._mass

        if self._acceleration.length() > self._max_acceleration:
            self._acceleration.scale_to_length(self._max_acceleration)

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity
    
    @velocity.setter
    def velocity(self, value: pygame.Vector2) -> None:
        self._velocity = value

    @property
    def acceleration(self) -> pygame.Vector2:
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self, value: pygame.Vector2) -> None:
        self._acceleration = value

    @property
    def angular_acceleration(self) -> float:
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, value: float) -> None:
        self._angular_acceleration = value
    
    @property
    def orientation(self) -> float:
        return self._orientation
    
    @orientation.setter
    def orientation(self, value: float) -> None:
        self._orientation = value
    
    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        self._rotation = value
    
    @property
    def mass(self) -> float:
        return self._mass
    
    @mass.setter
    def mass(self, value: float) -> None:
        if value <= 0:
            raise ValueError("A massa deve ser maior que zero.")
        self._mass = value
    
    @property
    def max_speed(self) -> float:
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value: float) -> None:
        if value < 0:
            value = 0
        self._max_speed = value
    
    @property
    def max_acceleration(self) -> float:
        return self._max_acceleration

    @max_acceleration.setter
    def max_acceleration(self, value: float) -> None:
        if value < 0:
            value = 0
        self._max_acceleration = value
    
    @property
    def max_rotation(self) -> float:
        return self._max_rotation

    @max_rotation.setter
    def max_rotation(self, value: float) -> None:
        self._max_rotation = value
    
    @property
    def max_angular_acceleration(self) -> float:
        return self._max_angular_acceleration

    @max_angular_acceleration.setter
    def max_angular_acceleration(self, value: float) -> None:
        self._max_angular_acceleration = value
    
    @property
    def color(self) -> pygame.Color:
        return self._color
    
    @color.setter
    def color(self, value) -> None:
        if isinstance(value, str):
            self._color = pygame.Color(value)
        else:
            self._color = value