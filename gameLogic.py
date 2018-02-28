import pygame
import numpy as np
import sys

SCREENWIDTH = 500
SCREENHEIGHT = 300
FPS = 30
G = 1
MAXV = 10.0
MINV = -10.0

def initLevel():
    floor = pygame.transform.scale(pygame.image.load("Assets/base.png"), (500,100))
    floorRect = floor.get_rect()
    ceiling = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Assets/base.png"), False, True), (500,100))
    ceilingRect = ceiling.get_rect()
    floorRect.x = 0
    floorRect.y = 260
    ceilingRect.x = 0
    ceilingRect.y = -ceilingRect.height + 28
    ceilingRect.width, floorRect.width = 512, 512
    return ceiling, ceilingRect, floor, floorRect

class Player():
    def __init__(self):
        self.player = pygame.transform.scale(pygame.image.load("Assets/Player.png"), (25,25))
        self.playerRect = self.player.get_rect()
        self.playerRect.x = SCREENWIDTH*.1
        self.playerRect.y = SCREENHEIGHT*.5
        self.vel = 1

    def update_frame(self):
        self.playerRect = self.playerRect.move(0, self.vel)

    def get_blit(self):
        return self.player, self.playerRect

    def update_vel(self, up_input):
        if up_input:
            self.vel = max(self.vel - G, MINV)
        else:
            self.vel = min(self.vel + G, MAXV)

def main():
    pygame.init()

    size = width, height = SCREENWIDTH, SCREENHEIGHT
    speed = [0, 2]
    white = 255,255,255
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    ceiling, ceilingRect, floor, floorRect = initLevel()
    playerObj = Player()

    obstacles = [ceilingRect, floorRect]
    up_input = False
    fail = False
    while True:
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                up_input = True
            if event.type == pygame.KEYUP and (event.key == pygame.K_SPACE):
                up_input = False

        playerObj.update_frame()
        playerObj.update_vel(up_input)
        screen.fill(white)
        screen.blit(floor, floorRect)
        screen.blit(ceiling, ceilingRect)
        screen.blit(*playerObj.get_blit())
        pygame.display.flip()

        if playerObj.playerRect.collidelist(obstacles) != -1:
            fail = True
        if fail:
            break

if __name__ == '__main__':
    while True:
        main()
