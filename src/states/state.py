from abc import ABC, abstractmethod

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput

class State(ABC):
    """
    Classe base abstrata para todos os estados em um sistema de Máquina de Estado Finito (FSM).
    """

    _entity: MovingEntity

    def __init__(self, entity: MovingEntity) -> None:
        if not entity:
            raise ValueError('A entidade (entity) não pode ser None.')
        
        self._entity = entity

    @abstractmethod
    def enter(self) -> None:
        """ Executa a lógica de entrada do estado. """
        pass

    @abstractmethod
    def exit(self) -> None:
        """ Executa a lógica de saída do estado. """
        pass
    
    @abstractmethod
    def execute(self, delta_time: float) -> None:
        """ Executa a lógica principal de atualização do estado. """
        pass
    
    @abstractmethod
    def get_steering(self) -> SteeringOutput:
        """ Calcula e retorna a força de direção (steering) do agente. """
        pass

    @property
    def entity(self) -> MovingEntity:
        return self._entity