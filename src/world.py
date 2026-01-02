from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.entities.base_game_entity import BaseGameEntity

class World:

    _screen: pygame.Surface
    _width: int
    _height: int
    _entities: list['BaseGameEntity']

    def __init__(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._width = screen.get_width()
        self._height = screen.get_height()
        self._entities = []

    def add_entity(self, entity: 'BaseGameEntity') -> None:
        """ Adiciona uma nova entidade ao mundo. Lança uma Exceção caso a entidade seja do tipo None. """

        if entity is None: 
            raise RuntimeError("Sua nova entidade não pode ser nula.")

        self._entities.append(entity)

    def remove_entity(self, entity: 'BaseGameEntity') -> None:
        """ Remove uma entidade do mundo. """
        self._entities = [e for e in self._entities if e != entity]

    def update(self, delta_time: float) -> None:
        """ Atualiza o mundo baseado-se no tempo. """

        for entity in self._entities:
            entity.update(delta_time)
            entity.draw(self._screen)

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height
    
    @property
    def screen(self) -> pygame.Surface:
        return self._screen
    
    @property
    def entities(self) -> list['BaseGameEntity']:
        return self._entities
    
    @screen.setter
    def screen(self, new_screen: pygame.Surface) -> None:
        self._screen = new_screen
        self._width = new_screen.get_width()
        self._height = new_screen.get_height()