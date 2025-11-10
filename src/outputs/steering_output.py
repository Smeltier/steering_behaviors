import pygame

class SteeringOutput ():
    def __init__(self):
        self.linear  = pygame.Vector2((0, 0))
        self.angular = 0.0