import asyncio
import pygame
from player import Player
from camera import Camera


async def main():
    pygame.init()
    pygame.font.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ascend')
    clock = pygame.time.Clock()

    background = pygame.image.load('assets/background.jpg').convert_alpha()
    background = pygame.transform.scale(background,(width,height))

    camera = Camera(width, height)

    player = Player()
    ground_y = 550
    bars = [
    pygame.Rect(350, 400, 100, 15),
    pygame.Rect(150, 300, 100, 15),
    pygame.Rect(400, 200, 100, 15),
    pygame.Rect(250, 100, 100, 15),
    pygame.Rect(25, 0, 100, 15),
    pygame.Rect(400, -100, 100, 15),
    pygame.Rect(650, -200, 100, 15),
    pygame.Rect(350, -300, 100, 15),
    pygame.Rect(100, -400, 100, 15),
    pygame.Rect(450, -500, 100, 15),
    pygame.Rect(600, -600, 100, 15),
    pygame.Rect(300, -700, 100, 15),
    pygame.Rect(50, -800, 100, 15),
    pygame.Rect(400, -900, 100, 15),
    pygame.Rect(650, -1000, 100, 15),
    pygame.Rect(350, -1100, 100, 15),
    pygame.Rect(100, -1200, 100, 15),
    pygame.Rect(400, -1300, 100, 15),
    pygame.Rect(200, -1400, 100, 15),
    pygame.Rect(500, -1500, 100, 15),
    ]

    platforms = [
        pygame.Rect(550, 500, 200, 15),
        pygame.Rect(150, 50, 150, 15),
        pygame.Rect(450, -350, 150, 15),
        pygame.Rect(50, -850, 180, 15),
        pygame.Rect(450, -1350, 180, 15),
        pygame.Rect(350, -1550, 100, 15),
    ]

    end_rect = pygame.Rect(350,-1500,width,50)

    game_state = "menu"

    title_font = pygame.font.SysFont('Arial', 128)
    help_font = pygame.font.SysFont('Verdana', 32)
    end_font = pygame.font.SysFont('Arial', 64)

    title = title_font.render('ASCEND', True, (0, 0, 0))
    clue = help_font.render("Press 'ENTER' to continue", False, (0, 0, 0))
    help = end_font.render("How to Play?", True,(255,0,0))
    play_1 = help_font.render("A/D to move around",False,(0,0,0))
    play_2 = help_font.render("SPACE to jump",False,(0,0,0))
    play_3 = help_font.render("Yellow are bars = hang", False,(0,0,0))
    play_4 = help_font.render("Green are platforms = stand", False,(0,0,0))

    title_rect = title.get_rect(center=(width * 0.5, height * 0.4))
    clue_rect = clue.get_rect(center=(width * 0.5, height * 0.6))
    clue_rect_2 = clue.get_rect(center=(width * 0.5, height * 0.8))
    help_rect = help.get_rect(center=(width*0.5,height*0.2))
    play_1_rect = play_1.get_rect(center=(width*0.5,height*0.4))
    play_2_rect = play_2.get_rect(center=(width*0.5,height*0.5))
    play_3_rect = play_3.get_rect(center=(width*0.5,height*0.6))
    play_4_rect = play_4.get_rect(center=(width*0.5,height*0.7))


    game_end = end_font.render("Congrats! You finished the game", True, (0,0,0))
    game_end_rect = game_end.get_rect(center=(width * 0.5, height * 0.4))

    running = True
    while running:
        dt = min(clock.tick(60) / 1000, 1 / 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.release_hold()
                if event.key == pygame.K_RETURN and game_state == 'menu':
                    game_state = "how_to"
                elif event.key == pygame.K_RETURN and game_state == 'how_to':
                    game_state = 'playing'
                elif event.key == pygame.K_RETURN and game_state == 'end':
                    game_state = 'playing'

        keys = pygame.key.get_pressed()

        if game_state == "menu":
            screen.fill('purple')
            screen.blit(title, title_rect)
            screen.blit(clue, clue_rect)

        elif game_state == "how_to":
            screen.fill('white')
            screen.blit(help,help_rect)
            screen.blit(play_1,play_1_rect)
            screen.blit(play_2,play_2_rect)
            screen.blit(play_3,play_3_rect)
            screen.blit(play_4,play_4_rect)
            screen.blit(clue, clue_rect_2)

        elif game_state == "playing":
            screen.blit(background)
            player.move(keys, dt)
            player.update(dt, ground_y)
            player.check_platform_collision(platforms)
            player.check_bar_collision(bars)

            player.update_animations(dt)

            player.check_hold_edge()

            camera.update(player, dt)

            ground_screen_y = ground_y + camera.offset_y
            pygame.draw.line(
                screen,
                'black',
                (0, round(ground_screen_y)),
                (width, round(ground_screen_y)),
                3,
            )
            for platform in platforms:
                pygame.draw.rect(screen, 'green', camera.apply(platform))

            for bar in bars:
                pygame.draw.rect(screen, 'yellow', camera.apply(bar))

            player.draw(screen, camera)

            if player.rect.colliderect(end_rect):
                pygame.time.wait(500)
                game_state = "end"

        elif game_state == "end":
            player.rect = pygame.Rect(0,33, player.width,player.height)
            player.pos = pygame.Vector2(player.rect.topleft)
            player.holding = False
            player.holding_bar = None
            player.locked_bar = None
            player.grab_locked = False
            player.velocity_x = 0
            player.velocity_y = 0
            player.on_ground = False
            screen.fill('pink')
            screen.blit(game_end, game_end_rect)
            screen.blit(clue,clue_rect)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())