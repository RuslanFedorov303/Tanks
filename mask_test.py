import pygame

# будущие хитбокси

pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()


pygame.mouse.set_visible(False)
mouse_surf = pygame.Surface((10, 10))
mouse_surf.fill((255, 0, 0))
mouse_mask = pygame.mask.from_surface(mouse_surf)


surf = pygame.Surface((100, 100))
surf_rect = surf.get_rect()
mask = pygame.mask.from_surface(surf)

surf_forehead = pygame.Surface((100, 100))
surf_forehead_rect = surf.get_rect()
forehead_mask = pygame.mask.from_surface(surf_forehead)

surf_center = pygame.Surface((100, 100))
surf_center_rect = surf.get_rect()
center_mask = pygame.mask.from_surface(surf_center)

surf_karma = pygame.Surface((100, 100))
surf_karma_rect = surf.get_rect()
karma_mask = pygame.mask.from_surface(surf_karma)

surfs = ({'surf': surf_forehead, 'rect': surf_forehead_rect, 'mask': forehead_mask, 'x': 100, 'y': 100},
         {'surf': surf_center, 'rect': surf_center_rect, 'mask': center_mask, 'x': 250, 'y': 100},
         {'surf': surf_karma, 'rect': surf_karma_rect, 'mask': karma_mask, 'x': 400, 'y': 100})
masks = (forehead_mask, center_mask, karma_mask)

rotate = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pos = pygame.mouse.get_pos()


    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        rotate += 1
    if keys[pygame.K_RIGHT]:
        rotate -= 1

    if rotate == 360 or rotate == -360:
        rotate = 0

    for surf in surfs:
        rotated_surf = pygame.transform.rotate(surf['surf'], rotate)
        l = pygame.mask.from_surface(rotated_surf)

        new_rect = rotated_surf.get_rect(center=(surf['x'] + 50, surf['y'] + 50))

        screen.blit(rotated_surf, (surf['x'], surf['y']), new_rect)
        if mouse_mask.overlap('mask', (surf['x'] - pos[0], surf['y'] - pos[1])):
            mouse_surf.fill((0, 255, 0))

    print(rotate)

    screen.blit(mouse_surf, pos)
    mouse_surf.fill((255, 0, 0))

    clock.tick(60)
    pygame.display.flip()