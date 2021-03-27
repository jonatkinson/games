import sys

import pygame

from engine import colors, draw, util


from tetraminos import tetraminos

class TetrisGame():
    """
    The main game class.
    """

    playfield = False
    score = 0
    level = 0


    def __init__(self):
        """
        Sets up the environment, and then starts the game.
        """

        pygame.init()

        # Infrastructure stuff.
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/slkscr.ttf', 24) 
        self.mixer = pygame.mixer.init()


        i = 0
        f = 0

        while True:

            # Clear the screen.
            self.screen.fill(colors.BLACK)

            for event in pygame.event.get():

                # Handle window close.
                if event.type == pygame.QUIT: 
                    sys.exit()


            if pygame.key.get_pressed()[pygame.K_UP]:
                i += 1

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                i -= 1

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                f -= 1

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                f += 1

            # Don't go out of bounds.
            if i < 0: i = len(tetraminos) - 1
            if i >= len(tetraminos): i = 0

            if f < 0: f = len(tetraminos[i]['frames']) - 1
            if f >= len(tetraminos[i]['frames']): f = 0

            print(f"tetramino {i}, frame {f}")           

            data = tetraminos[i]['frames'][f]

            for y, data_y in enumerate(util.chunks(data, tetraminos[i]['size'])):
                for x, data_x in enumerate(data_y):
                    
                    if data_x == 0:
                        color = colors.BLACK
                    if data_x == 1:
                        color = tetraminos[i]['color']

                    print(f"{x},{y}: {data_x}")

                    draw.box(self.screen, x, y, color)

            # Status message.
            msg = self.font.render(f"Tetramino {i} in position {f}", False, colors.ORANGE)
            msg_rect = msg.get_rect(center=(320, 50))
            self.screen.blit(msg, msg_rect)

            pygame.display.flip()
            self.clock.tick(10)

    def advance():
        """
        This advances the game.
        """

        # Drop active play piece.
        # Check for collisions.
        # Check for completed lines.

    def render():
        """
        This renders the current game.
        """

        # Draw the statusbar.
        # Draw the game frame.
        # Draw the playfield.
        


tg = TetrisGame()
