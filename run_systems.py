"""
This script distributes a given number of initial conditions (`num_ic`) across
all available CPUs and runs a selected system script in parallel.

Usage:
    python run_systems.py <num_ic>

How it works:
1. Determines the total number of logical CPUs available.
2. Computes how many jobs each CPU should handle.
3. Splits the jobs into contiguous ranges, one per CPU.
4. Launches each range as a background process.
5. Waits for all background processes to finish before exiting.

When run, the user is prompted to select the system:
    1: Henon map 3D
    2: Logistic map network
    3: FPU (Fermi-Pasta-Ulam)
    4: Cat map
    5: Baker map
    6: All systems
    7: Exit
"""

import os
import sys
import numpy as np

# --------------------------
# Input: number of initial conditions
# --------------------------
num_ic = int(sys.argv[1])

# --------------------------
# User menu
# --------------------------
print("Select the system to run:")
print("1. Henon map 3D")
print("2. Logistic map network")
print("3. FPU (Fermi-Pasta-Ulam)")
print("4. Cat map")
print("5. Baker map")
print("6. All")
print("7. Exit")

try:
    choice = int(input("Enter system number: "))
except ValueError:
    print("Invalid input. Exiting.")
    sys.exit(1)

# Map user input to script filenames
script_map = {
    1: "henon_map_3D.py",
    2: "logistic_map_network.py",
    3: "fpu.py",
    4: "cat_map.py",
    5: "baker_map.py",
}

# --------------------------
# Handle choices
# --------------------------
if choice == 7:
    print("Exiting.")
    sys.exit(0)
elif choice == 6:
    scripts_to_run = list(script_map.values())
elif choice in script_map:
    scripts_to_run = [script_map[choice]]
else:
    print(f"Invalid choice: {choice}")
    sys.exit(1)

# --------------------------
# Determine CPU batching
# --------------------------
# Number of CPUs available to this process (cross-platform)
try:
    # Linux-specific
    available_cpus = len(os.sched_getaffinity(0))
except AttributeError:
    import multiprocessing

    # Fallback for macOS, Windows, or systems without sched_getaffinity
    available_cpus = multiprocessing.cpu_count()
jobs_per_CPU = int(np.ceil(num_ic / available_cpus))

# --------------------------
# Launch batches for each selected script
# --------------------------
for script in scripts_to_run:
    print(f"Running {script} ...")
    for i in range(0, num_ic, jobs_per_CPU):
        i_ini = i
        i_end = min(i + jobs_per_CPU - 1, num_ic - 1)  # avoid going past last IC

        comm = f"python {script} {i_ini} {i_end} &"
        print(f"$ {comm}")
        os.system(comm)

# Wait for all background processes to finish
os.system("wait")
