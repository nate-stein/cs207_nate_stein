import doctest
from typing import Iterable, List, Sequence

import numpy as np


def progress_rate (x: Sequence[float], v: Sequence[float], k: float) -> float:
    """ Calculates progress rate for single reaction represented by inputs.

    Args:
        x: Concentration vector.
        v: Stoichiometric coefficients of reactants.
        k: Forward reaction rate coefficient.

    Notes:
        Raises ValueError if sequences x and v are not the same length.

    Returns:
        Reaction progress rate.

    Examples:
    >>> progress_rate([1.0, 2.0, 3.0], [2.0, 1.0, 1.0], 10)
    60.0
    """
    if len(x) != len(v):
        raise ValueError('x and v must be same length.')

    result = 1
    for i, x_i in enumerate(x):
        result *= pow(x_i, v[i])
    return k * result


def progress_rates (x: Sequence[float], v_react: Sequence[Sequence[float]],
                    k: float) -> List[float]:
    """ Calculates progress rates for system of reactions.

    Args:
        x: Concentration vector.
        v_react: Matrix of stoichiometric coefficients for reactants.
        k: Forward reaction rate coefficient.

    Notes:
        v_react is an m-by-n matrix, where the number of rows (m) must equal the number
        of species (i.e., length of concentration vector x) and the number of columns
        must equal the number of reactions.

    Returns:
        List of progress rates for system of reactions.

    Examples:
    >>> progress_rates([1.0, 2.0, 1.0], [[1.0, 2.0], [2.0, 0.0], [0.0, 2.0]], 10)
    [40.0, 10.0]
    """
    # Test inputs
    # Ensure all rows in v_react have same number of columns (corresponding to number
    # of reactions).
    M = len(v_react[0])
    for row in v_react:
        if len(row) != M:
            raise ValueError('Not all rows in v_react share the same dimension.')

    if len(x) != len(v_react):
        raise ValueError('Length of x != number of rows in v_react.')

    # Call progress_rate() on reaction formed from concentration vector x and the
    # reactant coefficients in each column of v_react.
    result = []
    for j in range(0, M):
        v = [row[j] for row in v_react]
        rate = progress_rate(x, v, k)
        result.append(rate)

    return result


def reaction_rate (x: Sequence[float], v_react: Sequence[Sequence[float]],
                   v_prod: Sequence[Sequence[float]], k: float) -> Iterable:
    """ Calculates reaction rates for species for a given system of reactions.

    Args:
        x: Concentration vector.
        v_react: Matrix of stoichiometric coefficients for reactants.
        v_prod: Matrix of stoichiometric coefficients for products.
        k: Forward reaction rate coefficient.

    Notes:
        v_react is an m-by-n matrix, where the number of rows (m) must equal the number
        of species (i.e., length of concentration vector x) and the number of columns
        must equal the number of reactions.

        v_react and v_prod must be of the same dimensions.

    Returns:
        List of reaction rates for species represented by concentration rates in x.

    Examples:
    >>> reaction_rate([1.0, 2.0, 1.0], [[1.0, 0.0], [2.0, 0.0], [0.0, 2.0]], [[0.0, 1.0], [0.0, 2.0], [1.0, 0.0]], 10)
    [-30.0, -60.0, 20.0]
    """
    reaction_rates = progress_rates(x, v_react, k)

    # Convert stoichiometric coefficients for reactants and products to np matrices to
    # make matrix transformations simpler.
    if not isinstance(v_react, np.matrix):
        v_react = np.matrix(v_react)
    if not isinstance(v_prod, np.matrix):
        v_prod = np.matrix(v_prod)

    if v_react.shape != v_prod.shape:
        raise ValueError('Dimensions of v_react and v_prod not equal.')

    v_ij = v_prod - v_react
    result = v_ij.dot(reaction_rates)
    # Convert 1D matrix to a simple list.
    return np.array(result).flatten().tolist()


if __name__ == '__main__':
    doctest.testmod(verbose=True)
