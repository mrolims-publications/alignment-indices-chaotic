"""
This script computes LDI indicators and Lyapunov exponents for the 3D Henon map
using pynamicalsys. It generates slightly perturbed initial conditions and searches
for those that satisfy predefined LDI intervals.

Usage:
    python henon_map_3D.py <i_ini> <i_end>

    or

    python run_systems.py <num_ic>

Arguments:
    i_ini : int
        Starting index of initial conditions for this batch.
    i_end : int
        Ending index of initial conditions for this batch.

Outputs:
    Data/Henon/henon_ldi_k=<k>_ic=<i>.dat
    Data/Henon/henon_lyapunov_k=<k>_ic=<i>.dat
"""

import os
import sys
import numpy as np
from pynamicalsys import DiscreteDynamicalSystem as dds
from models import henon_map_3D, henon_map_3D_jacobian
from parameters import HENON

# --------------------------
# System parameters
# --------------------------
u0 = HENON["u0"]
du = HENON["du"]
parameters = HENON["parameters"]

# --------------------------
# Iteration parameters
# --------------------------
sample_size = HENON["sample_size"]
transient_time = HENON["transient_time"]
total_time = sample_size + transient_time

# Indices of LDI calculations and corresponding target intervals
intervals = HENON["intervals"]

path = HENON["path"]  # Datafiles location
os.makedirs(path, exist_ok=True)

# --------------------------
# Create dynamical system
# --------------------------
ds = dds(
    mapping=henon_map_3D,
    jacobian=henon_map_3D_jacobian,
    system_dimension=3,
    number_of_parameters=3,
)

# --------------------------
# Batch indices from command line
# --------------------------
i_ini = int(sys.argv[1])
i_end = int(sys.argv[2])

# --------------------------
# Main computation loop
# --------------------------
for j, target_interval in enumerate(intervals):
    k_val = j + 2  # k-index for LDI, matching original code

    for ic in range(i_ini, i_end + 1):
        count = 0
        while True:
            # Set reproducible seed
            np.random.seed(ic * 13 + j + count)

            # Perturb initial condition
            u = u0 + np.random.rand(3) * du

            # Compute LDI history
            ldi_history = ds.LDI(
                u,
                total_time,
                k=k_val,
                parameters=parameters,
                seed=2,
                transient_time=transient_time,
                return_history=True,
            )
            ldi_history = ldi_history[ldi_history > 0]

            # Accept if LDI length falls in the target interval
            if target_interval[0] <= len(ldi_history) <= target_interval[1]:
                # Compute Lyapunov exponents
                lyapunov_values = ds.lyapunov(
                    u,
                    total_time,
                    parameters=parameters,
                    transient_time=transient_time,
                )
                break
            count += 1

        # --------------------------
        # Save LDI to file
        # --------------------------
        ldi_file = f"{path}/henon_ldi_k={k_val}_ic={ic}.dat"
        with open(ldi_file, "w") as f:
            for idx, val in enumerate(ldi_history):
                f.write(f"{idx + 1} {val:.16f}\n")

        # --------------------------
        # Save Lyapunov exponents to file
        # --------------------------
        lyap_file = f"{path}/henon_lyapunov_k={k_val}_ic={ic}.dat"
        with open(lyap_file, "w") as f:
            for idx, val in enumerate(lyapunov_values):
                f.write(f"{idx + 1} {val:.16f}\n")
