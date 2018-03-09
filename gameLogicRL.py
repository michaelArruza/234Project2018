import pygame
import numpy as np
import sys
#import a2rl

from q1_schedule import LinearExploration, LinearSchedule
from q2_linear import Linear
from q3_nature import NatureQN

from configs.q3_nature import config

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
        self.vel = -5.0

    def update_frame(self):
        self.playerRect = self.playerRect.move(0, self.vel)

    def get_blit(self):
        return self.player, self.playerRect

    def update_vel(self, up_input):
        if up_input:
            self.vel = max(self.vel - G, MINV)
        else:
            self.vel = min(self.vel + G, MAXV)

    def get_state(self):
        y_state = [self.playerRect.y/300, (260.0 - self.playerRect.y - 25.0) / (260.0-28.0), (self.playerRect.y - 28.0)/(260.0-25.0)]
        vel_state =  self.vel/float(MAXV)
        #print  np.array([y_state, vel_state])
        return np.array(y_state+[vel_state])

class Obstacles():
    def __init__(self):
        self.obstacle_vel = -5
        self.blockImg = pygame.transform.scale(pygame.image.load("Assets/block.png"), (BLOCK_SIZE,BLOCK_SIZE))
        self.setBlocks = []
        self.level_matrix = np.zeros((SCREENWIDTH/BLOCK_SIZE,SCREENHEIGHT/BLOCK_SIZE + UNSEEN))
        self.refresh_counter = 0
        self.unseen_counter = 0

    def add_wall(self, level_arr):
        for i in range(len(level_arr)):
            for j in range(len(level_arr[i])):
                if level_arr[i,j] >= 1:
                    self.level_matrix[i,SCREENHEIGHT/BLOCK_SIZE+j] = 1.0
                    self.setBlocks.append(self.blockImg.get_rect())
                    self.setBlocks[-1].x = SCREENWIDTH + j*BLOCK_SIZE
                    self.setBlocks[-1].y = i*BLOCK_SIZE

    def refresh(self):
        self.refresh_counter = 0
        self.unseen_counter += 1
        self.level_matrix[:,:-1] = self.level_matrix[:,1:]
        self.level_matrix[:,-1] = 0
        if self.unseen_counter == UNSEEN:
            self.add_wall((np.random.rand(SCREENHEIGHT/BLOCK_SIZE, UNSEEN) > 0.99).astype(np.float32))
            self.unseen_counter = 0
        for i in range(len(self.setBlocks)):
            if self.setBlocks[i].x > -BLOCK_SIZE:
                self.setBlocks = self.setBlocks[i:]
                break
            if i == len(self.setBlocks) - 1:
                self.setBlocks = []

    def update(self):
        self.setBlocks = [block.move(self.obstacle_vel, 0) for block in self.setBlocks]
        self.refresh_counter += 1
        if self.refresh_counter == BLOCK_SIZE/(-1*self.obstacle_vel):
            self.refresh()

    def blit_all(self, screen):
        for block in self.setBlocks:
            screen.blit(self.blockImg, block)

    def get_visible_state(self):
        return self.level_matrix[:,:SCREENWIDTH/BLOCK_SIZE]

class State():
    def __init__(self):
        self.playerObj = Player()
        self.obstacleObj = Obstacles()
        self.obstacleObj.add_wall((np.random.rand(SCREENHEIGHT/BLOCK_SIZE, UNSEEN) > 0.99).astype(int))
        size = width, height = SCREENWIDTH, SCREENHEIGHT
        self.speed = [0, 2]
        self.white = 255,255,255
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        self.ceiling, self.ceilingRect, self.floor, self.floorRect = initLevel()
        self.obstacles = [self.ceilingRect, self.floorRect]
        self.fail = False

    def get_player_state(self):
        #return self.playerObj.get_state()
        return np.concatenate([self.playerObj.get_state(),self.obstacleObj.get_visible_state().flatten()],axis=0)

    def reset(self):
        self.playerObj = Player()
        self.obstacleObj = Obstacles()
        self.obstacleObj.add_wall((np.random.rand(SCREENHEIGHT/BLOCK_SIZE, UNSEEN) > 0.99).astype(int))
        self.fail = False

    def advance_game(self, action, evaluate=False):


        #for event in pygame.event.get():
        #    print("yo")
        reward = 20.0
        for i in range(5):
            if action == 1:
                up_input = True
            else:
                up_input = False

            self.playerObj.update_frame()
            self.playerObj.update_vel(up_input)
            self.obstacleObj.update()
            if evaluate:
                self.FPSCLOCK.tick(FPS)
                self.screen.fill(self.white)
                self.screen.blit(self.floor, self.floorRect)
                self.screen.blit(self.ceiling, self.ceilingRect)
                self.screen.blit(*self.playerObj.get_blit())
                self.obstacleObj.blit_all(self.screen)
                pygame.display.flip()

            if self.playerObj.playerRect.collidelist(self.obstacles + self.obstacleObj.setBlocks) != -1:
                self.fail = True

            done = False
            if self.fail:
                reward = -1.0
                done = True
                self.fail = False
                break
            else:
                reward = 1#-.01*abs(150.0 - self.playerObj.playerRect.y)#20.0 - .1*abs(150.0 - self.playerObj.playerRect.y)
                #print reward
            #print self.get_player_state()[0:4]
        return (self.get_player_state(), reward, done, None)

def main():
    pygame.init()

    playerObj = Player()
    size = width, height = SCREENWIDTH, SCREENHEIGHT
    speed = [0, 2]
    white = 255,255,255
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    ceiling, ceilingRect, floor, floorRect = initLevel()

    s = State()
    # exploration strategy
    exp_schedule = LinearExploration(config.num_actions, config.eps_begin,
            config.eps_end, config.eps_nsteps)

    # learning rate schedule
    lr_schedule  = LinearSchedule(config.lr_begin, config.lr_end,
            config.lr_nsteps)

    # train model
    model = NatureQN(s, config)
    model.run(exp_schedule, lr_schedule)

    obstacles = [ceilingRect, floorRect]
    up_input = False
    fail = False

if __name__ == '__main__':
    #while True:
        main()
