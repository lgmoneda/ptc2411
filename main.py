from Agent import Agent 
from Environment import Environment

if __name__ == '__main__':

    episode_count = 2
    max_steps = 5000
    reward = 0
    done = False

    env = Environment(max_steps)
    agent = Agent()
    agent.loatAgentPolicy()


    for i in xrange(episode_count):
        observation = env.reset()
        for j in xrange(max_steps):
            env.render()
            action = agent.act(observation, reward, done)
            observation, reward, done = env.step(action)

            if done:
                break
