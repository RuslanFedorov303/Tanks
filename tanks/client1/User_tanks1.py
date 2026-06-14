import pygame

from Options1 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))


my_id = socket_player.recv(1024).decode().strip()

my_id = json.loads(my_id)

my_id = my_id['id']


camera_offset = {'x_offset': 0, 'y_offset': 0}


while True:
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            events.append('MOUSEBUTTONDOWN')


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

        if keys[pygame.K_SLASH]: events.append('K_SLASH')

        socket_player.send(
            json.dumps(
                {'keys': events,
                 'mouse_x': mouse_x - screen_size['width'] // 2,
                 'mouse_y': mouse_y - screen_size['height'] // 2}
            ).encode()
        )

        information_received = socket_player.recv(1024).decode().strip()

        information_received = json.loads(information_received)



        drawFons(information_received['map']['fon_images'], camera_offset)
        drawProjectiles(information_received['projectiles'], camera_offset)
        camera_offset = drawTanks(information_received['tanks'], my_id)
        drawDecorations(information_received['map']['decorations_list'], camera_offset)


    except Exception as ex:
        print(ex)



    pygame.display.flip()
    clock.tick(20)