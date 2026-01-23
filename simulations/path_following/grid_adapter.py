import pygame

from simulations.path_following.graph import Graph

class GridAdapter:

    _rows: int
    _cols: int
    _graph: Graph
    _width: float
    _height: float
    _tile_size: int
    _obstacles: list[pygame.Rect]

    def __init__(self, width, height, tile_size, obstacles = None) -> None:
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._rows = height // tile_size
        self._cols = width // tile_size
        self._obstacles = obstacles if obstacles is not None else []

        self._graph = Graph(self._rows * self._cols)
        self._build_graph()

    def get_path_waypoints(self, start, end, heuristic):
        start_col = int(start[0] // self._tile_size)
        start_row = int(start[1] // self._tile_size)
        end_col = int(end[0] // self._tile_size)
        end_row = int(end[1] // self._tile_size)

        start_node = f"{start_col},{start_row}"
        end_node = f"{end_col},{end_row}"

        if not (0 <= start_col < self._cols and 0 <= start_row < self._rows): return []
        if not (0 <= end_col < self._cols and 0 <= end_row < self._rows): return []

        path_nodes = self._graph.a_star(start_node, end_node, heuristic)

        if not path_nodes: return []

        waypoints = []
        for node in path_nodes:
            c, r = map(int, node.split(','))
            world_x = c * self._tile_size + self._tile_size // 2
            world_y = r * self._tile_size + self._tile_size // 2

            waypoints.append((world_x, world_y))

        return waypoints

    def _get_index(self, col, row) -> int:
        return row * self._cols + col
    
    def _is_walkable(self, x, y) -> bool:
        tile_rect = pygame.Rect(x, y, self._tile_size, self._tile_size)

        for obs in self._obstacles:
            if tile_rect.colliderect(obs):
                return False
            
        return True

    def _build_graph(self) -> None:
        for r in range(self._rows):
            for c in range(self._cols):
                u = self._get_index(c, r)
                self._graph.add_vertex_data(u, f"{c},{r}")

                neighbors = [
                    (c + 1, r, 1.0), (c - 1, r, 1.0),    
                    (c, r + 1, 1.0), (c, r - 1, 1.0),     
                    (c + 1, r + 1, 1.41), (c - 1, r - 1, 1.41),
                    (c - 1, r + 1, 1.41), (c + 1, r - 1, 1.41)
                ]

                for nc, nr, weight in neighbors:
                    if not (0 <= nc < self._cols and 0 <= nr < self._rows):
                        continue

                    if not self._is_walkable(nr * self._tile_size, nc * self._tile_size):
                        continue

                    v = self._get_index(nc, nr)
                    self._graph.add_edge(u, v, weight)