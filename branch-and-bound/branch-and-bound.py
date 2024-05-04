# Code for branch and bound

class Node:
    def __init__(self, location):
        self.location = location
        self.visited = False

def main():
    # Number of customers and vehicles of the dataset 
    num_customers = int(input("Enter the number of customers: "))
    num_vehicles = int(input("Enter the number of vehicles: "))

    # Locations of each customer
    nodes = []
    for i in range(num_customers):
        x, y = map(int, input(f"Location (x y) of customer {i+1}: ").split())
        nodes.append(Node((x, y)))

    # Add depot to end of list for separation of nodes
    depot = Node((0, 0))
    nodes.append(depot)

if __name__ == "__main__":
    main()