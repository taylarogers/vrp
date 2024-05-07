import numpy as np
import random
import math

class Vehicle:
    def __init__(self):
        self.route = []

class SimulatedAnnealing:
    def __init__(self, distance_matrix, num_vehicles):
        self.distance_matrix = distance_matrix
        self.num_vehicles = num_vehicles
        self.temperature = 1000  # Initial temperature
        self.cooling_rate = 0.003  # Cooling rate
        self.num_iterations = 1000
        self.runs_at_temperature = 100
        self.best_solution = None
        self.best_distance = float('inf')

    def initial_solution(self):
        # Generate initial solution by assigning cities to vehicles randomly
        #With "solution" being an array that holds the vehicle objects, and each vehicle object has an array that represents its own route
        solution = []
        cities = list(range(len(self.distance_matrix)))
        random.shuffle(cities)
        for i in range(self.num_vehicles):
            vehicle = Vehicle()
            vehicle.route = cities[i::self.num_vehicles]
            solution.append(vehicle)
        for vehicle in solution:
            print(vehicle.route)
        return solution
    

      

    def total_distance(self, solution):
        # Calculate total distance of a solution
        total_dist = 0
        for vehicle in solution:
            route = vehicle.route
            for i in range(len(route) - 1):
                total_dist += self.distance_matrix[route[i]][route[i+1]]
        return total_dist

    def acceptance_probability(self, old_dist, new_dist):
        # Calculate acceptance probability
        if new_dist < old_dist:
            return 1.0
        return math.exp((old_dist - new_dist) / self.temperature)

    def update_temperature(self):
        # Update temperature
        self.temperature *= 1 - self.cooling_rate

    def generate_neighbor(self, solution):
        # Generate a neighboring solution by swapping two randomly chosen cities within a vehicle's route according to a random probability
        #as well as by also according to a random , smaller possibility of swapping two cities between two vehicles, and when doing so, ensure 
        #thatt each city only apperas in a route once by selecting a random city from a random vehicle, selecting another vehicle which is NOT THE CURRENT OTHER CITY, 
        #and then removing the city from the first vehicles route, and adding it randomly in the array somewhere of the second vehicles route
    
       # Copy the current solution to a new solution
        new_solution = [Vehicle() for _ in range(self.num_vehicles)]
        for i in range(self.num_vehicles):
            new_solution[i].route = solution[i].route.copy()

       # Select a random vehicle
        selected_vehicle = random.choice(new_solution)

        if random.random() < 0.5:
            # Swap two cities within the selected vehicle's route
            if len(selected_vehicle.route) >= 2:
                idx1, idx2 = random.sample(range(len(selected_vehicle.route)), 2)
                selected_vehicle.route[idx1], selected_vehicle.route[idx2] = selected_vehicle.route[idx2], selected_vehicle.route[idx1]
                print("Swapped two cities within the selected vehicle's route    ", selected_vehicle.route)
        else:
            # Select another vehicle that is not the currently selected vehicle
            other_vehicles = [v for v in new_solution if v != selected_vehicle]
            other_vehicle = random.choice(other_vehicles)
 
            # Remove a random city from the first vehicle's route and insert it at a random position in the second vehicle's route
            if selected_vehicle.route and other_vehicle.route and len(selected_vehicle.route) > 1:
                city = random.choice(selected_vehicle.route)
                selected_vehicle.route.remove(city)
                other_vehicle.route.insert(random.randrange(len(other_vehicle.route)), city)
            print("Removed a random city from the first vehicle's route and inserted it at a random position in the second vehicle's route    ", selected_vehicle.route, other_vehicle.route)
 
        return new_solution


    def run(self):
        # Run simulated annealing
        current_solution = self.initial_solution()
        current_distance = self.total_distance(current_solution)

        for iteration in range(self.num_iterations):
            for _ in range(self.runs_at_temperature):

                print("\n")
                print("ITeration: ", iteration)
                print("Run at temperature: ", _, "temperature: ", self.temperature)
                print("Current solution: ", current_solution)
                print("Current distance: ", current_distance)   
                print("\n")
                new_solution = self.generate_neighbor(current_solution)
                print("New solution: ", new_solution)
                new_distance = self.total_distance(new_solution)
                print("New distance: ", new_distance)

                if new_distance < self.best_distance:
                    print("New distance is less than best distance")
                    print("Old solution was: ", self.best_solution)
                    print("Old distance was: ", self.best_distance)
                    print("New solution is: ", new_solution)
                    print("New distance is: ", new_distance)
                    self.best_solution = new_solution
                    self.best_distance = new_distance
                else:
                    print("New distance is not less than best distance")


                if self.acceptance_probability(current_distance, new_distance) > random.random():
                    print("Acceptance probability is greater than random number")
                    print("Old solution was: ", current_solution)
                    print("Old distance was: ", current_distance)
                    print("New solution is: ", new_solution)
                    print("New distance is: ", new_distance)    

                    current_solution = new_solution
                    current_distance = new_distance

            self.update_temperature()

        return self.best_solution, self.best_distance

def main():
    # Example distance matrix and number of vehicles
    distance_matrix = np.array([
        [0, 424, 421, 460, 64],
        [189, 0, 127, 241, 71],
        [270, 331, 0, 443, 252],
        [158, 239, 255, 0, 269],
        [488, 23, 296, 181, 0]
    ])
    num_vehicles = 2

    # Initialize and run simulated annealing
    sa = SimulatedAnnealing(distance_matrix, num_vehicles)
    best_solution, best_distance = sa.run()

    print("Best solution:", best_solution)
    print("Total distance:", best_distance)

if __name__ == "__main__":
    main()

# 0 424 421 460 64 
# 189 0 127 241 71 
# 270 331 0 443 252 
# 158 239 255 0 269 
# 488 23 296 181 0 