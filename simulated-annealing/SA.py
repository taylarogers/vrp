import numpy as np
import random
import math
import time
import os
import re
import sys

#DID THIS WORK
class Vehicle:
    def __init__(self):
        self.route = []

    def __str__(self):
        # Convert each city index in the route to city number (adding 1)
        route_with_depot = [0] + [city + 1 for city in self.route] + [0]
        return str(route_with_depot)

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
        # Generate initial solution by assigning cities to vehicles randomly
        #With "solution" being an array that holds the vehicle objects, and each vehicle object has an array that represents its own route
        solution = []
        cities = list(range(len(self.distance_matrix)))

        random.shuffle(cities)
        for i in range(self.num_vehicles):
            vehicle = Vehicle()
            vehicle.route = cities[i::self.num_vehicles]
            solution.append(vehicle)
        #for vehicle in solution:
            #print(vehicle)
        return solution
    

      

    def total_distance(self, solution):
        # Calculate total distance of a solution
        total_dist = 0
        for vehicle in solution:
            route = vehicle.route
            route_length = len(route)
            # Add distance from depot to starting city
            total_dist += self.depot_distances_to_cities[route[0]]
            for i in range(route_length - 1):
                total_dist += self.distance_matrix[route[i]][route[i+1]]
            # Add distance from ending city back to depot
            total_dist += self.depot_distances_from_cities[route[-1]]
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

        if(self.num_vehicles == 1):
            switch_chance = 1
        else:
            switch_chance = 0.65

        if random.random() < switch_chance:
            # Swap two cities within the selected vehicle's route
            if len(selected_vehicle.route) >= 2:
                idx1, idx2 = random.sample(range(len(selected_vehicle.route)), 2)
                selected_vehicle.route[idx1], selected_vehicle.route[idx2] = selected_vehicle.route[idx2], selected_vehicle.route[idx1]
                #print("Swapped two cities within the selected vehicle's route    ", selected_vehicle.route)
        else:
            # Select another vehicle that is not the currently selected vehicle
            other_vehicles = [v for v in new_solution if v != selected_vehicle]
            other_vehicle = random.choice(other_vehicles)
 
            # Remove a random city from the first vehicle's route and insert it at a random position in the second vehicle's route
            if selected_vehicle.route and other_vehicle.route and len(selected_vehicle.route) > 1:
                city = random.choice(selected_vehicle.route)
                selected_vehicle.route.remove(city)
                other_vehicle.route.insert(random.randrange(len(other_vehicle.route)), city)
               # print("Removed a random city from the first vehicle's route and inserted it at a random position in the second vehicle's route    ", selected_vehicle.route, other_vehicle.route)
           # else:
               # print("No change was made because only one city in a route chosen")
        return new_solution



    def clarke_wright_savings_general(self):
        num_customers = len(self.distance_matrix)
    
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
                if route_i[-1] == i and route_j[0] == j:
                    new_route = route_i + route_j
                elif route_i[0] == i and route_j[-1] == j:
                    new_route = route_j + route_i
                elif route_i[0] == i and route_j[0] == j:
                    new_route = list(reversed(route_j)) + route_i
                else:
                    new_route = route_i + list(reversed(route_j))
    
                # Update the routes
                routes.remove(route_i)
                routes.remove(route_j)
                routes.append(new_route)
    
                # Update the mapping
                for city in new_route:
                    city_to_route[city] = new_route
    
        # Ensure all cities are included
        all_cities = set(range(num_customers))
        included_cities = {city for route in routes for city in route}
    
        # Reinsert missing cities
        for missing_city in all_cities - included_cities:
            print(f"Reinserting missing city: {missing_city + 1}")
            best_route = None
            best_cost_increase = float('inf')
            for route in routes:
                for k in range(len(route) + 1):
                    new_route = route[:k] + [missing_city] + route[k:]
                    cost_increase = (self.depot_distances_to_cities[new_route[0]] +
                                     self.depot_distances_from_cities[new_route[-1]] +
                                     sum(self.distance_matrix[new_route[i]][new_route[i + 1]]
                                         for i in range(len(new_route) - 1)))
                    if cost_increase < best_cost_increase:
                        best_cost_increase = cost_increase
                        best_route = new_route
    
            if best_route:
                routes.append(best_route)
                for city in best_route:
                    city_to_route[city] = best_route
    
        # Reduce routes to specified number of vehicles by merging as necessary
        while len(routes) > self.num_vehicles:
            route1 = routes.pop()
            route2 = routes.pop()
            merged_route = route1 + route2
            routes.append(merged_route)
    
        # Convert the final routes into a list of Vehicle objects
        vehicles = []
        for route in routes:
            vehicle = Vehicle()
            vehicle.route = route
            vehicles.append(vehicle)
    
        # Calculate total cost for the final routes
        total_cost = 0
        for route in routes:
            if route:  # Ensure route is not empty
                total_cost += self.depot_distances_to_cities[route[0]]  # From depot to first city
                for k in range(len(route) - 1):
                    total_cost += self.distance_matrix[route[k]][route[k + 1]]  # Between cities
                total_cost += self.depot_distances_from_cities[route[-1]]  # From last city to depot
    
        return vehicles, total_cost
    


    



    def run(self):
        # Run simulated annealing
       # print("STARTING RUN")
       # print("DISTANCES TO CITIES FROM DEPOT ", self.depot_distances_to_cities)
       # print("DISTANCES FROM CITIES TO DEPOT ", self.depot_distances_from_cities)
        # current_solution = self.initial_solution()
        # current_distance = self.total_distance(current_solution)


        current_solution, current_distance = self.clarke_wright_savings_general()
        print("Routes:", current_solution)
        print("Total Cost:", current_distance)
       # print("BElow i am printing the starting solution now!!!")
       # for vehicle in current_solution: print(vehicle)
       # print("EXP done now")

        for iteration in range(self.num_iterations):
            for _ in range(self.runs_at_temperature):

                # print("\n")
                # print("ITeration: ", iteration)
                # print("Run at temperature: ", _, "temperature: ", self.temperature)
                # print("Current solution: ")
                # for vehicle in current_solution: print(vehicle)
                # print("Current distance: ", current_distance)   
                # print("\n")
                new_solution = self.generate_neighbor(current_solution)
                #for vehicle in new_solution: print(vehicle)
                new_distance = self.total_distance(new_solution)
                # print("New distance: ", new_distance)

                if new_distance < current_distance:
                    # print("New distance is less than current distance")
                    # print("Old solution was: ")
                    # for vehicle in current_solution: print(vehicle)
                    # print("Old distance was: ", self.best_distance)
                    # print("New solution is: ")
                    # for vehicle in new_solution: print(vehicle)
                    # print("New distance is: ", new_distance)


                    current_solution = new_solution
                    current_distance = new_distance
                    if new_distance < self.best_distance:
                       # print("New distance is less than best distance")
                        self.best_solution = new_solution
                        self.best_distance = new_distance
                        self.stagnation_counter = 0 
                    else:
                        self.stagnation_counter += 1
                      #  print("Stagnation counter: ", self.stagnation_counter)
                        if self.stagnation_counter >= self.stagnation_threshold:
                          #  print("Stagnation counter is greater than stagnation threshold")
                            return self.best_solution, self.best_distance
               


                elif self.acceptance_probability(current_distance, new_distance) > random.random():
                    # print("Acceptance probability is greater than random number")
                    # print("Old solution was: ")
                    # for vehicle in current_solution: print(vehicle)
                    # print("Old distance was: ", current_distance)
                    # print("New solution is: ")
                    # for vehicle in new_solution: print(vehicle)
                    # print("New distance is: ", new_distance)    

                    current_solution = new_solution
                    current_distance = new_distance

            self.update_temperature()

        return self.best_solution, self.best_distance

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

    # Convert to NumPy array - readability and performance
    distance_matrix = np.array(distances)

    # Start time - only measuring how long the solving function takes (not file reading etc.)
    startTime = time.time()

    # Example distance matrix and number of vehicles
    # distance_matrix = np.array([
    #     [0, 424, 421, 460, 64],
    #     [189, 0, 127, 241, 71],
    #     [270, 331, 0, 443, 252],
    #     [158, 239, 255, 0, 269],
    #     [488, 23, 296, 181, 0]
    # ])


    # num_vehicles = 2

    # distance_matrix = np.array([
    #     [0, 409, 112, 261 ],
    #     [326, 0, 58, 94 ],
    #     [252, 420, 0, 238 ],
    #     [403, 411, 125, 0]
    # ])

    # num_vehicles = 1

    # Initialize and run simulated annealing
    sa = SimulatedAnnealing(distance_matrix, num_vehicles)
    best_solution, best_distance = sa.run()

    endTime = time.time()

    # Calculate how long program took to solve
    timeTaken = endTime - startTime


    print("Best solution:")
    for vehicle in best_solution: print(vehicle)
    print("Optimal cost:", best_distance)
    print("Time taken: " +  str(timeTaken) + " seconds")

    

if __name__ == "__main__":
    main()

# 0 424 421 460 64 
# 189 0 127 241 71 
# 270 331 0 443 252 
# 158 239 255 0 269 
# 488 23 296 181 0 