            #encoding=utf-8
from graphical_setup import *
import itertools	
import numpy as np

class Environment(object):
	"""
	"""

	### Environment Params
	SIZE = (800, 600)
	Vx_max = 100
	Vx_min = -100
	Vy_max = 100
	Vy_min = -100

	Fx_max = 1 
	Fx_min = -1
	Fy_max = 1 
	Fy_min = -1


	def __init__(self, tmax):
		self.tmax = tmax 
		self.reset()
		print("Estado inicial: ")
		self.printState()
		self.gravity = 10

		self.Vx_range = range(Environment.Vx_min, Environment.Vx_max + 1)
		self.Vy_range = range(Environment.Vy_min, Environment.Vy_max + 1)
		#print(self.Vx_range)

		self.action_space = [range(Environment.Fx_min, Environment.Fx_max + 1),
							 range(Environment.Fy_min, Environment.Fy_max + 1)]

		self.lx = [x for x in range(Environment.SIZE[0])]
		self.ly = [y for y in range(Environment.SIZE[1])]

		### Points (t, x, y)
		desired_path = [(0, 0, 0),
					     	 (5, 70, 30),
							 (15, 100, 105),
							 (30, 150, 205),
							 (34, 200, 300),
							 (50, 300, 360),
							 (60, 350, 380),
							 (100, 600, 410),
							 (105, 560, 420),
							 (120, 500, 460),
							 (150, 430, 400),
							 (170, 580, 300),
							 (190, 610, 380),
							 (200, 800, 200)]

		desired_path2 = [(0, 0, 0),
					     	 (5, 70, 30),
							 (15, 100, 105),
							 (30, 150, 205),
							 (34, 200, 300),
							 (50, 300, 360),
							 (60, 350, 380),
							 (100, 400, 410),
							 (105, 460, 420),
							 (120, 500, 460),
							 (150, 630, 400),
							 (170, 680, 300),
							 (190, 710, 380),
							 (200, 800, 200)]
		
 		desired_path2 = [(0, 0, 0),
			     		 (1, 70, 30),
						 (2, 200, 300),
						 (3, 460, 420),
						 (4, 680, 300),
						 (5, 800, 200)]

 		desired_path2 = [(0, 0, 0),
			     		 (1, 400, 200),
						 (2, 200, 400),
						 (3, 100, 400),
						 (4, 100, 100),
						 (5, 800, 500)]
		
		self.desired_path = desired_path2

		self.final_state = self.desired_path[-1]

		self.actual_path = []
		#self.desired_path = self.createFullDesiredPath(self.tmax)
		
		self.desired_path = np.array(self.desired_path)
		#self.desired_path = self.createFullDesiredPath(5)
		self.reescale_path(2)
		self.path_track = np.zeros(800)



	def reescale_path(self, ratio):
		self.desired_path[:, 1:3] = self.desired_path[:, 1:3] / ratio

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

						desired_x = int(desired_x)
						desired_y = int(desired_y)

						fullDP.append((t, desired_x, desired_y))
						break

		return np.array(fullDP)


	def reset(self):
		""" Resets the environment to its initial state
		"""
		self.x = 0; self.y = 0
		self.Vx = 0; self.Vy = 0
		self.t = 0
		self.m = 1
		self.actual_path = []

	def setState(self, x, y, vx, vy, t):
		""" Sets the environment to a certain state
		"""
		self.x = x; self.y = y
		self.Vx = 0; self.Vy = 0
		self.t = t


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



	def rewardFunction(self, state, t, isPoint=False):
		### Reward to next point
		k1 = 150.0
		### Reward to final point
		k2 = 150.0
		k3 = 300.0
		kf = 3000.0
		

		if type(state) == dict:
			point = (state["x"], state["y"])
			desired_point = self.desired_path[state["t"], 1:3]
		else:
			point = state
			desired_point = self.desired_path[int(t), 1:3]

		distance = np.linalg.norm(desired_point - point)

		return 3000.0 / (distance + 1)
			

	def closestDesiredPoint(self, state):
		""" Returns the closest point and its distance to present point 

		Params:
			state: state dict or location tuple (x, y) 
		Returns:
			Closest point's index, minimum distance 
		"""
		x = self.desired_path[:, 1]
		y = self.desired_path[:, ]
		if type(state) == dict:
			point = (state["x"], state["y"])
		else:
			point = state
		xy = self.desired_path[:, 1:3]
		distances = np.linalg.norm(xy - point)

		return np.argmin(distances), np.min(distances)

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

		### Observation structure
		observation = {"t": None,
					   "x": None,
					   "y": None,
					   "vx": None,
					   "vy": None}
		
	    ### Increase time by 1 
		# if int(self.desired_path[self.t + 1][1]) in [i for i in range(int(self.x) - 10, int(self.x) + 10 )]:
		# 	self.t += 1
		margin = 10
		if int(self.desired_path[self.t + 1][1]) in [i for i in range(int(self.x) - margin, int(self.x) + margin)] and int(self.desired_path[int(self.t  + 1)][2]) in [i for i in range(int(self.y) - margin, int(self.y) + margin)]:
			self.t += 1

		# if self.x == self.desired_path[self.t][1] and self.y == self.desired_path[self.t][2]:
		# 	self.t += 1

		### Action, always considering delta t as 1 
		# self.Fx = action[0]
		# self.Fy = action[1]

		# self.Ax =  float(self.Fx) / self.m
		# self.Ay =  float(self.Fy) / self.m 

		# self.Vx += self.Ax
		# self.Vy += self.Ay

		# if int(self.Vx) not in self.Vx_range:
		# 	self.Vx -= self.Ax
		# if int(self.Vy) not in self.Vy_range:
		# 	self.Vy -= self.Ay

		# self.x += self.Vx
		# self.y += self.Vy

		self.x += action[0]
		self.y += action[1]

		### Passing values to the observation dict
		observation["x"] = self.x
		observation["y"] = self.y
		observation["t"] = self.t
		observation["vx"] = self.Vx
		observation["vy"] = self.Vy

		done = False
		if self.tmax <= self.t + 1:
			done = True
		if self.x not in self.lx or self.y not in self.ly:
			done = True
		try:
			print("Desired point {0}".format(self.desiredPoint()))
		except:
			print("No desired point!")
		self.printState()
		print("Error: {0:.2f}".format(self.squaredError(observation)))
		#print("Reward {0:.2f}".format(self.rewardFunction(observation)))

		reward = self.rewardFunction(observation, self.t)
		return observation, reward, done


	def render(self):
		""" Renders the environment
		"""

		### Making the window blue  
		ratio = 2
		window.fill(BLUE)
		### Drawing desired path
		for i in range(len(self.desired_path) - 1):
			pygame.draw.line(window, 
							 (255, 0, 0), 
							 self.desired_path[i][1:]*ratio, 
							 self.desired_path[i+1][1:]*ratio)

		## Drawing actual path
		for i in range(len(self.actual_path) - 1):
			pygame.draw.line(window, 
							 (100, 255, 100), 
							 np.array(self.actual_path[i][1:])*ratio, 
							 np.array(self.actual_path[i+1][1:])*ratio)

		### Displaying our submarine at (x, y)
		window.blit(submarine, (self.x*ratio - submarine.get_width()/2, self.y*ratio - submarine.get_height()/2))	
		pygame.image.save(window, "screenshot.jpeg")
		### Game loop
		final_loop()

