import pygame

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


            sendingData()

            # <delete>
            screen.fill((255, 255, 255))

            for tank in players:

                screen.blit(tank.center_hitbox['current_surface'], tank.center_hitbox['rect'])
                screen.blit(tank.forehead_hitbox['current_surface'], tank.forehead_hitbox['rect'])
                screen.blit(tank.karma_hitbox['current_surface'], tank.karma_hitbox['rect'])


            pygame.display.flip()
            # </delete>

            clock.tick(60)



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
                    control_mode='keys',
                    comand='green',
                    projectile_speed=1
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
                    projectile_speed=1
                )
        )