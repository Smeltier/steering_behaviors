import pygame

from src.states.seek import Seek
from src.outputs.collision import Collision
from src.outputs.steering_output import SteeringOutput
from src.extra.collision_detector import CollisionDetector

class CollisionAvoidance (Seek):

    def __init__ (self, entity, target, collision_ray, avoid_distance):
        super().__init__(entity, target)

        self.collision_detector = CollisionDetector()
        self.collision_ray = collision_ray
        self.avoid_distance = avoid_distance

    def enter (self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> CollisionAvoidance")
        self.entity.change_color("white")
    
    def exit (self) -> None:
        return super().exit()
    
    def execute (self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering (self) -> SteeringOutput:

        if self.entity.velocity.length() == 0:
            return SteeringOutput()

        ray_vector = self.entity.velocity.normalize() * self.collision_ray

        collision = self.collision_detector.get_collision(self.entity.position, ray_vector)

        if not collision: 
            return SteeringOutput()

        self.target = collision.position + collision.normal * self.avoid_distance    

        return super().get_steering()