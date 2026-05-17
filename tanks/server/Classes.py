# ----- !----- !-- Импортируем --! -----! ----- #
import pygame
from random import randint, choice
from time import time, sleep
import math
from socket import *
import threading
import json




# ----- !----- !-- Создаем - инициализируем --! -----! ----- #
# ----- !-- Настройки хоста --! ----- #
HOST = 'localhost'
IP = 8081
# ----- !-----! ----- #


pygame.init() # Инициализируем pygame
pygame.mixer.init() # Инициализируем mixer


screen = pygame.display.set_mode((1000, 1000)) # Создаем екран и время
clock = pygame.time.Clock()



# ----- !-- Загружаем картинки --! ----- #
body_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_body.png").convert_alpha(),
        (600, 300))

turret_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_turret.png").convert_alpha(),
        (600, 300))

gun_image = pygame.transform.scale(
        pygame.image.load("Image/Tank_gun.png").convert_alpha(),
        (600, 300))

projectile_image = pygame.transform.scale(
        pygame.image.load("Image/Projectile.png").convert_alpha(),
        (600, 300))

bush_image = pygame.transform.scale(
        pygame.image.load("Image/Bush.png").convert_alpha(),
        (600, 300))

projectiles = [] # Список снарядов
players = [] # Список танков
random_nickname = ['MadKing94', 'CyberGhost12', 'ToxicKing26', 'NeonTiger35', 'SwiftGhost15', 'CyberBlaze32', 'SuperStorm73', 'MegaSnake49', 'IronDragon46', 'SilentTiger98', 'CyberShadow79', 'CoolWolf76', 'WildHunter81', 'SwiftShadow19', 'ToxicHunter53', 'ShadowStorm38', 'ShadowFalcon43', 'DarkEagle99', 'SilentHunter52', 'CyberTiger40', 'FrostRaven64', 'NeonBlaze35', 'IronDragon62', 'WildShadow59', 'SilentGhost66', 'IronDragon56', 'IronTiger45', 'ShadowWolf35', 'DarkStorm32', 'MegaSnake96']



# ----- !-- Загружаем звуки --! ----- #
# s = pygame.mixer.Sound("../client2/Sound/Shoot.mp3")




