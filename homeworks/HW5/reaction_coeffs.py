import math

# Default ideal gas constant.
R = 8.314


def arrhenius (A: float, E: float, T: float, R: float = R) -> float:
    """
    Args:
        A: Pre-exponential (frequency) factor.
            ValueError raised if not > 0.
        E: Activation energy.
        T: Temperature in Kelvins.
            ValueError raised if not >= 0.
        R: Universal gas constant.

    Returns:
        Arrhenius reaction rate coefficient.
    """
    if A <= 0:
        raise ValueError('A must be > 0.')
    if T < 0:
        raise ValueError('T must be >= 0.')

    return A * math.exp(-E / (R * T))


def modified_arrhenius (A: float, E: float, T: float, b: float, R: float = R) -> float:
    """
    Args:
        A: Arrhenius prefactor (frequency factor).
            ValueError raised if not > 0.
        E: Activation energy.
        T: Temperature in Kelvins.
            ValueError raised if not >= 0.
        b: Modified Arrhenius parameter.
            Must be real number.
        R: Universal gas constant.

    Notes:
        Calculation done by multiplying the result of a call to arrhenius() with the
        modified Arrhenius parameter (T^b).

    Returns:
        Modified Arrhenius reaction rate coefficient.
    """
    if isinstance(b, complex):
        raise ValueError('b must be real number.')
    prelim = arrhenius(A, E, T, R)
    return prelim * (pow(T, b))
