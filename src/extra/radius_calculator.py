import math

class RadiusCalculator:

    def __init__ (self, world, character_radius: float) -> None:
        self.world = world
        self.character_radius = character_radius
        
    def __call__(self) -> float:
        total_slots = len(self.world.entities) - 1

        if total_slots <= 0: return 0.0
        if total_slots == 1: return self.character_radius * 2

        try:
            ideal_radius = self.character_radius / math.sin(math.pi / total_slots)
            return ideal_radius
        except Exception:
            return self.character_radius * 2