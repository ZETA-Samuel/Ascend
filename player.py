from pathlib import Path

import pygame

class Player:

    def __init__(self):
        self.width = 32
        self.height = 52

        self.rect = pygame.Rect(0,33, self.width,self.height)
        self.pos = pygame.Vector2(self.rect.topleft)

        self.previous_rect = self.rect.copy()

        self.gravity = 1200
        self.speed = 500
        self.jump_strength = 600

        self.holding = False
        self.holding_bar = None
        self.locked_bar = None
        self.grab_locked = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.swing_acceleration = 800
        self.max_swing_speed = 300
        self.friction = 0.95
        self.on_ground = False

        # Animations
        self.animations = {
            'idle': self.load_frames('idle.png', 30),
            'walk': self.load_frames('walk.png', 30),
            'jump': self.load_frames('jump.png', 30),
            'idle_hold': self.load_frames('idle_hang.png', 30),
            'moving_hold': self.load_frames('hang_left.png', 30)
        }

        self.animation_state = 'idle'
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speeds = {
            'idle': 0.6,
            'walk': 0.08,
            'jump': 0.1,
            'idle_hold': 0.15,
            'moving_hold': 0.08
        }

        self.facing_right = True

    def load_frames(self, filename, frame_width):
        path = Path(__file__).parent / "assets" / filename
        sheet = pygame.image.load(str(path)).convert_alpha()

        frames = []
        frame_height = sheet.get_height()

        for x in range(0,sheet.get_width(), frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

            frame.blit(sheet, (0,0), (x,0,frame_width,frame_height))

            frame = pygame.transform.scale(frame, (64,64))
            frames.append(frame)

        return frames

    def move(self,keys,dt):
        # vertical movement
        self.previous_rect = self.rect.copy()

        if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -self.jump_strength 
                self.on_ground = False

        # horizontal movement
        if keys[pygame.K_a]:
            self.velocity_x -= self.swing_acceleration * dt

        if keys[pygame.K_d]:
            self.velocity_x += self.swing_acceleration * dt

        self.velocity_x = max(-self.max_swing_speed,min(self.velocity_x, self.max_swing_speed))

        if self.velocity_x > 1:
            self.facing_right = True
        elif self.velocity_x < -1:
            self.facing_right = False

        self.pos.x += self.velocity_x * dt
        self.rect.x = round(self.pos.x)

    def update_animations(self, dt):

        if self.holding:

            if abs(self.velocity_x) > 25:
                new_state = 'moving_hold'
            else:
                new_state = 'idle_hold'

        elif self.on_ground:
            if abs(self.velocity_x) > 25:
                new_state = 'walk'

            else:
                new_state = 'idle'

        else:
            new_state = 'jump'

        if new_state != self.animation_state:
            self.animation_state = new_state
            self.frame_index = 0
            self.animation_timer = 0

        self.animation_timer += dt

        animation_speed = self.animation_speeds[self.animation_state]

        if self.animation_timer >= animation_speed:
            self.animation_timer -= animation_speed

            frames = self.animations[self.animation_state]

            self.frame_index = (self.frame_index + 1) % len(frames)

    def check_hold_edge(self):
        if not self.holding:
            return

        if self.holding_bar is None:
            return

        player_center = self.rect.centerx
        bar = self.holding_bar

        if not (bar.left <= player_center <= bar.right):

            self.holding = False
            self.holding_bar = None


    def check_platform_collision(self, platforms):

        if self.velocity_y < 0:
            return

        for platform in platforms:
            crossed_platform_top = (
                self.previous_rect.bottom <= platform.top
                and self.rect.bottom >= platform.top
            )
            overlaps_horizontally = (
                self.rect.right > platform.left
                and self.rect.left < platform.right
            )
            if crossed_platform_top and overlaps_horizontally:
                self.rect.bottom = platform.top
                self.pos.y = self.rect.y
                self.velocity_y = 0
                self.on_ground = True

    def check_bar_collision(self, bars):
        if self.holding:
            return

        head_hitbox = pygame.Rect(
            self.rect.left + 4,
            self.rect.top,
            self.rect.width - 8,
            10
        )

        if self.grab_locked:
            if self.locked_bar is not None and head_hitbox.colliderect(self.locked_bar):
                return
            self.grab_locked = False
            self.locked_bar = None

        for bar in bars:
            crossed_bar_bottom = (
                self.previous_rect.top >= bar.bottom
                and self.rect.top <= bar.bottom
            )
            crossed_bar_top = (
                self.previous_rect.top + head_hitbox.height <= bar.top
                and self.rect.top + head_hitbox.height >= bar.top
            )
            horizontal_overlap = (
                head_hitbox.right > bar.left and head_hitbox.left < bar.right
            )
            crossed_bar = horizontal_overlap and (
                crossed_bar_bottom or crossed_bar_top
            )
            if head_hitbox.colliderect(bar) or crossed_bar:
                self.holding = True
                self.holding_bar = bar
                self.grab_locked = False
                self.locked_bar = None
                self.velocity_y = 0

                self.rect.top = bar.bottom
                self.pos.y = self.rect.y

                return

    def release_hold(self):
        if self.holding:
            self.holding = False
            self.grab_locked = True
            self.locked_bar = self.holding_bar
            self.holding_bar = None
            self.velocity_y = -self.jump_strength

    def draw(self,surface,camera):
        image = self.animations[self.animation_state][self.frame_index]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        draw_rect =  image.get_rect(midbottom=self.rect.midbottom)

        surface.blit(image, camera.apply(draw_rect))

    def update(self, dt, ground_y):
        # apply gravity

        self.on_ground = False

        if not self.holding:
            self.velocity_y += self.gravity * dt
            self.pos.y += self.velocity_y * dt
            self.rect.y = round(self.pos.y)

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

        if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
            self.velocity_x *= self.friction  ** (dt * 60)

        