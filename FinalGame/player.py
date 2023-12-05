# modified from ChatGPT code

import pygame
from fsm import FSM

class Player:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        
    def move(self):
        if self.direction == 0:
            self.x += self.speed
        elif self.direction == 1:
            self.y += self.speed
        elif self.direction == 2:
            self.x -= self.speed
        elif self.direction == 3:
            self.y -= self.speed
    
    def update(self):
        self.move()
        print(self.direction)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)