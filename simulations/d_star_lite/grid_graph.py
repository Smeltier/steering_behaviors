class GridGraph:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.nodes = [(x, y) for x in range(width) for y in range(height)]
        self.obstacles = set()

    def get_successors(self, u: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = u
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        
        valid = []
        for n in neighbors:
            if 0 <= n[0] < self.width and 0 <= n[1] < self.height:
                if n not in self.obstacles:
                    valid.append(n)
        return valid

    def get_predecessors(self, u: tuple[int, int]) -> list[tuple[int, int]]:
        return self.get_successors(u)

    def cost(self, u: tuple[int, int], v: tuple[int, int]) -> float:
        if v in self.obstacles or u in self.obstacles:
            return float('inf')
        return 1.0