from Agent import Agent 
from Environment import Environment

if __name__ == '__main__':

    episode_count = 1
    max_steps = 35
    reward = 0
    done = False

    env = Environment(max_steps)
    agent = Agent()


    for i in xrange(episode_count):
        observation = env.reset()
        for j in xrange(max_steps):
            action = agent.act(observation, reward, done)
            observation, done = env.step(action)

            if done:
                break
