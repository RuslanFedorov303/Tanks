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
                 projectile_speed = 200.0,
                 username      = 'player',
                 comand        = 'green',
                 tank_id       = 0,
                 player_socket = None,
                 pushing_off_the_wall = 10,
                 pushing_off_the_tank = 3,
                 tanks_list       = list(),
                 projectiles_list = list(),
                 walls_list       = list(),
                 gun_animate_len = 50,
                 event_sounds = list()
                 ):

        self.x_coord = x_coord
        self.y_coord = y_coord
        self.forward_speed  = forward_speed
        self.backward_speed = backward_speed
        self.body_rotate         = __body_rotate
        self.turret_rotate       = __turret_rotate
        self.body_rotate_speed   = body_rotate_speed   / 5
        self.turret_rotate_speed = turret_rotate_speed / 5

        if control_mode.lower() == 'keys':
            self._controlMode = self._turretRotateKeys
        else:
            self._controlMode = self._turretRotateMouse

        self.health           = health
        self.damage           = damage
        self.penetration      = penetration
        self.recharge         = recharge
        self.projectile_speed = projectile_speed
        self.username         = username
        self.comand        = comand
        self.tank_id       = tank_id
        self.player_socket = player_socket
        self.pushing_off_the_wall = pushing_off_the_wall
        self.pushing_off_the_tank = pushing_off_the_tank
        self.tanks_list       = tanks_list     # Списки для взаемодействия
        self.projectiles_list = projectiles_list
        self.walls_list       = walls_list


        self.gun_animate_len       = gun_animate_len # Настройки перезарядки
        self.recharge_animate_long = self.gun_animate_len / self.recharge / 8
        self.recharging_long_start = recharge
        self.recharging_long_exit  = 0.0
        self.gun_offset_animate    = 0.0


        self.event_sounds = event_sounds


        self.position_vector         = pygame.Vector2((self.x_coord, self.y_coord))
        self.body_direction_vector   = pygame.Vector2((1, 0))
        self.turret_direction_vector = pygame.Vector2((1, 0))
        self.gun_position_vector     = pygame.Vector2((self.x_coord+0.1, self.y_coord+0.1))


        self.len_vector_of_hitbox_forehead = pygame.Vector2((140, 0))
        self.len_vector_of_hitbox_karma = pygame.Vector2((-140, 0))


        center_hitbox_original_surface = pygame.Surface((230, 185), pygame.SRCALPHA) # базовая поверхность
        center_hitbox_original_surface.fill((255, 0, 0))
        center_hitbox_current_surface = center_hitbox_original_surface # текущая поверхность
        center_hitbox_rect = center_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord)) # rect
        center_hitbox_mask = pygame.mask.from_surface(center_hitbox_current_surface) # mask
        self.center_hitbox = {
            'original_surface': center_hitbox_original_surface,
            'current_surface' : center_hitbox_current_surface,
            'rect': center_hitbox_rect,
            'mask': center_hitbox_mask,
            'type': 'center'
        }

        forehead_hitbox_original_surface = pygame.Surface((50, 180), pygame.SRCALPHA)  # базовая поверхность
        forehead_hitbox_original_surface.fill((0, 255, 0))
        forehead_hitbox_current_surface = forehead_hitbox_original_surface  # текущая поверхность
        forehead_hitbox_rect = forehead_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord))  # rect
        forehead_hitbox_mask = pygame.mask.from_surface(forehead_hitbox_current_surface)  # mask
        self.forehead_hitbox = {
            'original_surface': forehead_hitbox_original_surface,
            'current_surface': forehead_hitbox_current_surface,
            'rect': forehead_hitbox_rect,
            'mask': forehead_hitbox_mask,
            'type': 'forehead'
        }

        karma_hitbox_original_surface = pygame.Surface((50, 180), pygame.SRCALPHA)  # базовая поверхность
        karma_hitbox_original_surface.fill((0, 0, 255))
        karma_hitbox_current_surface = karma_hitbox_original_surface  # текущая поверхность
        karma_hitbox_rect = karma_hitbox_current_surface.get_rect(center=(self.x_coord, self.y_coord))  # rect
        karma_hitbox_mask = pygame.mask.from_surface(karma_hitbox_current_surface)  # mask
        self.karma_hitbox = {
            'original_surface': karma_hitbox_original_surface,
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
        move = self.body_direction_vector * self.forward_speed

        if 'K_w' in self.events:
            self.position_vector     += move
            self.gun_position_vector += move

        if 'K_s' in self.events:
            self.position_vector     -= move
            self.gun_position_vector -= move



    def _bodyRotate(self):
        if 'K_a' in self.events:
            self.body_rotate += self.body_rotate_speed
            self.turret_rotate += self.body_rotate_speed

            self.body_direction_vector.rotate_ip(-self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(-self.body_rotate_speed)

            self.len_vector_of_hitbox_forehead.rotate_ip(-self.body_rotate_speed)
            self.len_vector_of_hitbox_karma.rotate_ip(-self.body_rotate_speed)

            offset = self.gun_position_vector - self.position_vector
            rotated_offset = offset.rotate(-self.body_rotate_speed)
            self.gun_position_vector = self.position_vector + rotated_offset


        if 'K_d' in self.events:
            self.body_rotate -= self.body_rotate_speed
            self.turret_rotate -= self.body_rotate_speed

            self.body_direction_vector.rotate_ip(self.body_rotate_speed)
            self.turret_direction_vector.rotate_ip(self.body_rotate_speed)

            self.len_vector_of_hitbox_forehead.rotate_ip(self.body_rotate_speed)
            self.len_vector_of_hitbox_karma.rotate_ip(self.body_rotate_speed)

            offset = self.gun_position_vector - self.position_vector
            rotated_offset = offset.rotate(self.body_rotate_speed)
            self.gun_position_vector = self.position_vector + rotated_offset


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



    def _bodyColideWalls(self):
        for wall in self.walls_list:
            for hitbox in self.hitboxes_list:
                offset_for_rect = wall.hitbox['rect'].x - hitbox['rect'].x, \
                                 wall.hitbox['rect'].y - hitbox['rect'].y


                if hitbox['mask'].overlap(wall.hitbox['mask'], offset_for_rect):
                    offset_for_wall = self.x_coord - wall.x_coord, \
                                      self.y_coord - wall.y_coord


                    move_vector = pygame.Vector2(offset_for_wall).normalize()
                    self.position_vector     += move_vector * self.pushing_off_the_wall
                    self.gun_position_vector += move_vector * self.pushing_off_the_wall



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
                        self.position_vector     += move_vector * self.pushing_off_the_tank
                        self.gun_position_vector += move_vector * self.pushing_off_the_tank



    def _turretRotateMouse(self):
        rel_x = self.player_mouse_x_coord - self.x_coord
        rel_y = self.player_mouse_y_coord - self.y_coord

        target_angle = math.degrees(math.atan2(-rel_y, rel_x))
        angle_degrees = (target_angle - self.turret_rotate + 180) % 360 - 180


        if abs(angle_degrees) > self.turret_rotate_speed:
            if angle_degrees > 0:
                self.turret_rotate += self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(-self.turret_rotate_speed)

                offset = self.gun_position_vector - self.position_vector
                rotated_offset = offset.rotate(-self.turret_rotate_speed)
                self.gun_position_vector = self.position_vector + rotated_offset


            else:
                self.turret_rotate -= self.turret_rotate_speed
                self.turret_direction_vector.rotate_ip(self.turret_rotate_speed)

                offset = self.gun_position_vector - self.position_vector
                rotated_offset = offset.rotate(self.turret_rotate_speed)
                self.gun_position_vector = self.position_vector + rotated_offset



    def _turretRotateKeys(self):
        if 'K_LEFT' in self.events:
            self.turret_rotate += self.turret_rotate_speed
            self.turret_direction_vector.rotate_ip(-self.turret_rotate_speed)

            offset = self.gun_position_vector - self.position_vector
            rotated_offset = offset.rotate(-self.turret_rotate_speed)
            self.gun_position_vector = self.position_vector + rotated_offset


        if 'K_RIGHT' in self.events:
            self.turret_rotate -= self.turret_rotate_speed
            self.turret_direction_vector.rotate_ip(self.turret_rotate_speed)

            offset = self.gun_position_vector - self.position_vector
            rotated_offset = offset.rotate(self.turret_rotate_speed)
            self.gun_position_vector = self.position_vector + rotated_offset



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
                                                    tanks_list = self.tanks_list
            ))
            self.recharging_long_start = time()
            self.gun_position_vector -= self.turret_direction_vector * self.gun_animate_len
            self._soundEventLoad('Shoot', 1000)


        if abs(self.gun_position_vector.x - self.position_vector.x) > 1:
            self.gun_position_vector += self.turret_direction_vector * self.recharge_animate_long



    def _soundEventLoad(self, sound = '', max_distance = 0):
        for tank in self.tanks_list:
            distance = math.hypot(tank.x_coord - self.x_coord, tank.y_coord - self.y_coord)

            if distance < max_distance:
                volume = 1.0 - (distance / max_distance)
                self.event_sounds[tank.tank_id]['sounds_list'].append({'sound': sound, 'volume': volume})



    def _socketPlayerReceivingEvent(self):
        try:
            data = self.player_socket.recv(1024)

            if not data:
                return

            events = json.loads(data.decode().strip())

            self.events.extend(events['keys'])

            self.player_mouse_x_coord = events['mouse_x'] + self.x_coord
            self.player_mouse_y_coord = events['mouse_y'] + self.y_coord


        except BlockingIOError:
            pass # Данных в сокете пока нет, просто идем дальше, не ломая игру.


        except Exception as ex:
            print(ex)



    def tankUpdate(self):
        if self.health <= 0:
            return


        self._socketPlayerReceivingEvent()
        self._bodyMove()
        self._bodyRotate()
        self._hitboxesUpdate()
        self._bodyColideWalls()
        self._bodyColideTanks()
        self._controlMode()
        self._gunShoot()


        self.events.clear()



    def getData(self):
        return {
            'x_coord'      : self.x_coord,
            'y_coord'      : self.y_coord,
            'body_rotate'  : self.body_rotate,
            'turret_rotate': self.turret_rotate,
            'gun_x_coord': self.gun_position_vector.x,
            'gun_y_coord': self.gun_position_vector.y,
            'health' : self.health,
            'comand' : self.comand,
            'tank_id': self.tank_id
        }