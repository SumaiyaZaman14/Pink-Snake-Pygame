import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 720, 520
CELL = 20
COLS, ROWS = WIDTH // CELL, HEIGHT // CELL

BG = (255, 214, 225)       # baby pink
GREEN = (55, 150, 75)
DARK_GREEN = (35, 115, 55)
GOLD = (245, 190, 45)
OBSTACLE = (120, 95, 105)
TEXT = (70, 55, 65)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pink Snake")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 34)
big_font = pygame.font.Font(None, 64)


def new_position(blocked):
    available = [
        (x, y)
        for x in range(COLS)
        for y in range(ROWS)
        if (x, y) not in blocked
    ]
    return random.choice(available)


def reset():
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)
    next_direction = direction

    obstacles = set()
    while len(obstacles) < 8:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            obstacles.add(pos)

    coin = new_position(set(snake) | obstacles)
    score = 0
    return snake, direction, next_direction, obstacles, coin, score


snake, direction, next_direction, obstacles, coin, score = reset()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                next_direction = (1, 0)
            elif event.key == pygame.K_r and game_over:
                snake, direction, next_direction, obstacles, coin, score = reset()
                game_over = False

    if not game_over:
        direction = next_direction
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        hit_self = new_head in snake
        hit_obstacle = new_head in obstacles

        if hit_wall or hit_self or hit_obstacle:
            game_over = True
        else:
            snake.insert(0, new_head)

            if new_head == coin:
                score += 1
                blocked = set(snake) | obstacles
                coin = new_position(blocked)
            else:
                snake.pop()

    screen.fill(BG)

    # Obstacles
    for x, y in obstacles:
        rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(screen, OBSTACLE, rect, border_radius=5)

    # Coin
    cx, cy = coin
    pygame.draw.circle(
        screen, GOLD,
        (cx * CELL + CELL // 2, cy * CELL + CELL // 2),
        CELL // 3
    )

    # Snake
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x * CELL + 2, y * CELL + 2, CELL - 4, CELL - 4)
        pygame.draw.rect(
            screen,
            DARK_GREEN if i == 0 else GREEN,
            rect,
            border_radius=6
        )

    score_text = font.render(f"Coins: {score}", True, TEXT)
    screen.blit(score_text, (15, 12))

    controls = font.render("Move: Arrow Keys / WASD", True, TEXT)
    screen.blit(controls, (WIDTH - controls.get_width() - 15, 12))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 214, 225, 190))
        screen.blit(overlay, (0, 0))

        title = big_font.render("GAME OVER", True, TEXT)
        restart = font.render("Press R to restart", True, TEXT)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))

    pygame.display.flip()
    clock.tick(7)
