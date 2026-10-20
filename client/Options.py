import pygame
from socket import *
import json


pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)


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
driving_channel = None
driving_volume = 0.0
other_engine_channels = {}
other_driving_channels = {}
other_engine_volumes = {}
other_driving_volumes = {}

sounds_name = [
    'Shoot1',
    'Shoot2',
    'Penetration1',
    'Penetration2',
    'NoPenetration1',
    'NoPenetration2',
    'Recharge2',
    'Recharge1',
    'Boom',
    'Kill',
    'Win',
    'Lose',
    'Driving',
    'Engine'
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
        channel = sounds[sound['sound']]
        if channel:
            channel.play()
            channel.set_volume(sound['volume'])


# =========================================================
# ЗВУКИ
# =========================================================


def updateEngineSound(engine_on, moving):
    global engine_channel, engine_volume
    global driving_channel, driving_volume

    if engine_channel is None:
        engine_channel = pygame.mixer.Channel(0)
    if driving_channel is None:
        driving_channel = pygame.mixer.Channel(1)

    if 'Engine' not in sounds or 'Driving' not in sounds:
        return

    engine_target = 0.12 if engine_on else 0.0
    engine_fade_speed = 0.015

    if not engine_channel.get_busy():
        engine_channel.play(sounds['Engine'], loops=-1)

    if engine_volume < engine_target:
        engine_volume = min(engine_target, engine_volume + engine_fade_speed)
    elif engine_volume > engine_target:
        engine_volume = max(engine_target, engine_volume - engine_fade_speed)
    engine_channel.set_volume(engine_volume)

    driving_target = 0.10 if (engine_on and moving) else 0.0
    driving_fade_speed = 0.03

    if not driving_channel.get_busy():
        driving_channel.play(sounds['Driving'], loops=-1)

    if driving_volume < driving_target:
        driving_volume = min(driving_target, driving_volume + driving_fade_speed)
    elif driving_volume > driving_target:
        driving_volume = max(0.0, driving_volume - driving_fade_speed)
    driving_channel.set_volume(driving_volume)




def updateOtherEngineSound(engine_volumes):
    global other_engine_channels, other_driving_channels
    global other_engine_volumes, other_driving_volumes

    if 'Engine' not in sounds or 'Driving' not in sounds:
        return

    fade_speed = 0.02

    for tank_id in engine_volumes:
        if tank_id not in other_engine_channels:
            channel_number = 2 + len(other_engine_channels) * 2
            other_engine_channels[tank_id] = pygame.mixer.Channel(channel_number)
            other_driving_channels[tank_id] = pygame.mixer.Channel(channel_number + 1)
            other_engine_volumes[tank_id] = 0.0
            other_driving_volumes[tank_id] = 0.0
            other_engine_channels[tank_id].play(sounds['Engine'], loops=-1)
            other_driving_channels[tank_id].play(sounds['Driving'], loops=-1)

    for tank_id in list(other_engine_channels):
        data = engine_volumes.get(tank_id, {'engine': 0.0, 'driving': 0.0})
        target_engine = data.get('engine', 0.0)
        target_driving = data.get('driving', 0.0)
        current_engine = other_engine_volumes[tank_id]
        current_driving = other_driving_volumes[tank_id]

        if current_engine < target_engine:
            current_engine = min(target_engine, current_engine + fade_speed)
        elif current_engine > target_engine:
            current_engine = max(target_engine, current_engine - fade_speed)

        if current_driving < target_driving:
            current_driving = min(target_driving, current_driving + fade_speed)
        elif current_driving > target_driving:
            current_driving = max(target_driving, current_driving - fade_speed)

        other_engine_volumes[tank_id] = current_engine
        other_driving_volumes[tank_id] = current_driving
        other_engine_channels[tank_id].set_volume(current_engine)
        other_driving_channels[tank_id].set_volume(current_driving)




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