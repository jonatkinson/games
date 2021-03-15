import sys
import pygame
import random


paddle = {
    'position': 100,
    'size': 60,
    'score': 0
}

ball = {
    'position': {
        'x': 50,
        'y': 50
    },
    'vector': {
        'x': 2,
        'y': 2
    },
    'size': 6
}

colours = {
    'black': (0, 0, 0),
    'orange': (255, 95, 0),
    'white': (255, 255, 255)
}

size = width, height = 320, 240

pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Cascadia Mono', 30)

while True:

    # Handle window close.
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Handle input
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        paddle['position'] -= 4
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        paddle['position'] += 4

    # Limit paddle movement.
    if paddle['position'] < 10:
        paddle['position'] = 10
    if paddle['position'] > width - paddle['size'] - 10:
        paddle['position'] = width - paddle['size'] - 10

    # Move the ball.
    ball['position']['x'] += ball['vector']['x']
    ball['position']['y'] += ball['vector']['y']

    # Handle edge collision horizontally.
    if ball['position']['x'] <= 0 or ball['position']['x'] >= width:
        ball['vector']['x'] = -ball['vector']['x']

    # Handle top edge collision
    if ball['position']['y'] <= 0:
        ball['vector']['y'] = -ball['vector']['y']

    # Handle bottom collision, reset the ball.
    if ball['position']['y'] >= height:
        ball['position']['x'] = random.randint(0, width)
        ball['position']['y'] = random.randint(0, 50)
        ball['vector']['x'] = 2
        ball['vector']['y'] = 2
        paddle['score'] = 0

    # Handle paddle collision
    if ball['position']['y'] >= height - 16:
        if ball['position']['x'] >= paddle['position'] and ball['position']['x'] <= (paddle['position'] + paddle['size']):
            ball['position']['y'] = height - 16
            ball['vector']['y'] = -ball['vector']['y']

            # Add to the score.
            paddle['score'] += 1

            # Every 5 points, increase the difficulty.
            if paddle['score'] % 5 == 0:
                ball['vector']['x'] = ball['vector']['x'] * 1.5
                ball['vector']['y'] = ball['vector']['y'] * 1.5

    # Clear the screen.
    screen.fill(colours['black'])

    # Draw the paddle.
    pygame.draw.rect(
        screen, 
        pygame.Color(colours['white']), 
        pygame.Rect(paddle['position'], height - 16 , paddle['size'], 6)
    )

    # Draw the ball.
    pygame.draw.rect(
        screen, 
        pygame.Color(colours['orange']), 
        pygame.Rect(
            ball['position']['x'] - (ball['size'] / 2), 
            ball['position']['y'] - (ball['size'] / 2), 
            ball['size'], 
            ball['size']
        )
    )

    # Draw the score.
    status = font.render(str(paddle['score']), False, colours['white'])
    screen.blit(status,(5,5))

    # Render everything.
    pygame.display.flip()
    clock.tick(60)