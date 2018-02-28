import numpy as np

class StateMachine():
    def __init__(self, screen_height, screen_width, unseen_size):
        self.player_velocity = 0
        self.player_height = screen_height / 2.0
        self.level_matrix = np.zeros((screen_height, screen_width + unseen_size))

    def scroll_level(self):
        self.level_matrix[:,:-1] = self.level_matrix[:,1:]
        self.level_matrix[:,-1] = 0

    def check
