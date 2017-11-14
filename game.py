import pygame
from GameObjects import *
from pygamegame import PygameGame
import math
import copy


class Game(PygameGame):
    def init(self):
        self.gameTime = 0
        self.scotGroup = pygame.sprite.Group(Scottie(150, 100))
        self.bloons = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.target = [(225, 75, 0, -1), (150, 75, 1, 0), (150, 112, 0, -1), (112, 112, 1, 0), (112, 187, 0, 1),
                       (150, 187, 1, 0),
                       (150, 225, 0, 1), (225, 225, -1, 0), (225, 187, 0, 1), (375, 187, -1, 0), (375, 112, 0, 1), \
                       (412, 112, -1, 0), (412, 75, 0, 1), (487, 75, 1, 0), (487, 150, 0, 1), (525, 150, 1, 0),
                       (525, 412, 0, -1),
                       (487, 412, 1, 0), (487, 487, 0, -1), (412, 487, -1, 0), (412, 450, 0, -1), (375, 450, -1, 0), \
                       (375, 412, 0, -1), (375, 375, -1, 0), (337, 375, 0, -1), (337, 262, -1, 0), (262, 262, 0, -1),
                       (262, 300, -1, 0),
                       (225, 300, 0, 1), (225, 412, -1, 0), (112, 412, 0, -1), (112, 375, -1, 0), (75, 375, 0, -1),
                       (75, 337, -1, 0),
                       (0, 337, 0, 0)]

    def redrawAll(self, screen):
        self.bullets.draw(screen)
        self.scotGroup.draw(screen)
        self.bloons.draw(screen)

    def timerFired(self, dt):
        self.gameTime += 1
        self.bullets.update(self.width, self.height)
        self.dartCollision()
        self.swivel()
        self.inRange()
        self.swivel()
        self.moveBloons()
        if self.gameTime % 15 == 0:
            self.attack()

    def keyPressed(self, keyCode, mod):
        if keyCode == pygame.K_SPACE:
            for elem in self.scotGroup:
                scottie = elem
                self.bullets.add(Bullet(scottie.x, scottie.y, scottie.angle, scottie.power[1]))
                print(len(self.bloons.sprites()))

    def addTower(self, x, y):
        self.scotGroup.add(Scottie(x, y))

    def dartCollision(self):
        for dart in self.bullets:
            for bloon in self.bloons:
                if pygame.sprite.collide_circle(dart, bloon):
                    dart.hit(1)
                    print("Pop!")
                    bloon.hit(1)

    def mousePressed(self, x, y):
        x, y = pygame.mouse.get_pos()
        targetList = copy.deepcopy(self.target)
        bloon = Bloons(targetList, 0, 225)
        # self.setVelocity(bloon)
        self.bloons.add(bloon)

    def swivel(self):
        for scot in self.scotGroup:
            scot.update()

    def inRange(self):
        for scottie in self.scotGroup:
            x, y = scottie.x, scottie.y
            curBloon = self.getClosestBloon(scottie)
            if curBloon is None: break
            x2, y2 = curBloon.x, curBloon.y
            dist = self.getDistance(x, y, x2, y2)
            # print(dist)
            if self.getDistance(x, y, x2, y2) < scottie.range:
                scottie.angle = self.get_angle(x, y, scottie)

    def getClosestBloon(self, scottie):
        x, y = scottie.x, scottie.y
        smallestDistance = 600
        targetBloon = None
        bloons = self.bloons.sprites()
        if not bloons: return None
        for bloon in bloons:
            x2, y2 = bloon.x, bloon.y
            dist = self.getDistance(x, y, x2, y2)
            if dist is None or dist < smallestDistance and dist < scottie.range:
                smallestDistance = dist
                targetBloon = bloon
        return targetBloon

    def attack(self):
        for scottie in self.scotGroup:
            if not self.getClosestBloon(scottie) is None:
                self.bullets.add(Bullet(scottie.x, scottie.y, scottie.angle, scottie.power[1]))
                print(len(self.bloons.sprites()))

    def getDistance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def moveBloons(self):
        for bloon in self.bloons:
            x, y = bloon.x, bloon.y
            dx, dy = bloon.velocity
            y1, x1, deltaX, deltaY = bloon.targets[0]
            scaleY, scaleX = 1, 1
            # if y1 - y > 0:
            #     print('neg')
            #     scaleY *= -1
            # if x1 - x < 0:
            #     print('neg')
            #     scaleX *= -1
            if x1 - 5 < x < x1 + 5 and dy == 0:
                bloon.x = x1
                bloon.velocity = (deltaX * bloon.speed, deltaY * bloon.speed)
                print(bloon.targets[0])
                print(y, x)
                bloon.targets.pop(0)
            elif y1 - 5 < y < y1 + 5 and dx == 0:
                bloon.y = y1
                bloon.velocity = (deltaX * bloon.speed, deltaY * bloon.speed)
                print(bloon.targets[0])
                print(y, x)
                bloon.targets.pop(0)
                # print(bloon.x, bloon.y)
                # self.setVelocity(bloon)
            bloon.update()

    def get_angle(self, x, y, scottie):
        x1, y1 = x, y
        bloon = self.getClosestBloon(scottie)
        x2, y2 = bloon.x, bloon.y
        return - (math.atan2(y2 - y1, x2 - x1)) / (math.pi / 180)


Game(800, 600).run()
