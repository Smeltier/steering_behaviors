import pygame

from src.states.flee import Flee
from src.outputs.steering_output import SteeringOutput

class Evade (Flee):

    def __init__(self, entity, target, max_prediction=1.0):
        super().__init__(entity, target)

        if max_prediction <= 0:
            raise ValueError('max_prediction deve ser um valor positivo.')
            
        self.max_prediction = max_prediction

    def enter(self):
        print(f"[DEBUG] {self.entity.ID} -> Evade")
        self.entity.change_color("purple")
    
    def exit(self):
        return super().exit()
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        if not self.target: return steering

        try:
            direction = self.target.position - self.entity.position
            self.distance = direction.length()
            speed = self.entity.velocity.length()

            if speed == 0 or speed <= self.distance / self.max_prediction:
                prediction = self.max_prediction
            else:
                prediction = self.distance / speed

            predicted_position = self.target.position + self.target.velocity * prediction

            steering_vector = self.entity.position - predicted_position
            steering.linear = steering_vector.normalize()
            steering.linear *= self.entity.max_acceleration

            steering.angular = 0
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Evade (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Evade.get_steering: {e}")
            return steering