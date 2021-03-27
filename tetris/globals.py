import pygame

# Infrastructure stuff.
pygame.init()

# Setup resources.
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/slkscr.ttf', 24) 
mixer = pygame.mixer.init()

pygame.key.set_repeat(250, 250)
