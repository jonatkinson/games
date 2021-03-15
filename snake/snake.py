import sys
import pygame
import random

from levels import level_data

colours = {
    'black': (0, 0, 0),
    'orange': (255, 95, 0),
    'white': (255, 255, 255)
}

class Snake():

    body = []
    growing = False
    direction = False


    def proceed(self):
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

            # Increment the score, place some new food.
            game.score += 1
            game.food = game.empty_location()

            # Our snake will grow next turn.
            self.growing = True

        # If we have hit a wall...
        for y, data in enumerate(game.level):
            for x, tile in enumerate(data):
                if tile == "#":
                    if [x, y] == head:
                        game.lives -= 1
                        self.body = [game.empty_location()]
                        self.direction = False

        # If the snake hits itself.
        if head in self.body[1:]:
            game.lives -= 1
            self.body = [game.empty_location()]
            self.direction = False


class SnakeGame():
    """
    The main game class.
    """

    WIDTH = 640
    HEIGHT = 480

    GAME_OFFSET_X = 200
    GAME_OFFSET_Y = 40

    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    ORANGE = (255, 95, 0)
    PURPLE = (128, 0, 128)

    def __init__(self):
        """
        Sets up the environment, and then starts the game.
        """

        pygame.init()

        # Infrastructure stuff.
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('slkscr.ttf', 24)

        # Game stuff.
        while True:
            self.title()
            self.game()
            self.gameover()

    def title(self):
        """
        This displays the title screen.
        """

        # Display the title.
        title = self.font.render("SNAKE", False, self.ORANGE)
        title_rect = title.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2 - 72))
        self.screen.blit(title, title_rect)

        # Display the help.
        help = self.font.render("Press any key to start", False, self.WHITE)
        help_rect = help.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(help, help_rect)

        # Display the title screen.
        pygame.display.flip()

        wait = True
        while wait:
            for event in pygame.event.get():

                # Handle window close.
                if event.type == pygame.QUIT: 
                    sys.exit()

                # Handle any other key (to start the game).
                if event.type == pygame.KEYDOWN:
                    wait = False

    def game(self):
        """
        This plays the main game.
        """

        # Setup the game state.
        self.lives = 5
        self.score = 0

        # Setup the level.
        self.level_number = 0
        self.level = level_data[self.level_number]

        # Setup the snake.
        self.snake = Snake()
        self.snake.body = [self.empty_location()]

        # Setup some food.
        self.food = self.empty_location()

        while True:

            # Handle window close.
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Handle ESC key.
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                sys.exit()

            # Handle input
            key_pressed = False
            if pygame.key.get_pressed()[pygame.K_UP]:
                key_pressed = True
                self.snake.up()

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                key_pressed = True
                self.snake.down()

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                key_pressed = True
                self.snake.left()

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                key_pressed = True
                self.snake.right()

            # If there was no input, proceed in the current direction.
            if not key_pressed:
                self.snake.proceed()

            # Collide the snake (pass the SnakeGame instance).
            self.snake.collide(self)

            # Check some game state.
            if self.score == 10:

                self.level_number += 1
                self.level = level_data[self.level_number]

                self.snake = Snake()
                self.snake.body = [self.empty_location()]

                self.food = self.empty_location()
                self.score = 0

            # Render the screen.
            self.draw()
            self.clock.tick(10)
    
    def gameover(self):
        pass


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
                x * 20 + self.GAME_OFFSET_X, 
                y * 20 + self.GAME_OFFSET_Y, 
                20, 
                20
            )
        )


    def draw(self):
        """
        This renders the current game state.
        """

        # Blank the screen.
        self.screen.fill(self.BLACK)

        # Draw the status panel
        status = self.font.render(f"LEVEL {self.level_number}", False, self.ORANGE)
        self.screen.blit(status, (40, 40))

        lives = self.font.render(f"LIVES {self.lives}", False, self.WHITE)
        self.screen.blit(lives, (40, 70))

        score = self.font.render(f"SCORE {self.score}", False, self.WHITE)
        self.screen.blit(score, (40, 100))

        # Iterate through the level data, draw the map and snake.
        for y, data in enumerate(self.level):
            for x, tile in enumerate(data):

                # Draw walls.
                if tile == "#":
                    self.draw_box(x, y, self.WHITE)

                # Draw food.
                if [x, y] == self.food:
                    self.draw_box(x, y, self.PURPLE)

                # Draw snake.
                if [x, y] in self.snake.body:
                    self.draw_box(x, y, self.ORANGE)

        pygame.display.flip()

sg = SnakeGame()