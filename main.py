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

    camera = Camera(width, height)

    player = Player()
    ground_y = 550
    bars = [
        pygame.Rect(350, 400, 100, 15),
        pygame.Rect(350, 300, 100, 15),
        pygame.Rect(350, 200, 100, 15),
        pygame.Rect(350, 100, 100, 15),
        pygame.Rect(100, 0, 100, 15),
        pygame.Rect(400, -100, 100, 15),
        pygame.Rect(700, -200, 100, 15),
        pygame.Rect(400, -300, 100, 15),
        pygame.Rect(100, -400, 100, 15),
        pygame.Rect(350, -500, 100, 15),
    ]

    platforms = [
        pygame.Rect(350, 400, 150, 15),
        pygame.Rect(100, 0, 150, 15),
        pygame.Rect(400, -300, 150, 15),
    ]

    game_state = "menu"

    title_font = pygame.font.SysFont('Arial', 128)
    help_font = pygame.font.SysFont('Verdana', 32)

    title = title_font.render('ASCEND', True, (0, 0, 0))
    clue = help_font.render("Press 'ENTER' to continue", False, (0, 0, 0))

    title_rect = title.get_rect(center=(width * 0.5, height * 0.4))
    clue_rect = clue.get_rect(center=(width * 0.5, height * 0.6))

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
                    game_state = 'playing'

        keys = pygame.key.get_pressed()

        if game_state == "menu":
            screen.fill('purple')
            screen.blit(title, title_rect)
            screen.blit(clue, clue_rect)

        elif game_state == "playing":
            screen.fill('pink')
            player.move(keys, dt)
            player.update(dt, ground_y)
            player.check_bar_collision(bars)
            player.check_platform_collision(platforms)
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

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())