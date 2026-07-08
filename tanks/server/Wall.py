import pygame




class Wall:
    def __init__(self,
                 x_coord = 0,
                 y_coord = 0,
                 width  = 100,
                 height = 100,
                 rotate = 0
                 ):


        self.x_coord = x_coord
        self.y_coord = y_coord


        original_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        original_surface.fill((0, 0, 0))
        rotated_surface = pygame.transform.rotate(original_surface, rotate)
        rect = rotated_surface.get_rect(center = (x_coord, y_coord))
        mask = pygame.mask.from_surface(rotated_surface)


        self.hitbox = {
            'rect': rect,
            'mask': mask
        }