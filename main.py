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
hold_1 = pygame.Rect(350,400,100,15)
hold_2 = pygame.Rect(350,300,100,15)
hold_3 = pygame.Rect(350,200,100,15)
hold_4 = pygame.Rect(350,100,100,15)
holds = [hold_1,hold_2,hold_3,hold_4]

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
    player.check_hold_edge(holds)

    pygame.draw.line(screen, 'black', (0,ground_y), (width, ground_y), 3)
    for hold in holds:
        pygame.draw.rect(screen,'yellow',hold)
    player.check_collision(holds)
 
    player.draw(screen)
    player.update(dt, ground_y)
    pygame.display.update()

pygame.quit()
sys.exit()