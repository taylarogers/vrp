import pandas as pd

# Load the data files for each algorithm
bnb_stats = pd.read_csv('B&B_stats.csv')
qaoa_cobyla_stats = pd.read_csv('QAOA_COBLYA_5_stats.csv')
qaoa_spsa_stats = pd.read_csv('QAOA_SPSA_5_stats.csv')
sa_stats = pd.read_csv('SA_stats.csv')
vqe_cobyla_ra_stats = pd.read_csv('VQE_COBLYA_RA_stats.csv')
vqe_spsa_ra_stats = pd.read_csv('VQE_SPSA_RA_stats.csv')
sa_sp100_stats = pd.read_csv('SA_SP100_stats.csv')
sa_sp1000_stats = pd.read_csv('SA_SP1000_stats.csv')

# Extract the optimal costs from B&B, dropping rows with NaN values
bnb_stats['Lowest Optimal Cost'] = pd.to_numeric(bnb_stats['Lowest Optimal Cost'], errors='coerce')
bnb_optimal_costs = bnb_stats.dropna(subset=['Lowest Optimal Cost']).set_index('File')['Lowest Optimal Cost']

# List of dataframes to iterate over for processing
dataframes = [
    ("QAOA_COBLYA", qaoa_cobyla_stats),
    ("QAOA_SPSA", qaoa_spsa_stats),
    ("SA", sa_stats),
    ("VQE_COBLYA_RA", vqe_cobyla_ra_stats),
    ("VQE_SPSA_RA", vqe_spsa_ra_stats),
    ("SA SP=100", sa_sp100_stats),
    ("SA SP=1000", sa_sp1000_stats)
]

# Placeholder for the results
results = []

# Flag to include all results, change as needed
include_all = False

# Total number of dataset instances (assumed to be the same for each algorithm)
total_instances = 33

# Calculate metrics for each algorithm
for algorithm_name, df in dataframes:
    df['Lowest Optimal Cost'] = pd.to_numeric(df['Lowest Optimal Cost'], errors='coerce')
    
    # Strip "Filename: " prefix if present
    df['File'] = df['File'].str.replace('Filename: ', '')
    
    # Calculate scalability
    df_cleaned = df.dropna(subset=['Lowest Optimal Cost'])
    if not df_cleaned.empty:
        min_instance = df_cleaned['File'].iloc[0]
        max_instance = df_cleaned['File'].iloc[-1]
        scalability = f"({min_instance}; {max_instance})"
    else:
        scalability = "No successful runs"
    
    # Calculate success rates by counting valid results and checking within 95% and 99% of B&B
    success_count_95 = 0
    success_count_99 = 0
    valid_count = 0
    total_count = 0
    for _, row in df.iterrows():
        file = row['File']
        algo_cost = pd.to_numeric(row['Lowest Optimal Cost'], errors='coerce')
        if pd.notna(algo_cost) and file in bnb_optimal_costs:
            bnb_cost = bnb_optimal_costs[file]
            if algo_cost <= 1.05 * bnb_cost:
                success_count_95 += 1
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count 95%: {success_count_95}, Within 95% of B&B: True")
            else:
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count 95%: {success_count_95}, Within 95% of B&B: False")
            if algo_cost <= 1.01 * bnb_cost:
                success_count_99 += 1
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count 99%: {success_count_99}, Within 99% of B&B: True")
            else:
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count 99%: {success_count_99}, Within 99% of B&B: False")
            valid_count += 1
            total_count += 1
        elif include_all:
            if file in bnb_optimal_costs:
                total_count += 1

    success_rate_95 = success_count_95 / total_count if total_count > 0 else 0
    success_rate_99 = success_count_99 / total_count if total_count > 0 else 0
    print(valid_count, total_instances)
    feasibility_percentage = valid_count / total_instances if total_instances > 0 else 0
    results.append((algorithm_name, scalability, success_rate_95, success_rate_99, feasibility_percentage))

# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=["Algorithm Name", "Scalability", "Success Rate 95%", "Success Rate 99%", "Feasibility Percentage"])

# Write the results to a CSV file
results_df.to_csv('per_algorithm_stats.csv', index=False)

print("Results have been written to 'per_algorithm_stats.csv'")
