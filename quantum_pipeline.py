import multiprocessing
import os
import time
import subprocess
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def run_algorithm(script_name, script_folder, filename, runs, output_file):
    with open(output_file, 'a') as f:  # Open in append mode to add results
        for run in range(1, runs + 1):
            start_time = time.time()
            # Construct the command to run the algorithm
            #command = f'python3 "{script_name}" "{filename}"' # Mac/Linux
            command = f'python "{script_name}" "{filename}"' # Windows
            print(f"Running {script_name} on {filename} Run {run} in {script_folder}")
            
            # Change the working directory to the script's folder
            current_dir = os.getcwd()
            os.chdir(script_folder)
            
            # Run the command and capture output
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                end_time = time.time()
                
                output = {
                    "Filename": filename,
                    "Algorithm": script_name,
                    "Run": run,
                    "Output": result.stdout.strip(),
                    "Error": result.stderr.strip(),
                   # "TimeTaken": end_time - start_time
                }
                # Write the dictionary output to file with proper newlines
                for key, value in output.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "-"*50 + "\n")
            except Exception as e:
                print(f"Error running {script_name} on {filename} Run {run}: {e}")
                f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
            finally:
                # Revert to the original directory
                os.chdir(current_dir)

def worker(script_name, script_folder, dataset_folder, filenames, runs, timeout, output_file):
    print(f"Worker started for {script_name} in {script_folder}")
    for filename in filenames:
        filepath = os.path.join("..", dataset_folder, filename)
        p = multiprocessing.Process(target=run_algorithm, args=(script_name, script_folder, filepath, runs, output_file))
        p.start()
        print(f"Started process {p.pid} for {script_name} on {filename}")
        p.join(timeout)
        if p.is_alive():
            print(f"Terminating {script_name} on {filename} due to timeout")
            p.terminate()
            p.join()
            # Log timeout to the output file
            with open(output_file, 'a') as f:
                f.write(f"Filename: {filepath}\n")
                f.write(f"Algorithm: {script_name}\n")
                f.write(f"Error: Terminated due to timeout after {timeout} seconds\n")
                f.write("\n" + "-"*50 + "\n")
        print(f"Process {p.pid} for {script_name} on {filename} finished")

if __name__ == "__main__":
    dataset_folder = "dataset"  # Use relative path to the dataset folder
    runs = 30
    #timeout = 8 * 3600  # 8 hours
    timeout = 28800 
    
    # Define the algorithms and their respective folders
    algorithms = [
        {"script_name": "VQE.py", "script_folder": "VQE"},
        {"script_name": "QAOA.py", "script_folder": "QAOA"}
    ]

    # Output files for each algorithm
    output_files = {
        "VQE.py": "output_vqe.txt",
        "QAOA.py": "output_qaoa.txt"
    }

    # Clear the output files by opening them in write mode at the start of the program
    for output_file in output_files.values():
        open(output_file, 'w').close()

    # List and sort dataset files using natural sorting
    dataset_files = [f for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
    dataset_files.sort(key=natural_sort_key)  # Natural sort the files
    
    # Log the sorted filenames to verify order
    print("Sorted filenames:")
    for f in dataset_files:
        print(f)

    processes = []
    
    # Create a process for each algorithm
    for algo in algorithms:
        script_name = algo["script_name"]
        script_folder = algo["script_folder"]
        output_file = output_files[script_name]

        print(f"Starting process for {script_name} in {script_folder}")
        p = multiprocessing.Process(target=worker, args=(script_name, script_folder, dataset_folder, dataset_files, runs, timeout, output_file))
        processes.append(p)
        p.start()
        print(f"Started worker process {p.pid} for {script_name}")

    # Wait for all processes to finish
    for p in processes:
        p.join()
        print(f"Worker process {p.pid} finished")

    # Inform user where results are stored
   
