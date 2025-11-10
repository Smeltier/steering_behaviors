class StateMachine ():

    def __init__(self, owner, start_state=None):
        self.owner          = owner
        self.current_state  = start_state
        self.previous_state = None

        self.update()

    def update(self):
        """ Atualiza a Máquina de Estados. """

        if not self.current_state: return
        self.current_state.execute()
    
    def change_state(self, state):
        """ Troca o estado atual. """

        if not state: return

        if self.current_state:
            self.current_state.exit()
        
        self.previous_state = self.current_state
        self.current_state = state
        
        self.current_state.enter()

    def revert_to_previous_state(self):
        """ Troca para o estado anterior. """

        if not self.previous_state: return
        self.change_state(self.previous_state)        