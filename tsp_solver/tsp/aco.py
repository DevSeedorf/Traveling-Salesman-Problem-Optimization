import random
import numpy as np
from .utils import get_distance_matrix

class AntColonyTSP:
    def __init__(self, num_ants=15, num_iterations=100, alpha=1, beta=3, evaporation=0.3):
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        
        self.cities, self.distance_matrix = get_distance_matrix()
        self.num_cities = len(self.cities)
        self.ilorin_index = 0
        
        # Initialize pheromones
        self.pheromones = np.ones((self.num_cities, self.num_cities)) * 0.1
        np.fill_diagonal(self.pheromones, 0)
        
        # Precompute visibility (1/distance)
        self.visibility = 1 / (np.array(self.distance_matrix) + 1e-10)
        np.fill_diagonal(self.visibility, 0)

    def run_ant(self):
        route = [self.ilorin_index]
        unvisited = set(range(self.num_cities)) - {self.ilorin_index}
        
        while unvisited:
            current = route[-1]
            probabilities = []
            
            for city in unvisited:
                pheromone = self.pheromones[current][city] ** self.alpha
                visibility = self.visibility[current][city] ** self.beta
                probabilities.append(pheromone * visibility)
            
            # Normalize
            total = sum(probabilities)
            if total > 0:
                probabilities = [p/total for p in probabilities]
            else:
                probabilities = [1/len(unvisited)] * len(unvisited)
            
            next_city = random.choices(list(unvisited), weights=probabilities)[0]
            route.append(next_city)
            unvisited.remove(next_city)
        
        return route

    def update_pheromones(self, routes):
        # Evaporate
        self.pheromones *= (1 - self.evaporation)
        
        # Add new pheromones
        for route in routes:
            distance = self.calculate_distance(route)
            if distance > 0:
                pheromone = 1 / distance
                for i in range(len(route)):
                    from_city = route[i]
                    to_city = route[(i+1)%len(route)]
                    self.pheromones[from_city][to_city] += pheromone

    def calculate_distance(self, route):
        distance = 0
        for i in range(len(route)-1):
            distance += self.distance_matrix[route[i]][route[i+1]]
        distance += self.distance_matrix[route[-1]][route[0]]  # Return to start
        return distance

    def optimize(self):
        best_route = None
        best_distance = float('inf')
        
        for _ in range(self.num_iterations):
            routes = [self.run_ant() for _ in range(self.num_ants)]
            self.update_pheromones(routes)
            
            for route in routes:
                current_distance = self.calculate_distance(route)
                if current_distance < best_distance:
                    best_route = route
                    best_distance = current_distance
        
        return best_route, best_distance