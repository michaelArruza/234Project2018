import tensorflow as tf
import tensorflow.contrib.layers as layers

from utils.general import get_logger
from utils.test_env import EnvTest
from q1_schedule import LinearExploration, LinearSchedule
from q2_linear import Linear


from configs.q3_nature import config


class NatureQN(Linear):
    """
    Implementing DeepMind's Nature paper. Here are the relevant urls.
    https://storage.googleapis.com/deepmind-data/assets/papers/DeepMindNature14236Paper.pdf
    https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
    """
    def get_q_values_op(self, state, scope, reuse=False):
        """
        Returns Q values for all actions

        Args:
            state: (tf tensor)
                shape = (batch_size, img height, img width, nchannels)
            scope: (string) scope name, that specifies if target network or not
            reuse: (bool) reuse of variables in the scope

        Returns:
            out: (tf tensor) of shape = (batch_size, num_actions)
        """
        # this information might be useful
        num_actions = self.config.num_actions
        out = state
        ##############################################################
        """
        TODO: implement the computation of Q values like in the paper
                https://storage.googleapis.com/deepmind-data/assets/papers/DeepMindNature14236Paper.pdf
                https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf

              you may find the section "model architecture" of the appendix of the
              nature paper particulary useful.

              store your result in out of shape = (batch_size, num_actions)

        HINT: you may find tensorflow.contrib.layers useful (imported)
              make sure to understand the use of the scope param
              make sure to flatten() the tensor before connecting it to fully connected layers

              you can use any other methods from tensorflow
              you are not allowed to import extra packages (like keras,
              lasagne, cafe, etc.)

        """
        ##############################################################
        ################ YOUR CODE HERE - 10-15 lines ################

        with tf.variable_scope(scope, reuse=reuse):
            """x1 = layers.conv2d(inputs=state, num_outputs=32, kernel_size=8, stride=4)
            x2 = layers.conv2d(inputs=x1, num_outputs=64, kernel_size =4, stride=2)
            x3 = layers.conv2d(inputs=x2, num_outputs=64, kernel_size=3, stride=1)
            x4 = layers.fully_connected(layers.flatten(x3), 512)"""
            p_state = layers.flatten(state)
            #p_state = tf.Print(p_state,[p_state], summarize = 100000)
            #p_state = tf.Print(p_state, [p_state[0]])
            #l_state = tf.reshape(layers.flatten(state[:,4:,:]),[tf.shape(state)[0],17, 20])
            #x1 = layers.conv2d(inputs=l_state, num_outputs=10, kernel_size=4, stride=1)
            #x2 = layers.conv2d(inputs=x1, num_outputs=10, kernel_size =2, stride=1)
            #x3 = layers.conv2d(inputs=x2, num_outputs=5, kernel_size=1, stride=1)
            #x4 = layers.fully_connected(layers.flatten(x3), 50)
            #x4 = layers.fully_connected(layers.fully_connected(tf.concat([p_state, x4],axis=1), 30), 30)
            x4 = layers.fully_connected(layers.fully_connected(layers.fully_connected(layers.fully_connected(p_state, 100), 100),100),50)
            out = layers.fully_connected(x4, num_actions, activation_fn = None)

        ##############################################################
        ######################## END YOUR CODE #######################
        return out


"""
Use deep Q network for test environment.
"""
if __name__ == '__main__':
    env = EnvTest((80, 80, 1))

    # exploration strategy
    exp_schedule = LinearExploration(config.num_actions, config.eps_begin,
            config.eps_end, config.eps_nsteps)

    # learning rate schedule
    lr_schedule  = LinearSchedule(config.lr_begin, config.lr_end,
            config.lr_nsteps)

    # train model
    model = NatureQN(env, config)
    model.run(exp_schedule, lr_schedule)
