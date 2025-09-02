# FPU parameters
FPU = {
    "dof": 6,
    "X": 1.0,
    "dx": 1e-2,
    "total_time": 10000,
    "time_step": 0.005,
    "ks": [2, 3, 4, 5, 6, 8],
    "intervals": [[350, 450], [100, 150], [70, 100], [40, 50], [40, 45], [20, 27]],
    "beta": 1.0,
    "path": "Data/FPU",
    "num_ic": 100,
    "LDI_threshold": 1e-15,
}

# Henon map parameters
HENON = {
    "num_ic": 100,
    "intervals": [[1475, 1525], [80, 90]],
    "ks": [2, 3],
    "parameters": [0, 0.85, 0.7],
    "u0": [0.6, 0.2, 0.3],
    "du": [1e-3, 1e-3, 1e-3],
    "sample_size": int(1e6),
    "transient_time": int(5e5),
    "path": "Data/Henon",
}

# Logistic map network parameters
LOGISTIC_MAP_NETWORK = {
    "network_size": 10,
    "num_ic": 100,
    "intervals": [[700, 750], [275, 325], [145, 155], [95, 105], [50, 55], [23, 30]],
    "ks": [2, 3, 4, 5, 6, 8],
    "parameters": [3.8, 0.15, 0.15],
    "du": 1e-3,
    "sample_size": 50000,
    "transient_time": 50000,
    "path": "Data/LogisticMapNetwork",
}

CATMAP = {
    "num_ic": 100,
    "total_time": 10000,
    "SALI_threshold": 3e-16,
    "path": "Data/CatMap",
}

BAKERMAP = {
    "num_ic": 100,
    "sample_size": 10000,
    "transient_time": 10000,
    "SALI_threshold": 1e-16,
    "path": "Data/BakerMap",
    "parameters": [0.3],
}
