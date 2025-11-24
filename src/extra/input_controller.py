import pygame

from src.entities.moving_entity import MovingEntity
from src.states.state import State
from src.states.align import Align
from src.states.seek import Seek
from src.states.wander import Wander
from src.states.face import Face
from src.states.arrive import Arrive
from src.states.evade import Evade
from src.states.separation import Separation
from src.states.collision_avoidance import CollisionAvoidance
from src.states.pursue import Pursue
from src.states.velocity_match import VelocityMatch
from src.states.flee import Flee
from src.states.attraction import Attraction

class InputController:
    def __init__(self, character, target=None):
        self.character = character
        self.target = target

        self.key_to_state = {
            pygame.K_1: Wander,
            pygame.K_2: Pursue,
            pygame.K_3: Seek,
            pygame.K_4: Flee,
            pygame.K_5: Face,
            pygame.K_6: Align,
            pygame.K_7: Arrive,
            pygame.K_8: Evade,
            pygame.K_9: Separation,
            pygame.K_q: VelocityMatch,
            pygame.K_w: Attraction,
            pygame.K_e: CollisionAvoidance,
            pygame.K_r: CollisionAvoidance
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            state: State = self.key_to_state.get(event.key)

            if state in [Attraction, Separation, CollisionAvoidance]:
                new_state = state(self.character)
            else:
                new_state = state(self.character, self.target)

            if state: self.character.state_machine.change_state(new_state)