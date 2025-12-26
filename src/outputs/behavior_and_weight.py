from src.states.state import State

class BehaviorAndWeight:

    _state: State
    _weight: float

    def __init__(self, state: State, weight: float = 1.0):
        self._state = state
        self._weight: float = weight

    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, value: State) -> None:
        self._state = value
    
    @property
    def weight(self) -> float:
        return self._weight
    
    @weight.setter
    def weight(self, value: float) -> None:
        self._weight = value