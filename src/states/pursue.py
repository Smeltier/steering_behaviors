import pygame

from src.states.seek import Seek
from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput

class Pursue(Seek):

    _max_prediction: float

    def __init__(self, entity: MovingEntity, target: MovingEntity, max_prediction: float = 1.0):
        super().__init__(entity, target)
        
        if max_prediction <= 0:
            raise ValueError('max_prediction deve ser um valor positivo.')

        self._max_prediction = max_prediction

    def enter(self) -> None:
        print(f"[DEBUG] {self._entity.ID} -> Pursue")
        self._entity.change_color("orange")
    
    def exit(self) -> None:
        return super().exit()

    def execute(self, delta_time) -> None:
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self) -> SteeringOutput:
        steering = SteeringOutput()

        if not self._target: return steering
            
        try:
            direction = self._target.position - self._entity.position
            distance = direction.length()
            speed = self._entity.velocity.length()

            if speed == 0 or speed <= distance / self._max_prediction:
                prediction = self._max_prediction
            else:
                prediction = distance / speed

            predicted_position = self._target.position + self._target.velocity * prediction

            steering_vector = predicted_position - self._entity.position
            steering.linear = steering_vector.normalize()
            steering.linear *= self._entity.max_acceleration

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