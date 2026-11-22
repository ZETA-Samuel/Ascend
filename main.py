import pygame
import sys
from player import Player
from camera import Camera

pygame.init()
pygame.font.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Ascend')
clock = pygame.time.Clock()

camera = Camera(width, height)

player = Player()
ground_y = 550
hold_1 = pygame.Rect(350,400,100,15)
hold_2 = pygame.Rect(350,300,100,15)
hold_3 = pygame.Rect(350,200,100,15)
hold_4 = pygame.Rect(350,100,100,15)
hold_5 = pygame.Rect(100,00,100,15)
hold_6 = pygame.Rect(400,-100,100,15)
hold_7 = pygame.Rect(700,-200,100,15)
hold_8 = pygame.Rect(400,-300,100,15)
hold_9 = pygame.Rect(100,-400,100,15)
hold_10 = pygame.Rect(350,-500,100,15)
holds = [hold_1,hold_2,hold_3,hold_4,hold_5,hold_6,hold_7,hold_8,hold_9,hold_10]

# Text
title_font = pygame.font.Font(None, 24)
game_over = title_font.render('Game Over',False,(0,0,0))


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

    player.check_collision(holds)

    player.update(dt, ground_y)
    camera.update(player, dt)

    ground_screen_y = ground_y + camera.offset_y
    pygame.draw.line(screen, 'black',(0, round(ground_screen_y)),(width, round(ground_screen_y)), 3)
    for hold in holds:
        pygame.draw.rect(screen,'yellow',camera.apply(hold))
         
    player.draw(screen, camera)
    screen.blit(game_over, (350,0))
    pygame.display.update()

pygame.quit()
sys.exit()