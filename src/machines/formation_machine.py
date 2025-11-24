import pygame

class FormationMachine ():

    def __init__(self, owner, start_formation=None):
        if not owner:
            raise ValueError("O 'owner' da StateMachine não pode ser None.")

        self.owner = owner
        self.current_formation = start_formation
        self.previous_formation = None

    def update(self, delta_time):
        """ Atualiza a Máquina de Estados. """

        if self.current_formation:
            self.owner.update_slots()
    
    def change_state(self, new_formation):
        """ Troca o estado atual. """

        self.previous_formation = self.current_formation
        self.current_formation = new_formation

        self.owner.update_slots()

    def revert_to_previous_state(self):
        """ Troca para o estado anterior. """

        if not self.previous_formation: return
        self.change_state(self.previous_formation)        