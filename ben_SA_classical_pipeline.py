import multiprocessing
import os
import time
import subprocess
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def run_algorithm(script_name, script_folder, filename, runs, output_file, timeout):
    with open(output_file, 'a') as f:
        for run in range(1, runs + 1):
            start_time = time.time()
            command = f'python "{script_name}" "{filename}"'
            print(f"Running {script_name} on {filename} Run {run} in {script_folder}")
            
            current_dir = os.getcwd()
            os.chdir(script_folder)
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
                end_time = time.time()
                
                filename_only = os.path.basename(filename)
                
                output = {
                    "Filename": filename_only,  # Log only the filename
                    "Algorithm": script_name,
                    "Run": run,
                    "Output": result.stdout.strip(),
                    "Error": result.stderr.strip(),
                }
                for key, value in output.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "-"*50 + "\n")

                if end_time - start_time > timeout:
                    print(f"Run {run} for {script_name} exceeded timeout of {timeout} seconds.")
                    break  # Break out of the loop if timeout exceeded
                
            except subprocess.TimeoutExpired:
                print(f"Timeout expired for {script_name} on {filename} Run {run}")
                f.write(f"Filename: {filename}\n")
                f.write(f"Algorithm: {script_name}\n")
                f.write(f"Run: {run}\n")
                f.write(f"Error: Timeout expired after {timeout} seconds\n")
                f.write("\n" + "-"*50 + "\n")
                break  # Break out of the loop on timeout exception

            except Exception as e:
                print(f"Error running {script_name} on {filename} Run {run}: {e}")
                f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
            finally:
                os.chdir(current_dir)

def worker(script_name, script_folder, dataset_folder, filenames, runs, timeout, output_file):
    print(f"Worker started for {script_name} in {script_folder}")
    for filename in filenames:
        filepath = os.path.join("..", dataset_folder, filename)
        p = multiprocessing.Process(target=run_algorithm, args=(script_name, script_folder, filepath, runs, output_file, timeout))
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
    runs = 3
    #timeout = 6 * 3600 seconds # 6 hours
    timeout = 21600 
    
    # Define the algorithms and their respective folders
    algorithms = [
        {"script_name": "SA SP=100.py", "script_folder": "simulated-annealing"},
        {"script_name": "SA SP=1000.py"
         , "script_folder": "simulated-annealing"}
    ]

    # Output files for each algorithm
    output_files = {
        "SA SP=100.py": "new_sp=100_output_sa.txt",
        "SA SP=1000.py": "new_sp=1000_output_sa.txt"
    }

    # Clear the output files by opening them in write mode at the start of the program
    for output_file in output_files.values():
        open(output_file, 'w').close()

 


    dataset_files_ordered = [
        "vrp-2-1-1.txt",
        "vrp-3-1-1.txt",
        "vrp-3-2-1.txt",
        "vrp-4-3-3.txt",
        "vrp-5-4-1.txt",
        "vrp-4-1-1.txt",
        "vrp-6-5-1.txt",
        "vrp-4-2-1.txt",
        "vrp-7-6-1.txt",
        "vrp-8-7-1.txt",
        "vrp-5-3-1.txt",
        "vrp-5-1-1.txt",
        "vrp-10-8-1.txt",
        "vrp-5-2-1.txt",
        "vrp-6-4-1.txt",
        "vrp-6-1-1.txt",
        "vrp-7-5-1.txt",
        "vrp-8-6-1.txt",
        "vrp-6-2-1.txt",
        "vrp-10-7-1.txt",
        "vrp-8-5-1.txt",
        "vrp-7-4-1.txt",
        "vrp-6-3-1.txt",
        "vrp-8-1-1.txt",
        "vrp-8-4-1.txt",
        "vrp-10-6-1.txt",
        "vrp-8-3-1.txt",
        "vrp-8-2-1.txt",
        "vrp-10-5-1.txt",
        "vrp-10-1-1.txt",
        "vrp-10-4-1.txt",
        "vrp-10-3-1.txt",
        "vrp-15-8-1.txt",
        "vrp-15-7-1.txt",
        "vrp-15-6-1.txt",
        "vrp-15-5-1.txt",
        "vrp-15-1-1.txt",
        "vrp-15-4-1.txt",
        "vrp-15-2-1.txt",
        "vrp-15-3-1.txt"
    ]


    processes = []
    
    # Create a process for each algorithm
    for algo in algorithms:
        script_name = algo["script_name"]
        script_folder = algo["script_folder"]
        output_file = output_files[script_name]

        print(f"Starting process for {script_name} in {script_folder}")
        p = multiprocessing.Process(target=worker, args=(script_name, script_folder, dataset_folder, dataset_files_ordered, runs, timeout, output_file))
        processes.append(p)
        p.start()
        print(f"Started worker process {p.pid} for {script_name}")

    # Wait for all processes to finish
    for p in processes:
        p.join()
        print(f"Worker process {p.pid} finished")

    # Inform user where results are stored
   
