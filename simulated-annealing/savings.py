import numpy as np

def clarke_wright_savings_general(distance_matrix, num_vehicles):
    num_customers = len(distance_matrix) - 1
    depot = 0
    # Start with each customer as an individual route
    routes = [[i] for i in range(1, num_customers + 1)]
    route_costs = [distance_matrix[depot][i] + distance_matrix[i][depot] for i in range(1, num_customers + 1)]

    # Calculate savings
    savings = []
    for i in range(1, num_customers + 1):
        for j in range(i + 1, num_customers + 1):
            save = distance_matrix[depot][i] + distance_matrix[depot][j] - distance_matrix[i][j]
            savings.append((save, i, j))
    
    # Sort savings in descending order
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Merge routes based on savings until we have the desired number of vehicles
    while len(routes) > num_vehicles and savings:
        save, i, j = savings.pop(0)
        
        # Find routes that contain i and j
        route_i = next(route for route in routes if i in route)
        route_j = next(route for route in routes if j in route)
        
        if route_i != route_j:
            # Merge routes
            route_i.extend(route_j)
            routes.remove(route_j)
            
            # Update route costs
            route_costs.remove(distance_matrix[depot][route_j[0]] + distance_matrix[route_j[-1]][depot])
            new_cost = (
                distance_matrix[depot][route_i[0]] +
                distance_matrix[route_i[-1]][depot] +
                sum(distance_matrix[route_i[k]][route_i[k + 1]] for k in range(len(route_i) - 1))
            )
            route_costs.append(new_cost)
    
    total_cost = sum(route_costs)
    return routes, total_cost

# Example usage
distance_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

num_vehicles = 2
routes, cost = clarke_wright_savings_general(distance_matrix, num_vehicles)
print("Routes:", routes)
print("Total Cost:", cost)
