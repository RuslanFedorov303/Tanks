import pygame.display

from Classes import *


HOST = '0.0.0.0'
IP = 8081


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, IP))
server_socket.listen(5)



def sendingData():
    data_game = {'tanks': [], 'projectiles': []}


    for player in players:
        data_game['tanks'].append(
            player['tank'].getData()
        )


    for projectile in projectiles:
        data_game['projectiles'].append(
            projectile.getData()
        )


    for player in players:
        player['tank'].player_socket.send(
            json.dumps(
                data_game
            ).encode()
        )



def gameUpdate():
    global players, projectiles
    while True:
        try:
            for player in players:
                player['tank'].tankUpdate()


            for projectile in projectiles:
                projectile.projectileUpdate()

            sendingData()
            # <delete>



            screen.fill((255, 255, 255))


            for player in players:
                player['tank']._tankDraw(screen)

            for player in players:
                player['tank']._hitboxesUpdate()



            # </delete>
            pygame.display.flip()
            clock.tick(60)



        except Exception as ex:
            print(ex)



threading.Thread(target=gameUpdate,
                 daemon=True).start()



while True:
    player_socket, addr = server_socket.accept()
    players.append(
        {
            'tank': Tank(
                body_image=body_image,
                turret_image=turret_image,
                gun_image=gun_image,
                projectile_image=projectile_image,
                player_socket = player_socket,
                players=players, projectiles=projectiles,
                x_coord=400 + len(players) * 500, y_coord=500
            )
        }
    )