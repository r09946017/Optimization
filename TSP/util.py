import random

class Optimization(object):

	def __init__(self, num_node, distance_matrix, fit_f):

		self.num_node = num_node
		self.distance_matrix = distance_matrix

		self.fit_f = fit_f

	def _generate(self):

		l = list(range(self.num_node))
		random.shuffle(l)
		return l

