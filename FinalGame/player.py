# modified from ChatGPT code

import pygame
from fsm import FSM

class Player:

    IDLE, MOVE = "i", "m"
    WIN, SAMPLE, FREEZE = "w", "s", "f"

    #N_SOUTH, N_EAST, N_NORTH, N_WEST  = "1", "0", "3", "2"

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

        self.fsm = FSM(self.MOVE)
        self.init_fsm()
    
    def init_fsm(self):
        # TODO: Add the state transitions
        
        
        # for wall
        # self.fsm.add_transition('#', self.N_SOUTH, None, None)
        # self.fsm.add_transition('#', self.N_EAST, None, None)
        # self.fsm.add_transition('#', self.N_NORTH, None, None)
        # self.fsm.add_transition('#', self.N_WEST, None, None)

        self.fsm.add_transition('#', self.IDLE, None, self.IDLE)
        self.fsm.add_transition('#', self.MOVE, None, self.IDLE)
        self.fsm.add_transition('#', self.WIN, None, None)
        
        # for space
        # self.fsm.add_transition(' ', self.N_SOUTH, self.move_south, self.N_SOUTH)
        # self.fsm.add_transition(' ', self.N_EAST, self.move_east, self.N_EAST)
        # self.fsm.add_transition(' ', self.N_NORTH, self.move_north, self.N_NORTH)
        # self.fsm.add_transition(' ', self.N_WEST, self.move_west, self.N_WEST)
        
        self.fsm.add_transition(' ', self.IDLE, self.move, self.MOVE)
        self.fsm.add_transition(' ', self.MOVE, self.move, self.MOVE)
        self.fsm.add_transition(' ', self.WIN, None, None)

        # for win
        self.fsm.add_transition('C', self.MOVE, self.move, self.WIN)
        self.fsm.add_transition('C', self.IDLE, self.move, self.WIN)
        self.fsm.add_transition('C', self.WIN, None, None)

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
    
    # def move_south(self):
    #     """
    #     Changes the bot's location 1 spot South
    #     and records the movement in self.path
    #     """
    #     self.rect.centery += self.speed

    # def move_east(self):
    #     """
    #     Changes the bot's location 1 spot East
    #     and records the movement in self.path
    #     """
    #     self.rect.centerx += self.speed

    # def move_north(self):
    #     """
    #     Changes the bot's location 1 spot North
    #     and records the movement in self.path
    #     """
    #     self.rect.centery -= self.speed

    # def move_west(self):
    #     """
    #     Changes the bot's location 1 spot West
    #     and records the movement in self.path
    #     """
    #     self.rect.centerx -= self.speed

    def move(self):
        if self.direction == self.game.LEFT:
            self.rect.centerx -= self.speed
        elif self.direction == self.game.RIGHT:
            self.rect.centerx += self.speed
        elif self.direction == self.game.UP:
            self.rect.centery -= self.speed
        elif self.direction == self.game.DOWN:
            self.rect.centery += self.speed
        else:
            print("unknown direction", self.direction)

    def check_move(self):
        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING
        
        if self.direction == self.game.RIGHT:          # N_SOUTH, N_EAST, N_NORTH, N_WEST  = "1", "0", "3", "2"
            grid_x += 1
        elif self.direction == self.game.UP:
            grid_y -= 1
        elif self.direction == self.game.LEFT:
            grid_x -= 1
        elif self.direction == self.game.DOWN:
            grid_y += 1
         
        print("Next grid: ", grid_y, grid_x) 
        print(self.direction)
        next_char = self.maze[grid_y][grid_x]

        return next_char

    def update(self):
        # FSM with the next space
        next_space = self.check_move()

        if next_space == 'C':
            print("you win!")
            self.fsm.process(next_space)

        self.fsm.process(next_space)
        print(next_space, self.direction)

        
        
    def draw(self, screen):

        if self.get_state() == self.WIN:
            font = pygame.font.Font(None, 100)
            text = font.render("YOU WIN!", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.game.WIDTH // 2, self.game.HEIGHT // 2)
            screen.blit(text, text_rect)

        screen.blit(self.image, (self.rect.x , self.rect.y ))