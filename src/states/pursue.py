import pygame

from src.states.seek import Seek
from src.outputs.steering_output import SteeringOutput

class Pursue (Seek):

    def __init__(self, entity, target, max_prediction=1.0):
        super().__init__(entity, target)
        
        if max_prediction <= 0:
            raise ValueError('max_prediction deve ser um valor positivo.')

        self.max_prediction = max_prediction

    def enter(self) -> None:
        print(f"[DEBUG] {self.entity.ID} -> Pursue")
        self.entity.change_color("orange")
    
    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self.target: return steering
            
        try:
            direction = self.target.position - self.entity.position
            distance = direction.length()
            speed = self.entity.velocity.length()

            if speed == 0 or speed <= distance / self.max_prediction:
                prediction = self.max_prediction
            else:
                prediction = distance / speed

            predicted_position = self.target.position + self.target.velocity * prediction

            steering_vector = predicted_position - self.entity.position
            steering.linear = steering_vector.normalize()
            steering.linear *= self.entity.max_acceleration

            steering.angular = 0
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Pursue (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Pursue.get_steering: {e}")
            return steering