import pygame

pygame.init()

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Masks")

# colors
BG = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# ---------------- SOLDIER ---------------- #
class Soldier:
    def __init__(self, x, y, color = BLACK):
        # базовая поверхность
        self.original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.original_image.fill(color)

        # текущая поверхность
        self.image = self.original_image

        # rect
        self.rect = self.image.get_rect(center=(x, y))

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # rotation
        self.angle = 0

    def rotate(self):
        center = self.rect.center

        # вращаем оригинальную картинку
        self.image = pygame.transform.rotate(
            self.original_image,
            self.angle
        )

        # новый rect
        self.rect = self.image.get_rect(center=center)

        # новая mask
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- BULLET ---------------- #
class Bullet:
    def __init__(self):
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, colour):
        pos = pygame.mouse.get_pos()

        self.rect.center = pos

        self.image.fill(colour)

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- DESIGNS ---------------- #
class Designs:
    def __init__(self, parts = tuple):
        self.forehead_rect = parts[0]
        self.center_rect = parts[1]
        self.karma_rect = parts[2]

        self.center_vector = pygame.Vector2(self.center_rect.rect.center)

        self.direction_vector1 = pygame.Vector2((-150, 0))
        self.direction_vector2 = pygame.Vector2((150, 0))


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.center_rect.angle += 2
            self.direction_vector1.rotate_ip(-2)
            self.direction_vector2.rotate_ip(-2)

        if keys[pygame.K_d]:
            self.center_rect.angle -= 2
            self.direction_vector1.rotate_ip(2)
            self.direction_vector2.rotate_ip(2)


        self.forehead_rect.angle = self.center_rect.angle
        self.karma_rect.angle = self.center_rect.angle

        forehead_rect_pos = self.center_vector + self.direction_vector1
        karma_rect_pos = self.center_vector + self.direction_vector2

        self.forehead_rect.rect.center = forehead_rect_pos
        self.karma_rect.rect.center = karma_rect_pos


        self.forehead_rect.rotate()
        self.forehead_rect.draw(screen)

        self.center_rect.rotate()
        self.center_rect.draw(screen)

        self.karma_rect.rotate()
        self.karma_rect.draw(screen)


# проверка mask collision
def mask_collision(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))


# hide mouse
pygame.mouse.set_visible(False)

# objects
soldier = Soldier(400, 300)

soldier1 = Soldier(100, 300, RED)
soldier2 = Soldier(400, 300, GREEN)
soldier3 = Soldier(700, 300, BLUE)

parts = (soldier1, soldier2, soldier3)
des = Designs(parts)

bullet = Bullet()

# game loop
run = True
clock = pygame.time.Clock()

while run:

    clock.tick(60)

    screen.fill(BG)

    # rotate
    # soldier.rotate()

    # collision
    if (mask_collision(bullet, des.center_rect)
    or mask_collision(bullet, des.forehead_rect)
    or mask_collision(bullet, des.karma_rect)):
        color = RED
    else:
        color = GREEN

    # update bullet
    bullet.update(color)
    des.update()

    # draw
    # soldier.draw(screen)
    bullet.draw(screen)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # keys
    # keys = pygame.key.get_pressed()
    #
    # if keys[pygame.K_a]:
    #     soldier.angle += 2
    #
    # if keys[pygame.K_d]:
    #     soldier.angle -= 2

    pygame.display.flip()

pygame.quit()