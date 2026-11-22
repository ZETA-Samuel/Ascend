import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from camera import Camera
from player import Player


class GameLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.player = Player()

    def test_player_grabs_bar_crossed_between_frames(self):
        bar = pygame.Rect(350, 400, 100, 15)
        self.player.previous_rect = pygame.Rect(380, 430, 32, 52)
        self.player.rect = pygame.Rect(380, 370, 32, 52)
        self.player.pos.y = self.player.rect.y
        self.player.velocity_y = -600

        self.player.check_bar_collision([bar])

        self.assertTrue(self.player.holding)
        self.assertIs(self.player.holding_bar, bar)
        self.assertEqual(self.player.rect.top, bar.bottom)
        self.assertEqual(self.player.velocity_y, 0)

    def test_releasing_a_bar_unlocks_after_head_clears_it(self):
        bar = pygame.Rect(350, 400, 100, 15)
        self.player.holding = True
        self.player.holding_bar = bar
        self.player.rect.x = 380
        self.player.rect.top = bar.bottom

        self.player.release_hold()
        self.player.previous_rect = self.player.rect.copy()
        self.player.rect.top = 410
        self.player.check_bar_collision([bar])

        self.assertFalse(self.player.holding)
        self.assertTrue(self.player.grab_locked)

        self.player.previous_rect = self.player.rect.copy()
        self.player.rect.top = 390
        self.player.check_bar_collision([bar])

        self.assertFalse(self.player.holding)
        self.assertFalse(self.player.grab_locked)
        self.assertIsNone(self.player.locked_bar)

    def test_platform_landing_uses_crossed_surface(self):
        platform = pygame.Rect(350, 400, 150, 15)
        self.player.previous_rect = pygame.Rect(380, 343, 32, 52)
        self.player.rect = pygame.Rect(380, 353, 32, 52)
        self.player.pos.y = self.player.rect.y
        self.player.velocity_y = 600

        self.player.check_platform_collision([platform])

        self.assertTrue(self.player.on_ground)
        self.assertEqual(self.player.rect.bottom, platform.top)
        self.assertEqual(self.player.velocity_y, 0)

    def test_camera_does_not_overshoot_target(self):
        camera = Camera(800, 600)
        self.player.rect.center = (400, 100)

        for _ in range(120):
            camera.update(self.player, 1 / 60)

        self.assertEqual(self.player.rect.centery + camera.offset_y, camera.target_y)


if __name__ == "__main__":
    unittest.main()
