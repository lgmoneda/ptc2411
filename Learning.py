from Agent import Agent 
from Environment import Environment
import pandas as pd
import numpy as np
from time import time

X_MIN = 0
Y_MIN = 0
X_MAX = 399
Y_MAX = 299

def getRewards(env, next_states):
    rewards = np.zeros((next_states.shape[0], 1))
    for i in range(len(rewards)):
        rewards[i] = env.rewardFunction(next_states[i], isPoint=True)

    return rewards

def getV_kminus(value_table, next_states):
    v_kminus = np.zeros((next_states.shape[0], 1))
    for i in range(len(v_kminus)):
        v_kminus[i] = value_table[int(next_states[i][0]*(Y_MAX+1) + next_states[i][1])][2]
    return v_kminus

def getValidStates(next_states, actions, lx, ly):
    X_MIN = 0
    Y_MIN = 0
    X_MAX = 399
    Y_MAX = 299
    indexes = []
    for i in range(len(next_states)):
        #print(next_states[i])
        if next_states[i][0] not in lx or next_states[i][1] not in ly:
            indexes.append(i) 
    return np.delete(next_states, indexes, axis=0), np.delete(actions, indexes, axis=0)

def valueIteration(env):
    action_space = np.array(np.meshgrid([-1,0,1], [-1,0,1])).T.reshape(-1,2)
    lx = [x for x in range(X_MAX+1)]
    ly = [y for y in range(Y_MAX+1)]
    value_table = np.array(np.meshgrid(lx, ly)).T.reshape(-1,2)
    v0 = np.ones((value_table.shape[0], 1))
    v1 = np.ones((value_table.shape[0], 1))
    policy = np.ones((value_table.shape[0], 2))
    value_table = np.hstack((value_table, v0))
    value_table = np.hstack((value_table, v1))
    policy = np.zeros((value_table.shape[0], 2))


    steps = env.tmax
    value_function = {}
    new_value_function = {}
    discount_factor = 0.9
    k = 0

    max_mod = 15000
    iteration = 0
    n_states = len(value_table)
    max_iter = 2
    for _ in range(max_iter):
    #while(max_mod > 10):
        start = time()
        iteration += 1
        for i in range(len(value_table)):
            if i % 5000 == 0:
                print("{0}% da iteracao {1}.".format(int(100*float(i)/n_states), iteration))
            current_action_space = action_space.copy()
            next_states = np.zeros((action_space.shape[0], 2))
            next_states += value_table[i][:2]
            next_states += action_space
            next_states, current_action_space = getValidStates(next_states, current_action_space, lx, ly)
            #print(len(next_states))
            #print(next_states)

            rewards = getRewards(env, next_states)

            v_kminus = getV_kminus(value_table, next_states)
            value_candidates = rewards + discount_factor * v_kminus
            policy[i] = current_action_space[np.argmax(value_candidates)]
            value_table[i][3] = np.max(value_candidates)


        modification = value_table[:, 2] - value_table[:, 3] 
        modification = np.fabs(modification)
        max_mod = np.max(modification)
        value_table[:, 2] = value_table[:, 3] 
        np.save("policy_partial", policy)
        print("Iteracao {0} finalizada em {1} minutos, max mod de {2}.".format(iteration, (time() - start)/60, max_mod))

    np.save("policy8", policy)
    return policy
 

if __name__ == '__main__':

    episode_count = 2
    max_steps = 5000
    reward = 0
    done = False

    env = Environment(max_steps)
    agent = Agent()
    #print(env.state_space)
    policy = valueIteration(env)
    print(policy)
    agent.setAgentPolicy(policy)
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
    for i in xrange(episode_count):
        observation = env.reset()
        for j in xrange(max_steps):
            env.render()
            action = agent.act(observation, reward, done)
            observation, reward, done = env.step(action)

            if done:
                break