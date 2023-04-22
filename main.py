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
paddle_rect[0] = screen.get_width() // 2 - paddle_rect[2] // 2

# Ball
ball = pygame.image.load("./images/football.png").convert_alpha()
ball_rect = ball.get_rect()
ball_start = (screen.get_width() // 2, screen.get_height() // 2)
ball_speed = (0.3, 0.3)
ball_served = False
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

# Game State
game_state = {
    "ball_served": False,
    "ball_rect": ball_rect,
    "dt": 0,
    "paddle_rect": paddle_rect,
    "sx": ball_speed[0],
    "sy": ball_speed[1],
}
       
def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def draw_bricks():
    for b in bricks:
        screen.blit(brick, b)

def draw_paddle():
    screen.blit(paddle, game_state["paddle_rect"])

def move_paddle():
    if game_state["ball_served"]:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
          game_state["paddle_rect"][0] -= 1 * game_state["dt"]
      if keys[pygame.K_RIGHT]:
          game_state["paddle_rect"][0] += 1 * game_state["dt"]
      if game_state["paddle_rect"][0] < 0:
          game_state["paddle_rect"][0] = 0
      if game_state["paddle_rect"][0] > screen.get_width() - game_state["paddle_rect"][2]:
          game_state["paddle_rect"][0] = screen.get_width() - game_state["paddle_rect"][2]

def draw_ball():
    screen.blit(ball, game_state["ball_rect"])

def move_ball():
    if game_state["ball_served"]:
        game_state["ball_rect"][0] += game_state["sx"] * game_state["dt"]
        game_state["ball_rect"][1] += game_state["sy"] * game_state["dt"]
    # if bounce left
    if game_state["ball_rect"][0] <= 0:
        game_state["ball_rect"][0] = 0
        game_state["sx"] *= -1
    # if bounce right
    if game_state["ball_rect"][0] >= screen.get_width() - game_state["ball_rect"][2]:
        game_state["ball_rect"][0] = screen.get_width() - game_state["ball_rect"][2]
        game_state["sx"] *= -1
    # if bounce top
    if game_state["ball_rect"][1] <= 0:
        game_state["ball_rect"][1] = 0
        game_state["sy"] *= -1
    # if bounce bottom
    if game_state["ball_rect"][1] >= screen.get_height() - game_state["ball_rect"][3]:
        # set initial state
        game_state["ball_served"] = False
        game_state["ball_rect"] = ball_rect
        game_state["sx"] = ball_speed[0]
        game_state["sy"] = ball_speed[1]
        game_state["paddle_rect"] = paddle_rect
        game_state["ball_rect"].topleft = ball_start
    # if bounce paddle
    if ball_rect.colliderect(paddle_rect):
        game_state["ball_rect"][1] = paddle_rect[1] - game_state["ball_rect"][3]
        game_state["sy"] *= -1

def handle_serve():
    if game_state["ball_served"]:
        game_state["ball_served"] = True
        return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_state["ball_served"] = True
        return
    game_state["ball_served"] = False

def increase_dificulty(delta = 0.1):
    if game_state["sy"] > 0:
        game_state["sy"] += delta
    else:
        game_state["sy"] -= delta

while not game_over:
  game_state["dt"] = clock.tick(50)
  screen.fill((0, 0, 0))
  handle_serve()
  draw_bricks()
  draw_ball()
  draw_paddle()
  increase_dificulty(0.0001)
  move_paddle()
  move_ball()
  game_over = handle_quit()
  pygame.display.update()
pygame.quit()
