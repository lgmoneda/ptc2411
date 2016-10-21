#encoding=utf-8
from graphical_setup import *

class Environment(object):
	"""
	"""

	def __init__(self, tmax):
		self.tmax = tmax 
		self.reset()
		print("Estado inicial: ")
		self.printState()
		self.gravity = 10
		self.desired_path = [(0, 0, 0),
					     	 (5, 50, 10),
							 (15, 100, 15),
							 (30, 150, 5),
							 (34, 200, 30),
							 (50, 300, 160),
							 (60, 350, 400),
							 (100, 600, 410),
							 (200, 800, 500)]
		self.actual_path = []
		self.desired_path = self.createFullDesiredPath(self.tmax)

	def createFullDesiredPath(self, n):
		""" Creates a full list of desired points for the path

		Assumes we have a rect between two points from the desired path
		and creates a list of points to every time period.

		Params:
			n: int with the number of periods
		Returns:
			fullDP: A list of tuples with the form (t, x, y) as desired points
		"""

		fullDP = []
		for t in range(n+1):
			for i in range(len(self.desired_path)):
				if t == self.desired_path[i][0]:
					fullDP.append(self.desired_path[i])
					break
				else:
					if t < self.desired_path[i][0]:
						point1 = self.desired_path[i-1]
						point2 = self.desired_path[i]

						delta_t = point2[0] - point1[0]
						delta_x = point2[1] - point1[1]
						delta_y = point2[2] - point1[2]

						desired_x = point1[1] + (float(delta_x) / delta_t) * abs(t - point1[0])
						desired_y = point1[2] + (float(delta_y) / delta_t) * abs(t - point1[0])

						fullDP.append((t, desired_x, desired_y))
						break

		return fullDP


	def reset(self):
		""" Resets the environment to its initial state
		"""
		self.x = 0; self.y = 0
		self.Vx = 0; self.Vy = 0
		self.t = 0
		self.m = 10

	def printState(self):
		""" Prints the current state

		Params:
			None
		Returns:
			None
		"""
		print("t: {2} x: {0:.0f} y: {1:.0f} Vx: {3:.0f} Vy: {4:.0f}".
			format(self.x, self.y, self.t, self.Vx, self.Vy))

	def squaredError(self, state):
		""" Calculates the squared error from a single state
		"""
		desired_point = self.desiredPoint()
		errors = ((state["x"] - desired_point[1]) ** 2, (state["y"] - desired_point[2]) ** 2)
		return errors[0] + errors[1]

	def rewardFunction(self, state):
		""" Calculates the reward from a single state

		Params:
			state: a (t, x, y) tuple
		"""
		error = self.squaredError(state)
		return float(10000) / error
		#return float(100000000) / (((state["x"] - desired_point[1]) ** 2) + ((state["y"] - desired_point[2]) ** 2))


	def desiredPoint(self):
		""" Returns an intermediate point from certain two points from original desired path

		Params:
			None
		Returns:
			A tuple with (t, x, y)
		"""
		if self.t < len(self.desired_path):
			return self.desired_path[self.t]
		else:
			return self.desired_path[-1]

	def step(self, action):
		""" Receives an action and return the next environment state

		Params:
			action: agent action, a tuple with (Fx, Fy)
		Returns
			observation: a dict with the new state information
			done: boolean for simulation end

		"""
		### Saving the point the agent has passed
		self.actual_path.append((self.t, self.x, self.y))

		### Para deixar claro o formato da observation
		observation = {"x": None,
					   "y": None,
					   "t": None}
		
	    ### Incremento o tempo em uma unidade
		self.t += 1

		### Ação, considero o delta t como sendo sempre 1
		self.Fx = action[0]
		self.Fy = action[1]

		self.Ax =  float(self.Fx) / self.m
		self.Ay =  float(self.Fy) / self.m 

		self.Vx += self.Ax
		self.Vy += self.Ay

		self.x += self.Vx
		self.y += self.Vy

		### Monta dicionario para retorno
		observation["x"] = self.x
		observation["y"] = self.y
		observation["t"] = self.t
		done = False
		if self.tmax <= self.t + 1:
			done = True
		try:
			print("Desired point {0}".format(self.desiredPoint()))
		except:
			print("No desired point!")
		self.printState()
		print("Error: {0:.2f}".format(self.squaredError(observation)))
		#print("Reward {0:.2f}".format(self.rewardFunction(observation)))
		return observation, done


	def render(self):
		""" Renders the environment
		"""

		### Making the window blue  
		window.fill(BLUE)
		### Drawing desired path
		for i in range(len(self.desired_path) - 1):
			pygame.draw.line(window, 
							 (255, 0, 0), 
							 self.desired_path[i][1:], 
							 self.desired_path[i+1][1:])

		### Drawing actual path
		for i in range(len(self.actual_path) - 1):
			pygame.draw.line(window, 
							 (100, 255, 100), 
							 self.actual_path[i][1:], 
							 self.actual_path[i+1][1:])

		### Displaying our submarine at (x, y)
		window.blit(submarine, (self.x - submarine.get_width()/2, self.y - submarine.get_height()/2))	

		### Game loop
		final_loop()

