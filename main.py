import pygame
import sys
from player import Player

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Ascend')
clock = pygame.time.Clock()

player = Player()
ground_y = 550
hold = pygame.Rect(350,400,100,15)

running = True
while running:
    screen.fill('green')
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.release_hold()

    keys = pygame.key.get_pressed()

    player.move(keys, dt)

    pygame.draw.line(screen, 'black', (0,ground_y), (width, ground_y), 3)
    pygame.draw.rect(screen,'yellow',hold)
    player.check_collision(hold)
    player.draw(screen)
    player.update(dt, ground_y)
    pygame.display.update()

pygame.quit()
sys.exit()