"""
Welcome to the Costco Craze game!


You are a shopper going through the aisles at Costco.
Your goal to win the game is to reach the churro stand before the AI shopper does.
If you encounter a sample, you get a speed boost.
If you encounter the freezer section, you slow down.

Good Luck.

@author: Dorothy Zhang
@version: 2023
moderately from MangoGame code

"""

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
    LEFT, RIGHT, UP, DOWN = 2, 0, 3, 1

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
        self.player = None

        # maze
        self.load_level(1)
        self.HEIGHT = len(self.txt_grid) * self.SPACING
        self.WIDTH = len(self.txt_grid[0]) * self.SPACING

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Costco Craze")
        

    def load_level(self, maze_number=1):
        """
        Reads the selected maze file and loads the icon corresponding to the characters, 
        appends to text_grid for future use
        
        """
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
                    elif line[col] == 'C':
                        self.blocks.add(Block(pos_x, pos_y, Block.CHURRO))
                    elif line[col] == 'S':
                        self.blocks.add(Block(pos_x, pos_y, Block.SAMPLE))
                    elif line[col] == 'F':
                        self.blocks.add(Block(pos_x, pos_y, Block.FREEZER))
                    elif line[col] == 'M':
                        self.mango = MazeBot(self, pos_x, pos_y)
                        txt_row[-1] = ' '
                    elif line[col] == 'P':
                        player_speed = 10
                        self.player = Player(self, pos_x-25, pos_y-20, player_speed)
                        txt_row[-1] = ' '
                    elif line[col] == '\n':
                        txt_row.pop()

                self.txt_grid.append(txt_row)
                line = file.readline()
                row += 1
    
    def update(self):
        """
        calls the update functions for mango and player
        """
        self.mango.update()
        self.player.update()

    def run(self):
        # Main game loop
        self.show_start_screen()
        running = True

        # Draw the initial screen
        self.screen.fill(self.BACKGROUND_COLOR)
        self.blocks.draw(self.screen)
        self.mango.draw(self.screen)

        # Load the Costco icon image
        costco_icon = pygame.image.load("assets/images/Costco.png")
        costco_icon_rect = costco_icon.get_rect(center=(self.WIDTH // 2, 45))

        while running:
            # Set fps to 120
            self.dt += self.clock.tick(120)

            # Handle closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # check for user key movement
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = self.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = self.RIGHT
                    elif event.key == pygame.K_UP:
                        self.player.direction = self.UP
                    elif event.key == pygame.K_DOWN:
                        self.player.direction = self.DOWN
            
            # Only update every 120 fps
            if self.dt > 120:
                self.dt = 0
                self.update()

                # Draw to the screen
                self.screen.fill(self.BACKGROUND_COLOR)
                self.blocks.draw(self.screen)
                self.mango.draw(self.screen)
                self.player.draw(self.screen)
                self.screen.blit(costco_icon, costco_icon_rect)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def show_start_screen(self):
        """
        Draws the start screen that introduces the game
        From chatCPT
        """
        # Define the maximum width and height for the text
        max_width = self.WIDTH - 20
        max_height = self.HEIGHT - 20

        # Initialize font with a large size
        font_size = 36
        line_spacing = 5
        start_font = pygame.font.Font(None, font_size)

        # Define the instructions text
        instructions = (
            "You are a shopper going through the aisles at Costco.\n"
            "If you encounter a sample, you get a speed boost.\n"
            "If you encounter the freezer section, you slow down.\n"
            "Your goal to win the game is to reach the churro stand before the AI shopper does.\n"
            "Good Luck.\n"
            "Press space to continue"
        )

        # Render text with the current font size and line spacing
        start_text = self.render_multiline_text(instructions, start_font, line_spacing)

        # Calculate text size and position
        text_width, text_height = start_text.get_size()
        start_rect = start_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Adjust font size and line spacing to fit within the window
        while text_width > max_width or text_height > max_height:
            font_size -= 2
            line_spacing -= 1
            start_font = pygame.font.Font(None, font_size)
            start_text = self.render_multiline_text(instructions, start_font, line_spacing)
            text_width, text_height = start_text.get_size()
            start_rect = start_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Clear the screen
        self.screen.fill(self.BACKGROUND_COLOR)

        # Display the text on the screen
        self.screen.blit(start_text, start_rect)

        # Update the display
        pygame.display.flip()

        # Wait for any key press to start the game
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting_for_key = False

    def render_multiline_text(self, text, font, line_spacing):
        lines = text.split('\n')
        rendered_lines = []

        for line in lines:
            rendered_lines.append(font.render(line, True, (255, 255, 255)))

        total_height = sum([line.get_height() for line in rendered_lines])
        rendered_text = pygame.Surface((max(line.get_width() for line in rendered_lines), total_height), pygame.SRCALPHA)

        y = 0
        for line in rendered_lines:
            rendered_text.blit(line, (0, y))
            y += line.get_height() + line_spacing

        return rendered_text
        

if __name__ == "__main__":
    game = MangoGame()
    game.run()
