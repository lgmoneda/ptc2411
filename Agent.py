import numpy as np

class Agent(object):

	def __init__(self):
		pass

	def act(self, observation, reward, done):
		if observation != None:
			return self.policy[int(observation["x"]*600 + observation["y"])]
		else:
			return (1, 1)

	def setAgentPolicy(self, policy):
		self.policy = policy

	def loatAgentPolicy(self):
		self.policy = np.load("policy2.npy")