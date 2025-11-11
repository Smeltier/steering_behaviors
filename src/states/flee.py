import pygame

from src.outputs.steering_output import SteeringOutput
from src.states.single_target_state import SingleTargetState

class Flee (SingleTargetState):

    def __init__(self, entity, target):
        super().__init__(entity, target)

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Flee")
        self.entity.change_color("yellow")

    def exit(self):
        pass

    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self):
        steering = SteeringOutput()

        if not self.target: return steering

        try:
            direction = self.entity.position - self.target.position

            if direction.length_squared() == 0:
                return steering

            direction.normalize_ip()
            steering.linear = direction * self.entity.max_acceleration
            steering.angular = 0

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering (Atributo faltando): {e}")
            return steering
        
        except Exception as e:
            print(f"[ERROR] Erro inesperado no Flee.get_steering: {e}")
            return steering