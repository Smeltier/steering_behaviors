import heapq

class DStarLite:
    def __init__(self, graph, start, goal, heuristic):
        self.graph = graph
        self.s_start = start
        self.s_goal = goal
        self.s_last = start
        self.heuristic = heuristic
        self.km = 0
        self.g = {node: float('inf') for node in graph.nodes}
        self.rhs = {node: float('inf') for node in graph.nodes}
        self.U = []

        self.rhs[self.s_goal] = 0
        heapq.heappush(self.U, (self.calculate_key(self.s_goal), self.s_goal))

    def calculate_key(self, s):
        min_val = min(self.g[s], self.rhs[s])
        return (min_val + self.heuristic(self.s_start, s) + self.km, min_val)

    def update_vertex(self, u):
        self.U = [item for item in self.U if item[1] != u]
        heapq.heapify(self.U)
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculate_key(u), u))

    def compute_shortest_path(self):
        while self.U and (heapq.nsmallest(1, self.U)[0][0] < self.calculate_key(self.s_start) or 
                          self.rhs[self.s_start] != self.g[self.s_start]):
            
            k_old, u = heapq.heappop(self.U)
            k_new = self.calculate_key(u)

            if k_old < k_new:
                heapq.heappush(self.U, (k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.graph.get_predecessors(u):
                    if s != self.s_goal:
                        self.rhs[s] = min(self.rhs[s], self.graph.cost(s, u) + self.g[u])
                    self.update_vertex(s)
            else:
                self.g[u] = float('inf')
                for s in self.graph.get_predecessors(u) + [u]:
                    if s != self.s_goal:
                        self.rhs[s] = self.calculate_rhs(s)
                    self.update_vertex(s)

    def calculate_rhs(self, s):
        costs = [self.graph.cost(s, sprime) + self.g[sprime] for sprime in self.graph.get_successors(s)]
        return min(costs) if costs else float('inf')