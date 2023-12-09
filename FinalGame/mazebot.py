"""
Code for the AI mazebot shopper which the player competes against.

@author: Dorothy Zhang
@version: 2023
moderately modified from MangoGame code

"""

import pygame
from fsm import FSM

class MazeBot(pygame.sprite.Sprite):
    # States
    N_SOUTH, N_EAST, N_NORTH, N_WEST = "ns", "ne", "nn", "nw"
    B_SOUTH, B_EAST, B_NORTH, B_WEST = "bs", "be", "bn", "bw"
    WIN = "w"

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        # Load initial bot image
        self.image = pygame.image.load("assets/images/bot.png")
        self.rect = self.image.get_rect()

        # Set rectangle
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 5

        # The map of the maze
        self.maze = self.game.txt_grid

        # The route the bot will take to get to the churros
        self.path = []

        # Create bot's finite state machine with initial state
        self.fsm = FSM(self.N_SOUTH)
        self.init_fsm()
    
    def init_fsm(self):
        """
        Set up all the state transitions for mazebot.
        Transitions consider the direction of movement (sourth, east, north, west),
        and the character/obstacles ('#' wall, ' ' open space, 'C' winning churro) encountered
       
        """

        # for wall
        self.fsm.add_transition('#', self.N_SOUTH, None , self.N_EAST)
        self.fsm.add_transition('#', self.N_EAST, None, self.N_NORTH)
        self.fsm.add_transition('#', self.N_NORTH, None, self.N_WEST)
        self.fsm.add_transition('#', self.N_WEST, None, self.N_SOUTH)

        # for open space
        self.fsm.add_transition(' ', self.N_SOUTH, self.move_south, self.N_SOUTH)
        self.fsm.add_transition(' ', self.N_EAST, self.move_east, self.N_EAST)
        self.fsm.add_transition(' ', self.N_NORTH, self.move_north, self.N_NORTH)
        self.fsm.add_transition(' ', self.N_WEST, self.move_west, self.N_WEST)
        self.fsm.add_transition(' ', self.WIN, None, None)

        # for win
        self.fsm.add_transition('C', self.N_SOUTH, self.move_south, self.WIN)
        self.fsm.add_transition('C', self.N_EAST, self.move_east, self.WIN)
        self.fsm.add_transition('C', self.N_NORTH, self.move_north, self.WIN)
        self.fsm.add_transition('C', self.N_WEST, self.move_west, self.WIN)
        self.fsm.add_transition('C', self.WIN, None, self.WIN)

    def get_state(self):
        # returns bot's current state
        return self.fsm.current_state
    
    def move_south(self):
       # Changes the bot's location 1 velocity south
        self.rect.centery += self.velocity
        self.path.append("SOUTH")

    def move_east(self):
        # Changes the bot's location 1 velocity east
        self.rect.centerx += self.velocity
        self.path.append("EAST")

    def move_north(self):
        # Changes the bot's location 1 velocity north
        self.rect.centery -= self.velocity
        self.path.append("NORTH")

    def move_west(self):
        # Changes the bot's location 1 velocity west
        self.rect.centerx -= self.velocity
        self.path.append("WEST")
    
    def get_next_space(self):
        """
        Uses the bot's current state to determine the next 
        space in the maze the bot would go to. The next 
        space is returned as a String from self.maze.

        """

        # Current x and y indices of the bot
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING

        # Determine what the next maze location value is
        
        state = self.get_state()
        next_x = grid_x
        next_y = grid_y

        if state == "ns":
            next_y += 1
        elif state == "ne":
            next_x += 1
        elif state == "nn":
            next_y -= 1
        elif state == "nw":
            next_x -= 1
        elif state == "w":
            #print("already won")
            pass 
        elif state == "bs":
            next_y += 1
        elif state == "be":
            next_x += 1
        elif state == "bn":
            next_y -= 1
        elif state == "bw":
            next_x -= 1
        
        next_char = self.maze[next_y][next_x]
        return next_char
            
    def update(self, input=None):
        # Use the finite state machine to process input

        next_space = self.get_next_space()
        self.fsm.process(next_space)
    
    def draw(self, screen):
        # draw the mazebot onto the maze and win message

        if self.get_state() == self.WIN:
            font = pygame.font.Font(None, 100)
            text = font.render("YOU LOSE!", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.game.WIDTH // 2, self.game.HEIGHT // 2)
            screen.blit(text, text_rect)

        screen.blit(self.image, (self.rect.x , self.rect.y ))
