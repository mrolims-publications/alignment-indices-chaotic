# alignment-indices-chaotic

Code repository accompanying the publication entitled "On the behavior of Linear Dependence, Smaller, and Generalized Alignment Indices in chaotic discrete and continuous systems" by M. Rolim Sales, E. D. Leonel, and C. G. Antonopoulos.

This project contains the code to generate and plot all the data from all figures.

## Requirements

- Python 3.8 or higher.
- Dependencies listed in [requirements.txt](requirements.txt).
- This project uses [pynamicalsys](https://pynamicalsys.readthedocs.io/en/latest/) to calculate the Smaller, Generalized, and Linear Dependence Indices.

### Installation

You can install the required packages with:
```bash
pip install -r requirements.txt
``` 
## Usage

There are two ways to run simulations:

1. Run a specific system script

    Each system script (e.g. `henon_map_3D.py`, `fpu.py`, etc.) computes LDI indicators and Lyapunov exponents for the chosen model.

    ```bash
    python henon_map_3D.py <i_ini> <i_end>
    ```
    - `i_ini`: Starting index of initial conditions
    - `i_end`: Ending index of initial conditions

    In our paper, we have considered 100 initial conditions, so
    ```bash
    python henon_map_3D.py 1 100
    ```
    runs the 3D Hénon map for initial conditions 1 through 100.

2. Run multiple systems with parallelization

    The script `run_systems.py` distributes a given number of initial conditions across all available CPUs and runs one or more system scripts in parallel.

    ```bash
    python run_systems.py <num_ic>
    ```

    You will be prompted to choose the system:
	1.	Hénon map 3D
	2.	Logistic map network
	3.	FPU (Fermi–Pasta–Ulam)
	4.	Cat map
	5.	Baker map
	6.	All systems
	7.	Exit

    For example
    ```bash
    python run_systems.py 100
    ```
    splits 100 initial conditions among available CPUs and executes the selected system(s).

## Outputs

Each system script produces `.dat` files containing the computed indicators. For example, the 3D Hénon map generates:

- Data/Henon/henon_ldi_k=\<k>_ic=\<i>.dat
- Data/Henon/henon_ldi_k=\<k>_ic=\<i>.dat 

(similar directories exist for other systems).

## Plotting

The Jupyter notebook [Plots.ipynb](Plots.ipynb) reproduces the figures shown in the publication using the generated data.

## Project structure

```
.
├── baker_map.py              # Baker map simulation script
├── cat_map.py                # Cat map simulation script
├── fpu.py                    # Fermi–Pasta–Ulam simulation script
├── henon_map_3D.py           # 3D Hénon map simulation script
├── LICENSE                   # GNU License file
├── logistic_map_network.py   # Logistic map network simulation script
├── models.py                 # Shared model definitions
├── parameters.py             # Simulation parameters and defaults
├── utils.py                  # Utility functions
├── run_systems.py            # Master script to run systems in parallel
├── Plots.ipynb               # Jupyter notebook for reproducing paper figures
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
```

## Citation

If you use this repository or parts of it in your work, please consider citing our research paper:

*M. Rolim Sales et al.*, **On the behavior of Linear Dependence, Smaller, and Generalized Alignment Indices in discrete and continuous chaotic systems**, *[Chaos, Solitons and Fractals 205 117884 (2026)](https://doi.org/10.1016/j.chaos.2026.117884)*

```bibtex
@article{Sales2026,
title = {On the behavior of Linear Dependence, Smaller, and Generalized Alignment Indices in discrete and continuous chaotic systems},
journal = {Chaos, Solitons \& Fractals},
volume = {205},
pages = {117884},
year = {2026},
doi = {https://doi.org/10.1016/j.chaos.2026.117884},
url = {https://www.sciencedirect.com/science/article/pii/S0960077926000251},
author = {Matheus Rolim Sales and Edson Denis Leonel and Chris G. Antonopoulos},
}
```

## Contact

For questions, suggestions, or collaboration, please reach out to:

📧 [rolim.sales.m[at]gmail.com](mailto:rolim.sales.m@gmail.com)  
🔗 [mrolims.github.io](https://mrolims.github.io)

## License

This project is licensed under the GNU General Public License v3.0.
See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was financed, in part, by the São Paulo Research Foundation (FAPESP, Brazil), under process numbers 2023/08698-9 and 2024/09208-8.

## Disclaimer

As opiniões, hipóteses e conclusões ou recomendações expressas neste material são de responsabilidade do(s) autor(es) e não necessariamente refletem a visão da Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP, Brasil).

The opinions, hypotheses, and conclusions or recommendations expressed in this material are the sole responsibility of the author(s) and do not necessarily reflect the views of the São Paulo Research Foundation (FAPESP, Brazil).
