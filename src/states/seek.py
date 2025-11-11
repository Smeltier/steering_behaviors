import pygame

from src.outputs.steering_output import SteeringOutput
from src.states.single_target_state import SingleTargetState

class Seek (SingleTargetState):

    def __init__(self, entity, target):
        super().__init__(entity, target)
        
        if not target:
            raise ValueError('O alvo (target) não pode ser None.')

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> Seek")
        self.entity.change_color("green")
    
    def exit(self) -> None:
        return super().exit()
    
    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target: return steering
        
        try:
            desired_velocity = self.target.position - self.entity.position

            if desired_velocity.length_squared() == 0:
                return steering
            
            desired_velocity.normalize_ip()
            desired_velocity *= self.entity.max_acceleration

            steering.linear  = desired_velocity
            steering.angular = 0.0

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering no Seek: {e}")
            return steering
        
        except Exception as e:
            print(f"[ERROR] Erro inesperado no Seek.get_steering: {e}")
            return steering