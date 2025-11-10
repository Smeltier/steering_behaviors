import pygame

class World ():

    def __init__(self, screen):
        self.domain   = screen
        self.width    = screen.get_width()
        self.height   = screen.get_height()
        self.entities = []

    def add_entity(self, entity) -> None:
        """ Adiciona uma nova entidade ao mundo. Lança uma Exceção caso a entidade seja do tipo None. """

        if entity is None: 
            raise RuntimeError("Sua nova entidade não pode ser nula.")

        self.entities.append(entity)

    def remove_entity(self, entity) -> None:
        """ Remove uma entidade do mundo. """
        self.entities = [e for e in self.entities if e != entity]

    def update(self, delta_time: float) -> None:
        """ Atualiza o mundo baseado-se no tempo. """

        for entity in self.entities:
            entity.update(delta_time)
            entity.draw(self.domain)