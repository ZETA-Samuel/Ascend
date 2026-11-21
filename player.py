import pygame

class Player:

    def __init__(self):
        self.width = 32
        self.height = 52
        self.rect = pygame.Rect(380,300, self.width,self.height)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.gravity = 1200
        self.speed = 500
        self.jump_strength = 600
        self.holding = False
        self.grab_locked = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.swing_acceleration = 800
        self.max_swing_speed = 300
        self.friction = 0.95
        self.on_ground = False

    def move(self,keys,dt):
        # vertical movement
        if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = -self.jump_strength 
                self.on_ground = False

        # horizontal movement
        if keys[pygame.K_a]:
            self.velocity_x -= self.swing_acceleration * dt

        if keys[pygame.K_d]:
            self.velocity_x += self.swing_acceleration * dt

        self.velocity_x = max(-self.max_swing_speed,min(self.velocity_x, self.max_swing_speed))

        self.pos.x += self.velocity_x * dt
        self.rect.x = round(self.pos.x)

    def check_collision(self,holds):
        if self.holding:
            return

        top_hitbox = pygame.Rect(self.rect.x,self.rect.y,self.rect.width,10)

        for hold in holds:
            if top_hitbox.colliderect(hold):
                # if self.rect.x < hold.x : self.rect.x = hold.x
                # if self.rect.x > (hold.x + hold.width) : self.rect.x = hold.x + hold.width
                if not self.grab_locked:
                    self.holding = True
                    self.velocity_y = 0
                    self.rect.top = hold.top 
                    self.pos.y = self.rect.y
                return
        self.grab_locked = False

    def check_hold_edge(self,holds):
        if not self.holding:
            return

        player_center = self.rect.centerx

        standing_on_hold = False

        for hold in holds:
            if self.rect.top == hold.top:
                if hold.left <= player_center <= hold.right:
                    standing_on_hold = True
                    break

        if not standing_on_hold:
            self.holding = False

    def release_hold(self):
        if self.holding:
            # pygame.time.wait(1000)
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
            self.pos.y += self.velocity_y * dt
            self.rect.y = round(self.pos.y)

        # ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

        if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
            self.velocity_x *= self.friction  ** (dt * 60)

        