import pygame
import sys

#image 

# -----------------------------
# SCROLL SYSTEM
# -----------------------------
class ScrollSystem:
    def __init__(self, speed):
        self.speed = speed
        self.distance = 0.0
        self.active = True

    def update(self, dt):
        if self.active:
            self.distance += self.speed * dt

    def stop(self):
        self.active = False

    def resume(self):
        self.active = True

# -----------------------------
# BACKGROUND SYSTEM
# -----------------------------
class ScrollingBackground:
    def __init__(self, image, scroll_system):
        self.image = image
        self.scroll = scroll_system
        self.height = image.get_height()

    def draw(self, surface):
        offset = self.scroll.distance % self.height

        y1 = -offset
        y2 = y1 + self.height

        surface.blit(self.image, (0, y1))
        surface.blit(self.image, (0, y2))
