import pygame

class Player:

    def __init__(self):
        self.width = 32
        self.height = 52
        self.rect = pygame.Rect(380,300, self.width,self.height)
        self.gravity = 1200
        self.speed = 500
        self.jump_strength = 600
        self.holding = False
        self.grab_locked = False

        self.velocity_y = 0

        self.on_ground = False

    def move(self,keys,dt):
        # vertical movement
        if keys[pygame.K_w] and self.on_ground:
                self.velocity_y = -self.jump_strength 
                self.on_ground = False

        # horizontal movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt

        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt

    def check_collision(self,hold):
        top_hitbox = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,10)

        if top_hitbox.colliderect(hold):
            if not self.holding and not self.grab_locked:
                self.holding = True
                self.velocity_y = 0

                # center the player beneath the hold
                # self.rect.centerx = hold.centerx
                self.rect.top = hold.top
        else:
            self.grab_locked = False
            self.holding = False

    def release_hold(self):
        if self.holding:
            self.holding = False
            self.grab_locked = True
            self.velocity_y = -self.jump_strength

    def draw(self,surface):
        pygame.draw.rect(surface,'red', self.rect)

    def update(self, dt, ground_y):
        # apply gravity

        self.on_ground = False
        if not self.holding:
            self.velocity_y += self.gravity * dt
        
            self.rect.y += self.velocity_y * dt

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

        