import numpy as np
import matplotlib.pyplot as plt
from qiskit_algorithms.utils import algorithm_globals
from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import SPSA
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Sampler
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import math
import time
import os
import re
import sys



class QuantumOptimizer:
    def __init__(self, instance, n, K):
        self.instance = instance
        self.n = n
        self.K = K

    def binary_representation(self, x_sol=0):
        instance = self.instance
        n = self.n
        K = self.K
        A = np.max(instance) * 100

        instance_vec = instance.reshape(n**2)
        w_list = [instance_vec[x] for x in range(n**2) if instance_vec[x] > 0]
        w = np.zeros(n * (n - 1))
        for ii in range(len(w_list)):
            w[ii] = w_list[ii]

        Id_n = np.eye(n)
        Im_n_1 = np.ones([n - 1, n - 1])
        Iv_n_1 = np.ones(n)
        Iv_n_1[0] = 0
        Iv_n = np.ones(n - 1)
        neg_Iv_n_1 = np.ones(n) - Iv_n_1

        v = np.zeros([n, n * (n - 1)])
        for ii in range(n):
            count = ii - 1
            for jj in range(n * (n - 1)):
                if jj // (n - 1) == ii:
                    count = ii
                if jj // (n - 1) != ii and jj % (n - 1) == count:
                    v[ii][jj] = 1.0

        vn = np.sum(v[1:], axis=0)

        Q = A * (np.kron(Id_n, Im_n_1) + np.dot(v.T, v))

        g = (
            w
            - 2 * A * (np.kron(Iv_n_1, Iv_n) + vn.T)
            - 2 * A * K * (np.kron(neg_Iv_n_1, Iv_n) + v[0].T)
        )

        c = 2 * A * (n - 1) + 2 * A * (K**2)

        try:
            max(x_sol)
            fun = (
                lambda x: np.dot(np.around(x), np.dot(Q, np.around(x)))
                + np.dot(g, np.around(x))
                + c
            )
            cost = fun(x_sol)
        except:
            cost = 0

        return Q, g, c, cost

    def construct_problem(self, Q, g, c) -> QuadraticProgram:
        qp = QuadraticProgram()
        for i in range(n * (n - 1)):
            qp.binary_var(str(i))
        qp.objective.quadratic = Q
        qp.objective.linear = g
        qp.objective.constant = c
        return qp

    def solve_problem(self, qp):
        algorithm_globals.random_seed = 10598
        vqe = SamplingVQE(sampler=Sampler(), optimizer=SPSA(), ansatz=RealAmplitudes())
        optimizer = MinimumEigenOptimizer(min_eigen_solver=vqe)
        result = optimizer.solve(qp)
        _, _, _, level = self.binary_representation(x_sol=result.x)
        return result.x, level

def extract_routes(n, K, binary_solution):
    routes = [[] for _ in range(K)]
    binary_solution_list = binary_solution.tolist()

    # Identify starting nodes for each vehicle from the depot (node 0)
    depot_slice = binary_solution_list[0:(n-1)]
    starting_nodes = [i + 1 for i, v in enumerate(depot_slice) if v == 1]
    
    #print(f"Depot slice: {depot_slice}")
    #print(f"Starting nodes: {starting_nodes}")

    # Initialize routes with starting nodes
    for i, start in enumerate(starting_nodes):
        if i < K:
            routes[i].append(0)
            routes[i].append(start)
    #print("Routes initialized with starting nodes:")
    #for route in routes:
       # print(route)

    # Build routes for each vehicle
    for i, route in enumerate(routes):
        current_node = route[-1]
        visited = set(route)  # Track visited nodes
      #  print(f"Starting route for Vehicle {i+1} from node {current_node}")

        while current_node != 0:
            if current_node == 0:
                # Depot's section slice
                section_slice = binary_solution_list[:n-1]
                node_mapping = list(range(1, n))
            else:
                # Section slice for other nodes
                section_start = (current_node) * (n - 1)
                section_slice = binary_solution_list[section_start:section_start + (n - 1)]
                node_mapping = [j if j < current_node else j + 1 for j in range(n-1)]

            # Find next nodes by considering the node mapping
            next_nodes = [node_mapping[j] for j, v in enumerate(section_slice) if v == 1]

           # print(f"Vehicle {i+1} at node {current_node}")
           # print(f"Section slice: {section_slice}")
           # print(f"Next nodes: {next_nodes}")

            if next_nodes:
                next_node = next_nodes[0]
                if next_node in visited and next_node != 0:
                 #   print(f"Detected loop for Vehicle {i+1}, breaking to prevent infinite loop.")
                    break
                current_node = next_node
                route.append(current_node)
                visited.add(current_node)
            else:
             #   print(f"No valid next nodes for Vehicle {i+1}, ending route.")
                break

        if route[-1] != 0:
            route.append(0)
       # print(f"Completed route for Vehicle {i+1}: {route}")

    return routes

