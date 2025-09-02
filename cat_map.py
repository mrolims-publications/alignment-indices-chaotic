"""
This script computes SALI for the Cat map using pynamicalsys. It generates slightly
perturbed initial conditions and searches for those that satisfy predefined SALI
intervals.

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
    Data/Henon/henon_sali_k=<k>_ic=<i>.dat
    Data/Henon/henon_lyapunov_k=<k>_ic=<i>.dat
"""

import os
import sys
import numpy as np
from pynamicalsys import DiscreteDynamicalSystem as dds
from models import cat_map, cat_map_jacobian
from parameters import CATMAP


# --------------------------
# Iteration parameters
# --------------------------
total_time = CATMAP["total_time"]

path = CATMAP["path"]  # Datafiles location
os.makedirs(path, exist_ok=True)

threshold = CATMAP["SALI_threshold"]

# --------------------------
# Create dynamical system
# --------------------------
ds = dds(
    mapping=cat_map,
    jacobian=cat_map_jacobian,
    system_dimension=2,
    number_of_parameters=0,
)

# --------------------------
# Batch indices from command line
# --------------------------
i_ini = int(sys.argv[1])
i_end = int(sys.argv[2])

# --------------------------
# Main computation loop
# --------------------------

for ic in range(i_ini, i_end + 1):
    # Compute SALI history
    sali_history = ds.SALI(
        [0.1, 0.1],
        total_time,
        seed=1313 * ic,
        return_history=True,
        tol=threshold,
    )
    sali_history = sali_history[sali_history > 0]

    # --------------------------
    # Save SALI to file
    # --------------------------
    sali_file = f"{path}/catmap_sali_ic={ic}.dat"
    with open(sali_file, "w") as f:
        for idx, val in enumerate(sali_history):
            f.write(f"{idx + 1} {val:.16f}\n")
