import pygame
import sys

from engine import colors
from globals import font, screen

def message(primary_message, secondary_message=False):
    """
    This displays the title screen.
    """

    # Blank the screen.
    screen.fill(colors.BLACK)
    pygame.time.wait(500)

    # Display the primary message
    primary = font.render(primary_message, False, colors.ORANGE)
    primary_rect = primary.get_rect(center=(320, 170))
    screen.blit(primary, primary_rect)

    # Render
    pygame.display.flip()
    pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/collide.wav'))
    pygame.time.wait(1000)

    # Display the secondary message.
    if secondary_message:
        secondary = font.render(secondary_message, False, colors.WHITE)
        secondary_rect = secondary.get_rect(center=(320, 240))
        screen.blit(secondary, secondary_rect)

    # Render
    pygame.display.flip()
    pygame.mixer.Sound.play(pygame.mixer.Sound('sounds/collide.wav'))
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


def text(screen, msg, x, y, color):
    """
    This renders text.
    """

    t = font.render(msg, False, color)
    screen.blit(t, (x, y))


def tile(screen, x, y, color):
    """
    This renders a tile; our graphics primitive.
    """

    pygame.draw.rect(
        screen, 
        pygame.Color(color), 
        pygame.Rect(
            x * 20, 
            y * 20,
            20, 
            20
        )
    )


def box(screen, x, y, sx, sy, color):
    """
    This renders a box of a given size.
    """

    pygame.draw.rect(
        screen, 
        pygame.Color(color), 
        pygame.Rect(x, y, sx, sy)
    )

