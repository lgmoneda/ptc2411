from Agent import Agent 

if __name__ == '__main__':

    env = gym.make('CartPole-v0')
    agent = Agent()


    episode_count = 500
    max_steps = 200
    reward = 0
    done = False
    sum_reward_running = 0

    for i in xrange(episode_count):
        observation = env.reset()
        sum_reward = 0

        for j in xrange(max_steps):
            action = agent.act(observation, reward, done)
            observation, reward, done, _ = env.step(action)
            sum_reward += reward
            if done:
                break

        sum_reward_running = sum_reward_running * 0.95 + sum_reward * 0.05
        print '%d running reward: %f' % (i, sum_reward_running)
