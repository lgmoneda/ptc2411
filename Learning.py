from Agent import Agent 
from Environment import Environment


def calculate_value(env, state):



def valueIteration(env):
    steps = env.tmax
    value_function = {}

    ### Initializing all Vs with zero
    for state in env.state_space:
        if len(value_function[state[0]]) == 0:
            value_function[state[0]] = {}
        value_function[state[0]][state[1]] = 0


    for state in env.state_space:
        value_function[state[0]][state[1]] = calculate_value(env, state)
        
    

if __name__ == '__main__':

    episode_count = 2
    max_steps = 500
    reward = 0
    done = False

    env = Environment(max_steps)
    agent = Agent()
    #print(env.state_space)

    """

    for i in xrange(episode_count):
        observation = env.reset()
        for j in xrange(max_steps):
            env.render()
            action = agent.act(observation, reward, done)
            observation, reward, done = env.step(action)

            if done:
                break
    """