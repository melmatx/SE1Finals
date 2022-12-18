import random
import sys
from math import *

import pygame

import main

pygame.init()

width = 500
height = 600

maxTimeInSeconds = 30

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Shooter")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

margin = 100
lowerBound = 100

# Colors
white = (230, 230, 230)
lightBlue = (174, 214, 241)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (21, 67, 96)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)

font = pygame.font.SysFont(pygame.font.get_default_font(), 25)


# Balloon Class
class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])

    # Move balloon around the Screen
    def move(self):
        direct = random.choice(self.probPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    # Show/Draw the balloon  
    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b),
                         (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

    # Check if Balloon is popped
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if on_balloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            self.reset()

    # Reset the Balloon
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed -= 0.002
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])


balloons = []
noBalloon = 10


def create_balloons():
    balloons.clear()
    for i in range(noBalloon):
        obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        balloons.append(obj)


def on_balloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False


# show the location of Mouse
def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = lightGreen
    for i in range(noBalloon):
        if on_balloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r / 2, pos[1] - r / 2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l / 2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l / 2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l / 2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l / 2, pos[1]), (pos[0] - l, pos[1]), 4)


def lower_platform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))


def show_score():
    score_text = font.render("Balloons Popped : " + str(score), True, white)
    display.blit(score_text, (150, height - lowerBound + 50))


def show_timer():
    timer_text = font.render("Remaining Time : " + str(remaining_time), True, white)
    display.blit(timer_text, (150, height - lowerBound + 30))


def show_game_over():
    go_font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    go_text = go_font.render("Game Over", True, darkGray)

    display.blit(go_text, (160, 150))
    pygame.display.update()
    pygame.time.wait(500)


def close():
    pygame.quit()
    sys.exit()


def game_loop():
    global score, remaining_time
    score = 0
    remaining_time = maxTimeInSeconds
    loop = True

    create_balloons()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    main.main()
            if event.type == pygame.USEREVENT:
                if remaining_time > 0:
                    remaining_time -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noBalloon):
                    balloons[i].burst()
                if remaining_time == 0:
                    score = 0
                    game_loop()

        if remaining_time > 0:
            display.fill(lightBlue)

            for i in range(noBalloon):
                balloons[i].show()

            pointer()

            for i in range(noBalloon):
                balloons[i].move()
        else:
            show_game_over()

        lower_platform()
        show_score()
        show_timer()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
