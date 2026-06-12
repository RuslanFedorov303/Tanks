import pygame
from socket import *
import json


HOST = 'localhost'
IP = 8081


screen_size = {'width': 1300, 'height': 1000}

screen = pygame.display.set_mode((1300, 1000)) # Создаем екран и время
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



def drawTanks(data_players, my_id):
    for data_player in data_players:
        if data_player['tank_id'] == my_id:
            camera_offset = {'x_offset': data_player['x_coord'], 'y_offset': data_player['y_coord']}
            break


    for data_player in data_players:
        if data_player['tank_id'] == my_id:
            rotated_body = pygame.transform.rotate(body_image, data_player['body_rotate'])
            body_rect = rotated_body.get_rect(center=(screen_size['width'] // 2,
                                                      screen_size['height'] // 2))
            screen.blit(rotated_body, body_rect)

        else:
            rotated_body = pygame.transform.rotate(body_image, data_player['body_rotate'])
            body_rect = rotated_body.get_rect(center=(screen_size['width'] // 2 + (data_player['x_coord'] - camera_offset['x_offset']),
                                                      screen_size['height'] // 2 + (data_player['y_coord'] - camera_offset['y_offset'])))
            screen.blit(rotated_body, body_rect)


    for data_player in data_players:
        if data_player['tank_id'] == my_id:
            rotated_gun = pygame.transform.rotate(gun_image, data_player['turret_rotate'])
            gun_rect = rotated_gun.get_rect(center=(screen_size['width'] // 2,
                                                    screen_size['height'] // 2))
            screen.blit(rotated_gun, gun_rect)

            rotated_turret = pygame.transform.rotate(turret_image, data_player['turret_rotate'])
            turret_rect = rotated_turret.get_rect(center=(screen_size['width'] // 2,
                                                          screen_size['height'] // 2))
            screen.blit(rotated_turret, turret_rect)

        else:
            rotated_gun = pygame.transform.rotate(gun_image, data_player['turret_rotate'])
            gun_rect = rotated_gun.get_rect(center=(screen_size['width'] // 2 + (data_player['x_coord'] - camera_offset['x_offset']),
                                                    screen_size['height'] // 2 + (data_player['y_coord'] - camera_offset['y_offset'])))
            screen.blit(rotated_gun, gun_rect)

            rotated_turret = pygame.transform.rotate(turret_image, data_player['turret_rotate'])
            turret_rect = rotated_turret.get_rect(center=(screen_size['width'] // 2 + (data_player['x_coord'] - camera_offset['x_offset']),
                                                          screen_size['height'] // 2 + (data_player['y_coord'] - camera_offset['y_offset'])))
            screen.blit(rotated_turret, turret_rect)


    return camera_offset




def drawProjectiles(data_projectiles, camera_offset):
    for data_projectile in data_projectiles:
        rotated_projectile = pygame.transform.rotate(projectile_image, data_projectile['rotate'])
        body_projectile = rotated_projectile.get_rect(center=(screen_size['width'] // 2 + (data_projectile['x_coord'] - camera_offset['x_offset']),
                                                              screen_size['height'] // 2 + (data_projectile['y_coord'] - camera_offset['y_offset'])))
        screen.blit(rotated_projectile, body_projectile)