import pygame
from random import randint
from time import time
import math
import json

from Projectile import Projectile




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
                 damage           = {'min': 3000, 'max': 8000}, # От - до
                 penetration      = 20.0, # %
                 recharge         = 3.0,
                 projectile_speed = 50.0,
                 username      = 'player',
                 comand        = 'green',
                 tank_id       = 0,
                 player_socket = None,
                 tanks_list       = list,
                 projectiles_list = list,
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

        if control_mode == 'keys'.lower():
            self._controlMode = self._turretRotateKeys
        else:
            self._controlMode = self._turretRotateMouse

        self.health           = health
        self.damage           = damage
        self.penetration      = penetration
        self.recharge         = recharge
        self.projectile_speed = projectile_speed
        self.username         = username
        self.comand           = comand
        self.tank_id          = tank_id
        self.player_socket    = player_socket
        self.tanks_list       = tanks_list     # Списки для взаемодействия
        self.projectiles_list = projectiles_list
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


        self.len_vector_of_hitbox_forehead = pygame.Vector2((140, 0))
        self.len_vector_of_hitbox_karma = pygame.Vector2((-140, 0))


        center_hitbox_original_surfase = pygame.Surface((230, 185), pygame.SRCALPHA) # базовая поверхность
        center_hitbox_original_surfase.fill((255, 0, 0))
        center_hitbox_current_surface = center_hitbox_original_surfase # текущая поверхность
        center_hitbox_rect = center_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord)) # rect
        center_hitbox_mask = pygame.mask.from_surface(center_hitbox_current_surface) # mask
        self.center_hitbox = {
            'original_surface': center_hitbox_original_surfase,
            'current_surface' : center_hitbox_current_surface,
            'rect': center_hitbox_rect,
            'mask': center_hitbox_mask,
            'type': 'center'
        }

        forehead_hitbox_original_surfase = pygame.Surface((50, 180), pygame.SRCALPHA)  # базовая поверхность
        forehead_hitbox_original_surfase.fill((0, 255, 0))
        forehead_hitbox_current_surface = forehead_hitbox_original_surfase  # текущая поверхность
        forehead_hitbox_rect = forehead_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord))  # rect
        forehead_hitbox_mask = pygame.mask.from_surface(forehead_hitbox_current_surface)  # mask
        self.forehead_hitbox = {
            'original_surface': forehead_hitbox_original_surfase,
            'current_surface': forehead_hitbox_current_surface,
            'rect': forehead_hitbox_rect,
            'mask': forehead_hitbox_mask,
            'type': 'forehead'
        }

        karma_hitbox_original_surfase = pygame.Surface((50, 180), pygame.SRCALPHA)  # базовая поверхность
        karma_hitbox_original_surfase.fill((0, 0, 255))
        karma_hitbox_current_surface = karma_hitbox_original_surfase  # текущая поверхность
        karma_hitbox_rect = karma_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord))  # rect
        karma_hitbox_mask = pygame.mask.from_surface(karma_hitbox_current_surface)  # mask
        self.karma_hitbox = {
            'original_surface': karma_hitbox_original_surfase,
            'current_surface': karma_hitbox_current_surface,
            'rect': karma_hitbox_rect,
            'mask': karma_hitbox_mask,
            'type': 'karma'
        }

        self.hitboxes_list = (self.karma_hitbox, self.center_hitbox, self.forehead_hitbox)


        self.events = []            # События в игре и положение курсора игрока
        self.player_mouse_x_coord = 0
        self.player_mouse_y_coord = 0



    def _bodyMove(self):
        if 'K_w' in self.events: self.position_vector += self.body_direction_vector * self.forward_speed
        if 'K_s' in self.events: self.position_vector -= self.body_direction_vector * self.backward_speed



    def _bodyRotate(self):
        if 'K_a' in self.events:
            self.body_rotate += self.body_rotate_speed
            self.turret_rotate += self.body_rotate_speed

            self.body_direction_vector.rotate_ip(-self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(-self.body_rotate_speed)

            self.len_vector_of_hitbox_forehead.rotate_ip(-self.body_rotate_speed)
            self.len_vector_of_hitbox_karma.rotate_ip(-self.body_rotate_speed)


        if 'K_d' in self.events:
            self.body_rotate -= self.body_rotate_speed
            self.turret_rotate -= self.body_rotate_speed

            self.body_direction_vector.rotate_ip(self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(self.body_rotate_speed)

            self.len_vector_of_hitbox_forehead.rotate_ip(self.body_rotate_speed)
            self.len_vector_of_hitbox_karma.rotate_ip(self.body_rotate_speed)


        self.x_coord = self.position_vector.x
        self.y_coord = self.position_vector.y



    def _hitboxesUpdate(self):
        for hitbox in self.hitboxes_list:
            hitbox['current_surface'] = \
                pygame.transform.rotate(
                    hitbox['original_surface'],
                    self.body_rotate)

            hitbox['rect'] = \
                hitbox['current_surface'].get_rect(center=(self.x_coord, self.y_coord))

            hitbox['mask'] = \
                pygame.mask.from_surface(hitbox['current_surface'])


        forehead_rect_pos = self.position_vector + self.len_vector_of_hitbox_forehead
        karma_rect_pos = self.position_vector + self.len_vector_of_hitbox_karma

        self.forehead_hitbox['rect'].center = forehead_rect_pos
        self.karma_hitbox['rect'].center = karma_rect_pos



    def _bodyColideTanks(self):
        for tank in self.tanks_list:
            if tank == self: continue

            for tank_hitbox in tank.hitboxes_list:
                for hitbox in self.hitboxes_list:
                    offset_for_rect = tank_hitbox['rect'].x - hitbox['rect'].x, \
                                      tank_hitbox['rect'].y - hitbox['rect'].y


                    if hitbox['mask'].overlap(tank_hitbox['mask'], offset_for_rect):
                        offset_for_tank = self.x_coord - tank.x_coord, \
                                          self.y_coord - tank.y_coord


                        move_vector = pygame.Vector2(offset_for_tank).normalize()
                        self.position_vector += move_vector



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


        if ('MOUSELEFTKEY' in self.events or 'K_UP' in self.events) \
        and self.recharging_long_exit - self.recharging_long_start >= self.recharge:


            self.projectiles_list.append(Projectile(x_coord       = self.x_coord,
                                                    y_coord       = self.y_coord,
                                                    x_coord_speed = self.turret_direction_vector.x,
                                                    y_coord_speed = self.turret_direction_vector.y,
                                                    speed         = self.projectile_speed,
                                                    rotate        = self.turret_rotate,
                                                    damage      = randint(self.damage['min'], self.damage['max']),
                                                    penetration = self.penetration,
                                                    comand      = self.comand,
                                                    tanks_list = self.tanks_list,
                                                    image = self.projectile_image
            ))
            self.recharging_long_start = time()



    def _socketPlayerReceivingEvent(self):
        events = json.loads(
            self.player_socket.recv(1024).decode().strip()
        )

        for event in events['keys']:
            self.events.append(event)
        self.player_mouse_x_coord = events['mouse_x'] + self.x_coord
        self.player_mouse_y_coord = events['mouse_y'] + self.y_coord



    def tankUpdate(self):
        if self.health <= 0:
            return

        try:
            self._socketPlayerReceivingEvent()
            self._bodyMove()
            self._bodyRotate()
            self._hitboxesUpdate()
            self._bodyColideTanks()
            self._controlMode()
            self._gunShoot()

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
            'comand'       : self.comand,
            'tank_id'      : self.tank_id
        }