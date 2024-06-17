import numpy as np
import random
import math
import os
import re
import sys

class Vehicle:
    def __init__(self):
        self.route = []

    def __str__(self):
        route_with_depot = [0] + [city + 1 for city in self.route] + [0]
        return " -> ".join(map(str, route_with_depot))

class SimulatedAnnealing:
    def __init__(self, distance_matrix, num_vehicles):
        self.distance_matrix = distance_matrix[1:, 1:]
        self.num_vehicles = num_vehicles
        self.depot_distances_to_cities = distance_matrix[0, 1:]
        self.depot_distances_from_cities = distance_matrix[1:, 0]
        self.temperature = 1000  # Initial temperature
        self.cooling_rate = 0.01  # Cooling rate
        self.num_iterations = 100
        self.runs_at_temperature = 10
        self.best_solution = None
        self.best_distance = float('inf')
        self.stagnation_counter = 0  # Counter to track stagnant iterations
        self.stagnation_threshold = 100

    def initial_solution(self):
        solution = []
        cities = list(range(len(self.distance_matrix)))
        random.shuffle(cities)
        for i in range(self.num_vehicles):
            vehicle = Vehicle()
            vehicle.route = cities[i::self.num_vehicles]
            solution.append(vehicle)
        return solution

    def total_distance(self, solution):
        total_dist = 0
        for vehicle in solution:
            route = vehicle.route
            route_length = len(route)
            total_dist += self.depot_distances_to_cities[route[0]]
            for i in range(route_length - 1):
                total_dist += self.distance_matrix[route[i]][route[i + 1]]
            total_dist += self.depot_distances_from_cities[route[-1]]
        return total_dist

    def acceptance_probability(self, old_dist, new_dist):
        if new_dist < old_dist:
            return 1.0
        return math.exp((old_dist - new_dist) / self.temperature)

    def update_temperature(self):
        self.temperature *= 1 - self.cooling_rate

    def generate_neighbor(self, solution):
        new_solution = [Vehicle() for _ in range(self.num_vehicles)]
        for i in range(self.num_vehicles):
            new_solution[i].route = solution[i].route.copy()

        selected_vehicle = random.choice(new_solution)
        if self.num_vehicles == 1:
            switch_chance = 1
        else:
            switch_chance = 0.65

        if random.random() < switch_chance:
            if len(selected_vehicle.route) >= 2:
                idx1, idx2 = random.sample(range(len(selected_vehicle.route)), 2)
                selected_vehicle.route[idx1], selected_vehicle.route[idx2] = selected_vehicle.route[idx2], selected_vehicle.route[idx1]
        else:
            other_vehicles = [v for v in new_solution if v != selected_vehicle]
            other_vehicle = random.choice(other_vehicles)

            if selected_vehicle.route and other_vehicle.route and len(selected_vehicle.route) > 1:
                city = random.choice(selected_vehicle.route)
                selected_vehicle.route.remove(city)
                other_vehicle.route.insert(random.randrange(len(other_vehicle.route)), city)
        return new_solution

    def clarke_wright_savings_general(self):
        num_customers = len(self.distance_matrix)
        depot = 0

        # Initialize routes with each customer in their own route
        routes = [[i] for i in range(num_customers)]

        # Calculate savings
        savings = []
        for i in range(num_customers):
            for j in range(i + 1, num_customers):
                save = (self.depot_distances_to_cities[i] +
                        self.depot_distances_to_cities[j] -
                        self.distance_matrix[i][j])
                savings.append((save, i, j))

        # Sort savings in descending order
        savings.sort(reverse=True, key=lambda x: x[0])

        # Create a mapping from cities to their current route
        city_to_route = {i: routes[i] for i in range(num_customers)}

        # Merge routes based on savings until we have the desired number of vehicles
        while len(routes) > self.num_vehicles and savings:
            save, i, j = savings.pop(0)

            route_i = city_to_route[i]
            route_j = city_to_route[j]

            if route_i != route_j:
                # Merge the routes
                new_route = route_i + route_j

                # Update the routes
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(new_route)

                # Update the mapping
                for city in new_route:
                    city_to_route[city] = new_route

        # Calculate total cost for the final routes
        total_cost = 0
        for route in routes:
            if route:  # Ensure route is not empty
                total_cost += self.depot_distances_to_cities[route[0]]  # From depot to first city
                for k in range(len(route) - 1):
                    total_cost += self.distance_matrix[route[k]][route[k + 1]]  # Between cities
                total_cost += self.depot_distances_from_cities[route[-1]]  # From last city to depot

        return routes, total_cost

    def run(self):
        # Run simulated annealing
        current_solution = self.initial_solution()
        print("Initial random solution: ")
        for vehicle in current_solution:
            print(vehicle)

        current_distance = self.total_distance(current_solution)
        print("Initial random distance: ", current_distance)

        routes, cost = self.clarke_wright_savings_general()
        print("Clarke and Wright savings routes:")
        for route in routes:
            print("0 -> " + " -> ".join(map(lambda x: str(x + 1), route)) + " -> 0")
        print("Clarke and Wright savings total cost:", cost)

def main():
    datasetFolder = '../dataset'

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the filename: ")

    filePath = os.path.join(datasetFolder, filename)

    # Extract numbers from filename
    numbers = re.findall(r'\d+', filename)

    # Determine number of customers and number of vehicles from filename
    numCustomers = int(numbers[0])
    num_vehicles = int(numbers[1])

    # Open the file and read the distance matrix
    with open(filePath, 'r') as file:
        lines = file.readlines()[2:]
        distances = [[int(num) for num in line.split()] for line in lines]

    # Convert to NumPy array
    distance_matrix = np.array(distances)

    # Initialize and run simulated annealing
    sa = SimulatedAnnealing(distance_matrix, num_vehicles)
    sa.run()

if __name__ == "__main__":
    main()
