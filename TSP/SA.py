from util import *
import math

class SA(Optimization):

	def __init__(self, num_node, distance_matrix, fit_f):

		super().__init__(num_node, distance_matrix, fit_f)
		self.T = 0
		for _ in range(4):
			self.T += self.fit_f(self.num_node, self.distance_matrix, self._generate())
		self.T /= 4
		self.perm = self._generate()

	def train(self, tau = 0.8):

		i, j = random.choices(range(self.num_node), k = 2)
		new_perm = self.perm.copy()
		new_perm[i], new_perm[j] = self.perm[j], self.perm[i]
		diff = self.fit_f(self.num_node, self.distance_matrix, new_perm) - \
			 self.fit_f(self.num_node, self.distance_matrix, self.perm)
		if diff < 0:
			self.perm = new_perm
		elif random.uniform(0, 1) < math.exp(-diff / self.T):
			self.perm = new_perm
		self.T *= tau

		# print(self.fit_f(self.num_node, self.distance_matrix, self.perm))

		return
