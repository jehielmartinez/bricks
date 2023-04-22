import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bricks")

clock = pygame.time.Clock()
game_over = False

# Paddle
paddle = pygame.image.load("./images/paddle.png").convert_alpha()
paddle_rect = paddle.get_rect()
paddle_rect[1] = screen.get_height() - paddle_rect[3]

# Ball
ball = pygame.image.load("./images/football.png").convert_alpha()
ball_rect = ball.get_rect()
ball_start = (screen.get_width() // 2, screen.get_height() // 1)
ball_speed = (-0.3, -0.3)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start

# Bricks
brick = pygame.image.load("./images/brick.png").convert_alpha()
brick_rect = brick.get_rect()
bricks = []
bricks_gap = 5
brick_plus_gap = brick_rect[2] + bricks_gap
brick_rows = 5
brick_cols = (screen.get_width() // brick_plus_gap)

side_gap = (screen.get_width() - (brick_cols * brick_plus_gap) + bricks_gap) // 2

for y in range(brick_rows):
    brickY = y * (brick_rect[3] + bricks_gap)
    for x in range(brick_cols):
        brickX = x * (brick_rect[2] + bricks_gap) + side_gap
        bricks.append((brickX, brickY))
       


def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def draw_bricks():
    for b in bricks:
        screen.blit(brick, b)

def draw_paddle():
    screen.blit(paddle, paddle_rect)

def move_paddle(dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_rect[0] -= 5 * dt
    if keys[pygame.K_RIGHT]:
        paddle_rect[0] += 5 * dt
    if paddle_rect[0] < 0:
        paddle_rect[0] = 0
    if paddle_rect[0] > screen.get_width() - paddle_rect[2]:
        paddle_rect[0] = screen.get_width() - paddle_rect[2]

def draw_ball():
    screen.blit(ball, ball_rect)

def move_ball(dt, ball_served, sx, sy):
    if ball_served:
        ball_rect[0] += sx * dt
        ball_rect[1] += sy * dt
    # if bounce left
    if ball_rect[0] <= 0:
        ball_rect[0] = 0
        sx *= -1
    # if bounce right
    if ball_rect[0] >= screen.get_width() - ball_rect[2]:
        ball_rect[0] = screen.get_width() - ball_rect[2]
        sx *= -1
    # if bounce top
    if ball_rect[1] <= 0:
        ball_rect[1] = 0
        sy *= -1
    # if bounce bottom
    if ball_rect[1] >= screen.get_height() - ball_rect[3]:
        ball_rect[1] = screen.get_height() - ball_rect[3]
        sy *= -1
    return sx, sy

def handle_serve(current_serve):
    if current_serve:
        return True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return True
    return False

while not game_over:
  dt = clock.tick(50)
  screen.fill((0, 0, 0))
  draw_bricks()
  draw_ball()
  draw_paddle()
  move_paddle(dt)
  sx, sy = move_ball(dt, ball_served, sx, sy)
  ball_served = handle_serve(ball_served)
  game_over = handle_quit()
  pygame.display.update()
pygame.quit()
