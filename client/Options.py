import pygame
from socket import *
import json


pygame.init()
pygame.mixer.init()


HOST = 'localhost'
IP = 8081


screen_size = {
    'width': 1300,
    'height': 1000
}

camera_offset = {
    'x_offset': 0,
    'y_offset': 0
}

screen = pygame.display.set_mode(
    (screen_size['width'], screen_size['height'])
)


# =========================================================
# ЗАГРУЗКА ИЗОБРАЖЕНИЙ
# =========================================================

body_image = pygame.transform.scale(
    pygame.image.load(
        "Image/Tank_body.png"
    ).convert_alpha(),
    (600, 300)
)

turret_image = pygame.transform.scale(
    pygame.image.load(
        "Image/Tank_turret.png"
    ).convert_alpha(),
    (600, 300)
)

gun_image = pygame.transform.scale(
    pygame.image.load(
        "Image/Tank_gun.png"
    ).convert_alpha(),
    (600, 300)
)

projectile_image = pygame.transform.scale(
    pygame.image.load(
        "Image/Projectile.png"
    ).convert_alpha(),
    (600, 300)
)


# =========================================================
# КЭШИ
# =========================================================

body_rotate_cache = {}
turret_rotate_cache = {}
gun_rotate_cache = {}
projectile_rotate_cache = {}

decoration_cache = {}


# =========================================================
# ДАННЫЕ ДЛЯ ПЛАВНОГО ДВИЖЕНИЯ
# =========================================================

tank_render_positions = {}


# =========================================================
# ДЕКОРАЦИИ И ЗВУКИ
# =========================================================

decorations = {}
sounds = {}

engine_channel = None
engine_volume = 0.0
engine_target_volume = 0.0

sounds_name = [
    'Shoot1',
    'Shoot2',
    'Penetration1',
    'Penetration2',
    'NoPenetration1',
    'NoPenetration2',
    'Boom',
    'Kill',
    'Win',
    'Lose',
    'Driving'
]


# =========================================================
# ЗАГРУЗКА
# =========================================================

def loadImages(images_name):
    for img in images_name:
        decorations[img] = pygame.image.load(
            'Image/' + img + '.png'
        ).convert_alpha()


def loadSounds(sounds_name):
    for sound in sounds_name:
        sounds[sound] = pygame.mixer.Sound(
            'Sound/' + sound + '.mp3'
        )


def playSounds(sounds_list, sounds):
    for sound in sounds_list:
        channel = sounds[sound['sound']].play()
        channel.set_volume(sound['volume'])


# =========================================================
# ЗВУКИ
# =========================================================


def updateEngineSound(moving, turning):
    global engine_channel
    global engine_volume

    if engine_channel is None:
        engine_channel = pygame.mixer.Channel(0)

    if 'Driving' not in sounds:
        return

    # Громкость
    normal_volume = 0.1
    turning_volume = 0.08

    # Скорость изменения громкости
    fade_speed = 0.03

    # Выбираем целевую громкость
    if turning:
        target_volume = turning_volume

    elif moving:
        target_volume = normal_volume

    else:
        target_volume = 0.0

    # Запускаем двигатель один раз
    if not engine_channel.get_busy():
        engine_channel.play(
            sounds['Driving'],
            loops=-1
        )

    # Плавное увеличение
    if engine_volume < target_volume:
        engine_volume += fade_speed

        if engine_volume > target_volume:
            engine_volume = target_volume

    # Плавное уменьшение
    elif engine_volume > target_volume:
        engine_volume -= fade_speed

        if engine_volume < target_volume:
            engine_volume = target_volume

    engine_channel.set_volume(engine_volume)


# =========================================================
# ПОЛУЧЕНИЕ ПОВЁРНУТОГО ИЗОБРАЖЕНИЯ
# =========================================================

def getRotatedBody(angle):
    angle = int(angle) % 360

    if angle not in body_rotate_cache:
        body_rotate_cache[angle] = pygame.transform.rotate(
            body_image,
            angle
        )

    return body_rotate_cache[angle]


def getRotatedTurret(angle):
    angle = int(angle) % 360

    if angle not in turret_rotate_cache:
        turret_rotate_cache[angle] = pygame.transform.rotate(
            turret_image,
            angle
        )

    return turret_rotate_cache[angle]


def getRotatedGun(angle):
    angle = int(angle) % 360

    if angle not in gun_rotate_cache:
        gun_rotate_cache[angle] = pygame.transform.rotate(
            gun_image,
            angle
        )

    return gun_rotate_cache[angle]


def getRotatedProjectile(angle):
    angle = int(angle) % 360

    if angle not in projectile_rotate_cache:
        projectile_rotate_cache[angle] = pygame.transform.rotate(
            projectile_image,
            angle
        )

    return projectile_rotate_cache[angle]


