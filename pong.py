import sys

import pygame
from pygame.locals import *

FPS = 100
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

LINE_THICKNESS = 20
PADDLE_HEIGHT = 50
PADDLE_OFFSET = 20
PADDLE_VY = 3

# colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BG_COLOR = BLACK
ARENA_COLOR = GREEN
PADDLE_COLOR = WHITE
BALL_COLOR = WHITE

def main():
    pygame.init()
    global DISPLAYSURF

    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Pong')


    ball_x = WINDOW_WIDTH / 2 - LINE_THICKNESS / 2
    ball_y = WINDOW_HEIGHT / 2 - LINE_THICKNESS / 2
    ball_vx = -2
    ball_vy = 2

    player_one_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2
    player_two_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2

    paddle1 = pygame.Rect(PADDLE_OFFSET, player_one_y, LINE_THICKNESS,
                          PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WINDOW_WIDTH - LINE_THICKNESS - PADDLE_OFFSET,
                          player_two_y, LINE_THICKNESS, PADDLE_HEIGHT)
    ball = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, LINE_THICKNESS,
                       LINE_THICKNESS)

    draw_arena()
    draw_paddle(paddle1)
    draw_paddle(paddle2)
    draw_ball(ball)

    pygame.mouse.set_visible(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        _, mouse_y = pygame.mouse.get_pos()
        paddle1 = move_paddle(paddle1, mouse_y)

        if ball.x >= WINDOW_HEIGHT / 2:
            move_paddle(paddle2, ball.y)

        ball_vx, ball_vy = check_wall_collision(ball, ball_vx, ball_vy)
        ball_vx *= check_paddle_collision(ball, paddle1, paddle2, ball_vx)
        ball = move_ball(ball, ball_vx, ball_vy)

        draw_arena()
        draw_paddle(paddle1)
        draw_paddle(paddle2)
        draw_ball(ball)

        pygame.display.update()
        FPS_CLOCK.tick()


def draw_arena():
    DISPLAYSURF.fill(BG_COLOR)
    pygame.draw.rect(DISPLAYSURF, ARENA_COLOR, ((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT)), LINE_THICKNESS * 2)
    pygame.draw.line(DISPLAYSURF, ARENA_COLOR, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), LINE_THICKNESS / 4)


def draw_paddle(paddle):
    if paddle.top < LINE_THICKNESS:
        paddle.top = LINE_THICKNESS
    elif paddle.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
        paddle.bottom = WINDOW_HEIGHT - LINE_THICKNESS

    pygame.draw.rect(DISPLAYSURF, PADDLE_COLOR, paddle)


def move_paddle(paddle, target_y):
    paddle_center = paddle.y + PADDLE_HEIGHT / 2

    if -PADDLE_VY < target_y - paddle_center < PADDLE_VY:
        return paddle

    paddle.y += PADDLE_VY if target_y > paddle_center else -PADDLE_VY
    return paddle


def draw_ball(ball):
    pygame.draw.rect(DISPLAYSURF, BALL_COLOR, ball)


def move_ball(ball, vx, vy):
    ball.x += vx
    ball.y += vy
    return ball


def check_wall_collision(ball, vx, vy):
    if ball.top < LINE_THICKNESS:
        vy *= -1
    elif ball.bottom > WINDOW_HEIGHT - LINE_THICKNESS:
        vy *= -1
    return vx, vy


def check_paddle_collision(ball, paddle1, paddle2, ball_vx):
    print(ball_vx)
    if ball_vx < 0 and paddle1.right >= ball.left and ball_in_paddle_range(ball, paddle1):
        return -1.1
    elif ball_vx > 0 and paddle2.left <= ball.right and ball_in_paddle_range(ball, paddle2):
        return -1.1
    return 1


def ball_in_paddle_range(ball, paddle):
    return paddle.top < ball.top and paddle.bottom > ball.bottom

if __name__ == '__main__':
    main()

