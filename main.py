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

running = True
while running:
    screen.fill('green')
    dt = clock.tick(120) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.move(keys, dt)

    pygame.draw.line(screen, 'black', (0,ground_y), (width, ground_y), 3)
        
    player.draw(screen)
    player.update(dt, ground_y)
    pygame.display.update()

pygame.quit()
sys.exit()