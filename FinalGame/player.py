"""
Code for the user interactive player.
Player can move up/down/left/right according to the key input.
With the idle and move states, player is blocked by the maze
The sample state provides a speed boost
The freeze state slows the player down
The win state will indicate if you win

@author: Dorothy Zhang
@version: 2023
heavily modified from MangoGame code

"""

import pygame
from fsm import FSM

class Player:

    IDLE, MOVE = "i", "m"
    WIN, SAMPLE, FREEZE = "w", "s", "f"

    def __init__(self, game, x, y, speed):
        self.x = x
        self.y = y

        # Load initial image
        self.image = pygame.image.load("assets/images/cart.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 0 

        self.game = game
        
        self.maze = self.game.txt_grid

        self.fsm = FSM(self.MOVE)
        self.init_fsm()
    
    def init_fsm(self):        
        """
        Set up all the state transitions for player.
        Transitions consider the type of movement (move, idle)
        and the character/obstacles ('#' wall, ' ' open space, 'C' winning churro) encountered
       
        """
        # for wall
        self.fsm.add_transition('#', self.IDLE, None, self.IDLE)
        self.fsm.add_transition('#', self.MOVE, None, self.IDLE)
        self.fsm.add_transition('#', self.WIN, None, None)
        self.fsm.add_transition('#', self.SAMPLE, None, self.IDLE)
        self.fsm.add_transition('#', self.FREEZE, None, self.IDLE)
        
        # for space
        self.fsm.add_transition(' ', self.IDLE, self.regular, self.MOVE)
        self.fsm.add_transition(' ', self.MOVE, self.regular, self.MOVE)
        self.fsm.add_transition(' ', self.WIN, None, None)
        self.fsm.add_transition(' ', self.SAMPLE, self.fast, self.SAMPLE)
        self.fsm.add_transition(' ', self.FREEZE, self.slow, self.FREEZE)

        # for win
        self.fsm.add_transition('C', self.MOVE, self.regular, self.WIN)
        self.fsm.add_transition('C', self.IDLE, self.regular, self.WIN)
        self.fsm.add_transition('C', self.WIN, None, None)
        self.fsm.add_transition('C', self.SAMPLE, None, self.WIN)
        self.fsm.add_transition('C', self.FREEZE, None, self.WIN)

        # for speed boost
        self.fsm.add_transition('S', self.MOVE, self.fast, self.SAMPLE)
        self.fsm.add_transition('S', self.IDLE, self.fast, self.SAMPLE)
        self.fsm.add_transition('S', self.WIN, self.fast, self.SAMPLE)
        self.fsm.add_transition('S', self.SAMPLE, self.fast, self.SAMPLE)
        self.fsm.add_transition('S', self.FREEZE, self.slow, self.FREEZE)


        # for freezer
        self.fsm.add_transition('F', self.MOVE, self.slow, self.FREEZE)
        self.fsm.add_transition('F', self.IDLE, self.slow, self.FREEZE)
        self.fsm.add_transition('F', self.WIN, self.slow, self.FREEZE)
        self.fsm.add_transition('F', self.SAMPLE, self.slow, self.FREEZE)
        self.fsm.add_transition('F', self.FREEZE, self.slow, self.FREEZE)

    def get_state(self):
        # Return the player's current state
        return self.fsm.current_state
    
    def stick_next(self, x):
        return (x // self.game.SPACING) * self.game.SPACING + self.game.SPACING//2

    def move(self, in_speed):
        """
        Based on the direction key input from the game class,
        The user input will be reflected in the change in positioning on the x y maze

        """
        if self.direction == self.game.LEFT:
            self.rect.centerx -= in_speed
            self.rect.centery = self.stick_next(self.rect.centery)
        elif self.direction == self.game.RIGHT:
            self.rect.centerx += in_speed
            self.rect.centery = self.stick_next(self.rect.centery)
        elif self.direction == self.game.UP:
            self.rect.centery -= in_speed
            self.rect.centerx = self.stick_next(self.rect.centerx)
        elif self.direction == self.game.DOWN:
            self.rect.centery += in_speed
            self.rect.centerx = self.stick_next(self.rect.centerx)
        else:
            print("unknown direction", self.direction)
    
    def check_move(self):
        """
        Uses the player's current state to determine the next 
        space in the maze the palyer would go to. The next 
        space is returned as a String from self.maze.

        """
        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING
        
        if self.direction == self.game.RIGHT:
            grid_x = self.rect.left // self.game.SPACING
            grid_x += 1
        elif self.direction == self.game.UP:
            grid_y = self.rect.bottom // self.game.SPACING
            grid_y -= 1
        elif self.direction == self.game.LEFT:
            grid_x = self.rect.right // self.game.SPACING
            grid_x -= 1
        elif self.direction == self.game.DOWN:
            grid_y = self.rect.top // self.game.SPACING
            grid_y += 1
         
        next_char = self.maze[grid_y][grid_x]

        return next_char

    def regular(self):
        self.move(self.speed)

    def fast(self):
        self.move(self.speed*2)

    def slow(self):
        self.move(self.speed/2)

    def update(self):
        # Use the finite state machine to process input
        
        next_space = self.check_move()
        self.fsm.process(next_space)
        
    def draw(self, screen):
        # draw the player onto the maze and win message

        if self.get_state() == self.WIN:
            font = pygame.font.Font(None, 100)
            lines = ("YOU WIN!\n"
                    "press space to play again")
            text = font.render(lines, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.game.WIDTH // 2, self.game.HEIGHT // 2)
            screen.blit(text, text_rect)

        screen.blit(self.image, (self.rect.x , self.rect.y ))