# ----- !----- !-- Импортируем --! -----! ----- #
import pygame
from socket import *
import threading
import json
from random import randint #, choice
# from time import time, sleep

from Tank import Tank
from Map import Map




# ----- !----- !-- Создаем - инициализируем --! -----! ----- #
# ----- !-- Настройки хоста --! ----- #
HOST = 'localhost'
IP = 8081
# ----- !-----! ----- #


pygame.init() # Инициализируем pygame


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



projectiles = [] # Список снарядов
players = [] # Список танков
random_nickname = ['MadKing94', 'CyberGhost12', 'ToxicKing26', 'NeonTiger35', 'SwiftGhost15', 'CyberBlaze32', 'SuperStorm73', 'MegaSnake49', 'IronDragon46', 'SilentTiger98', 'CyberShadow79', 'CoolWolf76', 'WildHunter81', 'SwiftShadow19', 'ToxicHunter53', 'ShadowStorm38', 'ShadowFalcon43', 'DarkEagle99', 'SilentHunter52', 'CyberTiger40', 'FrostRaven64', 'NeonBlaze35', 'IronDragon62', 'WildShadow59', 'SilentGhost66', 'IronDragon56', 'IronTiger45', 'ShadowWolf35', 'DarkStorm32', 'MegaSnake96']



current_map = Map(
    fon_images = (
        {'image': 'fon1', 'x_coord': 0 / 1.5, 'y_coord': 0, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5},
        {'image': 'fon3', 'x_coord': 1600 / 1.5 - 2, 'y_coord': 0, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5},
        {'image': 'fon2', 'x_coord': 3200 / 1.5 - 4, 'y_coord': 0, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5},
        {'image': 'fon1', 'x_coord': 0 / 1.5, 'y_coord': 900 / 1.5 - 2, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5},
        # {'image': 'fon1', 'x_coord': 1600 / 1.5 - 2, 'y_coord':  900 / 1.5 - 2, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5},
        # {'image': 'fon3', 'x_coord': 3200 / 1.5 - 4, 'y_coord':  900 / 1.5 - 2, 'rotate': 0, 'width': 1600 / 1.5, 'height': 900 / 1.5}
    ),
    decorations_list = (
        {'image': 'bush1', 'x_coord': 200, 'y_coord': 200, 'rotate': 0, 'width': 200, 'height': 200},
        {'image': 'bush1', 'x_coord': 300, 'y_coord': 250, 'rotate': 40, 'width': 230, 'height': 230}
    ),
    walls_list = (

    )
)





server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, IP))
server_socket.listen(5)




def sendingData():
    data_game = {'tanks': [],
                 'projectiles': [],
                 'map': current_map.getData()}


    for player in players:
        data_game['tanks'].append(
            player.getData()
        )


    for projectile in projectiles:
        data_game['projectiles'].append(
            projectile.getData()
        )


    for player in players:
        player.player_socket.send(
            json.dumps(
                data_game
            ).encode()
        )



def gameUpdate():
    global players, projectiles
    while True:
        try:
            for player in players:
                player.tankUpdate()


            for projectile in projectiles:
                if projectile.colide:
                    projectiles.remove(projectile)
                else:
                    projectile.projectileUpdate()

            threading.Thread(target=sendingData,
                             daemon=True).start()
            # sendingData()
            # pygame.display.flip()
            clock.tick(10)



        except Exception as ex:
            print(ex)



threading.Thread(target=gameUpdate,
                 daemon=True).start()



while True:
    player_socket, addr = server_socket.accept()
    if len(players) % 2 == 0:
        players.append(
                Tank(
                    body_image=body_image,
                    turret_image=turret_image,
                    gun_image=gun_image,
                    projectile_image=projectile_image,
                    player_socket = player_socket,
                    projectiles_list=projectiles, tanks_list=players,
                    x_coord=400 + len(players) * 500, y_coord=500,
                    control_mode='mouse',
                    comand='green',
                    tank_id=len(players),
                    turret_rotate_speed=15,
                    forward_speed=15,
                    backward_speed=15,
                    body_rotate_speed=5
                )
        )
    else:
        players.append(
                Tank(
                    body_image=body_image,
                    turret_image=turret_image,
                    gun_image=gun_image,
                    projectile_image=projectile_image,
                    player_socket=player_socket,
                    projectiles_list=projectiles, tanks_list=players,
                    x_coord=400 + len(players) * 500, y_coord=500,
                    control_mode='keys',
                    comand='red',
                    tank_id=len(players)
                    # forward_speed=15,
                    # backward_speed=15,
                    # body_rotate_speed=5
                )
        )
    player_socket.send(
        json.dumps(
            {'id': players[-1].tank_id}
        ).encode()
    )