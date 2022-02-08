from util import *

class GA(Optimization):

	def __init__(self, num_node, distance_matrix, fit_f, num_particle):		

		super().__init__(num_node, distance_matrix, fit_f)
		self.perm = [self._generate() for _ in range(num_particle)]

	def _selection(self, k):
		### Rank selection, simplest!

		self.perm.sort(key = lambda s: self.fit_f(self.num_node, self.distance_matrix, s))
		return list(range(2 * k))

	def _crossover(self, parent1, parent2):

		g1, g2 = random.choices(range(self.num_node), k = 2)
		g1, g2 = min(g1, g2), max(g1, g2)

		child = [parent1[i] for i in range(g1, g2)]
		child.extend([g for g in parent2 if g not in child])
		return child

	def _mutation(self, perm):

		i, j = random.choices(range(self.num_node), k = 2)
		perm[i], perm[j] = perm[j], perm[i]		
		return perm

	def train(self, k = 1):
		
		mating_pool = self._selection(k)

		for i in range(k):
			new_perm = self._crossover(self.perm[mating_pool[2 * i]], self.perm[mating_pool[2 * i + 1]])
			new_perm = self._mutation(new_perm)
			self.perm[-k+i] = new_perm

		# print(self.fit_f(self.num_node, self.distance_matrix, self.perm[0]))

		return

