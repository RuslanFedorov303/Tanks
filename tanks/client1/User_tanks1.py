import pygame

from Options1 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))


my_id = socket_player.recv(1024).decode().strip()

my_id = json.loads(my_id)

my_id = my_id['id']


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
                 'mouse_x': mouse_x,
                 'mouse_y': mouse_y}
            ).encode()
        )

        information_received = socket_player.recv(1024).decode().strip()

        information_received = json.loads(information_received)


        drawProjectiles(information_received['projectiles'],
            drawTanks(information_received['tanks'], my_id)
        )



    except Exception as ex:
        print(ex)



    pygame.display.flip()
    clock.tick(60)