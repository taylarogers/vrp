import os
import time
import subprocess

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

def process_algorithms(algorithms, dataset_files_ordered, runs, timeout):
    for algo in algorithms:
        scripts = algo["scripts"]
        script_folder = algo["script_folder"]
        output_files = algo["output_files"]

        print(f"Running scripts in {script_folder}")
        for script_name, output_file in zip(scripts, output_files):
            for filename in dataset_files_ordered:
                run_algorithm(script_name, script_folder, filename, runs, output_file, timeout)
                print(f"Finished running {script_name} on {filename}")

if __name__ == "__main__":
    dataset_folder = "dataset"
    runs = 5
    timeout = 60  # You can set it back to 21600 for 6 hours

    vqe_scripts = [
        "vqe_coblya_ES.py",
        "vqe_coblya_RA.py",
        "vqe_spsa_ES.py",
        "vqe_spsa_RA.py"
    ]

    qaoa_scripts = [
        "qaoa_coblya_4.py",
        "qaoa_coblya_10.py",
        "qaoa_coblya_16.py",
        "qaoa_spsa_4.py",
        "qaoa_spsa_10.py",
        "qaoa_spsa_16.py"
    ]

    qaoa_output_files = [
        "output_qaoa_coblya_4.txt",
        "output_qaoa_coblya_10.txt",
        "output_qaoa_coblya_16.txt",
        "output_qaoa_spsa_4.txt",
        "output_qaoa_spsa_10.txt",
        "output_qaoa_spsa_16.txt"
    ]

    vqe_output_files = [
        "output_vqe_coblya_ES.txt",
        "output_vqe_coblya_RA.txt",
        "output_vqe_spsa_ES.txt",
        "output_vqe_spsa_RA.txt"
    ]

    algorithms = [
        {"scripts": vqe_scripts, "script_folder": "VQE", "output_files": vqe_output_files},
        {"scripts": qaoa_scripts, "script_folder": "QAOA", "output_files": qaoa_output_files}
    ]

    for output_file in vqe_output_files:
        open(output_file, 'w').close()

    for output_file in qaoa_output_files:
        open(output_file, 'w').close()

    dataset_files_ordered = [
        "vrp-2-1-1.txt",
        "vrp-3-1-1.txt",
        "vrp-3-2-1.txt",
        "vrp-4-3-1.txt",
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

    process_algorithms(algorithms, dataset_files_ordered, runs, timeout)

    print("Results are stored in the respective output files.")
