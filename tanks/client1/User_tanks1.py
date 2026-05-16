from Options1 import *


socket_player = socket(AF_INET, SOCK_STREAM)
socket_player.connect((HOST, IP))



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

        if keys[pygame.K_UP]: events.append('K_UP')

        socket_player.send(
            json.dumps(
                (events, mouse_x, mouse_y)
            ).encode()
        )

        information_received = socket_player.recv(1024).decode().strip()

        information_received = json.loads(information_received)

        print(information_received)

        drawTanks(information_received['tanks'])
        drawProjectiles(information_received['projectiles'])



    except Exception as ex:
        print(ex)



    pygame.display.flip()
    clock.tick(60)