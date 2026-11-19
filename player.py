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
  

        self.velocity_y = 0

        self.on_ground = False

    def move(self,keys,dt):
        # vertical movement
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]):

            if self.on_ground:
                self.velocity_y = -self.jump_strength 
                self.on_ground = False

        # horizontal movement
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt

        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt

    def check_collision(self,hold,keys,dt):
        if self.rect.colliderect(hold):
            self.holding = True
            print("holding")
            if keys[pygame.K_q]:
                self.holding = False
            if keys[pygame.K_SPACE]:
                self.holding = False
                self.rect.y += -self.jump_strength * dt
        else:
            self.holding = False
        # if keys[pygame.K_q]:
        #     self.holding = False

    def draw(self,surface):
        pygame.draw.rect(surface,'red', self.rect)

    def update(self, dt, ground_y):
        # apply gravity

        self.on_ground = False
        self.velocity_y += self.gravity * dt

        # apply vertical movement
        if self.holding:
            self.velocity_y = 0
        self.rect.y += self.velocity_y * dt

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

        