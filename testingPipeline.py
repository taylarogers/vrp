import multiprocessing
import os
import time
import subprocess
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def run_algorithm(script_name, script_folder, filename, runs, output_file):
    for run in range(1, runs + 1):
        start_time = time.time()
        command = f'python "{script_name}" "{filename}"'

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
                "TimeTaken": end_time - start_time
            }

            # Print to console
            print("\n" + "-"*50 + "\n")
            print(f"Filename: {filename}")
            print(f"Algorithm: {script_name}")
            print(f"Run: {run}")
            print(f"Output:\n{result.stdout.strip()}")
            print(f"Error:\n{result.stderr.strip()}")
            print(f"TimeTaken: {end_time - start_time:.2f} seconds")
            print("\n" + "-"*50 + "\n")
            
            # Write to file
            with open(output_file, 'a') as f:
                for key, value in output.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "-"*50 + "\n")
                
            # Also write to runs_checker.txt
            with open("runs_checker.txt", 'a') as f:
                for key, value in output.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "-"*50 + "\n")
                
        except Exception as e:
            print(f"Error running {script_name} on {filename} Run {run}: {e}")
            with open(output_file, 'a') as f:
                f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
            with open("runs_checker.txt", 'a') as f:
                f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
        finally:
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
            with open(output_file, 'a') as f:
                f.write(f"Filename: {filepath}\n")
                f.write(f"Algorithm: {script_name}\n")
                f.write(f"Error: Terminated due to timeout after {timeout} seconds\n")
                f.write("\n" + "-"*50 + "\n")
            with open("runs_checker.txt", 'a') as f:
                f.write(f"Filename: {filepath}\n")
                f.write(f"Algorithm: {script_name}\n")
                f.write(f"Error: Terminated due to timeout after {timeout} seconds\n")
                f.write("\n" + "-"*50 + "\n")
        print(f"Process {p.pid} for {script_name} on {filename} finished")

if __name__ == "__main__":
    dataset_folder = "dataset"
    runs = 30
    timeout = 120
    
    algorithms = [
        {"script_name": "SAcwstester.py", "script_folder": "simulated-annealing"},
    ]

    output_files = {
        "SAcwstester.py": "output_sa.txt",
    }

    dataset_files = [f for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
    dataset_files.sort(key=natural_sort_key)
    
    print("Sorted filenames:")
    for f in dataset_files:
        print(f)

    processes = []
    
    for algo in algorithms:
        script_name = algo["script_name"]
        script_folder = algo["script_folder"]
        output_file = output_files[script_name]

        print(f"Starting process for {script_name} in {script_folder}")
        p = multiprocessing.Process(target=worker, args=(script_name, script_folder, dataset_folder, dataset_files, runs, timeout, output_file))
        processes.append(p)
        p.start()
        print(f"Started worker process {p.pid} for {script_name}")
