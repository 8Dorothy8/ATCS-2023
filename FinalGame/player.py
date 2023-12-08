# modified from ChatGPT code

import pygame
from fsm import FSM

class Player:

    N_SOUTH, N_EAST, N_NORTH, N_WEST  = "1", "0", "3", "2"
    #S_SOUTH, S_EAST, S_NORTH, S_WEST = "ss", "se", "sn", "sw"
    #F_SOUTH, F_EAST, F_NORTH, F_WEST = "fs", "fe", "fn", "fw"

    def __init__(self, game, x, y, speed):
        self.x = x
        self.y = y

        # Load initial image
        self.image = pygame.image.load("assets/images/cart.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up

        self.game = game
        
        self.maze = self.game.txt_grid

        self.fsm = FSM(self.N_EAST)
        self.init_fsm()
    
    def init_fsm(self):
        # TODO: Add the state transitions
        
        # for wall
        self.fsm.add_transition('#', self.N_SOUTH, None, None)
        self.fsm.add_transition('#', self.N_EAST, None, None)
        self.fsm.add_transition('#', self.N_NORTH, None, None)
        self.fsm.add_transition('#', self.N_WEST, None, None)

        # for space
        self.fsm.add_transition(' ', self.N_SOUTH, self.move_south, self.N_SOUTH)
        self.fsm.add_transition(' ', self.N_EAST, self.move_east, self.N_EAST)
        self.fsm.add_transition(' ', self.N_NORTH, self.move_north, self.N_NORTH)
        self.fsm.add_transition(' ', self.N_WEST, self.move_west, self.N_WEST)

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
    
    def move_south(self):
        """
        Changes the bot's location 1 spot South
        and records the movement in self.path
        """
        self.rect.centery += self.speed

    def move_east(self):
        """
        Changes the bot's location 1 spot East
        and records the movement in self.path
        """
        self.rect.centerx += self.speed

    def move_north(self):
        """
        Changes the bot's location 1 spot North
        and records the movement in self.path
        """
        self.rect.centery -= self.speed

    def move_west(self):
        """
        Changes the bot's location 1 spot West
        and records the movement in self.path
        """
        self.rect.centerx -= self.speed

    def move(self):
        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING
        

        # TODO: Use the bot's current state to determine
        # what the next maze location value is
        
        state = self.get_state()

        if state == "0":          # N_SOUTH, N_EAST, N_NORTH, N_WEST  = "1", "0", "3", "2"
            grid_x = self.rect.centerx // self.game.SPACING
            grid_y = self.rect.centery // self.game.SPACING
            grid_x += 1
        elif state == "1":
            grid_x = self.rect.bottomright[1] // self.game.SPACING
            grid_y = self.rect.bottomright[0] // self.game.SPACING
            grid_y += 1
        elif state == "2":
            grid_x = self.rect.topleft[1] // self.game.SPACING
            grid_y = self.rect.topleft[0] // self.game.SPACING
            grid_x -= 1
        elif state == "3":
            grid_x = self.rect.topleft[1] // self.game.SPACING
            grid_y = self.rect.topleft[0] // self.game.SPACING
            grid_y -= 1
         
        print("Next grid: ", grid_y, grid_x) 
        next_char = self.maze[grid_y][grid_x]

        return next_char

    def update(self):
        # FSM with the next space
        next_space = self.move()
        self.fsm.process(next_space)
        print(next_space, self.direction)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))