# modified from mangogame code

import pygame
from fsm import FSM

class MazeBot(pygame.sprite.Sprite):
    # States
    N_SOUTH, N_EAST, N_NORTH, N_WEST, WIN, B_SOUTH, B_EAST, B_NORTH, B_WEST = "ns", "ne", "nn", "nw", "w", "bs", "be", "bn", "bw"

    def __init__(self, game, x=50, y=50):
        super().__init__()

        self.game = game

        # Load initial image
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

        # The route the bot will take to get to the $
        self.path = []

        # TODO: Create the Bot's finite state machine (self.fsm) with initial state
        self.fsm = FSM(self.N_SOUTH)
        self.init_fsm()
    
    def init_fsm(self):
        # TODO: Add the state transitions
        
        # for obstacles
        self.fsm.add_transition('X', self.N_SOUTH, None, self.N_EAST)
        self.fsm.add_transition('X', self.N_EAST, None, self.N_NORTH)
        self.fsm.add_transition('X', self.N_NORTH, None, self.N_WEST)
        self.fsm.add_transition('X', self.N_WEST, None, self.N_SOUTH)
        self.fsm.add_transition('X', self.B_SOUTH, self.move_south, self.B_SOUTH)
        self.fsm.add_transition('X', self.B_EAST, self.move_east, self.B_EAST)
        self.fsm.add_transition('X', self.B_NORTH, self.move_north, self.B_NORTH)
        self.fsm.add_transition('X', self.B_WEST, self.move_west, self.B_WEST)
        
        # for wall
        self.fsm.add_transition('#', self.N_SOUTH, None , self.N_EAST)
        self.fsm.add_transition('#', self.N_EAST, None, self.N_NORTH)
        self.fsm.add_transition('#', self.N_NORTH, None, self.N_WEST)
        self.fsm.add_transition('#', self.N_WEST, None, self.N_SOUTH)
        self.fsm.add_transition('#', self.B_SOUTH, None, self.B_EAST)
        self.fsm.add_transition('#', self.B_EAST, None, self.B_NORTH)
        self.fsm.add_transition('#', self.B_NORTH, None, self.B_WEST)
        self.fsm.add_transition('#', self.B_WEST, None, self.B_SOUTH)

        # for breaker
        for symbol in ['$', 'B']:
            self.fsm.add_transition(symbol, self.N_SOUTH, self.move_south, self.B_SOUTH)
            self.fsm.add_transition(symbol, self.N_EAST, self.move_east, self.B_EAST)
            self.fsm.add_transition(symbol, self.N_NORTH, self.move_north, self.B_NORTH)
            self.fsm.add_transition(symbol, self.N_WEST, self.move_west, self.B_WEST)
            self.fsm.add_transition(symbol, self.B_SOUTH, self.move_south, self.N_SOUTH)
            self.fsm.add_transition(symbol, self.B_EAST, self.move_east, self.N_EAST)
            self.fsm.add_transition(symbol, self.B_NORTH, self.move_north, self.N_NORTH)
            self.fsm.add_transition(symbol, self.B_WEST, self.move_west, self.N_WEST)

        # for open space
        for symbol in [' ', 'M']:
            self.fsm.add_transition(symbol, self.N_SOUTH, self.move_south, self.N_SOUTH)
            self.fsm.add_transition(symbol, self.N_EAST, self.move_east, self.N_EAST)
            self.fsm.add_transition(symbol, self.N_NORTH, self.move_north, self.N_NORTH)
            self.fsm.add_transition(symbol, self.N_WEST, self.move_west, self.N_WEST)
            self.fsm.add_transition(symbol, self.B_SOUTH, self.move_south, self.B_SOUTH)
            self.fsm.add_transition(symbol, self.B_EAST, self.move_east, self.B_EAST)
            self.fsm.add_transition(symbol, self.B_NORTH, self.move_north, self.B_NORTH)
            self.fsm.add_transition(symbol, self.B_WEST, self.move_west, self.B_WEST)

    def get_state(self):
        # TODO: Return the maze bot's current state
        return self.fsm.current_state
    
    def move_south(self):
        """
        Changes the bot's location 1 spot South
        and records the movement in self.path
        """
        self.rect.centery += self.velocity
        self.path.append("SOUTH")

    def move_east(self):
        """
        Changes the bot's location 1 spot East
        and records the movement in self.path
        """
        self.rect.centerx += self.velocity
        self.path.append("EAST")

    def move_north(self):
        """
        Changes the bot's location 1 spot North
        and records the movement in self.path
        """
        self.rect.centery -= self.velocity
        self.path.append("NORTH")

    def move_west(self):
        """
        Changes the bot's location 1 spot West
        and records the movement in self.path
        """
        self.rect.centerx -= self.velocity
        self.path.append("WEST")
    
    def get_next_space(self):
        """
        Uses the bot's current state to determine the next 
        space in the maze the bot would go to. The next 
        space is returned as a String from self.maze.

        Ex. If the bot is facing South, you should get 
        the character one row down from you.

        Returns:
            String: The next character in the maze the bot could go to
        """

        # This is the current x and y indices of the bot in the maze
        grid_x = self.rect.centerx // self.game.SPACING
        grid_y = self.rect.centery // self.game.SPACING

        # TODO: Use the bot's current state to determine
        # what the next maze location value is
        
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
            print("already won") 
        elif state == "bs":
            next_y += 1
        elif state == "be":
            next_x += 1
        elif state == "bn":
            next_y -= 1
        elif state == "bw":
            next_x -= 1
        
        #print(next_x, next_y)
        #print(state)
        
        next_char = self.maze[next_y][next_x]

        return next_char
            
    def update(self, input=None):
        # TODO: Use the finite state machine to process input
        next_space = self.get_next_space()
    
        self.fsm.process(next_space)

        if next_space == '$':
            print("win")
            print(self.path)
            exit(0)
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y ))
