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
       


def check_quit():
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

while not game_over:
  dt = clock.tick(60)
  screen.fill((0, 0, 0))
  draw_bricks()
  draw_paddle()
  move_paddle(dt)
  game_over = check_quit()
  pygame.display.update()
pygame.quit()
