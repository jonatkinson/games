import pygame


def text(screen, font, msg, x, y, color):
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