# =========================================================
# ТАНКИ
# =========================================================

def drawTanks(data_players, camera_offset, my_id):

    # Чем меньше число — тем плавнее,
    # но тем больше задержка.
    smooth = 0.2

    current_ids = set()

    for data_player in data_players:

        tank_id = data_player['tank_id']
        current_ids.add(tank_id)

        server_x = data_player['x_coord']
        server_y = data_player['y_coord']

        # ---------------------------------------------
        # Создаём постоянную позицию отрисовки
        # ---------------------------------------------

        if tank_id not in tank_render_positions:

            tank_render_positions[tank_id] = {
                'x': server_x,
                'y': server_y
            }

        render_position = tank_render_positions[tank_id]

        # ---------------------------------------------
        # Интерполяция
        # ---------------------------------------------

        render_position['x'] += (
            server_x - render_position['x']
        ) * smooth

        render_position['y'] += (
            server_y - render_position['y']
        ) * smooth

        render_x = render_position['x']
        render_y = render_position['y']

        # ---------------------------------------------
        # Позиция на экране
        # ---------------------------------------------

        if tank_id == my_id:

            x_coord = screen_size['width'] / 2
            y_coord = screen_size['height'] / 2

        else:

            x_coord = (
                screen_size['width'] / 2
                + render_x
                - camera_offset['x_offset']
            )

            y_coord = (
                screen_size['height'] / 2
                + render_y
                - camera_offset['y_offset']
            )

        # ---------------------------------------------
        # Корпус
        # ---------------------------------------------

        rotated_body = getRotatedBody(
            data_player['body_rotate']
        )

        body_rect = rotated_body.get_rect(
            center=(x_coord, y_coord)
        )

        screen.blit(
            rotated_body,
            body_rect
        )

        # ---------------------------------------------
        # Башня и пушка
        # ---------------------------------------------

        if data_player['health'] > 0:

            gun_offset_x = (
                data_player['gun_x_coord']
                - data_player['x_coord']
            )

            gun_offset_y = (
                data_player['gun_y_coord']
                - data_player['y_coord']
            )

            gun_x = x_coord + gun_offset_x
            gun_y = y_coord + gun_offset_y

            # Пушка

            rotated_gun = getRotatedGun(
                data_player['turret_rotate']
            )

            gun_rect = rotated_gun.get_rect(
                center=(gun_x, gun_y)
            )

            screen.blit(
                rotated_gun,
                gun_rect
            )

            # Башня

            rotated_turret = getRotatedTurret(
                data_player['turret_rotate']
            )

            turret_rect = rotated_turret.get_rect(
                center=(x_coord, y_coord)
            )

            screen.blit(
                rotated_turret,
                turret_rect
            )

    # ---------------------------------------------
    # Удаляем старые танки
    # ---------------------------------------------

    old_ids = set(tank_render_positions.keys()) - current_ids

    for tank_id in old_ids:
        del tank_render_positions[tank_id]


# =========================================================
# СНАРЯДЫ
# =========================================================

def drawProjectiles(data_projectiles, camera_offset):

    for data_projectile in data_projectiles:

        rotated_projectile = getRotatedProjectile(
            data_projectile['rotate']
        )

        x = (
            screen_size['width'] / 2
            + data_projectile['x_coord']
            - camera_offset['x_offset']
        )

        y = (
            screen_size['height'] / 2
            + data_projectile['y_coord']
            - camera_offset['y_offset']
        )

        rect_projectile = rotated_projectile.get_rect(
            center=(x, y)
        )

        screen.blit(
            rotated_projectile,
            rect_projectile
        )


# =========================================================
# ДЕКОРАЦИИ
# =========================================================

def drawDecorations(dicorations_list, camera_offset):

    for current_decorate in dicorations_list:

        image_name = current_decorate['image']

        width = current_decorate['width']
        height = current_decorate['height']

        rotate = int(current_decorate['rotate']) % 360

        # Уникальный ключ для кэша
        cache_key = (
            image_name,
            width,
            height,
            rotate
        )

        if cache_key not in decoration_cache:

            scaled_image = pygame.transform.scale(
                decorations[image_name],
                (width, height)
            )

            decoration_cache[cache_key] = (
                pygame.transform.rotate(
                    scaled_image,
                    rotate
                )
            )

        rotated_decorate = decoration_cache[cache_key]

        x = (
            screen_size['width'] / 2
            + current_decorate['x_coord']
            - camera_offset['x_offset']
        )

        y = (
            screen_size['height'] / 2
            + current_decorate['y_coord']
            - camera_offset['y_offset']
        )

        rect_decorate = rotated_decorate.get_rect(
            center=(x, y)
        )

        screen.blit(
            rotated_decorate,
            rect_decorate
        )