import pygame

from src.outputs.steering_output import SteeringOutput
from src.entities.moving_entity import MovingEntity
from src.states.arrive import Arrive

class PathFollow(Arrive):

    _current_index: int
    _waypoint_tolerance: float
    _waypoints: list[tuple[int, int]]

    def __init__(self, entity: MovingEntity, target: MovingEntity, slow_radius: float = 100, target_radius: float = 10, time_to_target: float = 0.1, waypoints = None, waypoint_tolerance: float = 1.0):
        super().__init__(entity, target, slow_radius, target_radius, time_to_target)

        if waypoints is None or len(waypoints) <= 0:
            raise ValueError("A lista de waypoints não pode ser vazia ou nula.")

        self._waypoints = waypoints
        self._current_index = 0
        self._waypoint_tolerance = waypoint_tolerance

    def get_steering(self) -> SteeringOutput:
        if self._current_index >= len(self._waypoints):
            return SteeringOutput()

        current_target_position = self._waypoints[self._current_index]
        self._target.position = pygame.Vector2(current_target_position)

        distance = self.entity.position.distance_to(self._target.position)

        if distance < self._waypoint_tolerance:
            self._current_index += 1

        return super().get_steering()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering=steering, delta_time=delta_time)

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> PathFollow")
        self._entity.change_color("violet")
    
    def exit(self) -> None: pass