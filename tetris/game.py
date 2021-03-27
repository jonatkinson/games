import sys
import copy
import pygame

from globals import screen, clock, mixer, font
from engine import colors, draw, util, array

import piece

class TetrisGame():
    """
    The main game class.

    Some playfield data values:

    0 - empty space
    1 - border.
    2 - settled piece
    3 - active piece
    """
    
    def __init__(self):
        """
        Sets up the environment, and then starts the game.
        """

        # The playfield data. We build this large, then insert a
        # smaller, blank array to make room for the inner play.
        inner_playfield = array.TwoDArray(10, 20, -1)
        self.playfield = array.TwoDArray(12, 22, 1)
        self.playfield.combine(inner_playfield, 1, 1)        

        # The current and next pieces.
        self.current = piece.random_piece()
        self.next = piece.random_piece()

        # The current piece position.
        self.current_x = 4
        self.current_y = 1

        # Some game status.
        self.linescore = 0
        self.level = 0
        self.ticks = 0
        self.collided_previous_tick = 0

        # Title screen.
        draw.message("TETRIS", "Press key")
        draw.message("Arrows: Move    Z/X: Rotate", "Press key")

        # The main game loop.
        while self.level >= 0:
            self.input()
            self.advance()
        
        # Game over and quit.
        draw.message("Game Over", "Press key")
        sys.exit()

    def input(self):
        """
        This registers input.
        """

        current_time = pygame.time.get_ticks()

        # This handles a game input cycle: the game difficulty is increased 
        # here by reducing this number.
        while pygame.time.get_ticks() < current_time + 1000 - (self.level * 100):

            action = False

            # Make a copy of the game state, pre-input.
            previous_current_x = self.current_x
            previous_current_y = self.current_y
            previous_playfield = copy.deepcopy(self.playfield)

            for event in pygame.event.get():
                # Handle window close.
                if event.type == pygame.QUIT: 
                    sys.exit()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                action = True
                if self.current_y <= 18:
                    self.current_y += 1

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                action = True
                self.current_x -= 1

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                action = True
                self.current_x += 1

            if pygame.key.get_pressed()[pygame.K_z]:
                action = "clockwise"
                self.current.clockwise()

            if pygame.key.get_pressed()[pygame.K_x]:
                action = "counterclockwise"
                self.current.counterclockwise()

            # Remove any stale piece data.
            self.playfield.replace(3, 0)

            # Insert the game piece.
            try:
                self.playfield.combine(self.current.frame(), self.current_x, self.current_y)
            except IndexError:
                self.playfield = copy.deepcopy(previous_playfield)
                self.current_x -= 1
                self.current_y -= 1

            # If an action was taken...
            if action:
                # Check for collisions. If there is a collision, then we reset
                # to our previous state (hence, undoing the movement).
                if self.collide():

                    # Reset the playfield back to it's previous state.
                    self.playfield = copy.deepcopy(previous_playfield)
                    self.current_x = previous_current_x
                    self.current_y = previous_current_y

                    # If the collision was a rotation, reverse it.
                    if action == "clockwise": self.current.counterclockwise()
                    if action == "counterclockwise": self.current.clockwise()
                else:
                    # Re-render.
                    self.render()

                # Slight delay before the next action.
                # For some reason, a longer delay after a spin feels better.
                if action in ["clockwise", "counterclockwise"]:
                    pygame.time.wait(150)
                else:
                    pygame.time.wait(75)

                # Reset the action.
                action = False



    def collide(self):
        """
        This checks for collisions on the playfield. This is done by combining
        the value of the active piece array items, and the playfield array items,
        and anything > 3 will indicate where the active piece intersects with 
        another item on the playfield. We then reverse the movement back in input().
        """

        for d in self.playfield.data:
            if d > 3: 
                return True
        return False


    def advance(self):
        """
        This advances the game.
        """

        # Increase game ticks.
        self.ticks += 1

        # Copy the current playfield state.
        previous_playfield = copy.deepcopy(self.playfield)

        # Drop active play piece.
        self.current_y += 1

        # Remove any stale piece data.
        for i, d in enumerate(self.playfield.data):
            if d == 3: self.playfield.data[i] = 0

        # Insert the game piece.
        try:
            self.playfield.combine(self.current.frame(), self.current_x, self.current_y)
        except IndexError:
            self.playfield = copy.deepcopy(previous_playfield)
            self.current_y -= 1

        # Check for collisions.
        if self.collide():

            # Reset the playfield.
            self.playfield = copy.deepcopy(previous_playfield)

            # Convert active blocks to settled blocks.
            if self.playfield.replace(3, 2):
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/collide.wav'))

            # Prepare for gameover condition.
            if self.collided_previous_tick > 3:
                self.level = -1
            self.collided_previous_tick += 1

            # Check for lines.
            self.lines()

            # Reset a new piece.
            self.current_y = 1
            self.current_x = 4
            self.current = copy.deepcopy(self.next)
            self.next = piece.random_piece()
        else:
            self.collided_previous_tick = 0

        self.render()


    def lines(self):
        """
        This scans for completed lines.
        """

        complete_lines = []
        for y in range(1, 21):
            complete_line = True
            for x in range(1, 11):
                if self.playfield.get(x, y) == 0:
                    complete_line = False
            if complete_line:
                complete_lines.append(y)

        if complete_lines:

            # Play sound
            for s in range(len(complete_lines)):
                pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/collect.wav'))

            # Flash lines
            flashes = 0
            while flashes < 4:
                for y in complete_lines:
                    for x in range(1, 11):
                        self.playfield.set(x, y, 1)
                self.render()
                pygame.time.wait(75)
                for y in complete_lines:
                    for x in range(1, 11):
                        self.playfield.set(x, y, 3)
                self.render()
                pygame.time.wait(75)                    
                flashes += 1

            # Remove lines
            for y in complete_lines:
                above = self.playfield.slice(1, 1, 11, y)
                
                # Drop everything down.
                self.playfield.insert(above, 1, 2)

                # Fill the first row with empty data.
                for x in range(1, 11):
                    self.playfield.set(x, 1, 0)

            # Add to score.
            for l in range(len(complete_lines)):
                self.linescore += 1
                # Increase the level.
                if self.linescore % 10 == 0:
                    self.level += 1

    def render(self):
        """
        This renders the current game.
        """

        # Blank the screen.
        screen.fill(colors.BLACK)

        # Draw the status.
        draw.text(screen, f"Level: {self.level + 1}", 20, 20, colors.ORANGE)
        draw.text(screen, f"Lines: {self.linescore}", 20, 50, colors.ORANGE)
        draw.text(screen, f"Next:", 20, 80, colors.ORANGE)

        # Draw the next piece.
        for x in range(self.next.frame().sx):
            for y in range(self.next.frame().sy):
                try:
                    d = self.next.frame().get(x, y)
                    if d == 3:
                        draw.tile(screen, x + 1, y + 6, colors.ORANGE) 
                except IndexError:
                    continue

        # Draw the playfield.
        for x in range(self.playfield.sx):
            for y in range(self.playfield.sy):

                d = self.playfield.get(x, y)

                if d == 0: 
                    draw.tile(screen, x + 17, y + 1, colors.BLACK)

                if d == 1:
                    draw.tile(screen, x + 17, y + 1, colors.WHITE)

                if d == 2:
                    draw.tile(screen, x + 17, y + 1, colors.ORANGE)

                if d >= 3:
                    draw.tile(screen, x + 17, y + 1, colors.PURPLE)

        # Done.
        pygame.display.flip()

