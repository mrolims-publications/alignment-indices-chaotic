import numpy as np
from numba import njit


@njit
def cat_map(u, parameters):

    x, y = u

    x_new = 2 * x + y
    y_new = x + y
    x_new = x_new % 1.0
    y_new = y_new % 1.0

    return np.array([x_new, y_new], dtype=np.float64)


@njit
def cat_map_jacobian(u, parameters, *args):

    return np.array([[2, 1], [1, 1]], dtype=np.float64)


@njit
def baker_map(u, parameters):
    x, y = u
    k = parameters[0]

    if 0 <= y <= 0.5:
        x_new = k * x
        y_new = 2 * y
    else:
        x_new = 1 + k * (x - 1)
        y_new = 1 + 2 * (y - 1)

    return np.array([x_new, y_new], dtype=np.float64)


@njit
def baker_map_jacobian(u, parameters, *args):

    k = parameters[0]
    J = np.zeros((2, 2), dtype=np.float64)
    J[0, 0] = k
    J[0, 1] = 0
    J[1, 0] = 0
    J[1, 1] = 2

    return J


@njit
def henon_map_3D(u, parameters):
    x, y, z = u
    M1, M2, B = parameters

    x_new = y
    y_new = z
    z_new = M1 + B * x + M2 * y - z**2

    return np.array([x_new, y_new, z_new], dtype=np.float64)


@njit
def henon_map_3D_jacobian(u, parameters, *args):
    M1, M2, B = parameters

    J = np.array(
        [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [B, M2, -2.0 * u[2]]], dtype=np.float64
    )

    return J


@njit
def f(u, a):
    return a * u * (1 - u)


@njit
def logistic_map_network(u, parameters):
    a, r, sigma, N = parameters

    P = round(r * N)

    N = int(N)

    for i in range(N):
        coupling = 0
        for j in range(i - P, i + P + 1):
            coupling += f(u[j % N], a) - f(u[i], a)
        u[i] = f(u[i], a) + sigma * coupling / (2 * P)

    return u


@njit
def logistic_map_network_jacobian(u, parameters, *args):
    a, r, sigma, N = parameters

    P = round(r * N)

    N = int(N)

    J = np.zeros((N, N))

    f_prime = lambda u: a * (1 - 2 * u)

    for i in range(N):
        for j in range(i - P, i + P + 1):
            j_mod = j % N
            if j_mod == i:
                J[i, j_mod] = f_prime(u[j_mod]) * (1 - sigma)
            else:
                J[i, j_mod] = (sigma / (2 * P)) * f_prime(u[j_mod])

    return J


@njit
def fermi_pasta_ulam(time, u, parameters):
    dof = len(u) // 2  # total particles including fixed ends
    dudt = np.zeros_like(u)
    beta = parameters[0]
    x = u[0::2]
    p = u[1::2]

    # dx_j/dt = p_j (skip fixed ends j=0 and j=dof-1)
    dudt[2 : 2 * (dof - 1) : 2] = p[1:-1]

    # dp_j/dt for movable particles j = 1..dof-2
    for j in range(1, dof - 1):
        harmonic = x[j + 1] - 2 * x[j] + x[j - 1]
        nonlinear = beta * ((x[j + 1] - x[j]) ** 3 - (x[j] - x[j - 1]) ** 3)
        dudt[2 * j + 1] = harmonic + nonlinear

    # fixed ends (j=0 and j=dof-1) remain zero
    return dudt


@njit
def fermi_pasta_ulam_jacobian(time, u, parameters):

    dof = len(u) // 2
    J = np.zeros((2 * dof, 2 * dof))

    x = u[0::2]
    # p = u[1::2]  # not needed for Jacobian
    beta = parameters[0]

    # dx_i/dp_j = delta_ij for movable particles
    J[2 : 2 * (dof - 1) : 2, 3 : 2 * (dof - 1) : 2] = np.eye(dof - 2)

    # dp_i/dx_j for movable particles i=1..dof-2
    for i in range(1, dof - 1):
        for j in [i - 1, i, i + 1]:
            if j == i - 1:
                J[2 * i + 1, 2 * j] = 1 - 3 * beta * (x[i] - x[i - 1]) ** 2
            elif j == i:
                J[2 * i + 1, 2 * j] = -2 + 3 * beta * (
                    (x[i + 1] - x[i]) ** 2 + (x[i] - x[i - 1]) ** 2
                )
            elif j == i + 1:
                J[2 * i + 1, 2 * j] = 1 - 3 * beta * (x[i + 1] - x[i]) ** 2

    # dp_i/dp_j = 0, dx_i/dx_j already handled
    # fixed ends: first and last rows/columns are zero
    return J


def fermi_pasta_ulam_energy(u, parameters):
    u = np.atleast_2d(u)
    dof = u.shape[1] // 2
    beta = parameters[0]

    x = u[:, 0::2]
    p = u[:, 1::2]

    # kinetic energy: only movable particles j=1..dof-2
    T = 0.5 * np.sum(p[:, 1:-1] ** 2, axis=1)

    # potential energy: springs between j=0..dof-2 and j+1
    V = np.zeros(u.shape[0])
    for j in range(dof - 1):
        dx = x[:, j + 1] - x[:, j]
        V += 0.5 * dx**2 + 0.25 * beta * dx**4

    H = T + V
    return H if u.shape[0] > 1 else H[0]
