# Code for branch and bound
import numpy as np
import heapq
from itertools import combinations

class Node:
    def __init__(self):
        self.visited = False

# Generate all possible distributions of customers to vehicles
def distribute_customers(customers, numVehicles):
    if numVehicles == 1:
        return [(customers,)]
    else:
        distributions = []
        for r in range(1, len(customers)):
            for subset in combinations(customers, r):
                remaining = list(set(customers) - set(subset))
                for rest in distribute_customers(remaining, numVehicles - 1):
                    distributions.append((list(subset),) + rest)
        return distributions

# Solve the problem instance using branch and bound
def solve(distances, numVehicles, numCustomers):
    # Calculating distribution of customers between vehicles
    customers = list(range(1, numCustomers+1))
    customerDistributions = distribute_customers(customers, numVehicles)

    # Values to store the optimal solution
    bestCost = float('inf')
    bestRoute = []

    for distribution in customerDistributions:
        # Initialise distribution values
        distributionCost = 0
        distributionRoutes = []

        # Optimise the customer routes for each vehicle in current distribution
        for vehicle in range(numVehicles):
            minHeap = []

            # Path costs
            runningCosts = [0]

            # Remaining customers (decided by how customers split in distribution)
            remainingCustomers = [distribution[vehicle]]
            numVehicleCustomers = len(remainingCustomers[0])

            # List of potential solutions (originally all start from depot)
            potentialSolutions = [[0]]

            # Current best route cost - used to prune suboptimal branches
            currentBestRouteCost = float('inf')

            while (potentialSolutions != []):
                # Find next node to explore using a Best-First Search strategy on the minimum costs
                nextNodeIndex = runningCosts.index(min(runningCosts))

                # Retrieve current potential solution information
                path = potentialSolutions.pop(nextNodeIndex)
                currentRemainingCustomers = remainingCustomers.pop(nextNodeIndex)
                currentCost = runningCosts.pop(nextNodeIndex)

                # Last visited node for next distance calculation
                lastVisited = path[-1]

                # Iterate through which customer to visit next
                for customer in currentRemainingCustomers:
                    newRemainingCustomers = [c for c in currentRemainingCustomers if c != customer]
                    newPath = path + [customer]
                    newCost = currentCost + distances[lastVisited][customer]

                    # If not a complete solution then add to potential solutions to explore
                    # If a complete solution then add distance to depot and add to min heap
                    if (len(newPath) != numVehicleCustomers+1):
                        # Do not add current route to potential solutions if it is already over the current best known solution
                        if (newCost < currentBestRouteCost):
                            potentialSolutions.append(newPath)
                            remainingCustomers.append(newRemainingCustomers)
                            runningCosts.append(newCost)
                    else:
                        newPath += [0]
                        newCost += distances[customer][0]
                        heapq.heappush(minHeap, (newCost, newPath))

                        # Update new lowest full route cost
                        if (newCost < currentBestRouteCost):
                            currentBestRouteCost = newCost

            # Retrieve route with lowest cost
            vehicleCost, vehicleRoute = heapq.heappop(minHeap)

            # Update values for the distribution
            distributionCost += vehicleCost
            distributionRoutes.append(vehicleRoute)

        # Best distribution results - update
        if (distributionCost < bestCost):
            bestCost = distributionCost
            bestRoute = distributionRoutes
    
    return bestCost, bestRoute

def main():
    # Number of customers and vehicles of the dataset 
    numCustomers = int(input("Enter the number of customers: "))
    numVehicles = int(input("Enter the number of vehicles: "))

    # Pairwise distances between each customer
    distances = []
    for i in range(numCustomers + 1):
        distancesRow = list(map(int, input(f"Enter the distances from node {i} to all other nodes separated by a space: ").split()))
        distances.append(distancesRow)

    # Convert to NumPy array - readability and performance
    distancesMatrix = np.array(distances)

    # Solve VRP using branch and bound
    cost, routes = solve(distancesMatrix, numVehicles, numCustomers)

    # Print out info
    for i, route in enumerate(routes):
        print(f"Route for Vehicle {i+1}:", route)

    print("Optimal cost:", cost)

if __name__ == "__main__":
    main()