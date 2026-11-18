import pygame

class Player:

    def __init__(self):
        self.width = 32
        self.height = 52

        self.player1 = pygame.Surface((self.width,self.height))
        self.player1_rect = self.player1.get_rect(center=(400,300))

        self.speed = 300
        self.gravity = 1200
        self.jump_strength = 600
        self.velocity_y = 0

        self.on_ground = False

    def move(self,keys,dt):
        # vertical movement
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.velocity_y = -self.jump_strength 
            self.on_ground = False

        # horizontal movement
        if keys[pygame.K_a]:
            self.player1_rect.x -= self.speed * dt

        if keys[pygame.K_d]:
            self.player1_rect.x += self.speed * dt

    def draw(self,surface):
        pygame.draw.rect(surface,'red', self.player1_rect)

    def update(self, dt, ground_y):
        # apply gravity
        self.velocity_y += self.gravity * dt

        # apply vertical movement
        self.player1_rect.y += self.velocity_y * dt

        # ground collision
        if self.player1_rect.bottom >= ground_y:
            self.player1_rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

        