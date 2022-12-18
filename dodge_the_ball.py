import random
import sys
from math import *

import pygame

import main

pygame.init()

width = 500
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge The Ball!")
clock = pygame.time.Clock()

background = (51, 51, 51)
playerColor = (249, 231, 159)

red = (203, 67, 53)
yellow = (241, 196, 15)
blue = (46, 134, 193)
green = (34, 153, 84)
purple = (136, 78, 160)
orange = (214, 137, 16)

colors = [red, yellow, blue, green, purple, orange]

score = 0


class Ball:
    def __init__(self, radius, speed):
        self.x = 0
        self.y = 0
        self.r = radius
        self.color = 0
        self.speed = speed
        self.angle = 0

    def create_ball(self):
        self.x = width / 2 - self.r
        self.y = height / 2 - self.r
        self.color = random.choice(colors)
        self.angle = random.randint(-180, 180)

    def move(self):
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x < self.r or self.x + self.r > width:
            self.angle = 180 - self.angle
        if self.y < self.r or self.y + self.r > height:
            self.angle *= -1

    def draw(self):
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r * 2, self.r * 2))

    def collision(self, radius):
        pos = pygame.mouse.get_pos()

        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5

        if distance <= self.r + radius:
            game_over()


class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w

    def generate_new_coord(self):
        self.x = random.randint(self.w, width - self.w)
        self.y = random.randint(self.h, height - self.h)

    def draw(self):
        color = random.choice(colors)

        pygame.draw.rect(display, color, (self.x, self.y, self.w, self.h))


def game_over():
    loop = True

    font = pygame.font.SysFont("Agency FB", 100)
    text = font.render("Game Over!", True, (230, 230, 230))

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    main.main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_loop()

        display.fill(background)

        display.blit(text, (50, height / 2 - 100))
        display_score()

        pygame.display.update()
        clock.tick()


def check_collision(target, d, obj_target):
    pos = pygame.mouse.get_pos()
    distance = ((pos[0] - target[0] - obj_target.w) ** 2 + (pos[1] - target[1] - obj_target.h) ** 2) ** 0.5

    if distance <= d + obj_target.w:
        return True
    return False


def draw_player_pointer(pos, r):
    pygame.draw.ellipse(display, playerColor, (pos[0] - r, pos[1] - r, 2 * r, 2 * r))


def close():
    pygame.quit()
    sys.exit()


def display_score():
    font = pygame.font.SysFont("Forte", 30)
    score_text = font.render("Score: " + str(score), True, (230, 230, 230))
    display.blit(score_text, (10, 10))


def game_loop():
    global score
    score = 0

    loop = True

    p_radius = 10

    balls = []

    for i in range(1):
        new_ball = Ball(p_radius + 2, 5)
        new_ball.create_ball()
        balls.append(new_ball)

    target = Target()
    target.generate_new_coord()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    main.main()

        display.fill(background)

        for i in range(len(balls)):
            balls[i].move()

        for i in range(len(balls)):
            balls[i].draw()

        for i in range(len(balls)):
            balls[i].collision(p_radius)

        player_pos = pygame.mouse.get_pos()
        draw_player_pointer((player_pos[0], player_pos[1]), p_radius)

        collide = check_collision((target.x, target.y), p_radius, target)

        if collide:
            score += 1
            target.generate_new_coord()
        elif score == 2 and len(balls) == 1:
            new_ball = Ball(p_radius + 2, 5)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 5 and len(balls) == 2:
            new_ball = Ball(p_radius + 2, 6)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 10 and len(balls) == 3:
            new_ball = Ball(p_radius + 2, 7)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 15 and len(balls) == 4:
            new_ball = Ball(p_radius + 2, 8)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 20 and len(balls) == 5:
            new_ball = Ball(p_radius + 2, 9)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()

        target.draw()
        display_score()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
