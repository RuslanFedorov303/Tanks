import pygame
from socket import *
import json
from Options2 import drawTanks, drawProjectiles, drawFons, drawDecorations, screen, screen_size



HOST = 'localhost'
IP = 8081


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))


# my_id = socket_player.recv(2048).decode().strip()
#
# my_id = json.loads(my_id)
#
# my_id = my_id['id']

my_id = json.loads(socket_player.recv(2048).decode().strip())['id']






while True:
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                events.append('MOUSELEFTKEY')

            elif event.button == 4:
                camera_scale += 5

            elif event.button == 5:
                camera_scale -= 5


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

        information_received = socket_player.recv(2048).decode().strip()

        information_received = json.loads(information_received)


        for data_player in information_received['tanks']:
            if data_player['tank_id'] == my_id:
                camera_offset = {'x_offset': data_player['x_coord'], 'y_offset': data_player['y_coord']}
                break


        drawFons(information_received['map']['fon_images'], camera_offset)
        drawProjectiles(information_received['projectiles'], camera_offset)
        drawTanks(information_received['tanks'], camera_offset, my_id)
        drawDecorations(information_received['map']['decorations_list'], camera_offset)

        # scaled_screen = pygame.transform.scale(screen, (camera_scale, camera_scale))
        # true_screen.blit(scaled_screen, (screen_size['width'] / 2, screen_size['height'] / 2))
        # true_screen.blit(scaled_screen, (screen_size['width'] / 2 + camera_offset['x_offset'],
        #                                  screen_size['height'] / 2 + camera_offset['y_offset']))


    except timeout:
        continue


    except Exception as ex:
        print(ex)



    pygame.display.flip()