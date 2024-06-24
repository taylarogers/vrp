import re
import os

def compare_solutions(file_path):
    # Initialize counters
    random_better = 0
    clarke_wright_better = 0
    total_runs = 0

    # Define regular expressions to extract relevant data
    random_solution_cost_re = re.compile(r"Initial random distance:\s+(\d+)")
    clarke_wright_cost_re = re.compile(r"Clarke and Wright savings total cost:\s+(\d+)")

    # Read the file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Split content into runs
    runs = content.split("Filename:")

    for run in runs:
        if run.strip():
            total_runs += 1
            # Extract costs
            random_solution_cost_match = random_solution_cost_re.search(run)
            clarke_wright_cost_match = clarke_wright_cost_re.search(run)

            if random_solution_cost_match and clarke_wright_cost_match:
                random_cost = int(random_solution_cost_match.group(1))
                clarke_wright_cost = int(clarke_wright_cost_match.group(1))

                # Compare costs
                if random_cost < clarke_wright_cost:
                    random_better += 1
                elif clarke_wright_cost < random_cost:
                    clarke_wright_better += 1

    return random_better, clarke_wright_better, total_runs

def main():
    # Use an absolute path to ensure the file is found
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, 'runs_checker.txt')  # Absolute path to your file

    random_better, clarke_wright_better, total_runs = compare_solutions(file_path)

    if total_runs > 0:
        print(f"Total runs: {total_runs}")
        print(f"Random solution better: {random_better} times")
        print(f"Clarke and Wright solution better: {clarke_wright_better} times")
    else:
        print("No runs found or an error occurred.")

if __name__ == "__main__":
    main()
