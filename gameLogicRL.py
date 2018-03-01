import pygame
import numpy as np
import sys
import a2rl

from q1_schedule import LinearExploration, LinearSchedule
from q2_linear import Linear
from q3_nature import NatureQN

from configs.q3_nature import config

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

    def get_state(self):
        return [self.playerRect.x, self.playerRect.y, self.vel]

class State():
    def __init__(self):
        self.playerObj = Player()
        size = width, height = SCREENWIDTH, SCREENHEIGHT
        self.speed = [0, 2]
        self.white = 255,255,255
        self.FPSCLOCK = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        self.ceiling, self.ceilingRect, self.floor, self.floorRect = initLevel()
        self.obstacles = [self.ceilingRect, self.floorRect]
        self.fail = False

    def get_player_state(self):
        return self.playerObj.get_state()

    def reset(self):
        self.playerObj = Player()
        self.fail = False

    def advance_game(self, action):
        self.FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            print("yo")

        if action == 1:
            up_input = True
        else:
            up_input = False

        self.playerObj.update_frame()
        self.playerObj.update_vel(up_input)
        self.screen.fill(self.white)
        self.screen.blit(self.floor, self.floorRect)
        self.screen.blit(self.ceiling, self.ceilingRect)
        self.screen.blit(*self.playerObj.get_blit())
        pygame.display.flip()

        if self.playerObj.playerRect.collidelist(self.obstacles) != -1:
            self.fail = True

        done = False
        if self.fail:
            reward = -100
            done = True
            self.fail = False
        else:
            reward = 1

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