def calculate_route_costs(routes, instance):
    total_cost = 0
    for i, route in enumerate(routes):
        route_cost = 0
        for j in range(len(route) - 1):
            route_cost += instance[route[j], route[j + 1]]
        print(f"Cost for Vehicle {i + 1}: {route_cost}")
        total_cost += route_cost
    print(f"Total cost for all vehicles: {total_cost}")

# n = 3  # number of nodes + depot (n+1)
# K = 2  # number of vehicles


# instance = np.array([
#     [0, 277, 472],
#     [496, 0, 499],
#     [336, 34, 0]
# ])


datasetFolder = '../dataset'

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = input("Enter the filename: ")
filePath = os.path.join(datasetFolder, filename)
# Extract numbers from filename
numbers = re.findall(r'\d+', filename)
# Determine number of customers and number of vehicles from filename
#note: number of n = num customers + 1 (for depot)
n = int(numbers[0]) + 1 
K = int(numbers[1])

# Open the file and read the distance matrix
with open(filePath, 'r') as file:
    lines = file.readlines()[2:]  
    distances = [[int(num) for num in line.split()] for line in lines]
# Convert to NumPy array - readability and performance
instance = np.array(distances)





# Instantiate the quantum optimizer class with parameters:
quantum_optimizer = QuantumOptimizer(instance, n, K)

try:
    Q, g, c, binary_cost = quantum_optimizer.binary_representation()
except NameError as e:
    print("Warning: Please run the cells above first.")
    print(e)

qp = quantum_optimizer.construct_problem(Q, g, c)

startTime = time.time()
quantum_solution, quantum_cost = quantum_optimizer.solve_problem(qp)
endTime = time.time()


timeTaken = endTime - startTime
# Convert to binary array
binary_solution = np.round(quantum_solution).astype(int)

print("Quantum solution (binary):", binary_solution)

routes = extract_routes(n, K, binary_solution)
for i, route in enumerate(routes):
    print(f"Route for Vehicle {i+1}: {route}")
print("Optimal cost:", quantum_cost)
print("Time taken: " +  str(timeTaken) + " seconds")

calculate_route_costs(routes, instance)
# Convert solution to format compatible with visualization
# x_quantum = np.zeros(n**2)
# kk = 0
# for ii in range(n**2):
#     if ii // n != ii % n:
#         x_quantum[ii] = quantum_solution[kk]
#         kk += 1

# Visualize the solution
#visualize_solution(xc, yc, x_quantum, quantum_cost, n, K, "Quantum")

# print("\n")
# print("Now lets do some wizardry")
# binary_solution_list = binary_solution.tolist()
# print(binary_solution_list)
# for i in range(n):
#     print("Section " + str(i) + ":" +  str(binary_solution_list[i*(n-1):(i+1)*(n-1)]))
# depot_slice = binary_solution_list[0:(n-1)]
# print("from depot slice: " + str(depot_slice ))
    
# V1, V2 = [i+1 for i, v in enumerate(depot_slice) if v == 1][:2]
# print("start of V1: 0 -> " + str(V1))
# print("start of V2: 0 -> " + str(V2))
