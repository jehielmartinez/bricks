import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE

# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bricks")
clock = pygame.time.Clock()

# Load images
paddle_img = pygame.image.load("./images/paddle.png").convert_alpha()
ball_img = pygame.image.load("./images/football.png").convert_alpha()
brick_img = pygame.image.load("./images/brick.png").convert_alpha()

# Paddle setup
paddle_rect = paddle_img.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() - 10))

# Ball setup
ball_rect = ball_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
ball_speed = [300, 300]  # pixels per second
ball_served = False

# Brick setup
brick_rect = brick_img.get_rect()
brick_gap = 5
brick_rows = 5
brick_cols = screen.get_width() // (brick_rect.width + brick_gap)
side_gap = (screen.get_width() - (brick_cols * (brick_rect.width + brick_gap))) // 2

bricks = [(x * (brick_rect.width + brick_gap) + side_gap, y * (brick_rect.height + brick_gap))
          for y in range(brick_rows) for x in range(brick_cols)]

def draw_bricks():
    for brick_pos in bricks:
        screen.blit(brick_img, brick_pos)

def handle_events():
    global ball_served
    for event in pygame.event.get():
        if event.type == QUIT:
            return True
        if event.type == KEYDOWN and event.key == K_SPACE:
            ball_served = True
    return False

def move_paddle(dt):
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        paddle_rect.x -= 500 * dt
    if keys[K_RIGHT]:
        paddle_rect.x += 500 * dt
    paddle_rect.clamp_ip(screen.get_rect())

def move_ball(dt):
    global ball_served
    if ball_served:
        ball_rect.x += ball_speed[0] * dt
        ball_rect.y += ball_speed[1] * dt

        if ball_rect.left <= 0 or ball_rect.right >= screen.get_width():
            ball_speed[0] *= -1
        if ball_rect.top <= 0:
            ball_speed[1] *= -1
        if ball_rect.colliderect(paddle_rect):
            ball_rect.bottom = paddle_rect.top
            ball_speed[1] *= -1
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                ball_speed[0] -= 10
            if keys[K_RIGHT]:
                ball_speed[0] += 10

        for brick_pos in bricks[:]:
            brick_rect.topleft = brick_pos
            if ball_rect.colliderect(brick_rect):
                bricks.remove(brick_pos)
                ball_speed[1] *= -1
                break

        if ball_rect.bottom >= screen.get_height():
            ball_served = False
            ball_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            ball_speed[:] = [300, 300]

# Main game loop
game_running = True
while game_running:
    dt = clock.tick(60) / 1000  # seconds since last frame
    screen.fill((0, 0, 0))
    game_running = not handle_events()
    draw_bricks()
    screen.blit(ball_img, ball_rect)
    screen.blit(paddle_img, paddle_rect)
    move_paddle(dt)
    move_ball(dt)
    pygame.display.flip()

pygame.quit()
