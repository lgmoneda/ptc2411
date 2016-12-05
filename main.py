from Agent import Agent 
from Environment import Environment

if __name__ == '__main__':

    episode_count = 10
    max_steps = 3000000 * 5
    reward = 0
    done = False
    tmax = 5
    env = Environment(max_steps)
    agent = Agent()
    agent.loatAgentPolicy()
    t = 0

    for k in xrange(episode_count):
        observation = env.reset()
        t = 0
        j = 0
        while(t < tmax):
            # for j in xrange(max_steps):
            # j += 1
            # if j % 3000000 == 0:
            env.render()
            action = agent.act(observation, reward, done)
            observation, reward, done = env.step(action)
            t = observation["t"]

            # if done:
            #     break
                