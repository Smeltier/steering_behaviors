import pygame

class SteeringTarget:
    def __init__(self, position, orientation=0.0):
        self.position = pygame.math.Vector2(position)
        self.orientation = orientation
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0