# ----- !----- !-- Создаем - класи --! -----! ----- #
# ----- !-- Снаряды --! ----- #
class Projectile:
    def __init__(projectile,
                 x_coord       = 100.0,
                 y_coord       = 100.0,
                 x_coord_speed = 20.0,
                 y_coord_speed = 20.0,
                 speed         = 3.0,
                 rotate        = 0.0,
                 damage      = randint(3000, 8000),
                 penetration = 20,  # %
                 comand      = 'green',
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
        projectile.image = pygame.transform.rotate(image, rotate)
        projectile.projectile = pygame.mask.from_surface(
            pygame.Surface((600, 300)))



    def _projectileMove(projectile):
        projectile.x_coord += projectile.x_coord_speed * projectile.speed
        projectile.y_coord += projectile.y_coord_speed * projectile.speed



    def _projectileColide(projectile, colide):
        if __class__.colide == 'Tank' and colide.comand != projectile.comand:
            if colide.penetration <= randint(0, 100):
                colide.health -= projectile.damage



    def _projectileDraw(projectile, screen):
        projectile_rect = projectile.image.get_rect(center=(projectile.x_coord, projectile.y_coord))
        screen.blit(projectile.image, projectile_rect)



    def projectileUpdate(self, screen = None, colide = None):
        self._projectileMove()
        # self.projectileColide(colide)
        if not screen == None:
            self.projectileDraw(screen)



    def getData(self):
        return {
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'rotate' : self.rotate
        }




# ----- !-- Танки --! ----- #
class Tank:
    def __init__(self,
                 x_coord = 100.0,
                 y_coord = 100.0,
                 forward_speed  = 3.0,
                 backward_speed = 2.0,
                 __body_rotate       = 0.0,
                 __turret_rotate     = 0.0,
                 body_rotate_speed   = 1.0,
                 turret_rotate_speed = 1.2,
                 control_mode        = 'mouse', # 'mouse' или 'keys'
                 health           = 10_000,
                 damage           = (3000, 8000), # От - до
                 penetration      = 20, # %
                 recharge         = 3,
                 projectile_speed = 70,
                 comand           = 'green',
                 player_socket = None,
                 projectiles   = list,
                 username      = choice(random_nickname),
                 screen        = None,
                 body_image       = '',
                 turret_image     = '',
                 gun_image        = '',
                 projectile_image = ''
                 ):

        self.x_coord = x_coord
        self.y_coord = y_coord
        self.forward_speed  = forward_speed
        self.backward_speed = backward_speed
        self.body_rotate         = __body_rotate
        self.turret_rotate       = __turret_rotate
        self.body_rotate_speed   = body_rotate_speed   / 5
        self.turret_rotate_speed = turret_rotate_speed / 5

        if control_mode == 'keys':
            self._controlMode = self._turretRotateKeys
        else:
            self._controlMode = self._turretRotateMouse

        self.health           = health
        self.damage           = damage
        self.penetration      = penetration
        self.recharge         = recharge
        self.projectile_speed = projectile_speed
        self.comand           = comand
        self.player_socket    = player_socket

        if player_socket != None:
            self._updateEvent = self._socketPlayerReceivingEvent
        else:
            self._updateEvent = self._localGameLoadEvent

        self.projectiles   = projectiles  # Список для взаемодействия
        self.username      = username
        self.screen        = screen

        if screen != None:
            self._tankDrawAt = self._tankDraw
        else:
            self._tankDrawAt = None

        self.body_image       = body_image
        self.turret_image     = turret_image
        self.gun_image        = gun_image
        self.projectile_image = projectile_image


        self.recharging_long_start = recharge # Настройки перезарядки
        self.recharging_long_exit  = 0.0
        self.gun_offset_animate    = 0.0


        self.position_vector         = pygame.Vector2((self.x_coord, self.y_coord))
        self.body_direction_vector   = pygame.Vector2((1, 0))
        self.turret_direction_vector = pygame.Vector2((1, 0))
        self.gun_direction_vector    = pygame.Vector2((1, 0))


        self.forehead_hitbox = pygame.Surface((30, 180), pygame.SRCALPHA)
        self.center_hitbox = pygame.Surface((270, 180), pygame.SRCALPHA)
        self.karma_hitbox = pygame.Surface((30, 180), pygame.SRCALPHA)

        self.hitboxes = (
            {
                'surfase': self.forehead_hitbox,
                'offset': (140, -90)
            }, {
                'surfase': self.center_hitbox,
                'offset': (-135, -90)
            }, {
                'surfase': self.karma_hitbox,
                'offset': (-170, -90)
            }
        )


        self.events = []            # События в игре и положение курсора игрока
        self.player_mouse_x_coord = 0
        self.player_mouse_y_coord = 0



    def _bodyMove(self):
        if 'K_w' in self.events: self.position_vector += self.body_direction_vector * self.forward_speed
        if 'K_s' in self.events: self.position_vector -= self.body_direction_vector * self.backward_speed



    def _bodyRotate(self):
        if 'K_a' in self.events:
            self.body_rotate   += self.body_rotate_speed
            self.turret_rotate += self.body_rotate_speed

            self.body_direction_vector.rotate_ip(-self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(-self.body_rotate_speed)


        if 'K_d' in self.events:
            self.body_rotate   -= self.body_rotate_speed
            self.turret_rotate -= self.body_rotate_speed

            self.body_direction_vector.rotate_ip(self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(self.body_rotate_speed)


        self.x_coord = self.position_vector.x
        self.y_coord = self.position_vector.y



    def _hitboxesUpdate(self):
        for hitbox in self.hitboxes:
            surfase = pygame.transform.rotate(hitbox['surfase'], self.body_rotate)
            surfase.fill((255, 0, 0))
            mask = pygame.mask.from_surface(surfase)

            center_rect = surfase.get_rect(center=(self.x_coord + hitbox['offset'][0], self.y_coord + hitbox['offset'][1]))
            screen.blit(surfase, center_rect)



    def _colideWalls(self):
        pass



    def _turretRotateMouse(self):
        rel_x = self.player_mouse_x_coord - self.x_coord
        rel_y = self.player_mouse_y_coord - self.y_coord

        target_angle = math.degrees(math.atan2(-rel_y, rel_x))
        angle_degrees = (target_angle - self.turret_rotate + 180) % 360 - 180


        if abs(angle_degrees) > self.turret_rotate_speed:
            if angle_degrees > 0:
                self.turret_rotate += self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(-self.turret_rotate_speed)

            else:
                self.turret_rotate -= self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(self.turret_rotate_speed)



    def _turretRotateKeys(self):
        if 'K_LEFT' in self.events:
            self.turret_rotate += self.turret_rotate_speed
            self.turret_direction_vector.rotate_ip(-self.turret_rotate_speed)

        if 'K_RIGHT' in self.events:
            self.turret_rotate -= self.turret_rotate_speed
            self.turret_direction_vector.rotate_ip(self.turret_rotate_speed)



    def _gunShoot(self):
        self.recharging_long_exit = time()


        if (('MOUSEBUTTONDOWN' in self.events or 'K_UP' in self.events)
        and self.recharging_long_exit - self.recharging_long_start >= self.recharge):
            # self.gun_offset_animate += 50.0


            self.projectiles.append(Projectile(x_coord       = self.x_coord,
                                               y_coord       = self.y_coord,
                                               x_coord_speed = self.turret_direction_vector.x,
                                               y_coord_speed = self.turret_direction_vector.y,
                                               speed         = self.projectile_speed,
                                               rotate        = self.turret_rotate,
                                               damage      = randint(self.damage[0], self.damage[1]),
                                               penetration = self.penetration,
                                               comand      = self.comand,
                                               image = self.projectile_image
            ))
            self.recharging_long_start = time()



    def _socketPlayerReceivingEvent(self, _):
        events = json.loads(
            self.player_socket.recv(1024).decode().strip()
        )

        for event in events[0]:
            self.events.append(event)
        self.player_mouse_x_coord = events[1]
        self.player_mouse_y_coord = events[2]



    def _localGameLoadEvent(self, events):
        for event in events[0]:
            self.events.append(event)
        self.player_mouse_x_coord = events[1]
        self.player_mouse_y_coord = events[2]



    def _tankDraw(self):
        rotated_body = pygame.transform.rotate(self.body_image, self.body_rotate)
        body_rect = rotated_body.get_rect(center=(self.x_coord, self.y_coord))
        self.screen.blit(rotated_body, body_rect)


        rotated_gun = pygame.transform.rotate(self.gun_image, self.turret_rotate)
        gun_rect = rotated_gun.get_rect(center=(self.x_coord, self.y_coord))
        self.screen.blit(rotated_gun, gun_rect)


        rotated_turret = pygame.transform.rotate(self.turret_image, self.turret_rotate)
        turret_rect = rotated_turret.get_rect(center=(self.x_coord, self.y_coord))
        self.screen.blit(rotated_turret, turret_rect)



    def tankUpdate(self, events = tuple):
        try:
            self._updateEvent(events)
            self._bodyMove()
            self._bodyRotate()
            self._hitboxesUpdate()
            self._colideWalls()
            self._controlMode()
            self._gunShoot()
            self._tankDrawAt()

        except Exception as ex:
            print(ex)

        self.events = []



    def getData(self):
        return {
            'x_coord'      : self.x_coord,
            'y_coord'      : self.y_coord,
            'body_rotate'  : self.body_rotate,
            'turret_rotate': self.turret_rotate,
            'health'       : self.health,
            'comand'       : self.comand
        }




# ----- !-- Карты --! ----- #
# class Map:
#     def __init__(map,
#                  fon_image = '',
#                  walls_list = list({
#                      'coords': (x, y),
#                      'image' : ''
#                  }),
#                  decorate_list = list({
#                      'coords': (x, y),
#                      'image' : ''
#                  })
#                  ):
#
#         map.fon_image = fon_image
#         map.walls_list = walls_list
#         map.decorate_list = decorate_list