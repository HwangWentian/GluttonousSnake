import sys
import pygame as pg
from time import sleep
from random import randint
from threading import Thread


def create_food(head, body):
    while len(body) < 399:
        x = randint(0, 19)
        y = randint(0, 19)
        if not [x, y] in body and not [x, y] in head:
            return [x, y]


class Snake():
    def __init__(self, scr):
        global GAME_STARTED, GAME_FINISHED, GAME_WINNED
        self.scre = scr
        self.body = []
        self.head = [0, 0]  # The 400*400 screen is divided into 400 20*20pixels
        self.dest = 'R'  # 'L' for left, 'R' for right, 'U' for up, 'D' for down temporarily
        self.pdest = 'R'  # Used between two moves to record the destination
        self.food = create_food(self.head, self.body)

    def show_snake(self):
        for p in self.body:
            pg.draw.circle(self.scre, (20, 160, 0), (p[0] * 20 + 10, p[1] * 20 + 10), 10)
        pg.draw.circle(self.scre, (160, 40, 0), (self.head[0] * 20 + 10, self.head[1] * 20 + 10), 10)

    def show_food(self):
        points = [(self.food[0] * 20 + 7, self.food[1] * 20 + 10), (self.food[0] * 20 + 10, self.food[1] * 20 + 15),
                  (self.food[0] * 20 + 13, self.food[1] * 20 + 10), (self.food[0] * 20 + 10, self.food[1] * 20 + 5)]
        pg.draw.polygon(screen, (200, 200, 0), points)

    def move(self):
        self.dest = self.pdest

        if self.dest == 'L':
            h = [self.head[0] - 1, self.head[1]]
        elif self.dest == 'R':
            h = [self.head[0] + 1, self.head[1]]
        elif self.dest == 'U':
            h = [self.head[0], self.head[1] - 1]
        else:
            h = [self.head[0], self.head[1] + 1]

        if self.head == self.food:
            if not len(self.body):
                self.body.append(self.body)
                self.head = h
            else:
                self.body = [self.head] + self.body
                self.head = h
            self.food = create_food(self.head, self.body)
        else:
            self.body = [self.head] + self.body[:-1]
            self.head = h

        if h in self.body:
            GAME_FINISHED = True
            GAME_WINNED = False

        if not 0 <= h[0] <= 19 or not 0 <= h[1] <= 19:
            GAME_FINISHED = True
            GAME_WINNED = False

        if len(self.body) == 99:
            GAME_FINISHED = True
            GAME_WINNED = True

    def turn_to_left(self):
        if self.dest == 'U' or self.dest == 'D':
            self.pdest = 'L'

    def turn_to_right(self):
        if self.dest == 'U' or self.dest == 'D':
            self.pdest = 'R'

    def turn_to_up(self):
        if self.dest == 'L' or self.dest == 'R':
            self.pdest = 'U'

    def turn_to_down(self):
        if self.dest == 'L' or self.dest == 'R':
            self.pdest = 'D'


def move_(snake):
    while GAME_STARTED and not GAME_FINISHED:
        sleep(.2)
        snake.move()

if __name__ == "__main__":
    pg.init()
    GAME_STARTED = False
    GAME_FINISHED = False
    GAME_WINNED = False

    screen = pg.display.set_mode((400, 400), pg.NOFRAME)

    ft1 = pg.font.Font("/usr/share/fonts/truetype/ubuntu/Ubuntu-MI.ttf", 40)
    t1 = ft1.render("Snake", True, (0, 200, 0), (50, 50, 50))
    t1Rect = t1.get_rect()
    t1Rect.center = 200, 200

    ft2 = pg.font.Font("/usr/share/fonts/truetype/ubuntu/Ubuntu-MI.ttf", 20)
    t2 = ft2.render("Press Q to exit", True, (0, 150, 0), (50, 50, 50))
    t2Rect = t2.get_rect()
    t2Rect.center = 200, 240

    t3 = ft2.render("Click window to start", True, (0, 150, 0), (50, 50, 50))
    t3Rect = t3.get_rect()
    t3Rect.center = 200, 270

    t4 = ft1.render("You win", True, (0, 150, 0), (50, 50, 50))
    t4Rect = t4.get_rect()
    t4Rect.center = 200, 270

    t5 = ft1.render("You lose", True, (0, 150, 0), (50, 50, 50))
    t5Rect = t5.get_rect()
    t5Rect.center = 200, 270

    t6 = ft2.render("Click window to restart", True, (0, 150, 0), (50, 50, 50))
    t6Rect = t6.get_rect()
    t6Rect.center = 200, 270


    while True:
        screen.fill((50, 50, 50))
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and not GAME_STARTED:
                GAME_STARTED = True
                snake = Snake(screen)
                moving = Thread(target=move_, args=(snake,))
                moving.start()
            elif event.type == pg.MOUSEBUTTONDOWN and GAME_FINISHED:
                GAME_STARTED = True
                GAME_FINISHED = False
                GAME_WINNED = False
                snake = Snake(screen)
                moving = Thread(target=move_, args=(snake,))
                moving.start()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    snake.turn_to_left()
                elif event.key == pg.K_RIGHT:
                    snake.turn_to_right()
                elif event.key == pg.K_UP:
                    snake.turn_to_up()
                elif event.key == pg.K_DOWN:
                    snake.turn_to_down()
                elif event.key == 113:  # Q
                    GAME_FINISHED = True
                    pg.quit()
                    sys.exit()

        if not GAME_STARTED:
            screen.blit(t1, t1Rect)
            screen.blit(t2, t2Rect)
            screen.blit(t3, t3Rect)
        elif not GAME_FINISHED:
            snake.show_food()
            snake.show_snake()
        elif GAME_WINNED:
            screen.blit(t4, t4Rect)
            screen.blit(t6, t6Rect)
        else:
            screen.blit(t5, t5Rect)
            screen.blit(t6, t6Rect)
        pg.display.flip()
