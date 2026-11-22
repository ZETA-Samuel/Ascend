import pygame

class Camera:

    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.offset_y = 0
        self.target_y = height * 0.5
        self.smoothing = 4

    def update(self, player,dt):
        target_offset = self.target_y - player.rect.centery

        if player.rect.centery < self.target_y:
            if target_offset > self.offset_y:
                self.offset_y += (target_offset - self.offset_y) * min(1, self.smoothing * dt)

        elif player.rect.centery > self.target_y:
            if target_offset < self.offset_y:
                self.offset_y += (target_offset - self.offset_y) * min(1, self.smoothing * dt)

    def apply(self,rect):
        return rect.move(0, round(self.offset_y))