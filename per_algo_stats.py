import pandas as pd

# Load the data files for each algorithm
bnb_stats = pd.read_csv('B&B_stats.csv')
qaoa_cobyla_stats = pd.read_csv('QAOA_COBLYA_5_stats.csv')
qaoa_spsa_stats = pd.read_csv('QAOA_SPSA_5_stats.csv')
sa_stats = pd.read_csv('SA_stats.csv')
vqe_cobyla_ra_stats = pd.read_csv('VQE_COBLYA_RA_stats.csv')
vqe_spsa_ra_stats = pd.read_csv('VQE_SPSA_RA_stats.csv')

# Extract the optimal costs from B&B, dropping rows with NaN values
bnb_stats['Lowest Optimal Cost'] = pd.to_numeric(bnb_stats['Lowest Optimal Cost'], errors='coerce')
bnb_optimal_costs = bnb_stats.dropna(subset=['Lowest Optimal Cost']).set_index('File')['Lowest Optimal Cost']

# List of dataframes to iterate over for processing
dataframes = [
    ("QAOA_COBLYA", qaoa_cobyla_stats),
    ("QAOA_SPSA", qaoa_spsa_stats),
    ("SA", sa_stats),
    ("VQE_COBLYA_RA", vqe_cobyla_ra_stats),
    ("VQE_SPSA_RA", vqe_spsa_ra_stats)
]

# Placeholder for the results
results = []

# Flag to include all results, change as needed
include_all = True

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
    
    # Calculate success rate by counting valid results and checking within 90% of B&B
    success_count = 0
    total_count = 0
    for _, row in df.iterrows():
        file = row['File']
        algo_cost = pd.to_numeric(row['Lowest Optimal Cost'], errors='coerce')
        if pd.notna(algo_cost) and file in bnb_optimal_costs:
            bnb_cost = bnb_optimal_costs[file]
            if algo_cost <= 1.1 * bnb_cost:
                success_count += 1
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count: {success_count}, Within 90% of B&B: True")
            else:
                print(f"Algorithm: {algorithm_name}, File: {file}, Success Count: {success_count}, Within 90% of B&B: False")
            total_count += 1
        elif include_all:
            if file in bnb_optimal_costs:
                total_count += 1

    success_rate = success_count / total_count if total_count > 0 else 0
    results.append((algorithm_name, scalability, success_rate))

# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=["Algorithm Name", "Scalability", "Success Rate"])

# Write the results to a CSV file
results_df.to_csv('per_algorithm_stats.csv', index=False)

print("Results have been written to 'per_algorithm_stats.csv'")
