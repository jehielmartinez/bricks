import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bricks")

clock = pygame.time.Clock()
game_over = False

# Paddle
paddle = pygame.image.load("./images/paddle.png").convert_alpha()
paddle_rect = paddle.get_rect()

# Ball
ball = pygame.image.load("./images/football.png").convert_alpha()
ball_rect = ball.get_rect()

# Bricks
brick = pygame.image.load("./images/brick.png").convert_alpha()
brick_rect = brick.get_rect()


def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

while not game_over:
    dt = clock.tick(60)
    screen.fill((0, 0, 0))
    game_over = check_quit()

pygame.quit()
