import pygame

from src.states.single_target_state import SingleTargetState
from src.outputs.steering_output import SteeringOutput

class MaintainRadius (SingleTargetState):

    def __init__(self, entity, leader, radius_calculator, tolerance=5.0):
        super().__init__(entity, leader)

        if radius_calculator == None:
            raise ValueError('radius_calculator não pode ser None') 

        self.radius_calculator = radius_calculator
        self.tolerance = tolerance
        self.max_acceleration = entity.max_acceleration

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> MaintainDistance")
        self.entity.change_color("white")
    
    def exit(self) -> None:
        return super().exit()
    
    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target: return steering

        try:
            ideal_radius = self.radius_calculator()
        except Exception as e:
            print(f'Erro ao calcular o raio: {e}')
            return steering
        
        vector_to_target = self.target.position - self.entity.position
        distance_to_target = vector_to_target.length()

        if distance_to_target == 0: return steering

        radial_direction = vector_to_target.normalize()
        error = distance_to_target - ideal_radius

        tangential_dir = pygame.Vector2(-radial_direction.y, radial_direction.x)
        steering.linear = tangential_dir * self.max_acceleration

        if abs(error) > self.tolerance:
            direction_sign = (error / abs(error))
            radial_force = radial_direction * (self.max_acceleration * direction_sign)
            steering.linear += radial_force
            steering.linear.scale_to_length(self.max_acceleration)

        steering.angular = 0
        return steering