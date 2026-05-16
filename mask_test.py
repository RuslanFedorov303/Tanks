import pygame

pygame.init()

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Masks")

# colors
BG = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# ---------------- SOLDIER ---------------- #
class Soldier:
    def __init__(self, x, y):
        # базовая поверхность
        self.original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.original_image.fill(BLUE)

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


# проверка mask collision
def mask_collision(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))


# hide mouse
pygame.mouse.set_visible(False)

# objects
soldier = Soldier(400, 300)
bullet = Bullet()

# game loop
run = True
clock = pygame.time.Clock()

while run:

    clock.tick(60)

    screen.fill(BG)

    # rotate
    soldier.rotate()

    # collision
    if mask_collision(bullet, soldier):
        color = RED
    else:
        color = GREEN

    # update bullet
    bullet.update(color)

    # draw
    soldier.draw(screen)
    bullet.draw(screen)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        soldier.angle += 2

    if keys[pygame.K_RIGHT]:
        soldier.angle -= 2

    pygame.display.flip()

pygame.quit()