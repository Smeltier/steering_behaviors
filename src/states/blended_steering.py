import pygame

from src.states.state import State
from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput
from src.outputs.behavior_and_weight import BehaviorAndWeight

class BlendedSteering(State):

    _max_rotation: float
    _max_acceleration: float
    _behaviors: list[BehaviorAndWeight]

    def __init__(self, entity: MovingEntity, behaviors: list[BehaviorAndWeight]):
        super().__init__(entity)

        if len(behaviors) <= 0: 
            raise ValueError('behaviors deve ter pelo menos um estado.')

        self._behaviors = behaviors
        self._max_acceleration = entity.max_acceleration
        self._max_rotation = entity.max_rotation

    def enter(self):
        print(f"[DEBUG] {self._entity.ID} -> BlendedSteering")
        self._entity.change_color("white")
    
    def exit(self):
        pass
    
    def execute(self, delta_time):
        steering = self.get_steering()
        self._entity.apply_steering(steering, delta_time)
    
    def get_steering(self):
        steering = SteeringOutput()

        try:
            for behavior in self._behaviors:
                behavior_steering = behavior._state.get_steering()
                steering.linear += (behavior_steering.linear * behavior.weight)
                steering.angular += (behavior_steering.angular * behavior.weight)

            if steering.linear.length() > self._max_acceleration:
                steering.linear.scale_to_length(self._max_acceleration)

            steering.angular = max(min(steering.angular, self._max_rotation), -self._max_rotation)

            return steering

        except AttributeError as e:
            print(f"[WARNING] Falha ao calcular steering Blended Steering (Atributo faltando): {e}")
            return steering

        except ValueError:
            return steering

        except Exception as e:
            print(f"[ERROR] Erro inesperado no BlendedSteering.get_steering: {e}")
            return steering