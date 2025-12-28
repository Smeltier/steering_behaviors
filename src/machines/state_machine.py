from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.state import State
    from src.entities.moving_entity import MovingEntity

class StateMachine:

    _owner: 'MovingEntity'
    _current_state: 'State'
    _previous_state: 'State'

    def __init__(self, owner: 'MovingEntity', start_state: 'State' = None) -> None:
        if not owner:
            raise ValueError("O 'owner' da StateMachine não pode ser None.")

        self._owner = owner
        self._current_state = start_state
        self._previous_state = None

        if self._current_state:
            self._current_state.enter()

    def update(self, delta_time: float) -> None:
        """ Atualiza a Máquina de Estados. """

        if not self._current_state: 
            return

        try:
            self._current_state.execute(delta_time)
        except Exception as e:
            print(f"[ERROR] Falha no {self._current_state}.execute(): {e}")
            self._current_state = None
    
    def change_state(self, new_state: 'State') -> None:
        """ Troca o estado atual. """

        if not new_state: 
            return

        if self._current_state:
            self._current_state.exit()
        
        self._previous_state = self._current_state
        self._current_state = new_state
        
        try:
            self._current_state.enter()
            
        except Exception as e:
            print(f"[ERROR] Falha no {self._current_state}.enter(): {e}")
            self._current_state = None

    def revert_to_previous_state(self) -> None:
        """ Troca para o estado anterior. """

        if not self._previous_state: 
            return
        
        self.change_state(self._previous_state)        