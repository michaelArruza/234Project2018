import pygame
import numpy as np
import sys

SCREENWIDTH = 500
SCREENHEIGHT = 300
FPS = 30
G = 0.5
MAXV = 5.0
MINV = -5.0
BLOCK_SIZE = 25
UNSEEN = 5

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
            self.vel = max(min(self.vel - G,-1), MINV)
        else:
            self.vel = min(self.vel + G, MAXV)

class Obstacles():
    def __init__(self):
        self.obstacle_vel = -5
        self.blockImg = pygame.transform.scale(pygame.image.load("Assets/block.png"), (BLOCK_SIZE,BLOCK_SIZE))
        self.setBlocks = []
        self.level_matrix = np.zeros((SCREENWIDTH/BLOCK_SIZE,SCREENHEIGHT/BLOCK_SIZE + UNSEEN))

    def add_wall(self, level_arr):
        for i in range(len(level_arr)):
            for j in range(len(level_arr[i])):
                if level_arr[i,j] >= 1:
                    self.setBlocks.append(self.blockImg.get_rect())
                    self.setBlocks[-1].x = SCREENWIDTH + j*BLOCK_SIZE
                    self.setBlocks[-1].y = i*BLOCK_SIZE

    def update(self):
        self.setBlocks = [block.move(self.obstacle_vel, 0) for block in self.setBlocks]

    def blit_all(self, screen):
        for block in self.setBlocks:
            screen.blit(self.blockImg, block)


def main():
    pygame.init()

    size = width, height = SCREENWIDTH, SCREENHEIGHT
    speed = [0, 2]
    white = 255,255,255
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    ceiling, ceilingRect, floor, floorRect = initLevel()
    playerObj = Player()

    obstacleObj = Obstacles()
    obstacleObj.add_wall(np.array([[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,0,1],[1,0,1]]))
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
        obstacleObj.update()

        screen.fill(white)
        screen.blit(floor, floorRect)
        screen.blit(ceiling, ceilingRect)
        screen.blit(*playerObj.get_blit())
        obstacleObj.blit_all(screen)
        pygame.display.flip()

        if playerObj.playerRect.collidelist(obstacleObj.setBlocks) != -1:
            fail = True
        if playerObj.playerRect.collidelist([floorRect,ceilingRect]) != -1:
            fail = True
        if fail:
            break

if __name__ == '__main__':
    while True:
        main()
