"""
This script computes LDI indicators and Lyapunov exponents for a network of N coupled
logistic maps using pynamicalsys. It generates slightly perturbed initial conditions
and searches for those that satisfy predefined LDI intervals.

Usage:
    python logistic_map_network.py <i_ini> <i_end>

    or

    python run_systems.py <num_ic>

Arguments:
    i_ini : int
        Starting index of initial conditions for this batch.
    i_end : int
        Ending index of initial conditions for this batch.

Outputs:
    Data/LogisticMapNetwork/lmn_ldi_k=<k>_ic=<i>.dat
    Data/LogisticMapNetwork/lmn_lyapunov_k=<k>_ic=<i>.dat
"""

import os
import sys
import numpy as np
from pynamicalsys import DiscreteDynamicalSystem as dds
from models import logistic_map_network, logistic_map_network_jacobian
from parameters import LOGISTIC_MAP_NETWORK

# --------------------------
# System parameters
# --------------------------
network_size = LOGISTIC_MAP_NETWORK["network_size"]
parameters = LOGISTIC_MAP_NETWORK["parameters"]
parameters.append(network_size)
np.random.seed(5)
u0 = np.random.uniform(0.0, 1, network_size) + 1e-4
du = LOGISTIC_MAP_NETWORK["du"]

# --------------------------
# Iteration parameters
# --------------------------
sample_size = LOGISTIC_MAP_NETWORK["sample_size"]
transient_time = LOGISTIC_MAP_NETWORK["transient_time"]
total_time = sample_size + transient_time

# Indices of LDI calculations and corresponding target intervals
intervals = LOGISTIC_MAP_NETWORK["intervals"]
ks = LOGISTIC_MAP_NETWORK["ks"]

path = LOGISTIC_MAP_NETWORK["path"]  # Datafiles location
os.makedirs(path, exist_ok=True)

# --------------------------
# Create dynamical system
# --------------------------
ds = dds(
    mapping=logistic_map_network,
    jacobian=logistic_map_network_jacobian,
    system_dimension=network_size,
    number_of_parameters=4,
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
    k_val = ks[j]  # k-index for LDI, matching original code

    for ic in range(i_ini, i_end + 1):
        count = 0
        while True:
            # Set reproducible seed
            np.random.seed(ic * 10 + j + count)

            # Generate random initial condition
            u = np.random.rand(network_size)
            u = u0 + u * du

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
        ldi_file = f"{path}/lmn_ldi_k={k_val}_ic={ic}.dat"
        with open(ldi_file, "w") as f:
            for idx, val in enumerate(ldi_history):
                f.write(f"{idx + 1} {val:.16f}\n")

        # --------------------------
        # Save Lyapunov exponents to file
        # --------------------------
        lyap_file = f"{path}/lmn_lyapunov_k={k_val}_ic={ic}.dat"
        with open(lyap_file, "w") as f:
            for idx, val in enumerate(lyapunov_values):
                f.write(f"{idx + 1} {val:.16f}\n")
