# Code for branch and bound

class Node:
    def __init__(self):
        self.visited = False

def main():
    # Number of customers and vehicles of the dataset 
    num_customers = int(input("Enter the number of customers: "))
    num_vehicles = int(input("Enter the number of vehicles: "))

    # Pairwise distances between each customer
    distances = []
    for i in range(num_customers + 1):
        distances_row = list(map(int, input(f"Enter the distances from node {i} to all other nodes separated by space: ").split()))
        distances.append(distances_row)

if __name__ == "__main__":
    main()