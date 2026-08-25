import math
import random
import time
import pygame

# 1. Инициализация звукового движка Pygame
pygame.mixer.init()

# 2. Загрузка короткого звука (например, взрыв, клик или шаг)
# Эффект воспроизведется ровно один раз и сам остановится
event_sound = pygame.mixer.Sound("explosion.wav")

# Настройки игрового мира
MAX_DISTANCE = 500.0  # Дистанция полной тишины
PLAYER_POS = (400, 300)  # Игрок стоит неподвижно в центре экрана


def play_event_sound(object_pos):
    """Рассчитывает громкость и панораму, затем воспроизводит звук один раз"""

    # Вычисляем расстояние между игроком и объектом по формуле Пифагора
    distance = math.hypot(object_pos[0] - PLAYER_POS[0], object_pos[1] - PLAYER_POS[1])

    # Если объект слишком далеко, звук вообще не имеет смысла включать
    if distance >= MAX_DISTANCE:
        print(f"Событие в {object_pos} произошло слишком далеко ({int(distance)}px). Звук пропущен.")
        return

    # 1. Общая громкость от расстояния (от 1.0 до 0.0)
    volume = 1.0 - (distance / MAX_DISTANCE)

    # 2. Баланс лево/право (панорама)
    # Определяем, где объект относительно игрока по горизонтали
    # От -1.0 (максимально слева) до +1.0 (максимально справа)
    dx = object_pos[0] - PLAYER_POS[0]
    pan = dx / MAX_DISTANCE
    pan = max(-1.0, min(1.0, pan))  # Ограничиваем рамками

    # Раскладываем общую громкость на левое и правое ухо
    left_ear = volume * max(0.0, 1.0 - pan)
    right_ear = volume * max(0.0, 1.0 + pan)

    # 3. Находим свободный звуковой канал и воспроизводим звук
    # Pygame сам выберет свободный канал, чтобы звуки могли накладываться друг на друга
    channel = event_sound.play()

    if channel:  # Если канал успешно выделился
        channel.set_volume(left_ear, right_ear)
        print(
            f"БУМ! Сработало событие в {object_pos}. Дистанция: {int(distance)}px. Громкость Л/П: {left_ear:.2f}/{right_ear:.2f}")


# --- Симуляция случайных событий ---
print("Игрок в центре (400, 300). Каждые 1.5 секунды где-то на карте что-то происходит:")

for i in range(5):
    # Генерируем случайную точку взрыва/события на карте
    random_x = random.randint(0, 800)
    random_y = random.randint(0, 600)
    event_position = (random_x, random_y)

    # Вызываем функцию звука ТОЛЬКО в момент события
    play_event_sound(event_position)

    # Ждем полторы секунды до следующего события
    time.sleep(1.5)

print("Симуляция завершена.")