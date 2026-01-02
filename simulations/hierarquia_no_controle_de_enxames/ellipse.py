import pygame

class Ellipse:

    _position: pygame.Vector2
    _velocity: pygame.Vector2
    _rotation: float
    _a: float
    _b: float

    def __init__(self, x: float, y: float, a: float, b: float, rotation: float = 0, color: str = "white") -> None:
        self._position = pygame.Vector2((x, y))
        self._velocity = pygame.Vector2((0, 0))
        self._rotation = rotation
        self._a = a
        self._b = b
        self._color = color

    def update(self, delta_time: float, dx: float = 0.0, dy: float = 0.0, dtheta: float = 0) -> None:
        if delta_time > 0:
            self._velocity = pygame.Vector2(dx / delta_time, dy / delta_time)

        self._position.x += dx * delta_time
        self._position.y += dy * delta_time
        self._rotation += dtheta

    def draw(self, surface: pygame.Surface) -> None:
        max_radius = max(self._a, self._b)
        size = int(max_radius * 2.5) 

        shape_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        rect_width = self._a * 2
        rect_height = self._b * 2
        
        draw_rect = pygame.Rect(0, 0, rect_width, rect_height)
        draw_rect.center = (size // 2, size // 2)
        
        pygame.draw.ellipse(shape_surface, self._color, draw_rect, 2)

        rotated_surf = pygame.transform.rotate(shape_surface, -self._rotation)
        
        rot_rect = rotated_surf.get_rect(center=(int(self._position.x), int(self._position.y)))
        surface.blit(rotated_surf, rot_rect)

    @property
    def position(self): return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def rotation(self): return self._rotation

    @property
    def a(self): return self._a

    @property
    def b(self): return self._b