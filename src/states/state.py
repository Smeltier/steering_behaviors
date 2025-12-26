from abc import ABC as AbstractClass, abstractmethod

from src.entities.moving_entity import MovingEntity
from src.outputs.steering_output import SteeringOutput

class State (AbstractClass):
    """
    Classe base abstrata para todos os estados em um sistema de Máquina de Estado Finito (FSM).
    """

    def __init__ (self, entity: MovingEntity) -> None:
        if not entity:
            raise ValueError('A entidade (entity) não pode ser None.')
        
        self.entity = entity

    @abstractmethod
    def enter (self) -> None:
        """ Executa a lógica de entrada do estado. """
        raise NotImplementedError('A subclasse deve implementar o método enter.')

    @abstractmethod
    def exit (self) -> None:
        """ Executa a lógica de saída do estado. """
        raise NotImplementedError('A subclasse deve implementar o método exit.')
    
    @abstractmethod
    def execute (self, delta_time) -> None:
        """ Executa a lógica principal de atualização do estado. """
        raise NotImplementedError('A subclasse deve implementar o método execute.')
    
    @abstractmethod
    def get_steering (self) -> SteeringOutput:
        """ Calcula e retorna a força de direção (steering) do agente. """
        raise NotImplementedError('A subclasse deve implementar o método get_steering.')