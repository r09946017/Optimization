from util import *

class ACO(Optimization):

	def __init__(self, num_node, distance_matrix, fit_f, num_particle):
		
		super().__init__(num_node, distance_matrix, fit_f)

		self.num_particle = num_particle
		self.pheromone = [[1 for i in range(self.num_node)] for j in range(self.num_node)]
	
	def train(self, tau = 0.8):
		ant = []
		for i in range(self.num_particle):
			### Select a start point
			k = random.randint(0, self.num_node-1)
			perm = [k]
			unvisited = list(range(self.num_node))
			unvisited.remove(k)
			### Generate a random cycle
			for j in range(1, self.num_node):
				s = sum([self.pheromone[k][dst] for dst in unvisited])
				prob = [self.pheromone[k][dst] / s for dst in unvisited]
				k = random.choices(unvisited, prob, k = 1)[0]
				perm += [k]
				unvisited.remove(k)
			ant += [[perm, self.fit_f(self.num_node, self.distance_matrix, perm)]]

		### Find max, min and count the number of "best" ants
		best_ind, best_score, worst_score = [], ant[0][1], ant[0][1]
		for i in range(self.num_particle):
			if ant[i][1] < best_score:
				best_score = ant[i][1]
				best_ind = [i]
			elif ant[i][1] == best_score:
				best_ind += [i]
			
			worst_score = min(worst_score, ant[i][1])
		### Update pheromone according to the simulation results
		for i in range(self.num_node):
			for j in range(self.num_node):
				self.pheromone[i][j] *= tau
		for ind in best_ind:
			for i in range(self.num_node):
				x = ant[ind][0][i]
				y = ant[ind][0][(i+1) % self.num_node]
				self.pheromone[x][y] += 2 * best_score / worst_score
				self.pheromone[y][x] += 2 * best_score / worst_score

		# print(best_score)
		
		return 
