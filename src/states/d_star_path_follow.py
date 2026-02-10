import random

import pygame

from src.outputs.steering_output import SteeringOutput
from src.states.path_follow import PathFollow

class DStarPathFollow(PathFollow):

    def __init__(self, entity, target, planner, graph, tile_size, **kwargs):
        super().__init__(entity, target, waypoints=[entity.position], **kwargs)
        self.planner = planner
        self.graph = graph
        self.tile_size = tile_size

    def update_path_from_planner(self):
        new_waypoints = []
        curr = (int(self.entity.position.x // self.tile_size), 
                int(self.entity.position.y // self.tile_size))
        
        self.planner.km += self.planner.heuristic(self.planner.s_last, curr)
        self.planner.s_last = curr
        self.planner.s_start = curr

        visited = {curr}
        while curr != self.planner.s_goal:
            successors = self.graph.get_successors(curr)

            if not successors: 
                break
            
            curr = min(successors, key=lambda s: self.graph.cost(curr, s) + self.planner.g[s])
            
            if curr in visited or self.planner.g[curr] == float('inf'): 
                break

            visited.add(curr)
            
            wp = pygame.Vector2(curr[0] * self.tile_size + self.tile_size // 2, 
                                curr[1] * self.tile_size + self.tile_size // 2)
            
            new_waypoints.append(wp)

        self._waypoints = new_waypoints
        self._current_index = 0

    def check_for_obstacles(self):
        changed = False
        curr_x = int(self.entity.position.x // self.tile_size)
        curr_y = int(self.entity.position.y // self.tile_size)
        
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                node = (curr_x + dx, curr_y + dy)
                if node in self.graph.nodes and self.is_physically_blocked(node):
                    if node not in self.graph.obstacles:
                        self.update_obstacle_in_planner(node, is_add=True)
                        changed = True

        return changed

    def update_obstacle_in_planner(self, node, is_add):
        if is_add:
            self.graph.obstacles.add(node)
        else:
            self.graph.obstacles.discard(node)

        self.planner.km += self.planner.heuristic(self.planner.s_last, 
                           (int(self.entity.position.x // self.tile_size), 
                            int(self.entity.position.y // self.tile_size)))
        self.planner.s_last = (int(self.entity.position.x // self.tile_size), 
                               int(self.entity.position.y // self.tile_size))
        
        for neighbor in self.graph.get_predecessors(node) + [node]:
            if neighbor != self.planner.s_goal:
                self.planner.rhs[neighbor] = self.planner.calculate_rhs(neighbor)
            self.planner.update_vertex(neighbor)

    def execute(self, delta_time):
        curr_cell = (
            int(self.entity.position.x // self.tile_size),
            int(self.entity.position.y // self.tile_size)
        )

        if curr_cell != self.planner.s_start:
            self.planner.km += self.planner.heuristic(self.planner.s_last, curr_cell)
            self.planner.s_last = curr_cell
            self.planner.s_start = curr_cell

            self.planner.compute_shortest_path()
            self.update_path_from_planner()

        if self.check_for_obstacles():
            self.planner.compute_shortest_path()
            self.update_path_from_planner()

        super().execute(delta_time)

    def is_physically_blocked(self, node):
        return False