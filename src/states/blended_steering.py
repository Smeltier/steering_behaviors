import pygame

from src.states.state import State
from src.outputs.steering_output import SteeringOutput
from src.outputs.behavior_and_weight import BehaviorAndWeight

class BlendedSteering (State):

    def __init__(self, entity, behaviors: list[BehaviorAndWeight]):
        super().__init__(entity)

        if len(behaviors) <= 0: 
            raise ValueError('behaviors deve ter pelo menos um estado.')

        self.behaviors = behaviors
        self.max_acceleration = entity.max_acceleration
        self.max_rotation = entity.max_rotation

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> BlendedSteering")
        self.entity.change_color("white")
    
    def exit(self):
        return super().exit()
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        try:
            for behavior in self.behaviors:
                behavior_steering = behavior.state.get_steering()
                steering.linear += (behavior_steering.linear * behavior.weight)
                steering.angular += (behavior_steering.angular * behavior.weight)

            if steering.linear.length() > self.max_acceleration:
                steering.linear.scale_to_length(self.max_acceleration)

            steering.angular = max(min(steering.angular, self.max_rotation), -self.max_rotation)

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Blended Steering (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no BlendedSteering.get_steering: {e}")
            return steering