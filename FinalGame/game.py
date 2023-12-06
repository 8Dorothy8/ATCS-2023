# modified from mangogame code

import pygame
import sys
from block import Block
from mazebot import MazeBot
from player import Player

class MangoGame:
    # Constants
    START_X, START_Y = 24, 24
    SPACING = 50
    BACKGROUND_COLOR = (0, 0, 0)
    START_POS_X = 70
    START_POS_Y = 70
    PLAYER_SIZE = 15

    def __init__(self):
        self.DEBUG = True

        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.ghost_timer = 8000

        # Paths
        self.txt_grid = []
        self.grid = []

        # sprites
        self.blocks = pygame.sprite.Group()
        self.mango = None

        player_speed = 5
        self.player = Player(self, self.START_POS_X, self.START_POS_Y, self.PLAYER_SIZE, player_speed)

        # Load the game level and available paths
        self.load_level(1)
        print(self.txt_grid)
        #print(self.txt_grid[3][4])

        self.HEIGHT = len(self.txt_grid) * self.SPACING
        self.WIDTH = len(self.txt_grid[0]) * self.SPACING

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Costco Craze")

    def load_level(self, maze_number=1):
        filepath = "assets/mazes/maze" + str(maze_number) + ".txt"
        row = 0
        with open(filepath, "r") as file:
            line = file.readline().strip()
            while line:
                txt_row = []
                for col in range(len(line)):
        
                    pos_x = self.START_X + (self.SPACING * col)
                    pos_y = self.START_Y + (self.SPACING * row)
                    txt_row.append(line[col])
                    if line[col] == '#':
                        self.blocks.add(Block(pos_x, pos_y))
                    elif line[col] == '$':
                        self.blocks.add(Block(pos_x, pos_y, Block.MONEY))
                    elif line[col] == 'B':
                        self.blocks.add(Block(pos_x, pos_y, Block.BOOSTER))
                    elif line[col] == 'S':
                        self.mango = MazeBot(self, pos_x, pos_y)
                    elif line[col] == '\n':
                        txt_row.pop()

                self.txt_grid.append(txt_row)
                line = file.readline()
                row += 1
    
    # def handle_events(self):

    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_LEFT]:
    #         self.player.direction = 2
    #     elif keys[pygame.K_RIGHT]:
    #         self.player.direction = 0
    #     elif keys[pygame.K_UP]:
    #         self.player.direction = 3
    #     elif keys[pygame.K_DOWN]:
    #         self.player.direction = 1
    
    def update(self):
        self.mango.update()
        self.player.update()

        # Collision detection with walls
        # player_rect = pygame.Rect(self.player.x - self.player.radius, self.player.y - self.player.radius,
        #                            2 * self.player.radius, 2 * self.player.radius)
        # for i, row in enumerate(self.txt_grid):
        #     for j, cell in enumerate(row):
        #         if cell == "#":
        #             wall_rect = pygame.Rect(j * 30, i * 30, 30, 30)
        #             if player_rect.colliderect(wall_rect):
        #                 # Pacman hit a wall, stop moving
        #                 if self.player.direction == 0:
        #                     self.player.x -= self.player.speed
        #                 elif self.player.direction == 1:
        #                     self.player.y -= self.player.speed
        #                 elif self.player.direction == 2:
        #                     self.player.x += self.player.speed
        #                 elif self.player.direction == 3:
        #                     self.player.y += self.player.speed

    def run(self):
        # Main game loop
        running = True

        # Draw the initial screen
        self.screen.fill(self.BACKGROUND_COLOR)
        self.blocks.draw(self.screen)
        self.mango.draw(self.screen)

        while running:
            # Set fps to 120
            self.dt += self.clock.tick(120)

            # Handle closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = 2
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = 0
                    elif event.key == pygame.K_UP:
                        self.player.direction = 3
                    elif event.key == pygame.K_DOWN:
                        self.player.direction = 1
            
            # check for user key movement
            # self.update()

            # Only update every 120 fps
            if self.dt > 120:
                self.dt = 0
                self.update()

                # Draw to the screen
                self.screen.fill(self.BACKGROUND_COLOR)
                self.blocks.draw(self.screen)
                self.mango.draw(self.screen)
                self.player.draw(self.screen)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MangoGame()
    game.run()
