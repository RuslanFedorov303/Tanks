import pygame
from random import randint




class Projectile:
    def __init__(projectile,
                 x_coord       = 100.0,
                 y_coord       = 100.0,
                 x_coord_speed = 20.0,
                 y_coord_speed = 20.0,
                 speed         = 70.0,
                 rotate        = 0.0,
                 damage      = 5000,
                 penetration = 20.0, # %
                 comand      = 'green',
                 tanks_list = list,
                 image = ''
                 ):

        projectile.x_coord       = x_coord
        projectile.y_coord       = y_coord
        projectile.x_coord_speed = x_coord_speed
        projectile.y_coord_speed = y_coord_speed
        projectile.speed         = speed
        projectile.rotate        = rotate
        projectile.damage      = damage
        projectile.penetration = penetration
        projectile.comand      = comand
        projectile.tanks_list = tanks_list
        projectile.image = pygame.transform.rotate(image, rotate)
        projectile.rect  = projectile.image.get_rect()
        projectile.mask  = pygame.mask.from_surface(projectile.image)
        projectile.colide = False



    def _projectileMove(projectile):
        projectile.x_coord += projectile.x_coord_speed * projectile.speed
        projectile.y_coord += projectile.y_coord_speed * projectile.speed

        projectile.rect.center = projectile.x_coord, projectile.y_coord



    def _projectileColideTanks(projectile):
        for tank in projectile.tanks_list:
            if tank.comand == projectile.comand: continue

            for hitbox in tank.hitboxes_list:
                offset_for_rect = hitbox['rect'].x - projectile.rect.x, \
                                  hitbox['rect'].y - projectile.rect.y
                if projectile.mask.overlap(hitbox['mask'], offset_for_rect):


                    if hitbox['type'] == 'center':
                        if randint(1, 100) <= projectile.penetration:
                            tank.health -= projectile.damage


                    elif hitbox['type'] == 'forehead':
                        if randint(1, 100) <= projectile.penetration * 1.5:
                            tank.health -= projectile.damage


                    elif hitbox['type'] == 'karma':
                        if randint(1, 100) <= projectile.penetration / 1.5:
                            tank.health -= projectile.damage


                    projectile.colide = True
                    return



    def projectileUpdate(projectile):
        if not projectile.colide:
            projectile._projectileMove()
            projectile._projectileColideTanks()



    def getData(self):
        return {
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'rotate' : self.rotate
        }