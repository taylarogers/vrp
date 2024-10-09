# Benchmarking Classical Methods against the Quantum Approximate Optimisation Algorithm to Solve the Vehicle Routing Problem: Branch and Bound and Simulated Annealing

This repository contains code to aid in the comparative analysis of classical and quantum techniques in solving the Vehicle Routing Problem (VRP). The VRP is a significant challenge in combinatorial optimisation. The primary objective is to find the most cost-effective routes for a fleet of vehicles delivering goods or services to a set of customers.

This code base includes the implementations of Branch and Bound (B&B), Simulated Annealing (SA), Variational Quantum Eigensolve (VQE) and the Quantum Approximate Optimisation Algorithm (QAOA) using two different classical optimisers for the quantum algorithms. It performs multiple runs of each algorithm over various inputs, aiming to test each algorithm's ability to handle increased problem sizes. It provides statistics to analyse the solution quality, CPU time, scalability, feasibility and success rate of all algorithms.

NOTE: This guide uses the `python` keyword, but depending on your computer you may need `python3` in order to run the commands.

## Dataset
The dataset was adapted from a classical Capacitated VRP dataset available at: https://doi.org/10.17632/kcc52cw4zs.1

Changes to the dataset:
* Remove CVRP-specific constraints (e.g. capacity and demand)
* Scaling down the size of the dataset to be appropriate for the small-scale capabilities of both algorithms

All data inputs can be found with the `dataset` folder.

### Structure of The Data Inputs:
The input is given to the program as a distance matrix between each point and every other point. In both the y- and x-axis, the index of 0 is reserved for information from the depot. Teh rest of the indices related to the corresponding customer - i.e. index 1 refers to the distances from customer 1 to every other point.

For example, in the distance matrix input below a distance of 136 is found when travelling from the depot to customer 1, and a value of 496 when travelling from customer 1 to customer 2.

```
CUSTOMERS : 2
VEHICLES : 1
0 136 337 
364 0 496 
5 335 0 
```

## Algorithm Implementations
All algorithms were implemented using Python and can be found within their respective folders. Various Qiskit libraries were crucial in creating the quantum implementations of QAOA and VQE. Quantum code was adapted from a publically available Qiskit tutorial on using quantum algorithms to solve the VRP - for more information, please see the notices at the beginning of both quantum implementations.

Both algorithms are created to run on classical computers, with the use of a quantum simulator to mimic the performance of quantum algorithms on a quantum device.

## Installation
To use this repository, you will first need to create a virtual environment using either `venv` or `conda`.

```
python -m venv myenv
```
```
conda create --name myenv python=3.9
```

In this virtual enironment, you will now need to load in all of the packages necessary for the implementations to run. Firstly, you will need to activate your newly created environment.

```
source myenv/bin/activate
```
```
conda activate myenv
```

The packages and their versions necessary to install into the environment are shown in the table below. All of these are included in the `requirements.txt` file for easy installation.

| Package  | Version |
| ------------- | ------------- |
| matplotlib  | 3.9.0  |
| networkx  | 3.2.1  |
| numpy  | 1.26.4  |
| qiskit  | 1.1.0  |
| qiskit_aer  | 0.14.1  |
| qiskit_algorithms  | 0.3.0  |
| qiskit_optimization  | 0.6.1  |
| python  | 3.9  |

Now install all packages within the `requirements.txt` into your virtual environment.

```
pip install -r requirements.txt
```

Now you are all set to be able to run the code.

Once you're done, you can deactivate your virtual environments to exit.

```
deactivate
```
```
conda deactivate
```

## Usage
Before you follow this section, please make sure to refer to the previous Installation section in order to ensure that your virtual environment is set up correctly.

### Running a Single Input
If you simply want to run an algorithm on a single input file, you will need to run the algorithm within their respective folders.

```
python branch-and-bound/branch-and-bound.py
```

Once running, you will then type in a single input of the file name that you want it to run on.

```
Enter the filename: 2-1.txt
```

After completion, the output including the optimal costs and routes will be displayed within the terminal.

### Running on All Inputs
To see te performance of the algorithms on all inputs, you can use the included pipelines. The classical pipeline runs B&B and SA implementations concurrently, whereas the quantum pipeline runs the QAOA and VQE implementations sequentially. This is due to the resource requirements necessary with each of the respective algorithms.

In order to run a pipeline, you will simply need to type in the command to get it started.

```
python classical_pipeline.py
```

The outputs of all the runs will be stored in their respective outputs files. For example, this would be `output_bnb.txt` for the B&B and `output_qaoa_coblya_5.txt` and `output_qaoa_spsa_5.txt` for QAOA.

### Calculating Statistics On Runs
If you are interested in further analysis of the algorithms on the full dataset, statistical scripts are included to calculate useful information on the algorithms' performance on each input problem size as well as their performance on the dataset as a whole.

In order to run either of these files you would have had to run both the classical and quantum pipeline in order to have the output files to analyse.

The `average-stats-csv.py` file creates an in-depth summary of how the algorithms performed per input problem size. It makes note of the lowest optimal cost, number of runs with the lowest optimal cost, highest optimal cost, number of runs with the highest optimal cost, best time (seconds), average time (seconds), worst time (seconds), standard deviation of optimal cost, standard deviation of time, average optimal cost, median optimal cost, and median time. These stats are output to each algorithm's respective CSV files, for example this would look like `B&B_stats.csv`, `QAOA_COBLYA_5_stats.csv` and `QAOA_SPSA_5_stats.csv`.

The `per_algo_stats.py` file provides a summary of how the algorithms performed as a whole. This mainly helps to look at the comparison between the quantum and classical algorithms. It calculates the scalability, success rate in the 95% percentile, success rate in the 99% percentile, and feasibility percentage. This data is outputed to the `per_algorithm_stats.csv`.

## Experimental Output Files
All of the output files used in the analysis of quantum and classical algorithms are attached. These can be used to verify the conclusions that were come to based on experimental results, as well as reflect back on in the future to see the possible improvements in quantum computing.

## Acknowledgements
We would like to acknowledge the help of our supervisor Krupa Prag in the creation of this code. Attention must also be brought to Qiskit's publically available tutorial which created a base for all quantum implementations within this code base.

## Note
This code is licensed under the Apache License, Version 2.0. You may obtain a copy of this license in the LICENSE.txt file in the root directory of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

Any modifications or derivative works of this code must retain this copyright notice, and modified files need to carry a notice indicating that they have been altered from the originals.
