import heapq

class Graph:

    _size: int
    _vertex_data: list[str]
    _adj_matrix: list[list[int]]

    def __init__(self, size):
        self._size = size
        self._adj_matrix = [[0] * size for _ in range(size)]
        self._vertex_data = [''] * size

    def add_edge(self, u, v, weight):
        if not (0 <= u < self._size and 0 <= v < self._size):
            return
        self._adj_matrix[u][v] = weight
        self._adj_matrix[v][u] = weight

    def add_vertex_data(self, vertex, data):
        if not (0 <= vertex < self._size):
            return
        self._vertex_data[vertex] = data
    
    def dijkstra(self, src_data):
        src = self._vertex_data.index(src_data)
        distances = [float('inf')] * self._size
        distances[src] = 0
        heap = [(0, src)]

        while heap:
            atual_weight, u = heapq.heappop(heap)

            if atual_weight > distances[u]:
                continue

            for v, weight in enumerate(self._adj_matrix[u]):
                if weight == 0: continue

                new_distance = atual_weight + weight

                if new_distance < distances[v]:
                    distances[v] = new_distance
                    heapq.heappush(heap, (new_distance, v))

        return distances
    
    def a_star(self, start_data, end_data, heuristic):
        start = self._vertex_data.index(start_data)
        end = self._vertex_data.index(end_data)

        heap = []
        came_from = {}
        g_score = [float('inf')] * self._size
        f_score = [float('inf')] * self._size

        heapq.heappush(heap, (0, start))
        g_score[start] = 0
        f_score[start] = heuristic(start, end)

        while heap:
            current_f, current = heapq.heappop(heap)

            if current == end:
                path = []
                while current in came_from:
                    path.append(self._vertex_data[current])
                    current = came_from[current]
                path.append(start_data)
                return path[::-1]
            
            if current_f > f_score[current]:
                continue

            for neighbor, weight in enumerate(self._adj_matrix[current]):
                if weight == 0: continue
                
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    f_score[neighbor] = f
                    heapq.heappush(heap, (f, neighbor))
        
        return None