# modified from ChatGPT code

import pygame
from fsm import FSM

class Player:

    N_SOUTH, N_EAST, N_NORTH, N_WEST  = "1", "0", "3", "2"
    #S_SOUTH, S_EAST, S_NORTH, S_WEST = "ss", "se", "sn", "sw"
    #F_SOUTH, F_EAST, F_NORTH, F_WEST = "fs", "fe", "fn", "fw"

    def __init__(self, game, x, y, radius, speed):
        self.x = x
        self.y = y

        # Load initial image
        self.image = pygame.image.load("assets/images/bot.png")
        self.rect = self.image.get_rect()

        # self.radius = radius
        self.speed = speed
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up

        self.game = game
        
        self.maze = self.game.txt_grid

        self.fsm = FSM(self.N_SOUTH)
        self.init_fsm()
    
    def init_fsm(self):
        # TODO: Add the state transitions
        
        # for wall
        self.fsm.add_transition('#', self.N_SOUTH, None, None)
        self.fsm.add_transition('#', self.N_EAST, None, None)
        self.fsm.add_transition('#', self.N_NORTH, None, None)
        self.fsm.add_transition('#', self.N_WEST, None, None)
        # self.fsm.add_transition('X', self.S_SOUTH, None, None)
        # self.fsm.add_transition('X', self.S_EAST, None, None)
        # self.fsm.add_transition('X', self.S_NORTH, None, None)
        # self.fsm.add_transition('X', self.S_WEST, None, None)
        # self.fsm.add_transition('X', self.F_SOUTH, None, None)
        # self.fsm.add_transition('X', self.F_EAST, None, None)
        # self.fsm.add_transition('X', self.F_NORTH, None, None)
        # self.fsm.add_transition('X', self.F_WEST, None, None)
    
    def get_state(self):
        # Return the player's current state
        return self.fsm.current_state

    def move(self):
        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING

        # TODO: Use the bot's current state to determine
        # what the next maze location value is
        
        state = self.get_state()
        next_x = grid_x
        next_y = grid_y

        if state == 0:
            next_x += self.speed
        elif state == 1:
            next_y += self.speed
        elif state == 2:
            next_x -= self.speed
        elif state == 3:
            next_y -= self.speed
         
    
    def update(self):
        # FSM with the next space
        next_space = self.get_next_space()
        self.fsm.process(next_space)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))

# modified from mangogame code
