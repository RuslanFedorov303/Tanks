# ----- !----- !-- Импортируем --! -----! ----- #
import pygame
from socket import *
import threading
import json
import os
from random import randint #, choice
# from time import time, sleep

from Tank import Tank
from Wall import Wall




# ----- !----- !-- Создаем - инициализируем --! -----! ----- #
# ----- !-- Настройки хоста --! ----- #
HOST = 'localhost'
IP = 8081
# ----- !-----! ----- #



pygame.init() # Инициализируем pygame
clock = pygame.time.Clock()




players = [] # Список танков
green_comand = []
red_comand = []
projectiles = [] # Список снарядов
walls = []
random_nickname = ['MadKing94', 'CyberGhost12', 'ToxicKing26', 'NeonTiger35', 'SwiftGhost15', 'CyberBlaze32', 'SuperStorm73', 'MegaSnake49', 'IronDragon46', 'SilentTiger98', 'CyberShadow79', 'CoolWolf76', 'WildHunter81', 'SwiftShadow19', 'ToxicHunter53', 'ShadowStorm38', 'ShadowFalcon43', 'DarkEagle99', 'SilentHunter52', 'CyberTiger40', 'FrostRaven64', 'NeonBlaze35', 'IronDragon62', 'WildShadow59', 'SilentGhost66', 'IronDragon56', 'IronTiger45', 'ShadowWolf35', 'DarkStorm32', 'MegaSnake96']



server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, IP))
server_socket.listen(5)




def sendingData():
    data_game = {'tanks': [], 'projectiles': []}


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
            clock.tick(10)



        except Exception as ex:
            print(ex)




current_map = "Зідьки.json"
with open('Maps/' + current_map, 'r') as map_data:
    map_data = json.load(map_data)

for d in map_data['walls']:
    walls.append(Wall(d['x_coord'], d['y_coord'], d['width'], d['height'], d['rotate']))

threading.Thread(target=gameUpdate,
                 daemon=True).start()




while True:
    player_socket, addr = server_socket.accept()
    if len(players) % 2 == 0:
        players.append(
                Tank(
                    player_socket = player_socket,
                    projectiles_list=projectiles, tanks_list=players, walls_list=walls,
                    x_coord = map_data['appearance']['green'][len(green_comand) - 1]['x'],
                    y_coord = map_data['appearance']['green'][len(green_comand) - 1]['y'],
                    control_mode='mouse',
                    comand='green',
                    tank_id=len(players),
                    turret_rotate_speed=15,
                    forward_speed=15,
                    backward_speed=15,
                    body_rotate_speed=5
                )
        )
        green_comand.append(players[-1])


    else:
        players.append(
                Tank(
                    player_socket=player_socket,
                    projectiles_list=projectiles, tanks_list=players,
                    x_coord = map_data['appearance']['red'][len(red_comand) - 1]['x'],
                    y_coord = map_data['appearance']['red'][len(red_comand) - 1]['y'],
                    control_mode='keys',
                    comand='red',
                    tank_id=len(players)
                )
        )
        red_comand.append(players[-1])



    player_socket.send(
        json.dumps(
            {'my_id': players[-1].tank_id, 'map_data': map_data}
        ).encode()
    )