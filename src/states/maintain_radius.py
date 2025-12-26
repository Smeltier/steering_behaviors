import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.extra.radius_calculator import RadiusCalculator
from src.states.single_target_state import SingleTargetState

class MaintainRadius(SingleTargetState):

    _tolerance: float
    _max_acceleration: float
    _radius_calculator: RadiusCalculator

    def __init__(self, entity: MovingEntity, leader: MovingEntity, radius_calculator: RadiusCalculator, tolerance: float = 5.0):
        super().__init__(entity, leader)

        if radius_calculator == None:
            raise ValueError('radius_calculator não pode ser None') 

        self._radius_calculator = radius_calculator
        self._tolerance = tolerance
        self._max_acceleration = entity.max_acceleration

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> MaintainDistance")
        self._entity.change_color("white")
    
    def exit(self) -> None:
        return super().exit()
    
    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self._target: return steering

        try:
            ideal_radius = self._radius_calculator()
        except Exception as e:
            print(f'Erro ao calcular o raio: {e}')
            return steering
        
        vector_to_target = self._target.position - self._entity.position
        distance_to_target = vector_to_target.length()

        if distance_to_target == 0: return steering

        radial_direction = vector_to_target.normalize()
        error = distance_to_target - ideal_radius

        tangential_dir = pygame.Vector2(-radial_direction.y, radial_direction.x)
        steering.linear = tangential_dir * self._max_acceleration

        if abs(error) > self._tolerance:
            direction_sign = (error / abs(error))
            radial_force = radial_direction * (self._max_acceleration * direction_sign)
            steering.linear += radial_force
            steering.linear.scale_to_length(self._max_acceleration)

        steering.angular = 0
        return steering