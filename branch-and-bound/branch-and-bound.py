# Code for branch and bound
import numpy as np
import heapq

class Node:
    def __init__(self):
        self.visited = False

def solve(distances, numVehicles, numCustomers):
    # Initialisation of routes and cost
    routes = []
    cost = float('inf')
    minHeap = []

    # Path costs
    runningCosts = [0]

    # Remaining customers
    remainingCustomers = [list(range(1,numCustomers+1))]

    # List of potential solutions - originally all start from depot
    potentialSolutions = [[0]]

    while (potentialSolutions != []):
        # Retrieve current potential solution information
        path = potentialSolutions.pop(0)
        currentRemainingCustomers = remainingCustomers.pop(0)
        currentCost = runningCosts.pop(0)

        # Last visited node for next distance calculation
        lastVisited = path[-1]

        # Iterate through which customer to visit next
        for customer in currentRemainingCustomers:
            newRemainingCustomers = [c for c in currentRemainingCustomers if c != customer]
            newPath = path + [customer]
            newCost = currentCost + distances[lastVisited][customer]

            # If not a complete solution then add to potential solutions to explore
            # If a complete solution then add distance to depot and add to min heap
            if (len(newPath) != numCustomers+1):
                potentialSolutions.append(newPath)
                remainingCustomers.append(newRemainingCustomers)
                runningCosts.append(newCost)
            else:
                newPath += [0]
                newCost += distances[customer][0]
                heapq.heappush(minHeap, (newCost, [newPath]))

    # Retrive best route
    cost, routes = heapq.heappop(minHeap)
    return cost, routes

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