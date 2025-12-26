class StateMachine ():

    def __init__(self, owner, start_state=None):
        if not owner:
            raise ValueError("O 'owner' da StateMachine não pode ser None.")

        self.owner          = owner
        self.current_state  = start_state
        self.previous_state = None

        if self.current_state:
            self.current_state.enter()

    def update(self, delta_time):
        """ Atualiza a Máquina de Estados. """

        if not self.current_state: return

        try:
            self.current_state.execute(delta_time)
        except Exception as e:
            print(f"[ERROR] Falha no {self.current_state}.execute(): {e}")
            self.current_state = None
    
    def change_state(self, new_state):
        """ Troca o estado atual. """

        if not new_state: return

        if self.current_state:
            self.current_state.exit()
        
        self.previous_state = self.current_state
        self.current_state = new_state
        
        try:
            self.current_state.enter()
            
        except Exception as e:
            print(f"[ERROR] Falha no {self.current_state}.enter(): {e}")
            self.current_state = None

    def revert_to_previous_state(self):
        """ Troca para o estado anterior. """

        if not self.previous_state: return
        self.change_state(self.previous_state)        