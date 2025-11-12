import pygame

from src.states.multi_target_steering import MultiTargetSteering
from src.outputs.steering_output import SteeringOutput

class Attraction (MultiTargetSteering):

    def __init__(self, entity, threshold=50, decay_coefficient=100000):
        super().__init__(entity, threshold)

        if decay_coefficient <= 0:
            raise ValueError('decay_coefficient deve ser maior que zero.')
        
        self.max_acceleration = entity.max_acceleration
        self.decay_coefficient = decay_coefficient

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Attraction")
        self.entity.change_color("brown")
    
    def exit(self):
        return super().exit()
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        self.targets = self.entity.environment.entities
        if len(self.targets) == 1: return steering

        try:
            for target in self.targets:

                if target == self.entity: 
                    continue

                direction = target.position - self.entity.position
                distance = direction.length()

                if distance == 0 or distance >= self.threshold:
                    continue

                strength = min(self.decay_coefficient / (distance * distance), self.max_acceleration)

                direction.normalize_ip()
                steering.linear += strength * direction

            if steering.linear.length_squared() > self.max_acceleration ** 2:
                steering.linear.scale_to_length(self.max_acceleration)

            steering.angular = 0.0
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Attraction (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Attraction.get_steering: {e}")
            return steering