import math
import pygame

from src.world import World
from src.entities.base_game_entity import BaseGameEntity

class MovingEntity (BaseGameEntity):

    def __init__(self, x, y, world: World, mass=1, max_speed=1, max_acceleration=1, max_rotation=math.pi, max_angular_acceleration=math.pi/4, color="white"):
        super().__init__(x, y, world)

        self.velocity = pygame.Vector2()
        self.orientation = 0.0
        self.rotation = 0.0
        self.mass = mass
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration
        self.color = pygame.Color(color)

    