import matplotlib.pyplot as plt
import random

def sample_valid_f(weight, gene):

	carry = sum(gene[:3]) * sum(gene[3:6]) * sum(gene[12:])
	total_weight = sum(x * y for x, y in zip(weight, gene))

	return (carry > 0 and total_weight <= 529)

def sample_fit_f(point, gene):
	
	total_point = sum(x * y for x, y in zip(point, gene))
	bonus = 5 * gene[0] * gene[5] + \
		15 * gene[3] * (gene[8] | gene[9]) + \
		25 * (gene[7] | gene[10]) * gene[5] * gene[14] + \
		70 * (gene[12] * gene[13] * gene[14])

	return (total_point + bonus)

class GA(object):

	def __init__(self, weight, point, valid_f, fit_f, n):

		self.weight = weight
		self.point = point
		self.valid_f = valid_f
		self.fit_f = fit_f

		self.n = n # num of particle
		self.L = len(weight)
		self.genes = [self._gen() for _ in range(n)]
	
		self.mut_prob = 0.1

	def _gen(self):

		check = False
		while check != True:
			gene = [random.randint(0, 1) for _ in range(self.L)]
			check = self.valid_f(self.weight, gene)
		return gene

	def _selection(self, k):
		
		self.genes.sort(key = lambda s: self.fit_f(self.point, s))
		
		"""
		Sample k pairs of genes according to their fitness    
		Here, we only support Roulette Wheel Selection
		"""
		points = [0] + [self.fit_f(self.point, self.genes[_]) for _ in range(self.n)]
		m = min(points)
		s = 0
		for i in range(self.n):
			s = s + (points[i] - m)
			points[i] = s
		
		mating_pool = []
	
		for _ in range(2 * k):
			r = random.uniform(0, s)
			for i in range(self.n):
				if points[i] <= r and points[i+1] > r:
					mating_pool += [i]
					break

		return mating_pool

	def _crossover(self, gene1, gene2):

		while True:
			new_gene = []

			for i in range(self.L):
				r = random.random()
				if r * gene1[i] + (1-r) * gene2[i] > 0.5:
					new_gene += [1]
				else:
					new_gene += [0]

			if self.valid_f(self.weight, new_gene):
				return new_gene

	def _mutation(self, gene):

		while True:
		
			a = random.randint(0, self.L)
			b = random.randint(a, self.L)
			
			_gene = [gene[_] if _ < a or _ > b else 1 - gene[_] for _ in range(self.L)]

			if self.valid_f(self.weight, _gene):
				return _gene

	def train(self, k = 1):
		
		mating_pool = self._selection(k)

		for i in range(k):
			new_gene = self._crossover(self.genes[mating_pool[2 * i]], self.genes[mating_pool[2 * i + 1]])
			new_gene = self._mutation(new_gene)
			self.genes[i] = new_gene

		# print(self.fit_f(self.point, self.genes[-1]))
	
		return
