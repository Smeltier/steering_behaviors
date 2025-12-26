import pygame

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.states.multi_target_steering import MultiTargetState

class Cohesion(MultiTargetState):

    def __init__(self, entity: MovingEntity, threshold: float = 50.0):
        super().__init__(entity, threshold)

    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        self._targets = self._entity._environment._entities
        if len(self._targets) == 1: return steering

        try:
            sum_positions = pygame.Vector2()
            count = 0

            for target in self._targets:

                if target == self._entity:
                    continue

                distance = (target.position - self._entity.position).length()

                if distance > self._threshold:
                    continue

                sum_positions += target.position
                count += 1

            if count == 0: return steering

            center_of_mass = sum_positions / count
            desired_direction = center_of_mass - self._entity.position

            if desired_direction.length_squared() > 0:
                desired_direction.normalize_ip()
                desired_direction *= self._entity.max_acceleration

            steering.linear = desired_direction
            steering.angular = 0
            
            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Cohesion (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no Cohesion.get_steering: {e}")
            return steering