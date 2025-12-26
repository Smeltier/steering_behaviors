import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.multi_target_steering import MultiTargetState

class Attraction(MultiTargetState):

    _max_acceleration: float
    _decay_coefficient: float

    def __init__(self, entity: MovingEntity, threshold: float = 50.0, decay_coefficient: float = 100000.0):
        super().__init__(entity, threshold)

        if decay_coefficient <= 0:
            raise ValueError('decay_coefficient deve ser maior que zero.')
        
        self._max_acceleration = entity.max_acceleration
        self._decay_coefficient = decay_coefficient

    def enter(self):
        print(f"[DEBUG] {self._entity.ID} -> Attraction")
        self._entity.change_color("brown")
    
    def exit(self):
        return super().exit()
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        self.targets = self._entity._environment._entities
        if len(self._targets) == 1: return steering

        try:
            for target in self._targets:

                if target == self._entity: 
                    continue

                direction = target.position - self._entity.position
                distance = direction.length()

                if distance == 0 or distance >= self._threshold:
                    continue

                strength = min(self._decay_coefficient / (distance * distance), self._max_acceleration)

                direction.normalize_ip()
                steering.linear += strength * direction

            if steering._linear.length_squared() > self._max_acceleration ** 2:
                steering._linear.scale_to_length(self._max_acceleration)

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