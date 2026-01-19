import pygame

from src.states.seek import Seek
from src.outputs.collision import Collision
from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.extra.collision_detector import CollisionDetector

class CollisionAvoidance(Seek):

    _collision_ray: float
    _avoid_distance: float
    _collision_detector: CollisionDetector

    def __init__(self, entity: MovingEntity, target: MovingEntity, collision_detector: CollisionDetector, collision_ray: float, avoid_distance: float):
        super().__init__(entity, target)

        if collision_detector is None:
            raise ValueError("collision_detector não poder ser None.")

        self._collision_detector = collision_detector
        self._collision_ray = collision_ray
        self._avoid_distance = avoid_distance

    def execute(self, delta_time: float) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        if self._entity.velocity.length() == 0:
            return SteeringOutput()

        ray_vector = self._entity.velocity.normalize() * self._collision_ray

        collision = self._collision_detector.get_collision(self._entity.position, ray_vector)

        if not collision: 
            return SteeringOutput()

        target_position = collision.position + collision.normal * self._avoid_distance    
        self._target.position = target_position

        return super().get_steering()
    
    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> CollisionAvoidance")
        self._entity.change_color("white")
    
    def exit(self) -> None:
        pass