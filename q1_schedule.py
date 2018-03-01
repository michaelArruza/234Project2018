import numpy as np
from utils.test_env import EnvTest


class LinearSchedule(object):
    def __init__(self, eps_begin, eps_end, nsteps):
        """
        Args:
            eps_begin: initial exploration
            eps_end: end exploration
            nsteps: number of steps between the two values of eps
        """
        self.epsilon        = eps_begin
        self.eps_begin      = eps_begin
        self.eps_end        = eps_end
        self.nsteps         = nsteps


    def update(self, t):
        """
        Updates epsilon

        Args:
            t: (int) nth frames
        """
        ##############################################################
        """
        TODO: modify self.epsilon such that 
               for t = 0, self.epsilon = self.eps_begin
               for t = self.nsteps, self.epsilon = self.eps_end
               linear decay between the two

              self.epsilon should never go under self.eps_end
        """
        ##############################################################
        ################ YOUR CODE HERE - 3-4 lines ################## 

        progress = t/float(self.nsteps)
        progress = min(progress, 1)
        self.epsilon = (1-progress)*self.eps_begin + progress*self.eps_end

        ##############################################################
        ######################## END YOUR CODE ############## ########


class LinearExploration(LinearSchedule):
    def __init__(self, num_actions, eps_begin, eps_end, nsteps):
        """
        Args:
            num_actions: number of actions in discrete action space
            eps_begin: initial exploration
            eps_end: end exploration
            nsteps: number of steps between the two values of eps
        """
        self.num_actions = num_actions
        super(LinearExploration, self).__init__(eps_begin, eps_end, nsteps)


    def get_action(self, best_action):
        """
        Returns a random action with prob epsilon, otherwise return the best_action

        Args:
            best_action: (int) best action according some policy
        Returns:
            an action
        """
        ##############################################################
        """
        TODO: with probability self.epsilon, return a random action
               else, return best_action

               you can access the environment stored in self.env
               and epsilon with self.epsilon

               you may want to use env.action_space.sample() to generate 
               a random action        
        """
        ##############################################################
        ################ YOUR CODE HERE - 4-5 lines ##################

        p = np.random.uniform(low=0.0, high=1.0)
        if p <= self.epsilon:
            return np.random.random_integers(0, self.num_actions-1)
        else:
            return best_action