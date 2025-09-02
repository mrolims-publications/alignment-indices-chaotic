import numpy as np


def propagate_error(func, values, errors):
    """
    Compute the result and propagated error of a function.

    Parameters:
    - func: The function to evaluate (e.g., lambda x, y: x + y).
    - values: List of input values (e.g., [a, b]).
    - errors: List of input errors (e.g., [da, db]).

    Returns:
    - (result, error): The computed result and its propagated error.
    """
    # Compute the nominal result
    result = func(*values)

    # Compute partial derivatives numerically (small perturbation)
    partials = []
    delta = 1e-8  # Small step for numerical differentiation
    for i in range(len(values)):
        perturbed_values = values.copy()
        perturbed_values[i] += delta
        partial = (func(*perturbed_values) - result) / delta
        partials.append(partial)

    # Compute propagated error
    error_squared = sum((p * e) ** 2 for p, e in zip(partials, errors))
    error = np.sqrt(error_squared)

    return result, error


def format_mean_std(a, b):
    try:
        if b == 0:
            return f"{a}(0)"

        # Order of magnitude of the uncertainty
        exponent = int(np.floor(np.log10(abs(b))))

        # Keep only 1 significant digit in the uncertainty
        rounded_b = round(b, -exponent)

        # Handle case like 9.7 -> 10
        if rounded_b >= 10 ** (exponent + 1):
            exponent += 1
            rounded_b = 10**exponent

        # Round a to the same decimal place
        rounded_a = round(a, -exponent)

        # Number of decimals
        decimals = max(-exponent, 0)

        # Build string in parentheses notation
        return f"{rounded_a:.{decimals}f}({int(rounded_b / 10**exponent)})"

    except Exception:
        return "error"
