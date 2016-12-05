import numpy as np

class Agent(object):

	def __init__(self):
		pass

	def act_(self, observation, reward, done):
		if observation != None:
			action = self.policy[int(observation["x"]*600 + observation["y"])]
			return action 
		else:
			return (1, 0)

	def act(self, observation, reward, done):
		if observation != None:
			action = self.policy[int(observation["t"])*400*300 + int(observation["x"]*300 + observation["y"])]
			print(action)
			return action
		else:
			return (1, 0)

	def setAgentPolicy(self, policy):
		self.policy = policy

	def loatAgentPolicy(self):
		self.policy = np.load("policies/policy5_final.npy")
		#self.policy = self.policy 