import pygame


def ellipse_collision_axes(center:tuple[int,int], a:float, b:float, rect:pygame.Rect):
    """ Verifica se uma elipse colide com um retângulo e quais eixos estão colidindo. """

    if a <= 0 or b <= 0:
        return False, False, False

    cx, cy = center

    left = (rect.left - cx) / a
    right = (rect.right - cx) / a
    top = (rect.top - cy) / b
    bottom = (rect.bottom - cy) / b

    closest_x = max(left, min(0.0, right))
    closest_y = max(top, min(0.0, bottom))

    dist_sq = (closest_x**2) + (closest_y**2)

    colliding = dist_sq <= 1.0
    if not colliding:
        return False, False, False

    abs_x = abs(closest_x)
    abs_y = abs(closest_y)
    collide_a = abs_x >= abs_y
    collide_b = abs_y >= abs_x

    return True, collide_a, collide_b
