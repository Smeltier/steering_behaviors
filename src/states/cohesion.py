import pygame

from src.states.multi_target_steering import MultiTargetSteering
from src.outputs.steering_output import SteeringOutput

class Cohesion (MultiTargetSteering):

    def __init__(self, entity, threshold=50):
        super().__init__(entity, threshold)

    def enter(self):
        return super().enter()
    
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
            sum_positions = pygame.Vector2()
            count = 0

            for target in self.targets:

                if target == self.entity:
                    continue

                distance = (target.position - self.entity.position).length()

                if distance > self.threshold:
                    continue

                sum_positions += target.position
                count += 1

            if count == 0: return steering

            center_of_mass = sum_positions / count
            desired_direction = center_of_mass - self.entity.position

            if desired_direction.length_squared() > 0:
                desired_direction.normalize_ip()
                desired_direction *= self.entity.max_acceleration

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