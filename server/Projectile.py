import pygame
from random import randint, choice




class Projectile:
    def __init__(self,
                 x_coord       = 100.0,
                 y_coord       = 100.0,
                 x_coord_speed = 20.0,
                 y_coord_speed = 20.0,
                 speed         = 70.0,
                 rotate        = 0.0,
                 damage      = 5000,
                 penetration = 20.0, # %
                 comand      = 'green',
                 tanks_list  = list,
                 father_tank = None
                 ):

        self.x_coord       = x_coord
        self.y_coord       = y_coord
        self.x_coord_speed = x_coord_speed * speed
        self.y_coord_speed = y_coord_speed * speed
        self.rotate        = rotate
        self.damage      = damage
        self.penetration = penetration
        self.comand      = comand
        self.tanks_list  = tanks_list
        self.father_tank = father_tank
        self.surface = pygame.transform.rotate(pygame.Surface((10, 10)), rotate)
        self.rect  = self.surface.get_rect()
        self.mask  = pygame.mask.from_surface(self.surface)
        self.colide = False
        self.hit    = False



    def _projectileMoveStep(self, step_x, step_y):
        self.x_coord += step_x
        self.y_coord += step_y

        self.rect.center = (
            self.x_coord,
            self.y_coord
        )



    def _projectileColideTanks(self):
        for tank in self.tanks_list:
            if tank.comand == self.comand or tank.health <= 0:
                continue


            for hitbox in tank.hitboxes_list:
                if not self.rect.colliderect(hitbox['rect']):
                    continue

                offset_for_rect = hitbox['rect'].x - self.rect.x, \
                                  hitbox['rect'].y - self.rect.y

                if self.mask.overlap(hitbox['mask'], offset_for_rect):

                    if hitbox['type'] == 'center':
                        if randint(1, 100) <= self.penetration:
                            self.hit = True
                            tank.health -= self.damage


                    elif hitbox['type'] == 'forehead':
                        if randint(1, 100) <= self.penetration * 1.5:
                            self.hit = True
                            tank.health -= self.damage


                    else:
                        if randint(1, 100) <= self.penetration / 1.5:
                            self.hit = True
                            tank.health -= self.damage


                    if tank.health > 0:
                        if self.hit:
                            self.father_tank._soundEventLoad(choice(('Penetration1', 'Penetration2')), 5)
                        else:
                            self.father_tank._soundEventLoad(choice(('NoPenetration1', 'NoPenetration2')), 5)
                    else:
                        self.father_tank._soundEventLoad('Kill', 5)


                    self.colide = True
                    return



    def projectileUpdate(self):
        if self.colide:
            return

        # Полное перемещение пули за один тик
        move_x = self.x_coord_speed
        move_y = self.y_coord_speed

        # Максимальное расстояние одного шага
        max_step = 10

        # Сколько маленьких шагов нужно сделать
        distance = max(abs(move_x), abs(move_y))
        steps = max(1, int(distance / max_step))

        # Размер одного шага
        step_x = move_x / steps
        step_y = move_y / steps

        # Двигаем пулю маленькими шагами
        for _ in range(steps):

            self._projectileMoveStep(step_x, step_y)

            # Проверяем столкновение после каждого шага
            self._projectileColideTanks()

            if self.colide:
                return



    def getData(self):
        return {
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'rotate' : self.rotate
        }