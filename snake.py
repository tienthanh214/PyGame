"""
author: JugThanh
created: 10:00 18/04/2020
language: python3
"""
import random
import pygame
import os

""" --------- Game attributes ---------"""
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("comicsansms", 28)

width = 500
height = 500
rows = 20
cols = 20
yourScore = 0


class Food:
    """represents food"""
    def __init__(self, position = (1, 1), color = (0, 255, 0)):
        self.pos = position
        self.color = color

    def creat(self, snake):
        while True:
            x = random.randrange(rows)
            y = random.randrange(cols)
            if (x, y) in snake.turns: continue
            self.pos = (x, y)
            break

    def draw(self, surface):
        cellSize = width // rows
        center = ((2 * self.pos[0] + 1) * cellSize // 2 + 1, (2 * self.pos[1] + 1) * cellSize // 2 + 1)
        pygame.draw.circle(surface, self.color, center, cellSize // 2)


class Cube:
    """represents unit of snake"""
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    def __init__(self, position, color = (255, 0, 0)):
        self.pos = position
        self.color = color

    def move(self, dir):
        newX = (self.pos[0] + Cube.dx[dir] + rows) % rows
        newY = (self.pos[1] + Cube.dy[dir] + cols) % cols
        self.pos = (newX, newY)

    def draw(self, surface, eyes = False):
        cellSize = width // rows
        pygame.draw.rect(surface, self.color, (self.pos[0] * cellSize + 1, self.pos[1] * cellSize + 1, cellSize - 2, cellSize - 2))
        if eyes == True:
            radius = 3
            center = cellSize // 2
            eye1 = (self.pos[0] * cellSize + center - radius, self.pos[1] * cellSize + radius * 3)
            eye2 = ((self.pos[0] + 1) * cellSize - radius * 2, self.pos[1] * cellSize + radius * 3)
            pygame.draw.circle(surface, (0, 0, 0), eye1, radius)
            pygame.draw.circle(surface, (0, 0, 0), eye2, radius)


class Snake:
    """
    Represents a snake
    body: list of cube
    turns: to know where the snake turn
    """
    dkey = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    def __init__(self, position, color = (255, 0, 0)):
        self.body = [Cube(position, color)]
        self.turns = {position: 0}
        self.current_dir = 0
        self.color = color

    def reset(self, position):
        # print(position)
        # print(self.turns)
        # print(list(x.pos for x in self.body))
        while self.body[-1].pos != position:
            self.turns.pop(self.body[-1].pos)
            self.body.pop(-1)
        self.turns.pop(position)
        self.body.pop(-1)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed() # keys[x] = 1/0 if x pressed
            for dir in range(4):
                if keys[Snake.dkey[dir]]:
                    if (self.current_dir == (dir ^ 1)):
                        break
                    self.current_dir = dir
                    self.turns[self.body[0].pos[:]] = dir

        for i in range(len(self.body)):
            p = self.body[i].pos[:]
            self.body[i].move(self.turns[p])
            if (i == len(self.body) - 1):
                self.turns.pop(p)

        if self.body[0].pos in self.turns: # eat its self
            return False
            # self.reset(self.body[0].pos)
        self.turns[self.body[0].pos] = self.current_dir
        return True

    def addCube(self):
        pos = self.body[-1].pos
        dir = self.turns[pos]
        pos = (pos[0] + Cube.dx[dir ^ 1], pos[1] + Cube.dy[dir ^ 1])
        self.body.append(Cube(pos, self.body[-1].color))
        self.turns[pos] = dir

    def draw(self, surface):
        for i in range(len(self.body)):
            self.body[i].draw(surface, i == 0)

""" -------------------- GRAPHIC AREA ---------------------------"""

def gameIntro(surface):
    font = pygame.font.SysFont("bahnschrift", 50)
    value = font.render("Snake Game", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 - 90)
    surface.blit(value, rect)

    font = pygame.font.Font('freesansbold.ttf', 18)
    value = font.render("author: JugThanh", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 - 30)
    surface.blit(value, rect)

    value = font.render("press ENTER to play", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 + 90)
    surface.blit(value, rect)

    value = font.render("press ESC to quit", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 + 120)
    surface.blit(value, rect)
    pygame.display.update()


def fadeScreen(surface):
    fade = pygame.Surface((width + 1, height + 1))
    fade.fill(0)
    for alpha in range(0, 300, 5):
        pygame.time.delay(50)
        fade.set_alpha(alpha)
        gameIntro(surface)
        surface.blit(fade, (0, 0))
        pygame.display.flip()


def drawGrid(width, height, rows, surface):
    cellSize = width // rows
    for i in range(rows + 1):
        pygame.draw.line(surface, (255, 255, 255), (cellSize * i, 0), (cellSize * i, height))
    for i in range(cols + 1):
        pygame.draw.line(surface, (255, 255, 255), (0, cellSize * i), (width, cellSize * i))

def redrawWindow(surface, snake, snack):
    surface.fill((255, 153, 204))
    showScore(surface, len(snake.body) - 1)
    drawGrid(width, height, rows, surface)
    snack.draw(surface) # draw a snack (food of snake)
    snake.draw(surface) # draw a snake
    pygame.display.update()

def showScore(surface, score):
    value = score_font.render("Your Score: " + str(score), True, (255, 255, 102));
    surface.blit(value, [0, 0])

def gameOver(surface, score):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont("freesansbold.ttf", 100)
    value = font.render("GAME OVER", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 - 90)
    surface.blit(value, rect)

    font = pygame.font.SysFont("freesansbold.ttf", 60)
    value = font.render("Your score: " + str(score), True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2)
    surface.blit(value, rect)

    font = pygame.font.Font('freesansbold.ttf', 18)
    value = font.render("press ENTER to play", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 + 90)
    surface.blit(value, rect)

    value = font.render("press ESC to quit", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 + 120)
    surface.blit(value, rect)
    pygame.display.update()

def gamePlay(snake, snack):
    #print(snack.pos)
    if not snake.move():
        return False
    if (snake.body[0].pos == snack.pos):
        snake.addCube()
        snack.creat(snake)
    return True

if __name__ == '__main__':

    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake game - made by Jug")
    win = pygame.display.set_mode((width + 1, height + 1))

    snake = Snake(position = (5, 5), color = (255, 0, 10))
    snack = Food()
    snack.creat(snake)

    inGame = 0
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        if inGame == 0:
            win.fill((51, 204, 255))
            gameIntro(win)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        inGame = True
                        fadeScreen(win)
                        break
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        elif inGame == 1:
            if not gamePlay(snake, snack):
                inGame = 2
            redrawWindow(win, snake, snack)
            if inGame == 2:
                pygame.time.delay(1000)
        else:
            gameOver(win, len(snake.body) - 1)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        inGame = True
                        snake = Snake(position=(5, 5), color=(255, 0, 10))
                        break
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()