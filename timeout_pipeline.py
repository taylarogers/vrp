import os
import time
import subprocess

def run_algorithm(script_name, script_folder, filename, runs, output_file):
    with open(output_file, 'a') as f:
        for run in range(1, runs + 1):
            start_time = time.time()
            command = f'python "{script_name}" "{filename}"'
            print(f"Running {script_name} on {filename} Run {run} in {script_folder}")
            
            current_dir = os.getcwd()
            os.chdir(script_folder)
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                end_time = time.time()
                
                output = {
                    "Filename": filename,
                    "Algorithm": script_name,
                    "Run": run,
                    "Output": result.stdout.strip(),
                    "Error": result.stderr.strip(),
                }
                for key, value in output.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "-"*50 + "\n")

            except Exception as e:
                print(f"Error running {script_name} on {filename} Run {run}: {e}")
                f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
            finally:
                os.chdir(current_dir)

def process_algorithms(algorithm_mapping, runs):
    for algo in algorithm_mapping.values():
        script_name = algo["script_name"]
        script_folder = algo["script_folder"]
        output_file = algo["output_file"]
        files = algo["files"]

        print(f"Running {script_name} in {script_folder} for specified files")
        for filename in files:
            run_algorithm(script_name, script_folder, filename, runs, output_file)
            print(f"Finished running {script_name} on {filename}")

if __name__ == "__main__":
    runs = 1

    # Mapping algorithms to their specific files and respective folders
    algorithm_mapping = {
        "vqe_coblya_RA": {
            "script_name": "vqe_coblya_RA.py",
            "script_folder": "VQE",
            "output_file": "output_vqe_coblya_RA_TIMEOUT.txt",
            "files": ["vrp-4-3-3.txt", "vrp-4-1-1.txt"]
        },
        "branch_and_bound": {
            "script_name": "branch-and-bound.py",
            "script_folder": "branch-and-bound",
            "output_file": "output_branch_and_bound_TIMEOUT.txt",
            "files": ["vrp-15-2-1.txt", "vrp-15-3-1.txt"]
        }
    }

    # Clear the output files before starting
    for algo in algorithm_mapping.values():
        open(algo["output_file"], 'w').close()

    # Run the algorithms on their respective files
    process_algorithms(algorithm_mapping, runs)

    print("Results are stored in the respective output files.")
