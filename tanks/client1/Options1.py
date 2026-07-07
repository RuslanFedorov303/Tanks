import pygame
from socket import *
import json


HOST = 'localhost'
IP = 8081


screen_size = {'width': 1300, 'height': 1000}

camera_offset = {'x_offset': 0, 'y_offset': 0}
camera_scale = 2000

# screen = pygame.Surface((3000, 3000))
screen = pygame.display.set_mode((screen_size['width'], screen_size['height'])) # Создаем екран и время
clock = pygame.time.Clock()


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


# fon1_image = pygame.transform.scale(
#         pygame.image.load("Image/fon_1.png").convert_alpha(),
#         (100, 100))
#
# fon2_image = pygame.transform.scale(
#         pygame.image.load("Image/fon_2.png").convert_alpha(),
#         (100, 100))
#
# fon3_image = pygame.transform.scale(
#         pygame.image.load("Image/fon_3.png").convert_alpha(),
#         (100, 100))


fon1_image = pygame.image.load("Image/fon_1.png").convert_alpha()

fon2_image = pygame.image.load("Image/fon_2.png").convert_alpha()

fon3_image = pygame.image.load("Image/fon_3.png").convert_alpha()

buch1_image = pygame.image.load("Image/Bush.png").convert_alpha()

decorations = {'fon1': fon1_image, 'fon2': fon2_image, 'fon3': fon3_image, 'bush1': buch1_image}



def drawTanks(data_players, camera_offset, my_id):
    for data_player in data_players:
        if data_player['tank_id'] == my_id:
            x_coord = screen_size['width'] / 2
            y_coord = screen_size['height'] / 2

        else:
            x_coord = screen_size['width'] / 2 + (data_player['x_coord'] - camera_offset['x_offset'])
            y_coord = screen_size['height'] / 2 + (data_player['y_coord'] - camera_offset['y_offset'])


        rotated_body = pygame.transform.rotate(body_image, data_player['body_rotate'])
        body_rect = rotated_body.get_rect(center=(x_coord, y_coord))
        screen.blit(rotated_body, body_rect)



    for data_player in data_players:
        if data_player['tank_id'] == my_id:
            x_coord = screen_size['width'] / 2
            y_coord = screen_size['height'] / 2

        else:
            x_coord = screen_size['width'] / 2 + (data_player['x_coord'] - camera_offset['x_offset'])
            y_coord = screen_size['height'] / 2 + (data_player['y_coord'] - camera_offset['y_offset'])


        rotated_gun = pygame.transform.rotate(gun_image, data_player['turret_rotate'])
        gun_rect = rotated_gun.get_rect(center=(x_coord, y_coord))
        screen.blit(rotated_gun, gun_rect)

        rotated_turret = pygame.transform.rotate(turret_image, data_player['turret_rotate'])
        turret_rect = rotated_turret.get_rect(center=(x_coord, y_coord))
        screen.blit(rotated_turret, turret_rect)




def drawProjectiles(data_projectiles, camera_offset):
    for data_projectile in data_projectiles:
        rotated_projectile = pygame.transform.rotate(projectile_image, data_projectile['rotate'])
        rect_projectile = rotated_projectile.get_rect(center=(screen_size['width'] / 2 + (data_projectile['x_coord'] - camera_offset['x_offset']),
                                                              screen_size['height'] / 2 + (data_projectile['y_coord'] - camera_offset['y_offset'])))
        screen.blit(rotated_projectile, rect_projectile)



# def drawFons(fon_images, camera_offset):
#     for current_fon in fon_images:
#         scaled_fon = pygame.transform.scale(fons[current_fon['image']], (current_fon['width'], current_fon['height']))
#         rotated_fon = pygame.transform.rotate(scaled_fon, current_fon['rotate'])
#
#         rect_fon = rotated_fon.get_rect(
#             center=(screen_size['width'] / 2 + (current_fon['x_coord'] - camera_offset['x_offset']),
#                     screen_size['height'] / 2 + (current_fon['y_coord'] - camera_offset['y_offset'])))
#         screen.blit(rotated_fon, rect_fon)



def drawDecorations(dicorations_list, camera_offset):
    for current_decorate in dicorations_list:
        scaled_decorate = pygame.transform.scale(decorations[current_decorate['image']], (current_decorate['width'], current_decorate['height']))
        rotated_decorate = pygame.transform.rotate(scaled_decorate, current_decorate['rotate'])

        rect_decorate = rotated_decorate.get_rect(
            center=(screen_size['width'] / 2 + (current_decorate['x_coord'] - camera_offset['x_offset']),
                    screen_size['height'] / 2 + (current_decorate['y_coord'] - camera_offset['y_offset'])))
        screen.blit(rotated_decorate, rect_decorate)