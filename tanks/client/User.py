import pygame
from socket import *
import json
from Options import loadImages, loadSounds, playSounds, drawTanks, drawProjectiles, drawDecorations, \
                     screen, screen_size, sounds_name, sounds

pygame.mixer.init()



HOST = 'localhost'
IP = 8081


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))


data_for_game = json.loads(socket_player.recv(2048).decode().strip())


my_id = data_for_game['my_id']
map_data = data_for_game['map_data']
use_images = data_for_game['use_images']


loadImages(use_images)
loadSounds(sounds_name)


events = []
pygame.mixer_music.load('Sound/Shoot.mp3')
while True:
    events.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                events.append('MOUSELEFTKEY')
                pygame.mixer_music.play()

    screen.fill((255, 255, 255))



    try:
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if keys[pygame.K_w]: events.append('K_w')
        if keys[pygame.K_s]: events.append('K_s')
        if keys[pygame.K_a]: events.append('K_a')
        if keys[pygame.K_d]: events.append('K_d')

        if keys[pygame.K_LEFT]: events.append('K_LEFT')
        if keys[pygame.K_RIGHT]: events.append('K_RIGHT')

        if keys[pygame.K_UP]: events.append('K_UP')

        socket_player.send(
            json.dumps(
                {'keys': events,
                 'mouse_x': mouse_x - screen_size['width'] // 2,
                 'mouse_y': mouse_y - screen_size['height'] // 2}
            ).encode()
        )



        information_received, sounds_list = json.loads(socket_player.recv(2048).decode().strip())

        for data_player in information_received['tanks']:
            if data_player['tank_id'] == my_id:
                camera_offset = {'x_offset': data_player['x_coord'], 'y_offset': data_player['y_coord']}
                break


        playSounds(sounds_list)


        drawDecorations(map_data['backgrounds'], camera_offset)
        drawDecorations(map_data['down_decorations'], camera_offset)

        drawTanks(information_received['tanks'], camera_offset, my_id)
        drawProjectiles(information_received['projectiles'], camera_offset)

        drawDecorations(map_data['up_decorations'], camera_offset)
        drawDecorations(map_data['walls'], camera_offset)



    except timeout:
        continue


    except Exception as ex:
        print(ex)



    pygame.display.flip()