"""
image: https://www.flaticon.com/
Space
You must destroy all the enemy before they defeat you
"""

import pygame
import random
import math

width = 800
height = 600

pygame.init()
score_font = pygame.font.SysFont("bahnschrift", 30)
game_font = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.set_caption("Space Invader - made by Jug")
surface = pygame.display.set_mode((width, height))
background = pygame.image.load("background.png").convert()
playerImg = pygame.image.load('spaceship.png')
bulletImg = pygame.image.load('bullet.png')
enemyImg = pygame.image.load('enemy.png')
rocketImg = pygame.image.load('rocket.png')


class Bullet:
    def __init__(self, x, y = 480, speedFire = 0.5):
        self.x = x
        self.y = y
        self.isFire = True
        self.speedFire = speedFire
        self.angle = 0
    def show(self):
        surface.blit(pygame.transform.rotate(bulletImg, self.angle), (self.x + 16, self.y))
        self.angle = (self.angle + 5) % 360
    def move(self):
        if self.isFire:
            self.show()
            self.y -= self.speedFire
        if self.y <= 0:
            self.isFire = False
            self.y = 480

class Rocket(Bullet):
    def __init__(self, x, y = 450, speedFire = 0.1):
        super().__init__(x, y, speedFire)
        self.oldX = x
    def show(self):
        surface.blit(rocketImg, (self.x - 10, self.y))
        surface.blit(pygame.transform.rotate(rocketImg, 90), (2 * self.oldX - self.x + 64, self.y))
    def move(self):
        if self.y <= 0:
            self.isFire = False
            self.y = 450
        if self.isFire:
            self.show()
            self.x += self.speedFire
            self.y -= self.speedFire

class Ship:
    def __init__(self, x, y, speedX, speedY):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
    def move(self):
        self.x = max(0, min(self.speedX + self.x, width - 64))
        self.y += self.speedY

class Player(Ship):
    def __init__(self, x, y, speedX = 0, speedY = 0, fireSpeed = 0.5):
        super().__init__(x, y, speedX, speedY)
        self.bullet = []
    def show(self):
        surface.blit(playerImg, (self.x, self.y))
    def move(self):
        super().move()
    def fireBullet(self):
        for bul in self.bullet:
            bul.move()
            if not bul.isFire:
                self.bullet.remove(bul)

class Enemy(Ship):
    def __init__(self, x, y, speedX = 0.4, speedY = 0):
        super().__init__(x, y, speedX, speedY)
        self.visible = True
    def show(self):
        if self.visible:
            surface.blit(enemyImg, (self.x, self.y))
    def move(self):
        if (self.x <= 0) or (self.x >= width - 64):
            self.speedX *= -1
            self.y += 40
        super().move()

def checkCollision(A, listOfBullet):
    for B in listOfBullet:
        if math.hypot(A.x - B.x, A.y - B.y) <= 30:
            return True
    return False

def showScore(score):
    value = score_font.render("Your Score: " + str(score), True, (255, 255, 102));
    surface.blit(value, [0, 0])

def gameOver():
    font = pygame.font.Font('freesansbold.ttf', 64)
    value = game_font.render("GAME OVER", True, (255, 255, 255))
    rect = value.get_rect()
    rect.center = (width // 2, height // 2 - 90)
    surface.blit(value, rect)

if __name__ == '__main__':
    ship = Player(370, 480)
    Score = 0
    numberOfEnemy = 5
    enemyList = []
    for _ in range(numberOfEnemy):
        enemyList.append(Enemy(random.randint(0, 736), random.randint(0, 150), 0.4, 0))
    clock = pygame.time.Clock()
    gameState = 0
    while True:
        surface.fill(0)
        surface.blit(background, (0, 0))

        # handle event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.speedX = -0.5
                elif event.key == pygame.K_RIGHT:
                    ship.speedX = +0.5
                elif event.key == pygame.K_SPACE:
                    ship.bullet.append(Bullet(ship.x, 480, 0.5))
                elif event.key == pygame.K_RETURN:
                    ship.bullet.append(Rocket(ship.x, 480, 0.5))
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) and (ship.speedX < 0):
                    ship.speedX = 0
                if (event.key == pygame.K_RIGHT) and (ship.speedX > 0):
                    ship.speedX = 0
        # game
        showScore(Score)
        ship.fireBullet()
        ship.move()
        ship.show()

        for _ in range(numberOfEnemy):
            if checkCollision(enemyList[_], ship.bullet):
                if (enemyList[_].visible):
                    Score += 1
                    enemyList[_].visible = False
            if enemyList[_].y >= ship.y: # lose
                gameOver()
                break
            enemyList[_].move()
            enemyList[_].show()

        pygame.display.update()
