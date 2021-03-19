import sys
import pygame
import random

from pygame import color

from levels import level_data

colors = {
    'WHITE': (255, 255, 255),
    'BLACK': (0,0,0),
    'ORANGE': (255, 95, 0),
    'PURPLE': (128, 0, 128)
}

class Snake():

    body = []
    growing = False
    direction = False
    color = colors['ORANGE']

    def move(self):
        if self.direction == "up":
            self.up()
        if self.direction == "down":
            self.down()
        if self.direction == "left":
            self.left()
        if self.direction == "right":
            self.right()

    def up(self):
        if self.direction == "down":
            return
        self.direction = "up"
        self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def down(self):
        if self.direction == "up":
            return
        self.direction = "down"
        self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def left(self):
        if self.direction == "right":
            return
        self.direction = "left"
        self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def right(self):
        if self.direction == "left":
            return
        self.direction = "right"
        self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def collide(self, game):
        """
        Handles snake collisions (with walls, food, and tail)
        """

        head = [self.body[0][0], self.body[0][1]]

        # If we have got the food...
        if head == game.food:

            # Play sound
            pygame.mixer.Sound.play(pygame.mixer.Sound('collect.wav'))

            # Increment the score, place some new food.
            game.score += 1
            game.food = game.empty_location()

            # Our snake will grow next turn.
            self.growing = True

            return False

        # If we have hit a wall...
        for y, data in enumerate(game.level):
            for x, tile in enumerate(data):
                if tile == "#":
                    if [x, y] == head:
                        pygame.mixer.Sound.play(pygame.mixer.Sound('collide.wav'))
                        game.lives -= 1
                        self.body = [game.empty_location()]
                        self.direction = False
                        return True

        # If the snake hits itself.
        if head in self.body[1:]:
            pygame.mixer.Sound.play(pygame.mixer.Sound('collide.wav'))
            game.lives -= 1
            self.body = [game.empty_location()]
            self.direction = False
            return True


class SnakeGame():
    """
    The main game class.
    """

    def __init__(self):
        """
        Sets up the environment, and then starts the game.
        """

        pygame.init()

        # Infrastructure stuff.
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('slkscr.ttf', 24) 
        self.mixer = pygame.mixer.init()

        # Game stuff.
        while True:
            self.message("SNAKE.", "Press a key to begin.")
            self.game()
            self.message("GAME OVER.")


    def setup_level(self, level_number):
        """
        This handles setting up the state for a new level.
        """

        # Load the level.
        self.level = level_data[self.level_number]

        # Setup the snake in an empty location.
        self.snake = Snake()
        self.snake.body = [self.empty_location()]

        # Set the score.
        self.score = 0

        # Show the level message.
        self.message(f"Level {self.level_number + 1}.", f"Score 10 points. {self.lives} lives left.")

        # Setup some food.
        self.food = self.empty_location()

        # Flash the before we hand control to the player.
        for color in [colors['ORANGE'], colors['BLACK'], colors['ORANGE'], colors['BLACK']]:
            self.render(snake_color=color)
            pygame.time.wait(300)
            

    def game(self):
        """
        This plays the main game.
        """

        # Setup some global game state.
        self.lives = 5

        # Setup the level.
        self.level_number = 0
        self.setup_level(self.level_number)

        while True:

            # Handle window close.
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Handle ESC key.
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

            # Handle input, and set the snake direction.
            # The snake can never reverse direction.
            if pygame.key.get_pressed()[pygame.K_UP]:
                if not self.snake.direction == "down":
                    self.snake.direction = "up"

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if not self.snake.direction == "up":
                    self.snake.direction = "down"

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if not self.snake.direction == "right":
                    self.snake.direction = "left"

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not self.snake.direction == "left":
                    self.snake.direction = "right"

            # Implement the movement.
            self.snake.move()

            # Collide the snake (pass the SnakeGame instance).
            if self.snake.collide(self):
                self.setup_level(self.level_number)

            # A collision may have resulted in a game over.
            if self.lives == 0:
                return

            # Check some game state.
            if self.score == 10:

                self.level_number += 1
                self.setup_level(self.level_number)

            # Render the screen.
            self.render()
            self.clock.tick(10)


    def message(self, primary_message, secondary_message=False):
        """
        This displays the title screen.
        """

        # Blank the screen.
        self.screen.fill(colors['BLACK'])
        pygame.time.wait(500)

        # Display the primary message
        primary = self.font.render(primary_message, False, colors['ORANGE'])
        primary_rect = primary.get_rect(center=(320, 170))
        self.screen.blit(primary, primary_rect)

        # Render
        pygame.display.flip()
        pygame.mixer.Sound.play(pygame.mixer.Sound('collide.wav'))
        pygame.time.wait(1000)

        # Display the secondary message.
        if secondary_message:
            secondary = self.font.render(secondary_message, False, colors['WHITE'])
            secondary_rect = secondary.get_rect(center=(320, 240))
            self.screen.blit(secondary, secondary_rect)

        # Render
        pygame.display.flip()
        pygame.mixer.Sound.play(pygame.mixer.Sound('collide.wav'))
        pygame.time.wait(1000)

        wait = True
        while wait:
            for event in pygame.event.get():

                # Handle window close.
                if event.type == pygame.QUIT: 
                    sys.exit()

                # Handle any other key (to start the game).
                if event.type == pygame.KEYDOWN:
                    wait = False

    def empty_location(self):
        """
        Finds an empty spot on the playfield to place food.
        """

        found = False
        while not found:

            # Generate a location for the food.
            possible_x = random.randint(0, 20)
            possible_y = random.randint(0, 20)

            # Check if the location is valid.
            for y, data in enumerate(self.level):
                for x, tile in enumerate(data):
                    if x == possible_x and y == possible_y:
                        # If the tile empty?
                        if tile == " ":
                            # Is the tile occupted by the snakes body?
                            if not [possible_x, possible_y] in self.snake.body:
                                found = True

        return [possible_x, possible_y]


    def draw_box(self, x, y, color):
        """
        This renders a box; our graphics primitive.
        """

        pygame.draw.rect(
            self.screen, 
            pygame.Color(color), 
            pygame.Rect(
                x * 20 + 200, # offset the playfield by 200px. 
                y * 20 + 40, # offset the playfield by 40px.
                20, 
                20
            )
        )


    def render(self, snake_color=colors['ORANGE']):
        """
        This renders the current game state.
        """

        # Blank the screen.
        self.screen.fill(colors['BLACK'])

        # Draw the status panel
        status = self.font.render(f"LEVEL {self.level_number + 1}", False, colors['ORANGE'])
        self.screen.blit(status, (40, 40))

        lives = self.font.render(f"LIVES {self.lives}", False, colors['WHITE'])
        self.screen.blit(lives, (40, 70))

        score = self.font.render(f"SCORE {self.score}", False, colors['WHITE'])
        self.screen.blit(score, (40, 100))

        # Iterate through the level data, draw the map and snake.
        for y, data in enumerate(self.level):
            for x, tile in enumerate(data):

                # Draw walls.
                if tile == "#":
                    self.draw_box(x, y, colors['WHITE'])

                # Draw food.
                if self.food:
                    if [x, y] == self.food:
                        self.draw_box(x, y, colors['PURPLE'])

                # Draw snake.
                if [x, y] in self.snake.body:
                    self.draw_box(x, y, snake_color)

        pygame.display.flip()

sg = SnakeGame()