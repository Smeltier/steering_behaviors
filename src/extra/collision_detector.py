import pygame

from src.outputs.collision import Collision

class CollisionDetector: 

    def __init__ (self) -> None:
        raise NotImplementedError()

    def get_collision (self, position: pygame.Vector2, vector: pygame.Vector2) -> Collision:
        raise NotImplementedError()