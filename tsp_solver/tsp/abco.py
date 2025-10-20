import random
import copy
import numpy as np
from .utils import get_distance_matrix

class ArtificialBeeColonyTSP:
    def __init__(self, colony_size=20, max_iterations=200, trials_limit=15):
        self.colony_size = colony_size
        self.max_iterations = max_iterations
        self.trials_limit = trials_limit
        self.cities, self.distance_matrix = get_distance_matrix()
        self.num_cities = len(self.cities)
        self.ilorin_index = 0  # Ilorin is always first
        
        # Initialize colony with diverse routes
        self.colony = [self.generate_random_route() for _ in range(colony_size)]
        self.trials = [0] * colony_size
        self.best_route, self.best_distance = self.find_best()

    def generate_random_route(self):
        """Generate a random route starting and ending with Ilorin"""
        route = list(range(1, self.num_cities))  # Exclude Ilorin
        random.shuffle(route)
        route.insert(0, self.ilorin_index)  # Start with Ilorin
        return route

    def calculate_route_distance(self, route):
        """Calculate total distance of a route including return to start"""
        distance = 0
        for i in range(len(route)-1):
            from_city = route[i]
            to_city = route[i+1]
            distance += self.distance_matrix[from_city][to_city]
        # Add distance back to Ilorin
        distance += self.distance_matrix[route[-1]][route[0]]
        return distance

    def find_best(self):
        """Find the best route in current colony"""
        best_route = min(self.colony, key=self.calculate_route_distance)
        return best_route, self.calculate_route_distance(best_route)

    def optimize_route(self, route):
        """Apply different neighborhood operations to create new solutions"""
        new_route = route.copy()
        operation = random.choice([1, 2, 3, 4])  # Added more operations
        
        if operation == 1:  # Swap
            idx1, idx2 = random.sample(range(1, len(new_route)), 2)
            new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        elif operation == 2:  # Reverse segment
            start, end = sorted(random.sample(range(1, len(new_route)), 2))
            new_route[start:end+1] = reversed(new_route[start:end+1])
        elif operation == 3:  # Insert
            city = random.choice(new_route[1:])
            new_route.remove(city)
            new_route.insert(random.randint(1, len(new_route)), city)
        else:  # Scramble
            start, end = sorted(random.sample(range(1, len(new_route)), 2))
            segment = new_route[start:end+1]
            random.shuffle(segment)
            new_route[start:end+1] = segment
            
        return new_route

    def employed_phase(self):
        """Employed bees explore their current food sources"""
        for i in range(self.colony_size):
            new_route = self.optimize_route(self.colony[i])
            new_distance = self.calculate_route_distance(new_route)
            
            if new_distance < self.calculate_route_distance(self.colony[i]):
                self.colony[i] = new_route
                self.trials[i] = 0
            else:
                self.trials[i] += 1

    def onlooker_phase(self):
        """Onlooker bees select promising solutions based on fitness"""
        fitness = [1 / (self.calculate_route_distance(route) + 1e-10) for route in self.colony]
        total_fitness = sum(fitness)
        
        if total_fitness > 0:
            probabilities = [f / total_fitness for f in fitness]
        else:
            probabilities = [1/self.colony_size] * self.colony_size
            
        for _ in range(self.colony_size):
            i = random.choices(range(self.colony_size), weights=probabilities)[0]
            new_route = self.optimize_route(self.colony[i])
            new_distance = self.calculate_route_distance(new_route)
            
            if new_distance < self.calculate_route_distance(self.colony[i]):
                self.colony[i] = new_route
                self.trials[i] = 0
            else:
                self.trials[i] += 1

    def scout_phase(self):
        """Scout bees discover new food sources"""
        for i in range(self.colony_size):
            if self.trials[i] >= self.trials_limit:
                self.colony[i] = self.generate_random_route()
                self.trials[i] = 0

    def optimize(self):
        """Main optimization loop"""
        for _ in range(self.max_iterations):
            self.employed_phase()
            self.onlooker_phase()
            self.scout_phase()
            
            # Update global best
            current_best, current_distance = self.find_best()
            if current_distance < self.best_distance:
                self.best_route, self.best_distance = current_best, current_distance
        
        return self.best_route, self.best_distance