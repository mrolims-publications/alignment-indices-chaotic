"""
This script computes the Lyapunov and LDI indicators for a Fermi-Pasta-Ulam
system using the pynamicalsys package. It generates slightly perturbed initial
conditions and searches for those that satisfy predefined LDI intervals.

Usage:
    python fpu.py <i_ini> <i_end>

    or

    python run_systems.py <num_ic>

Arguments:
    i_ini : int
        The starting index of initial conditions for this batch.
    i_end : int
        The ending index of initial conditions for this batch.

Outputs:
    Data/FPU/fpu_ldi_k=<k>_ic=<i>.dat
    Data/FPU/fpu_lyapunov_k=<k>_ic=<i>.dat
"""

import os
import sys
import numpy as np
from pynamicalsys import ContinuousDynamicalSystem as cds
from models import fermi_pasta_ulam, fermi_pasta_ulam_jacobian
from parameters import FPU

# --------------------------
# System parameters
# --------------------------
dof = FPU["dof"]  # Degrees of freedom
N = 2 * dof  # Total number of equations (positions + momenta + boundaries)
X = FPU["X"]  # Reference displacement for the middle particle
dx = FPU["dx"]  # Maximum random perturbation from X
parameters = [FPU["beta"]]  # System parameter beta

path = FPU["path"]  # Datafiles location
os.makedirs(path, exist_ok=True)

# --------------------------
# Time integration setup
# --------------------------
total_time = FPU["total_time"]
time_step = FPU["time_step"]

# Create the dynamical system
ds = cds(
    equations_of_motion=fermi_pasta_ulam,
    jacobian=fermi_pasta_ulam_jacobian,
    system_dimension=N,
    number_of_parameters=1,
)

# Select numerical integrator
ds.integrator("rk4", time_step=time_step)

# --------------------------
# Initial conditions
# --------------------------
# Base state
u = np.zeros(N)
u[2] = X

# Indices of LDI calculations and corresponding target intervals
ks = FPU["ks"]
intervals = FPU["intervals"]

# Range of initial conditions handled by this batch
i_ini = int(sys.argv[1])
i_end = int(sys.argv[2])

# --------------------------
# Main computation loop
# --------------------------
for j, k in enumerate(ks):
    target_interval = intervals[j]

    for ic in range(i_ini, i_end + 1):
        count = 0

        # Keep generating perturbed initial conditions until the LDI falls within target
        while True:
            # Seed ensures reproducibility for each IC
            np.random.seed(ic * 1313 + j + count)

            # Perturb middle particle
            u[2] = X - dx * np.random.rand()

            # Compute LDI
            ldi_history = ds.LDI(
                u,
                total_time,
                k,
                parameters=parameters,
                seed=2,
                return_history=True,
                threshold=1e-15,
            )

            # Check if LDI falls into the target interval
            if target_interval[0] <= ldi_history[-1, 0] <= target_interval[1]:
                # Compute Lyapunov exponents only for accepted IC
                lyapunov_values = ds.lyapunov(u, total_time, parameters=parameters)
                break

            count += 1

        # --------------------------
        # Save results to files
        # --------------------------
        # LDI history
        ldi_file = f"{path}/fpu_ldi_k={k}_ic={ic}.dat"
        with open(ldi_file, "w") as f:
            for row in ldi_history:
                f.write(f"{row[0]:.16f} {row[1]:.16f}\n")

        # Lyapunov exponents
        lyap_file = f"{path}/fpu_lyapunov_k={k}_ic={ic}.dat"
        with open(lyap_file, "w") as f:
            for idx, val in enumerate(lyapunov_values):
                f.write(f"{idx + 1} {val:.16f}\n")
