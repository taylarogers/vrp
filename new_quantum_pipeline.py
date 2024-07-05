import multiprocessing
import os
import time
import subprocess
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

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

def worker(scripts, script_folder, dataset_folder, filenames, runs, timeout, output_file):
    print(f"Worker started for scripts in {script_folder}")
    for filename in filenames:
        for script_name in scripts:
            filepath = os.path.join("..",dataset_folder, filename)
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
            print(f"Process {p.pid} for {script_name} on {filename} finished")

if __name__ == "__main__":
    dataset_folder = "dataset"
    runs = 30
    timeout = 28800

    vqe_scripts = [
        "vqe_coblya_ES.py",
        "vqe_coblya_RA.py",
        "vqe_spsa_ES.py",
        "vqe_spsa_RA.py"
    ]

    algorithms = [
        {"scripts": vqe_scripts, "script_folder": "VQE"},
        {"scripts": ["QAOA.py"], "script_folder": "QAOA"}
    ]

    output_files = {
        "VQE": "output_vqe.txt",
        "QAOA": "output_qaoa.txt"
    }

    for output_file in output_files.values():
        open(output_file, 'w').close()

    dataset_files = [f for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
    dataset_files.sort(key=natural_sort_key)

    processes = []
    
    for algo in algorithms:
        scripts = algo["scripts"]
        script_folder = algo["script_folder"]
        output_file = output_files[script_folder]

        print(f"Starting process for scripts in {script_folder}")
        p = multiprocessing.Process(target=worker, args=(scripts, script_folder, dataset_folder, dataset_files, runs, timeout, output_file))
        processes.append(p)
        p.start()
        print(f"Started worker process {p.pid} for scripts in {script_folder}")

    for p in processes:
        p.join()
        print(f"Worker process {p.pid} finished")

    print("Results are stored in output_vqe.txt and output_qaoa.txt")




# import multiprocessing
# import os
# import time
# import subprocess
# import re

# def natural_sort_key(s):
#     return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# def run_algorithm(script_name, script_folder, filename, run, output_file):
#     with open(output_file, 'a') as f:
#         start_time = time.time()
#         command = f'python "{script_name}" "{filename}"'
#         print(f"Running {script_name} on {filename} Run {run} in {script_folder}")
        
#         current_dir = os.getcwd()
#         os.chdir(script_folder)
        
#         try:
#             result = subprocess.run(command, shell=True, capture_output=True, text=True)
#             end_time = time.time()
            
#             output = {
#                 "Filename": filename,
#                 "Algorithm": script_name,
#                 "Run": run,
#                 "Output": result.stdout.strip(),
#                 "Error": result.stderr.strip(),
#             }
#             for key, value in output.items():
#                 f.write(f"{key}: {value}\n")
#             f.write("\n" + "-"*50 + "\n")
#         except Exception as e:
#             print(f"Error running {script_name} on {filename} Run {run}: {e}")
#             f.write(f"Error running {script_name} on {filename} Run {run}: {e}\n")
#         finally:
#             os.chdir(current_dir)

# def worker(scripts, script_folder, dataset_folder, filenames, runs, timeout, output_file):
#     print(f"Worker started for scripts in {script_folder}")
#     for filename in filenames:
#         for script_name in scripts:
#             for run in range(1, runs + 1):
#                 filepath = os.path.join("..", dataset_folder, filename)
#                 p = multiprocessing.Process(target=run_algorithm, args=(script_name, script_folder, filepath, run, output_file))
#                 p.start()
#                 print(f"Started process {p.pid} for {script_name} on {filename} Run {run}")
#                 p.join(timeout)
#                 if p.is_alive():
#                     print(f"Terminating {script_name} on {filename} Run {run} due to timeout")
#                     p.terminate()
#                     p.join()
#                     with open(output_file, 'a') as f:
#                         f.write(f"Filename: {filepath}\n")
#                         f.write(f"Algorithm: {script_name}\n")
#                         f.write(f"Run: {run}\n")
#                         f.write(f"Error: Terminated due to timeout after {timeout} seconds\n")
#                         f.write("\n" + "-"*50 + "\n")
#                 print(f"Process {p.pid} for {script_name} on {filename} Run {run} finished")

# if __name__ == "__main__":
#     dataset_folder = "dataset"
#     runs = 30
#     timeout = 28800

#     vqe_scripts = [
#         "vqe_cobyla_ES.py",
#         "vqe_cobyla_RA.py",
#         "vqe_spsa_ES.py",
#         "vqe_spsa_RA.py"
#     ]

#     algorithms = [
#         {"scripts": vqe_scripts, "script_folder": "VQE"},
#         {"scripts": ["QAOA.py"], "script_folder": "QAOA"}
#     ]

#     output_files = {
#         "VQE": "output_vqe.txt",
#         "QAOA": "output_qaoa.txt"
#     }

#     for output_file in output_files.values():
#         open(output_file, 'w').close()

#     dataset_files = [f for f in os.listdir(dataset_folder) if os.path.isfile(os.path.join(dataset_folder, f))]
#     dataset_files.sort(key=natural_sort_key)

#     processes = []
    
#     for algo in algorithms:
#         scripts = algo["scripts"]
#         script_folder = algo["script_folder"]
#         output_file = output_files[script_folder]

#         print(f"Starting process for scripts in {script_folder}")
#         p = multiprocessing.Process(target=worker, args=(scripts, script_folder, dataset_folder, dataset_files, runs, timeout, output_file))
#         processes.append(p)
#         p.start()
#         print(f"Started worker process {p.pid} for scripts in {script_folder}")

#     for p in processes:
#         p.join()
#         print(f"Worker process {p.pid} finished")

#     print("Results are stored in output_vqe.txt and output_qaoa.txt")
