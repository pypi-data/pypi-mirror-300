import sympy
from cmath import exp, sin, cos, pi, sqrt

t, p = sympy.symbols("t p")
sw_sh_dict = dict()


def compute_spin_weighted_spherical_harmonics(l, m, theta, phi):
    r"""
    Compute the spin-weighted spherical harmonics of given degree and order.

    This function calculates the spin-weighted spherical harmonics :math:`_sY_{lm}(\theta, \phi)`
    using the specified degree :math:`l` and order :math:`m`. It uses symbolic differentiation
    to compute the necessary components, caching results for efficiency.

    Parameters
    ----------
    l : int
        The degree of the spherical harmonic. Must be a non-negative integer.
    m : int
        The order of the spherical harmonic. Must satisfy the condition :math:`|m| \leq l`.
    theta : float
        The polar angle in radians, where :math:`\theta` should be in the range [0, \pi].
    phi : float
        The azimuthal angle in radians, where :math:`\phi` should be in the range [0, 2\pi].

    Returns
    -------
    complex
        The value of the spin-weighted spherical harmonic :math:`_sY_{lm}(\theta, \phi)` evaluated
        at the given angles. The result is a complex number.

    Notes
    -----
    The function caches the computed harmonics in `sw_sh_dict` to avoid redundant calculations.
    The input `theta` is clamped to a minimum value to prevent division by zero.

    Raises
    ------
    ValueError
        If the inputs do not satisfy the conditions for :math:`l` and :math:`m`.
    """
    theta = max(1e-100, theta)
    if (l, m) not in sw_sh_dict:
        sph_harmonics = sympy.Ynm(l, m, t, p).expand(func=True)
        Wlm = (
            sympy.diff(sph_harmonics, t, 2)
            - sympy.cot(t) * sympy.diff(sph_harmonics, t)
            - sympy.csc(t) * sympy.csc(t) * sympy.diff(sph_harmonics, p, 2)
        )
        Xlm = 2 * sympy.diff(
            sympy.diff(sph_harmonics, t) - sympy.cot(t) * sph_harmonics, p
        )
        sw_sh_dict[(l, m)] = sympy.simplify(
            sympy.sqrt(sympy.factorial(l - 2) / sympy.factorial(l + 2))
            * (Wlm - sympy.I * Xlm / sympy.sin(t))
        )
    return complex(sw_sh_dict[(l, m)].subs([(t, theta), (p, phi)]).evalf())


def spin_weighted_spherical_harmonics(l, m, theta, phi):
    r"""
    Compute the spin-weighted spherical harmonics of given degree and order.

    This function calculates the spin-weighted spherical harmonics :math:`_sY_{lm}(\theta, \phi)`
    for the specified degree :math:`l` and order :math:`m`. The computation is done using
    closed-form expressions for degrees :math:`l \leq 16`. For higher degrees, it delegates
    the calculation to the `compute_spin_weighted_spherical_harmonics` function.

    The function raises a ValueError if the inputs do not meet the requirements for valid
    spherical harmonics.

    Parameters
    ----------
    l : int
        The degree of the spherical harmonic. Must be a non-negative integer with
        :math:`l \leq 16` and :math:`|m| \leq l`.
    m : int
        The order of the spherical harmonic. Must satisfy the condition :math:`-l \leq m \leq l`.
    theta : float
        The polar angle in radians, where :math:`\theta` should be in the range [0, \pi].
    phi : float
        The azimuthal angle in radians, where :math:`\phi` should be in the range [0, 2\pi].

    Returns
    -------
    complex
        The value of the spin-weighted spherical harmonic :math:`_sY_{lm}(\theta, \phi)` evaluated
        at the given angles. The result is a complex number.

    Raises
    ------
    ValueError
        If the inputs do not satisfy the conditions for :math:`l` and :math:`m`,
        specifically if :math:`l < |m|` or :math:`l > 16`.

    Notes
    -----
    The computation is performed using specific formulas for :math:`l` values
    from 0 to 16, ensuring efficiency for lower degrees. For degrees
    higher than 16, the function relies on an external computation method.

    Examples
    --------
    >>> Y = spin_weighted_spherical_harmonics(2, 1, 0.5, 1.0)
    >>> print(Y)
    (complex_number)  # Replace with the expected output
    """
    if l < abs(m):
        raise ValueError("need to -l <= m <= l")
    if l > 16:
        return compute_spin_weighted_spherical_harmonics(l, m, theta, phi)
    else:
        if l <= 9:
            if l <= 5:
                if l <= 3:
                    if l <= 2:
                        if m <= 0:
                            if m <= -1:
                                if m <= -2:
                                    return (
                                        sqrt(5)
                                        * (
                                            4 * 1j * sin(2 * phi) * cos(theta)
                                            - 1j * sin(2 * phi) * cos(2 * theta)
                                            - 3 * 1j * sin(2 * phi)
                                            - 4 * cos(2 * phi) * cos(theta)
                                            + cos(2 * phi) * cos(2 * theta)
                                            + 3 * cos(2 * phi)
                                        )
                                        / (16 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        -sqrt(5)
                                        * (1j * sin(phi) - cos(phi))
                                        * (2 * sin(theta) - sin(2 * theta))
                                        / (8 * sqrt(pi))
                                    )
                            else:
                                return sqrt(30) * sin(theta) ** 2 / (8 * sqrt(pi))
                        else:
                            if m <= 1:
                                return (
                                    sqrt(5)
                                    * (cos(theta) + 1)
                                    * exp(1j * phi)
                                    * sin(theta)
                                    / (4 * sqrt(pi))
                                )
                            else:
                                return (
                                    sqrt(5)
                                    * (4 * cos(theta) + cos(2 * theta) + 3)
                                    * exp(2 * 1j * phi)
                                    / (16 * sqrt(pi))
                                )
                    else:
                        if m <= 0:
                            if m <= -2:
                                if m <= -3:
                                    return (
                                        sqrt(42)
                                        * (
                                            5 * sin(theta)
                                            - 4 * sin(2 * theta)
                                            + sin(3 * theta)
                                        )
                                        * exp(-3 * 1j * phi)
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        sqrt(7)
                                        * (
                                            5 * cos(theta)
                                            - 8 * cos(2 * theta)
                                            + 3 * cos(3 * theta)
                                        )
                                        * exp(-2 * 1j * phi)
                                        / (32 * sqrt(pi))
                                    )
                            else:
                                if m <= -1:
                                    return (
                                        -sqrt(70)
                                        * (1j * sin(phi) - cos(phi))
                                        * (
                                            sin(theta)
                                            + 4 * sin(2 * theta)
                                            - 3 * sin(3 * theta)
                                        )
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        sqrt(210)
                                        * (cos(theta) - cos(3 * theta))
                                        / (32 * sqrt(pi))
                                    )
                        else:
                            if m <= 2:
                                if m <= 1:
                                    return (
                                        sqrt(70)
                                        * (
                                            -sin(theta)
                                            + 4 * sin(2 * theta)
                                            + 3 * sin(3 * theta)
                                        )
                                        * exp(1j * phi)
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        sqrt(7)
                                        * (
                                            5 * cos(theta)
                                            + 8 * cos(2 * theta)
                                            + 3 * cos(3 * theta)
                                        )
                                        * exp(2 * 1j * phi)
                                        / (32 * sqrt(pi))
                                    )
                            else:
                                return (
                                    -sqrt(42)
                                    * (
                                        5 * sin(theta)
                                        + 4 * sin(2 * theta)
                                        + sin(3 * theta)
                                    )
                                    * exp(3 * 1j * phi)
                                    / (64 * sqrt(pi))
                                )
                else:
                    if l <= 4:
                        if m <= 0:
                            if m <= -2:
                                if m <= -3:
                                    if m <= -4:
                                        return (
                                            3
                                            * sqrt(7)
                                            * (
                                                4 * 1j * sin(4 * phi) * cos(theta)
                                                + 4 * 1j * sin(4 * phi) * cos(2 * theta)
                                                - 4 * 1j * sin(4 * phi) * cos(3 * theta)
                                                + 1j * sin(4 * phi) * cos(4 * theta)
                                                - 5 * 1j * sin(4 * phi)
                                                - 4 * cos(4 * phi) * cos(theta)
                                                - 4 * cos(4 * phi) * cos(2 * theta)
                                                + 4 * cos(4 * phi) * cos(3 * theta)
                                                - cos(4 * phi) * cos(4 * theta)
                                                + 5 * cos(4 * phi)
                                            )
                                            / (128 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(14)
                                            * (
                                                sin(theta)
                                                + 2 * sin(2 * theta)
                                                - 3 * sin(3 * theta)
                                                + sin(4 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (64 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        3
                                        * (
                                            2 * 1j * sin(2 * phi) * cos(theta)
                                            - 4 * 1j * sin(2 * phi) * cos(2 * theta)
                                            + 14 * 1j * sin(2 * phi) * cos(3 * theta)
                                            - 7 * 1j * sin(2 * phi) * cos(4 * theta)
                                            - 5 * 1j * sin(2 * phi)
                                            - 2 * cos(2 * phi) * cos(theta)
                                            + 4 * cos(2 * phi) * cos(2 * theta)
                                            - 14 * cos(2 * phi) * cos(3 * theta)
                                            + 7 * cos(2 * phi) * cos(4 * theta)
                                            + 5 * cos(2 * phi)
                                        )
                                        / (64 * sqrt(pi))
                                    )
                            else:
                                if m <= -1:
                                    return (
                                        -3
                                        * sqrt(2)
                                        * (1j * sin(phi) - cos(phi))
                                        * (
                                            3 * sin(theta)
                                            + 2 * sin(2 * theta)
                                            + 7 * sin(3 * theta)
                                            - 7 * sin(4 * theta)
                                        )
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        3
                                        * sqrt(10)
                                        * (-56 * sin(theta) ** 4 + 48 * sin(theta) ** 2)
                                        / (128 * sqrt(pi))
                                    )
                        else:
                            if m <= 2:
                                if m <= 1:
                                    return (
                                        3
                                        * sqrt(2)
                                        * (
                                            3 * sin(theta)
                                            - 2 * sin(2 * theta)
                                            + 7 * sin(3 * theta)
                                            + 7 * sin(4 * theta)
                                        )
                                        * exp(1j * phi)
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        3
                                        * (
                                            2 * 1j * sin(2 * phi) * cos(theta)
                                            + 4 * 1j * sin(2 * phi) * cos(2 * theta)
                                            + 14 * 1j * sin(2 * phi) * cos(3 * theta)
                                            + 7 * 1j * sin(2 * phi) * cos(4 * theta)
                                            + 5 * 1j * sin(2 * phi)
                                            + 2 * cos(2 * phi) * cos(theta)
                                            + 4 * cos(2 * phi) * cos(2 * theta)
                                            + 14 * cos(2 * phi) * cos(3 * theta)
                                            + 7 * cos(2 * phi) * cos(4 * theta)
                                            + 5 * cos(2 * phi)
                                        )
                                        / (64 * sqrt(pi))
                                    )
                            else:
                                if m <= 3:
                                    return (
                                        -3
                                        * sqrt(14)
                                        * (
                                            -sin(theta)
                                            + 2 * sin(2 * theta)
                                            + 3 * sin(3 * theta)
                                            + sin(4 * theta)
                                        )
                                        * exp(3 * 1j * phi)
                                        / (64 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        3
                                        * sqrt(7)
                                        * (
                                            -2 * sin(theta) ** 4
                                            + 4 * sin(theta) ** 2
                                            + cos(theta)
                                            - cos(3 * theta)
                                        )
                                        * exp(4 * 1j * phi)
                                        / (32 * sqrt(pi))
                                    )
                    else:
                        if m <= 0:
                            if m <= -3:
                                if m <= -4:
                                    if m <= -5:
                                        return (
                                            sqrt(330)
                                            * (
                                                -32 * sin(theta) ** 3 * cos(theta)
                                                + 14 * sin(theta)
                                                - 3 * sin(3 * theta)
                                                - sin(5 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (512 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(33)
                                            * (
                                                -14 * cos(theta)
                                                + 16 * cos(2 * theta)
                                                + 9 * cos(3 * theta)
                                                - 16 * cos(4 * theta)
                                                + 5 * cos(5 * theta)
                                            )
                                            * exp(-4 * 1j * phi)
                                            / (256 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        sqrt(66)
                                        * (
                                            14 * sin(theta)
                                            + 8 * sin(2 * theta)
                                            + 13 * sin(3 * theta)
                                            - 36 * sin(4 * theta)
                                            + 15 * sin(5 * theta)
                                        )
                                        * exp(-3 * 1j * phi)
                                        / (512 * sqrt(pi))
                                    )
                            else:
                                if m <= -1:
                                    if m <= -2:
                                        return (
                                            sqrt(11)
                                            * (
                                                14 * cos(theta)
                                                - 8 * cos(2 * theta)
                                                + 3 * cos(3 * theta)
                                                - 24 * cos(4 * theta)
                                                + 15 * cos(5 * theta)
                                            )
                                            * exp(-2 * 1j * phi)
                                            / (128 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(77)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                2 * sin(theta)
                                                + 8 * sin(2 * theta)
                                                + 3 * sin(3 * theta)
                                                + 12 * sin(4 * theta)
                                                - 15 * sin(5 * theta)
                                            )
                                            / (256 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        sqrt(2310)
                                        * (
                                            2 * cos(theta)
                                            + cos(3 * theta)
                                            - 3 * cos(5 * theta)
                                        )
                                        / (256 * sqrt(pi))
                                    )
                        else:
                            if m <= 3:
                                if m <= 2:
                                    if m <= 1:
                                        return (
                                            sqrt(77)
                                            * (
                                                -2 * sin(theta)
                                                + 8 * sin(2 * theta)
                                                - 3 * sin(3 * theta)
                                                + 12 * sin(4 * theta)
                                                + 15 * sin(5 * theta)
                                            )
                                            * exp(1j * phi)
                                            / (256 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(11)
                                            * (
                                                14 * cos(theta)
                                                + 8 * cos(2 * theta)
                                                + 3 * cos(3 * theta)
                                                + 24 * cos(4 * theta)
                                                + 15 * cos(5 * theta)
                                            )
                                            * exp(2 * 1j * phi)
                                            / (128 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        -sqrt(66)
                                        * (
                                            14 * sin(theta)
                                            - 8 * sin(2 * theta)
                                            + 13 * sin(3 * theta)
                                            + 36 * sin(4 * theta)
                                            + 15 * sin(5 * theta)
                                        )
                                        * exp(3 * 1j * phi)
                                        / (512 * sqrt(pi))
                                    )
                            else:
                                if m <= 4:
                                    return (
                                        sqrt(33)
                                        * (
                                            14 * cos(theta)
                                            + 16 * cos(2 * theta)
                                            - 9 * cos(3 * theta)
                                            - 16 * cos(4 * theta)
                                            - 5 * cos(5 * theta)
                                        )
                                        * exp(4 * 1j * phi)
                                        / (256 * sqrt(pi))
                                    )
                                else:
                                    return (
                                        -sqrt(330)
                                        * (
                                            32 * sin(theta) ** 3 * cos(theta)
                                            + 14 * sin(theta)
                                            - 3 * sin(3 * theta)
                                            - sin(5 * theta)
                                        )
                                        * exp(5 * 1j * phi)
                                        / (512 * sqrt(pi))
                                    )
            else:
                if l <= 7:
                    if l <= 6:
                        if m <= 0:
                            if m <= -3:
                                if m <= -5:
                                    if m <= -6:
                                        return (
                                            3
                                            * sqrt(715)
                                            * (
                                                8 * 1j * sin(6 * phi) * cos(theta)
                                                + 17
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(2 * theta)
                                                - 12
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(3 * theta)
                                                - 2 * 1j * sin(6 * phi) * cos(4 * theta)
                                                + 4 * 1j * sin(6 * phi) * cos(5 * theta)
                                                - 1j * sin(6 * phi) * cos(6 * theta)
                                                - 14 * 1j * sin(6 * phi)
                                                - 8 * cos(6 * phi) * cos(theta)
                                                - 17 * cos(6 * phi) * cos(2 * theta)
                                                + 12 * cos(6 * phi) * cos(3 * theta)
                                                + 2 * cos(6 * phi) * cos(4 * theta)
                                                - 4 * cos(6 * phi) * cos(5 * theta)
                                                + cos(6 * phi) * cos(6 * theta)
                                                + 14 * cos(6 * phi)
                                            )
                                            / (4096 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(2145)
                                            * (
                                                4 * sin(theta)
                                                + 17 * sin(2 * theta)
                                                - 18 * sin(3 * theta)
                                                - 4 * sin(4 * theta)
                                                + 10 * sin(5 * theta)
                                                - 3 * sin(6 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (2048 * sqrt(pi))
                                        )
                                else:
                                    if m <= -4:
                                        return (
                                            sqrt(390)
                                            * (
                                                16 * 1j * sin(4 * phi) * cos(theta)
                                                - 17
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(2 * theta)
                                                + 72
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(3 * theta)
                                                + 26
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(4 * theta)
                                                - 88
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(5 * theta)
                                                + 33
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(6 * theta)
                                                - 42 * 1j * sin(4 * phi)
                                                - 16 * cos(4 * phi) * cos(theta)
                                                + 17 * cos(4 * phi) * cos(2 * theta)
                                                - 72 * cos(4 * phi) * cos(3 * theta)
                                                - 26 * cos(4 * phi) * cos(4 * theta)
                                                + 88 * cos(4 * phi) * cos(5 * theta)
                                                - 33 * cos(4 * phi) * cos(6 * theta)
                                                + 42 * cos(4 * phi)
                                            )
                                            / (4096 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(13)
                                            * (
                                                20 * sin(theta)
                                                + 51 * sin(2 * theta)
                                                + 6 * sin(3 * theta)
                                                + 20 * sin(4 * theta)
                                                - 110 * sin(5 * theta)
                                                + 55 * sin(6 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (2048 * sqrt(pi))
                                        )
                            else:
                                if m <= -1:
                                    if m <= -2:
                                        return (
                                            sqrt(13)
                                            * (
                                                40 * 1j * sin(2 * phi) * cos(theta)
                                                - 289
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(2 * theta)
                                                + 324
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(3 * theta)
                                                - 30
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(4 * theta)
                                                + 660
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(5 * theta)
                                                - 495
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(6 * theta)
                                                - 210 * 1j * sin(2 * phi)
                                                - 40 * cos(2 * phi) * cos(theta)
                                                + 289 * cos(2 * phi) * cos(2 * theta)
                                                - 324 * cos(2 * phi) * cos(3 * theta)
                                                + 30 * cos(2 * phi) * cos(4 * theta)
                                                - 660 * cos(2 * phi) * cos(5 * theta)
                                                + 495 * cos(2 * phi) * cos(6 * theta)
                                                + 210 * cos(2 * phi)
                                            )
                                            / (4096 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(130)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                20 * sin(theta)
                                                + 17 * sin(2 * theta)
                                                + 54 * sin(3 * theta)
                                                + 12 * sin(4 * theta)
                                                + 66 * sin(5 * theta)
                                                - 99 * sin(6 * theta)
                                            )
                                            / (2048 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        sqrt(1365)
                                        * (
                                            17 * cos(2 * theta)
                                            + 6 * cos(4 * theta)
                                            - 33 * cos(6 * theta)
                                            + 10
                                        )
                                        / (2048 * sqrt(pi))
                                    )
                        else:
                            if m <= 3:
                                if m <= 2:
                                    if m <= 1:
                                        return (
                                            sqrt(130)
                                            * (
                                                20 * sin(theta)
                                                - 17 * sin(2 * theta)
                                                + 54 * sin(3 * theta)
                                                - 12 * sin(4 * theta)
                                                + 66 * sin(5 * theta)
                                                + 99 * sin(6 * theta)
                                            )
                                            * exp(1j * phi)
                                            / (2048 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(13)
                                            * (
                                                40 * cos(theta)
                                                + 289 * cos(2 * theta)
                                                + 324 * cos(3 * theta)
                                                + 30 * cos(4 * theta)
                                                + 660 * cos(5 * theta)
                                                + 495 * cos(6 * theta)
                                                + 210
                                            )
                                            * exp(2 * 1j * phi)
                                            / (4096 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        -3
                                        * sqrt(13)
                                        * (
                                            -20 * sin(theta)
                                            + 51 * sin(2 * theta)
                                            - 6 * sin(3 * theta)
                                            + 20 * sin(4 * theta)
                                            + 110 * sin(5 * theta)
                                            + 55 * sin(6 * theta)
                                        )
                                        * exp(3 * 1j * phi)
                                        / (2048 * sqrt(pi))
                                    )
                            else:
                                if m <= 5:
                                    if m <= 4:
                                        return (
                                            sqrt(390)
                                            * (
                                                16 * cos(theta)
                                                + 17 * cos(2 * theta)
                                                + 72 * cos(3 * theta)
                                                - 26 * cos(4 * theta)
                                                - 88 * cos(5 * theta)
                                                - 33 * cos(6 * theta)
                                                + 42
                                            )
                                            * exp(4 * 1j * phi)
                                            / (4096 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(2145)
                                            * (
                                                4 * sin(theta)
                                                - 17 * sin(2 * theta)
                                                - 18 * sin(3 * theta)
                                                + 4 * sin(4 * theta)
                                                + 10 * sin(5 * theta)
                                                + 3 * sin(6 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (2048 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        3
                                        * sqrt(715)
                                        * (
                                            8 * cos(theta)
                                            - 17 * cos(2 * theta)
                                            - 12 * cos(3 * theta)
                                            + 2 * cos(4 * theta)
                                            + 4 * cos(5 * theta)
                                            + cos(6 * theta)
                                            + 14
                                        )
                                        * exp(6 * 1j * phi)
                                        / (4096 * sqrt(pi))
                                    )
                    else:
                        if m <= 0:
                            if m <= -4:
                                if m <= -6:
                                    if m <= -7:
                                        return (
                                            sqrt(30030)
                                            * (
                                                45 * sin(theta)
                                                - 20 * sin(2 * theta)
                                                - 19 * sin(3 * theta)
                                                + 16 * sin(4 * theta)
                                                + sin(5 * theta)
                                                - 4 * sin(6 * theta)
                                                + sin(7 * theta)
                                            )
                                            * exp(-7 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(2145)
                                            * (
                                                45 * cos(theta)
                                                - 40 * cos(2 * theta)
                                                - 57 * cos(3 * theta)
                                                + 64 * cos(4 * theta)
                                                + 5 * cos(5 * theta)
                                                - 24 * cos(6 * theta)
                                                + 7 * cos(7 * theta)
                                            )
                                            * exp(-6 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= -5:
                                        return (
                                            sqrt(330)
                                            * (
                                                225 * sin(theta)
                                                + 20 * sin(2 * theta)
                                                + 209 * sin(3 * theta)
                                                - 400 * sin(4 * theta)
                                                - 43 * sin(5 * theta)
                                                + 260 * sin(6 * theta)
                                                - 91 * sin(7 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(330)
                                            * (
                                                -135 * cos(theta)
                                                + 80 * cos(2 * theta)
                                                + 19 * cos(3 * theta)
                                                + 128 * cos(4 * theta)
                                                + 25 * cos(5 * theta)
                                                - 208 * cos(6 * theta)
                                                + 91 * cos(7 * theta)
                                            )
                                            * exp(-4 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                            else:
                                if m <= -2:
                                    if m <= -3:
                                        return (
                                            sqrt(30)
                                            * (
                                                405 * sin(theta)
                                                + 380 * sin(2 * theta)
                                                + 741 * sin(3 * theta)
                                                - 176 * sin(4 * theta)
                                                + 121 * sin(5 * theta)
                                                - 1716 * sin(6 * theta)
                                                + 1001 * sin(7 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(15)
                                            * (
                                                675 * cos(theta)
                                                - 200 * cos(2 * theta)
                                                + 361 * cos(3 * theta)
                                                - 704 * cos(4 * theta)
                                                + 11 * cos(5 * theta)
                                                - 1144 * cos(6 * theta)
                                                + 1001 * cos(7 * theta)
                                            )
                                            * exp(-2 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        return (
                                            -3
                                            * sqrt(10)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                75 * sin(theta)
                                                + 300 * sin(2 * theta)
                                                + 171 * sin(3 * theta)
                                                + 528 * sin(4 * theta)
                                                + 55 * sin(5 * theta)
                                                + 572 * sin(6 * theta)
                                                - 1001 * sin(7 * theta)
                                            )
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(35)
                                            * (
                                                75 * cos(theta)
                                                + 57 * cos(3 * theta)
                                                + 11 * cos(5 * theta)
                                                - 143 * cos(7 * theta)
                                            )
                                            / (4096 * sqrt(pi))
                                        )
                        else:
                            if m <= 4:
                                if m <= 2:
                                    if m <= 1:
                                        return (
                                            3
                                            * sqrt(10)
                                            * (
                                                -75 * sin(theta)
                                                + 300 * sin(2 * theta)
                                                - 171 * sin(3 * theta)
                                                + 528 * sin(4 * theta)
                                                - 55 * sin(5 * theta)
                                                + 572 * sin(6 * theta)
                                                + 1001 * sin(7 * theta)
                                            )
                                            * exp(1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(15)
                                            * (
                                                675 * cos(theta)
                                                + 200 * cos(2 * theta)
                                                + 361 * cos(3 * theta)
                                                + 704 * cos(4 * theta)
                                                + 11 * cos(5 * theta)
                                                + 1144 * cos(6 * theta)
                                                + 1001 * cos(7 * theta)
                                            )
                                            * exp(2 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= 3:
                                        return (
                                            -sqrt(30)
                                            * (
                                                405 * sin(theta)
                                                - 380 * sin(2 * theta)
                                                + 741 * sin(3 * theta)
                                                + 176 * sin(4 * theta)
                                                + 121 * sin(5 * theta)
                                                + 1716 * sin(6 * theta)
                                                + 1001 * sin(7 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(330)
                                            * (
                                                135 * cos(theta)
                                                + 80 * cos(2 * theta)
                                                - 19 * cos(3 * theta)
                                                + 128 * cos(4 * theta)
                                                - 25 * cos(5 * theta)
                                                - 208 * cos(6 * theta)
                                                - 91 * cos(7 * theta)
                                            )
                                            * exp(4 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                            else:
                                if m <= 6:
                                    if m <= 5:
                                        return (
                                            sqrt(330)
                                            * (
                                                -225 * sin(theta)
                                                + 20 * sin(2 * theta)
                                                - 209 * sin(3 * theta)
                                                - 400 * sin(4 * theta)
                                                + 43 * sin(5 * theta)
                                                + 260 * sin(6 * theta)
                                                + 91 * sin(7 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(2145)
                                            * (
                                                45 * cos(theta)
                                                + 40 * cos(2 * theta)
                                                - 57 * cos(3 * theta)
                                                - 64 * cos(4 * theta)
                                                + 5 * cos(5 * theta)
                                                + 24 * cos(6 * theta)
                                                + 7 * cos(7 * theta)
                                            )
                                            * exp(6 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    return (
                                        -sqrt(30030)
                                        * (
                                            45 * sin(theta)
                                            + 20 * sin(2 * theta)
                                            - 19 * sin(3 * theta)
                                            - 16 * sin(4 * theta)
                                            + sin(5 * theta)
                                            + 4 * sin(6 * theta)
                                            + sin(7 * theta)
                                        )
                                        * exp(7 * 1j * phi)
                                        / (16384 * sqrt(pi))
                                    )
                else:
                    if l <= 8:
                        if m <= 0:
                            if m <= -4:
                                if m <= -6:
                                    if m <= -7:
                                        if m <= -8:
                                            return (
                                                sqrt(34034)
                                                * (
                                                    20 * 1j * sin(8 * phi) * cos(theta)
                                                    + 64
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(2 * theta)
                                                    - 36
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(3 * theta)
                                                    - 20
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(4 * theta)
                                                    + 20
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(5 * theta)
                                                    - 4
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(7 * theta)
                                                    + 1j * sin(8 * phi) * cos(8 * theta)
                                                    - 45 * 1j * sin(8 * phi)
                                                    - 20 * cos(8 * phi) * cos(theta)
                                                    - 64 * cos(8 * phi) * cos(2 * theta)
                                                    + 36 * cos(8 * phi) * cos(3 * theta)
                                                    + 20 * cos(8 * phi) * cos(4 * theta)
                                                    - 20 * cos(8 * phi) * cos(5 * theta)
                                                    + 4 * cos(8 * phi) * cos(7 * theta)
                                                    - cos(8 * phi) * cos(8 * theta)
                                                    + 45 * cos(8 * phi)
                                                )
                                                / (32768 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(34034)
                                                * (
                                                    5 * sin(theta)
                                                    + 32 * sin(2 * theta)
                                                    - 27 * sin(3 * theta)
                                                    - 20 * sin(4 * theta)
                                                    + 25 * sin(5 * theta)
                                                    - 7 * sin(7 * theta)
                                                    + 2 * sin(8 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (16384 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(255255)
                                            * (
                                                1j * sin(6 * phi) * cos(theta)
                                                + 3 * 1j * sin(6 * phi) * cos(3 * theta)
                                                + 4 * 1j * sin(6 * phi) * cos(4 * theta)
                                                - 7 * 1j * sin(6 * phi) * cos(5 * theta)
                                                + 3 * 1j * sin(6 * phi) * cos(7 * theta)
                                                - 1j * sin(6 * phi) * cos(8 * theta)
                                                - 3 * 1j * sin(6 * phi)
                                                - cos(6 * phi) * cos(theta)
                                                - 3 * cos(6 * phi) * cos(3 * theta)
                                                - 4 * cos(6 * phi) * cos(4 * theta)
                                                + 7 * cos(6 * phi) * cos(5 * theta)
                                                - 3 * cos(6 * phi) * cos(7 * theta)
                                                + cos(6 * phi) * cos(8 * theta)
                                                + 3 * cos(6 * phi)
                                            )
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= -5:
                                        return (
                                            sqrt(24310)
                                            * (
                                                7 * sin(theta)
                                                + 32 * sin(2 * theta)
                                                - 9 * sin(3 * theta)
                                                + 12 * sin(4 * theta)
                                                - 45 * sin(5 * theta)
                                                + 35 * sin(7 * theta)
                                                - 14 * sin(8 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(1870)
                                            * (
                                                14 * 1j * sin(4 * phi) * cos(theta)
                                                - 64
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(2 * theta)
                                                + 90
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(3 * theta)
                                                + 36
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(4 * theta)
                                                + 78
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(5 * theta)
                                                - 182
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(7 * theta)
                                                + 91
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(8 * theta)
                                                - 63 * 1j * sin(4 * phi)
                                                - 14 * cos(4 * phi) * cos(theta)
                                                + 64 * cos(4 * phi) * cos(2 * theta)
                                                - 90 * cos(4 * phi) * cos(3 * theta)
                                                - 36 * cos(4 * phi) * cos(4 * theta)
                                                - 78 * cos(4 * phi) * cos(5 * theta)
                                                + 182 * cos(4 * phi) * cos(7 * theta)
                                                - 91 * cos(4 * phi) * cos(8 * theta)
                                                + 63 * cos(4 * phi)
                                            )
                                            / (16384 * sqrt(pi))
                                        )
                            else:
                                if m <= -2:
                                    if m <= -3:
                                        return (
                                            sqrt(1122)
                                            * (
                                                35 * sin(theta)
                                                + 96 * sin(2 * theta)
                                                + 51 * sin(3 * theta)
                                                + 100 * sin(4 * theta)
                                                - 65 * sin(5 * theta)
                                                - 273 * sin(7 * theta)
                                                + 182 * sin(8 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(17)
                                            * (
                                                35 * 1j * sin(2 * phi) * cos(theta)
                                                - 512
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(2 * theta)
                                                + 297
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(3 * theta)
                                                - 220
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(4 * theta)
                                                + 715
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(5 * theta)
                                                + 1001
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(7 * theta)
                                                - 1001
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(8 * theta)
                                                - 315 * 1j * sin(2 * phi)
                                                - 35 * cos(2 * phi) * cos(theta)
                                                + 512 * cos(2 * phi) * cos(2 * theta)
                                                - 297 * cos(2 * phi) * cos(3 * theta)
                                                + 220 * cos(2 * phi) * cos(4 * theta)
                                                - 715 * cos(2 * phi) * cos(5 * theta)
                                                - 1001 * cos(2 * phi) * cos(7 * theta)
                                                + 1001 * cos(2 * phi) * cos(8 * theta)
                                                + 315 * cos(2 * phi)
                                            )
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        return (
                                            -sqrt(1190)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                35 * sin(theta)
                                                + 32 * sin(2 * theta)
                                                + 99 * sin(3 * theta)
                                                + 44 * sin(4 * theta)
                                                + 143 * sin(5 * theta)
                                                + 143 * sin(7 * theta)
                                                - 286 * sin(8 * theta)
                                            )
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(595)
                                            * (
                                                64 * cos(2 * theta)
                                                + 44 * cos(4 * theta)
                                                - 143 * cos(8 * theta)
                                                + 35
                                            )
                                            / (16384 * sqrt(pi))
                                        )
                        else:
                            if m <= 4:
                                if m <= 2:
                                    if m <= 1:
                                        return (
                                            sqrt(1190)
                                            * (
                                                35 * sin(theta)
                                                - 32 * sin(2 * theta)
                                                + 99 * sin(3 * theta)
                                                - 44 * sin(4 * theta)
                                                + 143 * sin(5 * theta)
                                                + 143 * sin(7 * theta)
                                                + 286 * sin(8 * theta)
                                            )
                                            * exp(1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(17)
                                            * (
                                                35 * cos(theta)
                                                + 512 * cos(2 * theta)
                                                + 297 * cos(3 * theta)
                                                + 220 * cos(4 * theta)
                                                + 715 * cos(5 * theta)
                                                + 1001 * cos(7 * theta)
                                                + 1001 * cos(8 * theta)
                                                + 315
                                            )
                                            * exp(2 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= 3:
                                        return (
                                            -sqrt(1122)
                                            * (
                                                -35 * sin(theta)
                                                + 96 * sin(2 * theta)
                                                - 51 * sin(3 * theta)
                                                + 100 * sin(4 * theta)
                                                + 65 * sin(5 * theta)
                                                + 273 * sin(7 * theta)
                                                + 182 * sin(8 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(1870)
                                            * (
                                                14 * cos(theta)
                                                + 64 * cos(2 * theta)
                                                + 90 * cos(3 * theta)
                                                - 36 * cos(4 * theta)
                                                + 78 * cos(5 * theta)
                                                - 182 * cos(7 * theta)
                                                - 91 * cos(8 * theta)
                                                + 63
                                            )
                                            * exp(4 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                            else:
                                if m <= 6:
                                    if m <= 5:
                                        return (
                                            -sqrt(24310)
                                            * (
                                                -7 * sin(theta)
                                                + 32 * sin(2 * theta)
                                                + 9 * sin(3 * theta)
                                                + 12 * sin(4 * theta)
                                                + 45 * sin(5 * theta)
                                                - 35 * sin(7 * theta)
                                                - 14 * sin(8 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(255255)
                                            * (
                                                cos(theta)
                                                + 3 * cos(3 * theta)
                                                - 4 * cos(4 * theta)
                                                - 7 * cos(5 * theta)
                                                + 3 * cos(7 * theta)
                                                + cos(8 * theta)
                                                + 3
                                            )
                                            * exp(6 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                                else:
                                    if m <= 7:
                                        return (
                                            -sqrt(34034)
                                            * (
                                                -5 * sin(theta)
                                                + 32 * sin(2 * theta)
                                                + 27 * sin(3 * theta)
                                                - 20 * sin(4 * theta)
                                                - 25 * sin(5 * theta)
                                                + 7 * sin(7 * theta)
                                                + 2 * sin(8 * theta)
                                            )
                                            * exp(7 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(34034)
                                            * (
                                                -32 * sin(theta) ** 8
                                                + 64 * sin(theta) ** 6
                                                + 5 * cos(theta)
                                                - 9 * cos(3 * theta)
                                                + 5 * cos(5 * theta)
                                                - cos(7 * theta)
                                            )
                                            * exp(8 * 1j * phi)
                                            / (8192 * sqrt(pi))
                                        )
                    else:
                        if m <= 0:
                            if m <= -5:
                                if m <= -7:
                                    if m <= -8:
                                        if m <= -9:
                                            return (
                                                3
                                                * sqrt(4199)
                                                * (
                                                    154 * sin(theta)
                                                    - 56 * sin(2 * theta)
                                                    - 84 * sin(3 * theta)
                                                    + 56 * sin(4 * theta)
                                                    + 20 * sin(5 * theta)
                                                    - 24 * sin(6 * theta)
                                                    + sin(7 * theta)
                                                    + 4 * sin(8 * theta)
                                                    - sin(9 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (65536 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(8398)
                                                * (
                                                    154 * cos(theta)
                                                    - 112 * cos(2 * theta)
                                                    - 252 * cos(3 * theta)
                                                    + 224 * cos(4 * theta)
                                                    + 100 * cos(5 * theta)
                                                    - 144 * cos(6 * theta)
                                                    + 7 * cos(7 * theta)
                                                    + 32 * cos(8 * theta)
                                                    - 9 * cos(9 * theta)
                                                )
                                                * exp(-8 * 1j * phi)
                                                / (65536 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(247)
                                            * (
                                                1078 * sin(theta)
                                                - 56 * sin(2 * theta)
                                                + 756 * sin(3 * theta)
                                                - 1288 * sin(4 * theta)
                                                - 820 * sin(5 * theta)
                                                + 1512 * sin(6 * theta)
                                                - 89 * sin(7 * theta)
                                                - 476 * sin(8 * theta)
                                                + 153 * sin(9 * theta)
                                            )
                                            * exp(-7 * 1j * phi)
                                            / (65536 * sqrt(pi))
                                        )
                                else:
                                    if m <= -6:
                                        return (
                                            -sqrt(741)
                                            * (
                                                -154 * cos(theta)
                                                + 84 * cos(2 * theta)
                                                + 84 * cos(3 * theta)
                                                + 56 * cos(4 * theta)
                                                + 100 * cos(5 * theta)
                                                - 276 * cos(6 * theta)
                                                + 21 * cos(7 * theta)
                                                + 136 * cos(8 * theta)
                                                - 51 * cos(9 * theta)
                                            )
                                            * exp(-6 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(1235)
                                            * (
                                                154 * sin(theta)
                                                + 56 * sin(2 * theta)
                                                + 252 * sin(3 * theta)
                                                - 168 * sin(4 * theta)
                                                + 36 * sin(5 * theta)
                                                - 360 * sin(6 * theta)
                                                + 41 * sin(7 * theta)
                                                + 340 * sin(8 * theta)
                                                - 153 * sin(9 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (32768 * sqrt(pi))
                                        )
                            else:
                                if m <= -2:
                                    if m <= -3:
                                        if m <= -4:
                                            return (
                                                -sqrt(3458)
                                                * (
                                                    -154 * cos(theta)
                                                    + 56 * cos(2 * theta)
                                                    - 36 * cos(3 * theta)
                                                    + 144 * cos(4 * theta)
                                                    + 60 * cos(5 * theta)
                                                    + 72 * cos(6 * theta)
                                                    - 23 * cos(7 * theta)
                                                    - 272 * cos(8 * theta)
                                                    + 153 * cos(9 * theta)
                                                )
                                                * exp(-4 * 1j * phi)
                                                / (32768 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(399)
                                                * (
                                                    154 * sin(theta)
                                                    + 168 * sin(2 * theta)
                                                    + 348 * sin(3 * theta)
                                                    + 104 * sin(4 * theta)
                                                    + 260 * sin(5 * theta)
                                                    - 312 * sin(6 * theta)
                                                    - 39 * sin(7 * theta)
                                                    - 884 * sin(8 * theta)
                                                    + 663 * sin(9 * theta)
                                                )
                                                * exp(-3 * 1j * phi)
                                                / (32768 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(19)
                                            * (
                                                1078 * cos(theta)
                                                - 196 * cos(2 * theta)
                                                + 756 * cos(3 * theta)
                                                - 728 * cos(4 * theta)
                                                + 260 * cos(5 * theta)
                                                - 1404 * cos(6 * theta)
                                                + 13 * cos(7 * theta)
                                                - 1768 * cos(8 * theta)
                                                + 1989 * cos(9 * theta)
                                            )
                                            * exp(-2 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        return (
                                            -sqrt(418)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                98 * sin(theta)
                                                + 392 * sin(2 * theta)
                                                + 252 * sin(3 * theta)
                                                + 728 * sin(4 * theta)
                                                + 260 * sin(5 * theta)
                                                + 936 * sin(6 * theta)
                                                - 91 * sin(7 * theta)
                                                + 884 * sin(8 * theta)
                                                - 1989 * sin(9 * theta)
                                            )
                                            / (65536 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(1045)
                                            * (
                                                98 * cos(theta)
                                                + 84 * cos(3 * theta)
                                                + 52 * cos(5 * theta)
                                                - 13 * cos(7 * theta)
                                                - 221 * cos(9 * theta)
                                            )
                                            / (32768 * sqrt(pi))
                                        )
                        else:
                            if m <= 5:
                                if m <= 3:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                sqrt(418)
                                                * (
                                                    -98 * sin(theta)
                                                    + 392 * sin(2 * theta)
                                                    - 252 * sin(3 * theta)
                                                    + 728 * sin(4 * theta)
                                                    - 260 * sin(5 * theta)
                                                    + 936 * sin(6 * theta)
                                                    + 91 * sin(7 * theta)
                                                    + 884 * sin(8 * theta)
                                                    + 1989 * sin(9 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (65536 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(19)
                                                * (
                                                    1078 * cos(theta)
                                                    + 196 * cos(2 * theta)
                                                    + 756 * cos(3 * theta)
                                                    + 728 * cos(4 * theta)
                                                    + 260 * cos(5 * theta)
                                                    + 1404 * cos(6 * theta)
                                                    + 13 * cos(7 * theta)
                                                    + 1768 * cos(8 * theta)
                                                    + 1989 * cos(9 * theta)
                                                )
                                                * exp(2 * 1j * phi)
                                                / (16384 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -sqrt(399)
                                            * (
                                                154 * sin(theta)
                                                - 168 * sin(2 * theta)
                                                + 348 * sin(3 * theta)
                                                - 104 * sin(4 * theta)
                                                + 260 * sin(5 * theta)
                                                + 312 * sin(6 * theta)
                                                - 39 * sin(7 * theta)
                                                + 884 * sin(8 * theta)
                                                + 663 * sin(9 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (32768 * sqrt(pi))
                                        )
                                else:
                                    if m <= 4:
                                        return (
                                            sqrt(3458)
                                            * (
                                                154 * cos(theta)
                                                + 56 * cos(2 * theta)
                                                + 36 * cos(3 * theta)
                                                + 144 * cos(4 * theta)
                                                - 60 * cos(5 * theta)
                                                + 72 * cos(6 * theta)
                                                + 23 * cos(7 * theta)
                                                - 272 * cos(8 * theta)
                                                - 153 * cos(9 * theta)
                                            )
                                            * exp(4 * 1j * phi)
                                            / (32768 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(1235)
                                            * (
                                                154 * sin(theta)
                                                - 56 * sin(2 * theta)
                                                + 252 * sin(3 * theta)
                                                + 168 * sin(4 * theta)
                                                + 36 * sin(5 * theta)
                                                + 360 * sin(6 * theta)
                                                + 41 * sin(7 * theta)
                                                - 340 * sin(8 * theta)
                                                - 153 * sin(9 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (32768 * sqrt(pi))
                                        )
                            else:
                                if m <= 7:
                                    if m <= 6:
                                        return (
                                            sqrt(741)
                                            * (
                                                154 * cos(theta)
                                                + 84 * cos(2 * theta)
                                                - 84 * cos(3 * theta)
                                                + 56 * cos(4 * theta)
                                                - 100 * cos(5 * theta)
                                                - 276 * cos(6 * theta)
                                                - 21 * cos(7 * theta)
                                                + 136 * cos(8 * theta)
                                                + 51 * cos(9 * theta)
                                            )
                                            * exp(6 * 1j * phi)
                                            / (16384 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(247)
                                            * (
                                                1078 * sin(theta)
                                                + 56 * sin(2 * theta)
                                                + 756 * sin(3 * theta)
                                                + 1288 * sin(4 * theta)
                                                - 820 * sin(5 * theta)
                                                - 1512 * sin(6 * theta)
                                                - 89 * sin(7 * theta)
                                                + 476 * sin(8 * theta)
                                                + 153 * sin(9 * theta)
                                            )
                                            * exp(7 * 1j * phi)
                                            / (65536 * sqrt(pi))
                                        )
                                else:
                                    if m <= 8:
                                        return (
                                            sqrt(8398)
                                            * (
                                                154 * cos(theta)
                                                + 112 * cos(2 * theta)
                                                - 252 * cos(3 * theta)
                                                - 224 * cos(4 * theta)
                                                + 100 * cos(5 * theta)
                                                + 144 * cos(6 * theta)
                                                + 7 * cos(7 * theta)
                                                - 32 * cos(8 * theta)
                                                - 9 * cos(9 * theta)
                                            )
                                            * exp(8 * 1j * phi)
                                            / (65536 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -3
                                            * sqrt(4199)
                                            * (
                                                154 * sin(theta)
                                                + 56 * sin(2 * theta)
                                                - 84 * sin(3 * theta)
                                                - 56 * sin(4 * theta)
                                                + 20 * sin(5 * theta)
                                                + 24 * sin(6 * theta)
                                                + sin(7 * theta)
                                                - 4 * sin(8 * theta)
                                                - sin(9 * theta)
                                            )
                                            * exp(9 * 1j * phi)
                                            / (65536 * sqrt(pi))
                                        )
        else:
            if l <= 13:
                if l <= 11:
                    if l <= 10:
                        if m <= 0:
                            if m <= -5:
                                if m <= -8:
                                    if m <= -9:
                                        if m <= -10:
                                            return (
                                                3
                                                * sqrt(293930)
                                                * (
                                                    56 * 1j * sin(10 * phi) * cos(theta)
                                                    + 238
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(2 * theta)
                                                    - 112
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(3 * theta)
                                                    - 104
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(4 * theta)
                                                    + 80
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(5 * theta)
                                                    + 19
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(6 * theta)
                                                    - 28
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(7 * theta)
                                                    + 2
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(8 * theta)
                                                    + 4
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(9 * theta)
                                                    - 1j
                                                    * sin(10 * phi)
                                                    * cos(10 * theta)
                                                    - 154 * 1j * sin(10 * phi)
                                                    - 56 * cos(10 * phi) * cos(theta)
                                                    - 238
                                                    * cos(10 * phi)
                                                    * cos(2 * theta)
                                                    + 112
                                                    * cos(10 * phi)
                                                    * cos(3 * theta)
                                                    + 104
                                                    * cos(10 * phi)
                                                    * cos(4 * theta)
                                                    - 80
                                                    * cos(10 * phi)
                                                    * cos(5 * theta)
                                                    - 19
                                                    * cos(10 * phi)
                                                    * cos(6 * theta)
                                                    + 28
                                                    * cos(10 * phi)
                                                    * cos(7 * theta)
                                                    - 2 * cos(10 * phi) * cos(8 * theta)
                                                    - 4 * cos(10 * phi) * cos(9 * theta)
                                                    + cos(10 * phi) * cos(10 * theta)
                                                    + 154 * cos(10 * phi)
                                                )
                                                / (1048576 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(58786)
                                                * (
                                                    28 * sin(theta)
                                                    + 238 * sin(2 * theta)
                                                    - 168 * sin(3 * theta)
                                                    - 208 * sin(4 * theta)
                                                    + 200 * sin(5 * theta)
                                                    + 57 * sin(6 * theta)
                                                    - 98 * sin(7 * theta)
                                                    + 8 * sin(8 * theta)
                                                    + 18 * sin(9 * theta)
                                                    - 5 * sin(10 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(1547)
                                            * (
                                                224 * 1j * sin(8 * phi) * cos(theta)
                                                + 238
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(2 * theta)
                                                + 448
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(3 * theta)
                                                + 1144
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(4 * theta)
                                                - 1600
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(5 * theta)
                                                - 589
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(6 * theta)
                                                + 1232
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(7 * theta)
                                                - 118
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(8 * theta)
                                                - 304
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(9 * theta)
                                                + 95
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(10 * theta)
                                                - 770 * 1j * sin(8 * phi)
                                                - 224 * cos(8 * phi) * cos(theta)
                                                - 238 * cos(8 * phi) * cos(2 * theta)
                                                - 448 * cos(8 * phi) * cos(3 * theta)
                                                - 1144 * cos(8 * phi) * cos(4 * theta)
                                                + 1600 * cos(8 * phi) * cos(5 * theta)
                                                + 589 * cos(8 * phi) * cos(6 * theta)
                                                - 1232 * cos(8 * phi) * cos(7 * theta)
                                                + 118 * cos(8 * phi) * cos(8 * theta)
                                                + 304 * cos(8 * phi) * cos(9 * theta)
                                                - 95 * cos(8 * phi) * cos(10 * theta)
                                                + 770 * cos(8 * phi)
                                            )
                                            / (524288 * sqrt(pi))
                                        )
                                else:
                                    if m <= -6:
                                        if m <= -7:
                                            return (
                                                sqrt(9282)
                                                * (
                                                    252 * sin(theta)
                                                    + 1666 * sin(2 * theta)
                                                    - 616 * sin(3 * theta)
                                                    + 208 * sin(4 * theta)
                                                    - 1400 * sin(5 * theta)
                                                    - 817 * sin(6 * theta)
                                                    + 2254 * sin(7 * theta)
                                                    - 264 * sin(8 * theta)
                                                    - 798 * sin(9 * theta)
                                                    + 285 * sin(10 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(546)
                                                * (
                                                    1512
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(theta)
                                                    - 4522
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(2 * theta)
                                                    + 7728
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(3 * theta)
                                                    + 8632
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(4 * theta)
                                                    - 400
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(5 * theta)
                                                    + 4503
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(6 * theta)
                                                    - 20468
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(7 * theta)
                                                    + 3162
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(8 * theta)
                                                    + 11628
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(9 * theta)
                                                    - 4845
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(10 * theta)
                                                    - 6930 * 1j * sin(6 * phi)
                                                    - 1512 * cos(6 * phi) * cos(theta)
                                                    + 4522
                                                    * cos(6 * phi)
                                                    * cos(2 * theta)
                                                    - 7728
                                                    * cos(6 * phi)
                                                    * cos(3 * theta)
                                                    - 8632
                                                    * cos(6 * phi)
                                                    * cos(4 * theta)
                                                    + 400
                                                    * cos(6 * phi)
                                                    * cos(5 * theta)
                                                    - 4503
                                                    * cos(6 * phi)
                                                    * cos(6 * theta)
                                                    + 20468
                                                    * cos(6 * phi)
                                                    * cos(7 * theta)
                                                    - 3162
                                                    * cos(6 * phi)
                                                    * cos(8 * theta)
                                                    - 11628
                                                    * cos(6 * phi)
                                                    * cos(9 * theta)
                                                    + 4845
                                                    * cos(6 * phi)
                                                    * cos(10 * theta)
                                                    + 6930 * cos(6 * phi)
                                                )
                                                / (1048576 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(2730)
                                            * (
                                                252 * sin(theta)
                                                + 1190 * sin(2 * theta)
                                                + 56 * sin(3 * theta)
                                                + 1040 * sin(4 * theta)
                                                - 1240 * sin(5 * theta)
                                                - 19 * sin(6 * theta)
                                                - 1666 * sin(7 * theta)
                                                + 408 * sin(8 * theta)
                                                + 1938 * sin(9 * theta)
                                                - 969 * sin(10 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (262144 * sqrt(pi))
                                        )
                            else:
                                if m <= -2:
                                    if m <= -3:
                                        if m <= -4:
                                            return (
                                                sqrt(273)
                                                * (
                                                    336 * 1j * sin(4 * phi) * cos(theta)
                                                    - 3094
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(2 * theta)
                                                    + 2464
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(3 * theta)
                                                    + 104
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(4 * theta)
                                                    + 4000
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(5 * theta)
                                                    + 1577
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(6 * theta)
                                                    + 952
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(7 * theta)
                                                    - 1122
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(8 * theta)
                                                    - 7752
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(9 * theta)
                                                    + 4845
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(10 * theta)
                                                    - 2310 * 1j * sin(4 * phi)
                                                    - 336 * cos(4 * phi) * cos(theta)
                                                    + 3094
                                                    * cos(4 * phi)
                                                    * cos(2 * theta)
                                                    - 2464
                                                    * cos(4 * phi)
                                                    * cos(3 * theta)
                                                    - 104
                                                    * cos(4 * phi)
                                                    * cos(4 * theta)
                                                    - 4000
                                                    * cos(4 * phi)
                                                    * cos(5 * theta)
                                                    - 1577
                                                    * cos(4 * phi)
                                                    * cos(6 * theta)
                                                    - 952
                                                    * cos(4 * phi)
                                                    * cos(7 * theta)
                                                    + 1122
                                                    * cos(4 * phi)
                                                    * cos(8 * theta)
                                                    + 7752
                                                    * cos(4 * phi)
                                                    * cos(9 * theta)
                                                    - 4845
                                                    * cos(4 * phi)
                                                    * cos(10 * theta)
                                                    + 2310 * cos(4 * phi)
                                                )
                                                / (262144 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(546)
                                                * (
                                                    588 * sin(theta)
                                                    + 1666 * sin(2 * theta)
                                                    + 1176 * sin(3 * theta)
                                                    + 2288 * sin(4 * theta)
                                                    + 200 * sin(5 * theta)
                                                    + 1311 * sin(6 * theta)
                                                    - 2618 * sin(7 * theta)
                                                    - 408 * sin(8 * theta)
                                                    - 5814 * sin(9 * theta)
                                                    + 4845 * sin(10 * theta)
                                                )
                                                * exp(-3 * 1j * phi)
                                                / (262144 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(21)
                                            * (
                                                1176 * 1j * sin(2 * phi) * cos(theta)
                                                - 28322
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(2 * theta)
                                                + 10192
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(3 * theta)
                                                - 17576
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(4 * theta)
                                                + 26000
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(5 * theta)
                                                - 4693
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(6 * theta)
                                                + 43316
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(7 * theta)
                                                - 1326
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(8 * theta)
                                                + 50388
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(9 * theta)
                                                - 62985
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(10 * theta)
                                                - 16170 * 1j * sin(2 * phi)
                                                - 1176 * cos(2 * phi) * cos(theta)
                                                + 28322 * cos(2 * phi) * cos(2 * theta)
                                                - 10192 * cos(2 * phi) * cos(3 * theta)
                                                + 17576 * cos(2 * phi) * cos(4 * theta)
                                                - 26000 * cos(2 * phi) * cos(5 * theta)
                                                + 4693 * cos(2 * phi) * cos(6 * theta)
                                                - 43316 * cos(2 * phi) * cos(7 * theta)
                                                + 1326 * cos(2 * phi) * cos(8 * theta)
                                                - 50388 * cos(2 * phi) * cos(9 * theta)
                                                + 62985 * cos(2 * phi) * cos(10 * theta)
                                                + 16170 * cos(2 * phi)
                                            )
                                            / (524288 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        return (
                                            -3
                                            * sqrt(7)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                1764 * sin(theta)
                                                + 1666 * sin(2 * theta)
                                                + 5096 * sin(3 * theta)
                                                + 2704 * sin(4 * theta)
                                                + 7800 * sin(5 * theta)
                                                + 2223 * sin(6 * theta)
                                                + 9282 * sin(7 * theta)
                                                - 1768 * sin(8 * theta)
                                                + 8398 * sin(9 * theta)
                                                - 20995 * sin(10 * theta)
                                            )
                                            / (262144 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(770)
                                            * (
                                                1666 * cos(2 * theta)
                                                + 1352 * cos(4 * theta)
                                                + 741 * cos(6 * theta)
                                                - 442 * cos(8 * theta)
                                                - 4199 * cos(10 * theta)
                                                + 882
                                            )
                                            / (524288 * sqrt(pi))
                                        )
                        else:
                            if m <= 5:
                                if m <= 3:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                3
                                                * sqrt(7)
                                                * (
                                                    1764 * sin(theta)
                                                    - 1666 * sin(2 * theta)
                                                    + 5096 * sin(3 * theta)
                                                    - 2704 * sin(4 * theta)
                                                    + 7800 * sin(5 * theta)
                                                    - 2223 * sin(6 * theta)
                                                    + 9282 * sin(7 * theta)
                                                    + 1768 * sin(8 * theta)
                                                    + 8398 * sin(9 * theta)
                                                    + 20995 * sin(10 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (262144 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(21)
                                                * (
                                                    1176 * cos(theta)
                                                    + 28322 * cos(2 * theta)
                                                    + 10192 * cos(3 * theta)
                                                    + 17576 * cos(4 * theta)
                                                    + 26000 * cos(5 * theta)
                                                    + 4693 * cos(6 * theta)
                                                    + 43316 * cos(7 * theta)
                                                    + 1326 * cos(8 * theta)
                                                    + 50388 * cos(9 * theta)
                                                    + 62985 * cos(10 * theta)
                                                    + 16170
                                                )
                                                * exp(2 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -sqrt(546)
                                            * (
                                                -588 * sin(theta)
                                                + 1666 * sin(2 * theta)
                                                - 1176 * sin(3 * theta)
                                                + 2288 * sin(4 * theta)
                                                - 200 * sin(5 * theta)
                                                + 1311 * sin(6 * theta)
                                                + 2618 * sin(7 * theta)
                                                - 408 * sin(8 * theta)
                                                + 5814 * sin(9 * theta)
                                                + 4845 * sin(10 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (262144 * sqrt(pi))
                                        )
                                else:
                                    if m <= 4:
                                        return (
                                            sqrt(273)
                                            * (
                                                336 * cos(theta)
                                                + 3094 * cos(2 * theta)
                                                + 2464 * cos(3 * theta)
                                                - 104 * cos(4 * theta)
                                                + 4000 * cos(5 * theta)
                                                - 1577 * cos(6 * theta)
                                                + 952 * cos(7 * theta)
                                                + 1122 * cos(8 * theta)
                                                - 7752 * cos(9 * theta)
                                                - 4845 * cos(10 * theta)
                                                + 2310
                                            )
                                            * exp(4 * 1j * phi)
                                            / (262144 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(2730)
                                            * (
                                                252 * sin(theta)
                                                - 1190 * sin(2 * theta)
                                                + 56 * sin(3 * theta)
                                                - 1040 * sin(4 * theta)
                                                - 1240 * sin(5 * theta)
                                                + 19 * sin(6 * theta)
                                                - 1666 * sin(7 * theta)
                                                - 408 * sin(8 * theta)
                                                + 1938 * sin(9 * theta)
                                                + 969 * sin(10 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (262144 * sqrt(pi))
                                        )
                            else:
                                if m <= 8:
                                    if m <= 7:
                                        if m <= 6:
                                            return (
                                                sqrt(546)
                                                * (
                                                    1512 * cos(theta)
                                                    + 4522 * cos(2 * theta)
                                                    + 7728 * cos(3 * theta)
                                                    - 8632 * cos(4 * theta)
                                                    - 400 * cos(5 * theta)
                                                    - 4503 * cos(6 * theta)
                                                    - 20468 * cos(7 * theta)
                                                    - 3162 * cos(8 * theta)
                                                    + 11628 * cos(9 * theta)
                                                    + 4845 * cos(10 * theta)
                                                    + 6930
                                                )
                                                * exp(6 * 1j * phi)
                                                / (1048576 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(9282)
                                                * (
                                                    -252 * sin(theta)
                                                    + 1666 * sin(2 * theta)
                                                    + 616 * sin(3 * theta)
                                                    + 208 * sin(4 * theta)
                                                    + 1400 * sin(5 * theta)
                                                    - 817 * sin(6 * theta)
                                                    - 2254 * sin(7 * theta)
                                                    - 264 * sin(8 * theta)
                                                    + 798 * sin(9 * theta)
                                                    + 285 * sin(10 * theta)
                                                )
                                                * exp(7 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(1547)
                                            * (
                                                224 * cos(theta)
                                                - 238 * cos(2 * theta)
                                                + 448 * cos(3 * theta)
                                                - 1144 * cos(4 * theta)
                                                - 1600 * cos(5 * theta)
                                                + 589 * cos(6 * theta)
                                                + 1232 * cos(7 * theta)
                                                + 118 * cos(8 * theta)
                                                - 304 * cos(9 * theta)
                                                - 95 * cos(10 * theta)
                                                + 770
                                            )
                                            * exp(8 * 1j * phi)
                                            / (524288 * sqrt(pi))
                                        )
                                else:
                                    if m <= 9:
                                        return (
                                            3
                                            * sqrt(58786)
                                            * (
                                                28 * sin(theta)
                                                - 238 * sin(2 * theta)
                                                - 168 * sin(3 * theta)
                                                + 208 * sin(4 * theta)
                                                + 200 * sin(5 * theta)
                                                - 57 * sin(6 * theta)
                                                - 98 * sin(7 * theta)
                                                - 8 * sin(8 * theta)
                                                + 18 * sin(9 * theta)
                                                + 5 * sin(10 * theta)
                                            )
                                            * exp(9 * 1j * phi)
                                            / (524288 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(293930)
                                            * (
                                                56 * cos(theta)
                                                - 238 * cos(2 * theta)
                                                - 112 * cos(3 * theta)
                                                + 104 * cos(4 * theta)
                                                + 80 * cos(5 * theta)
                                                - 19 * cos(6 * theta)
                                                - 28 * cos(7 * theta)
                                                - 2 * cos(8 * theta)
                                                + 4 * cos(9 * theta)
                                                + cos(10 * theta)
                                                + 154
                                            )
                                            * exp(10 * 1j * phi)
                                            / (1048576 * sqrt(pi))
                                        )
                    else:
                        if m <= 0:
                            if m <= -6:
                                if m <= -9:
                                    if m <= -10:
                                        if m <= -11:
                                            return (
                                                sqrt(2860165)
                                                * (
                                                    546 * sin(theta)
                                                    - 168 * sin(2 * theta)
                                                    - 342 * sin(3 * theta)
                                                    + 192 * sin(4 * theta)
                                                    + 123 * sin(5 * theta)
                                                    - 108 * sin(6 * theta)
                                                    - 17 * sin(7 * theta)
                                                    + 32 * sin(8 * theta)
                                                    - 3 * sin(9 * theta)
                                                    - 4 * sin(10 * theta)
                                                    + sin(11 * theta)
                                                )
                                                * exp(-11 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(520030)
                                                * (
                                                    -546 * cos(theta)
                                                    + 336 * cos(2 * theta)
                                                    + 1026 * cos(3 * theta)
                                                    - 768 * cos(4 * theta)
                                                    - 615 * cos(5 * theta)
                                                    + 648 * cos(6 * theta)
                                                    + 119 * cos(7 * theta)
                                                    - 256 * cos(8 * theta)
                                                    + 27 * cos(9 * theta)
                                                    + 40 * cos(10 * theta)
                                                    - 11 * cos(11 * theta)
                                                )
                                                * exp(-10 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(111435)
                                            * (
                                                1638 * sin(theta)
                                                - 168 * sin(2 * theta)
                                                + 798 * sin(3 * theta)
                                                - 1344 * sin(4 * theta)
                                                - 1599 * sin(5 * theta)
                                                + 2196 * sin(6 * theta)
                                                + 493 * sin(7 * theta)
                                                - 1248 * sin(8 * theta)
                                                + 151 * sin(9 * theta)
                                                + 252 * sin(10 * theta)
                                                - 77 * sin(11 * theta)
                                            )
                                            * exp(-9 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= -7:
                                        if m <= -8:
                                            return (
                                                sqrt(7429)
                                                * (
                                                    2730 * cos(theta)
                                                    - 1344 * cos(2 * theta)
                                                    - 2394 * cos(3 * theta)
                                                    - 1845 * cos(5 * theta)
                                                    + 4320 * cos(6 * theta)
                                                    + 1309 * cos(7 * theta)
                                                    - 4096 * cos(8 * theta)
                                                    + 585 * cos(9 * theta)
                                                    + 1120 * cos(10 * theta)
                                                    - 385 * cos(11 * theta)
                                                )
                                                * exp(-8 * 1j * phi)
                                                / (1048576 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(391)
                                                * (
                                                    19110 * sin(theta)
                                                    + 2856 * sin(2 * theta)
                                                    + 26334 * sin(3 * theta)
                                                    - 20160 * sin(4 * theta)
                                                    - 5535 * sin(5 * theta)
                                                    - 18900 * sin(6 * theta)
                                                    - 10931 * sin(7 * theta)
                                                    + 46816 * sin(8 * theta)
                                                    - 8265 * sin(9 * theta)
                                                    - 18620 * sin(10 * theta)
                                                    + 7315 * sin(11 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -3
                                            * sqrt(3910)
                                            * (
                                                -2730 * cos(theta)
                                                + 1008 * cos(2 * theta)
                                                + 266 * cos(3 * theta)
                                                + 1792 * cos(4 * theta)
                                                + 2173 * cos(5 * theta)
                                                - 1128 * cos(6 * theta)
                                                + 595 * cos(7 * theta)
                                                - 4864 * cos(8 * theta)
                                                + 1159 * cos(9 * theta)
                                                + 3192 * cos(10 * theta)
                                                - 1463 * cos(11 * theta)
                                            )
                                            * exp(-6 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                            else:
                                if m <= -3:
                                    if m <= -4:
                                        if m <= -5:
                                            return (
                                                sqrt(345)
                                                * (
                                                    13650 * sin(theta)
                                                    + 6888 * sin(2 * theta)
                                                    + 27930 * sin(3 * theta)
                                                    - 5824 * sin(4 * theta)
                                                    + 16195 * sin(5 * theta)
                                                    - 32436 * sin(6 * theta)
                                                    - 2601 * sin(7 * theta)
                                                    - 31008 * sin(8 * theta)
                                                    + 12597 * sin(9 * theta)
                                                    + 45220 * sin(10 * theta)
                                                    - 24871 * sin(11 * theta)
                                                )
                                                * exp(-5 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(2415)
                                                * (
                                                    -2730 * cos(theta)
                                                    + 672 * cos(2 * theta)
                                                    - 1254 * cos(3 * theta)
                                                    + 2048 * cos(4 * theta)
                                                    + 533 * cos(5 * theta)
                                                    + 2448 * cos(6 * theta)
                                                    + 867 * cos(7 * theta)
                                                    - 969 * cos(9 * theta)
                                                    - 5168 * cos(10 * theta)
                                                    + 3553 * cos(11 * theta)
                                                )
                                                * exp(-4 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(322)
                                            * (
                                                2730 * sin(theta)
                                                + 3192 * sin(2 * theta)
                                                + 6802 * sin(3 * theta)
                                                + 3520 * sin(4 * theta)
                                                + 7175 * sin(5 * theta)
                                                - 1020 * sin(6 * theta)
                                                + 3179 * sin(7 * theta)
                                                - 10336 * sin(8 * theta)
                                                - 1615 * sin(9 * theta)
                                                - 19380 * sin(10 * theta)
                                                + 17765 * sin(11 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        if m <= -2:
                                            return (
                                                sqrt(23)
                                                * (
                                                    57330 * cos(theta)
                                                    - 7056 * cos(2 * theta)
                                                    + 45486 * cos(3 * theta)
                                                    - 26880 * cos(4 * theta)
                                                    + 25215 * cos(5 * theta)
                                                    - 55080 * cos(6 * theta)
                                                    + 4913 * cos(7 * theta)
                                                    - 82688 * cos(8 * theta)
                                                    + 4845 * cos(9 * theta)
                                                    - 90440 * cos(10 * theta)
                                                    + 124355 * cos(11 * theta)
                                                )
                                                * exp(-2 * 1j * phi)
                                                / (1048576 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(2990)
                                                * (1j * sin(phi) - cos(phi))
                                                * (
                                                    882 * sin(theta)
                                                    + 3528 * sin(2 * theta)
                                                    + 2394 * sin(3 * theta)
                                                    + 6720 * sin(4 * theta)
                                                    + 3075 * sin(5 * theta)
                                                    + 9180 * sin(6 * theta)
                                                    + 2023 * sin(7 * theta)
                                                    + 10336 * sin(8 * theta)
                                                    - 2907 * sin(9 * theta)
                                                    + 9044 * sin(10 * theta)
                                                    - 24871 * sin(11 * theta)
                                                )
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(98670)
                                            * (
                                                882 * cos(theta)
                                                + 798 * cos(3 * theta)
                                                + 615 * cos(5 * theta)
                                                + 289 * cos(7 * theta)
                                                - 323 * cos(9 * theta)
                                                - 2261 * cos(11 * theta)
                                            )
                                            / (1048576 * sqrt(pi))
                                        )
                        else:
                            if m <= 6:
                                if m <= 3:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                sqrt(2990)
                                                * (
                                                    -882 * sin(theta)
                                                    + 3528 * sin(2 * theta)
                                                    - 2394 * sin(3 * theta)
                                                    + 6720 * sin(4 * theta)
                                                    - 3075 * sin(5 * theta)
                                                    + 9180 * sin(6 * theta)
                                                    - 2023 * sin(7 * theta)
                                                    + 10336 * sin(8 * theta)
                                                    + 2907 * sin(9 * theta)
                                                    + 9044 * sin(10 * theta)
                                                    + 24871 * sin(11 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(23)
                                                * (
                                                    57330 * cos(theta)
                                                    + 7056 * cos(2 * theta)
                                                    + 45486 * cos(3 * theta)
                                                    + 26880 * cos(4 * theta)
                                                    + 25215 * cos(5 * theta)
                                                    + 55080 * cos(6 * theta)
                                                    + 4913 * cos(7 * theta)
                                                    + 82688 * cos(8 * theta)
                                                    + 4845 * cos(9 * theta)
                                                    + 90440 * cos(10 * theta)
                                                    + 124355 * cos(11 * theta)
                                                )
                                                * exp(2 * 1j * phi)
                                                / (1048576 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -3
                                            * sqrt(322)
                                            * (
                                                2730 * sin(theta)
                                                - 3192 * sin(2 * theta)
                                                + 6802 * sin(3 * theta)
                                                - 3520 * sin(4 * theta)
                                                + 7175 * sin(5 * theta)
                                                + 1020 * sin(6 * theta)
                                                + 3179 * sin(7 * theta)
                                                + 10336 * sin(8 * theta)
                                                - 1615 * sin(9 * theta)
                                                + 19380 * sin(10 * theta)
                                                + 17765 * sin(11 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= 5:
                                        if m <= 4:
                                            return (
                                                sqrt(2415)
                                                * (
                                                    2730 * cos(theta)
                                                    + 672 * cos(2 * theta)
                                                    + 1254 * cos(3 * theta)
                                                    + 2048 * cos(4 * theta)
                                                    - 533 * cos(5 * theta)
                                                    + 2448 * cos(6 * theta)
                                                    - 867 * cos(7 * theta)
                                                    + 969 * cos(9 * theta)
                                                    - 5168 * cos(10 * theta)
                                                    - 3553 * cos(11 * theta)
                                                )
                                                * exp(4 * 1j * phi)
                                                / (524288 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(345)
                                                * (
                                                    13650 * sin(theta)
                                                    - 6888 * sin(2 * theta)
                                                    + 27930 * sin(3 * theta)
                                                    + 5824 * sin(4 * theta)
                                                    + 16195 * sin(5 * theta)
                                                    + 32436 * sin(6 * theta)
                                                    - 2601 * sin(7 * theta)
                                                    + 31008 * sin(8 * theta)
                                                    + 12597 * sin(9 * theta)
                                                    - 45220 * sin(10 * theta)
                                                    - 24871 * sin(11 * theta)
                                                )
                                                * exp(5 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(3910)
                                            * (
                                                2730 * cos(theta)
                                                + 1008 * cos(2 * theta)
                                                - 266 * cos(3 * theta)
                                                + 1792 * cos(4 * theta)
                                                - 2173 * cos(5 * theta)
                                                - 1128 * cos(6 * theta)
                                                - 595 * cos(7 * theta)
                                                - 4864 * cos(8 * theta)
                                                - 1159 * cos(9 * theta)
                                                + 3192 * cos(10 * theta)
                                                + 1463 * cos(11 * theta)
                                            )
                                            * exp(6 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                            else:
                                if m <= 9:
                                    if m <= 8:
                                        if m <= 7:
                                            return (
                                                -sqrt(391)
                                                * (
                                                    19110 * sin(theta)
                                                    - 2856 * sin(2 * theta)
                                                    + 26334 * sin(3 * theta)
                                                    + 20160 * sin(4 * theta)
                                                    - 5535 * sin(5 * theta)
                                                    + 18900 * sin(6 * theta)
                                                    - 10931 * sin(7 * theta)
                                                    - 46816 * sin(8 * theta)
                                                    - 8265 * sin(9 * theta)
                                                    + 18620 * sin(10 * theta)
                                                    + 7315 * sin(11 * theta)
                                                )
                                                * exp(7 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(7429)
                                                * (
                                                    2730 * cos(theta)
                                                    + 1344 * cos(2 * theta)
                                                    - 2394 * cos(3 * theta)
                                                    - 1845 * cos(5 * theta)
                                                    - 4320 * cos(6 * theta)
                                                    + 1309 * cos(7 * theta)
                                                    + 4096 * cos(8 * theta)
                                                    + 585 * cos(9 * theta)
                                                    - 1120 * cos(10 * theta)
                                                    - 385 * cos(11 * theta)
                                                )
                                                * exp(8 * 1j * phi)
                                                / (1048576 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -sqrt(111435)
                                            * (
                                                1638 * sin(theta)
                                                + 168 * sin(2 * theta)
                                                + 798 * sin(3 * theta)
                                                + 1344 * sin(4 * theta)
                                                - 1599 * sin(5 * theta)
                                                - 2196 * sin(6 * theta)
                                                + 493 * sin(7 * theta)
                                                + 1248 * sin(8 * theta)
                                                + 151 * sin(9 * theta)
                                                - 252 * sin(10 * theta)
                                                - 77 * sin(11 * theta)
                                            )
                                            * exp(9 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= 10:
                                        return (
                                            sqrt(520030)
                                            * (
                                                546 * cos(theta)
                                                + 336 * cos(2 * theta)
                                                - 1026 * cos(3 * theta)
                                                - 768 * cos(4 * theta)
                                                + 615 * cos(5 * theta)
                                                + 648 * cos(6 * theta)
                                                - 119 * cos(7 * theta)
                                                - 256 * cos(8 * theta)
                                                - 27 * cos(9 * theta)
                                                + 40 * cos(10 * theta)
                                                + 11 * cos(11 * theta)
                                            )
                                            * exp(10 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            -sqrt(2860165)
                                            * (
                                                546 * sin(theta)
                                                + 168 * sin(2 * theta)
                                                - 342 * sin(3 * theta)
                                                - 192 * sin(4 * theta)
                                                + 123 * sin(5 * theta)
                                                + 108 * sin(6 * theta)
                                                - 17 * sin(7 * theta)
                                                - 32 * sin(8 * theta)
                                                - 3 * sin(9 * theta)
                                                + 4 * sin(10 * theta)
                                                + sin(11 * theta)
                                            )
                                            * exp(11 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                else:
                    if l <= 12:
                        if m <= 0:
                            if m <= -6:
                                if m <= -9:
                                    if m <= -11:
                                        if m <= -12:
                                            return (
                                                5
                                                * sqrt(490314)
                                                * (
                                                    168
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(theta)
                                                    + 888
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(2 * theta)
                                                    - 360
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(3 * theta)
                                                    - 465
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(4 * theta)
                                                    + 300
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(5 * theta)
                                                    + 140
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(6 * theta)
                                                    - 140
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(7 * theta)
                                                    - 14
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(8 * theta)
                                                    + 36
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(9 * theta)
                                                    - 4
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(10 * theta)
                                                    - 4
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(11 * theta)
                                                    + 1j
                                                    * sin(12 * phi)
                                                    * cos(12 * theta)
                                                    - 546 * 1j * sin(12 * phi)
                                                    - 168 * cos(12 * phi) * cos(theta)
                                                    - 888
                                                    * cos(12 * phi)
                                                    * cos(2 * theta)
                                                    + 360
                                                    * cos(12 * phi)
                                                    * cos(3 * theta)
                                                    + 465
                                                    * cos(12 * phi)
                                                    * cos(4 * theta)
                                                    - 300
                                                    * cos(12 * phi)
                                                    * cos(5 * theta)
                                                    - 140
                                                    * cos(12 * phi)
                                                    * cos(6 * theta)
                                                    + 140
                                                    * cos(12 * phi)
                                                    * cos(7 * theta)
                                                    + 14
                                                    * cos(12 * phi)
                                                    * cos(8 * theta)
                                                    - 36
                                                    * cos(12 * phi)
                                                    * cos(9 * theta)
                                                    + 4
                                                    * cos(12 * phi)
                                                    * cos(10 * theta)
                                                    + 4
                                                    * cos(12 * phi)
                                                    * cos(11 * theta)
                                                    - cos(12 * phi) * cos(12 * theta)
                                                    + 546 * cos(12 * phi)
                                                )
                                                / (8388608 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(81719)
                                                * (
                                                    42 * sin(theta)
                                                    + 444 * sin(2 * theta)
                                                    - 270 * sin(3 * theta)
                                                    - 465 * sin(4 * theta)
                                                    + 375 * sin(5 * theta)
                                                    + 210 * sin(6 * theta)
                                                    - 245 * sin(7 * theta)
                                                    - 28 * sin(8 * theta)
                                                    + 81 * sin(9 * theta)
                                                    - 10 * sin(10 * theta)
                                                    - 11 * sin(11 * theta)
                                                    + 3 * sin(12 * theta)
                                                )
                                                * exp(-11 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -10:
                                            return (
                                                5
                                                * sqrt(7106)
                                                * (
                                                    420
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(theta)
                                                    + 888
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(2 * theta)
                                                    + 540
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(3 * theta)
                                                    + 2325
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(4 * theta)
                                                    - 2850
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(5 * theta)
                                                    - 2100
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(6 * theta)
                                                    + 3010
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(7 * theta)
                                                    + 406
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(8 * theta)
                                                    - 1350
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(9 * theta)
                                                    + 188
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(10 * theta)
                                                    + 230
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(11 * theta)
                                                    - 69
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(12 * theta)
                                                    - 1638 * 1j * sin(10 * phi)
                                                    - 420 * cos(10 * phi) * cos(theta)
                                                    - 888
                                                    * cos(10 * phi)
                                                    * cos(2 * theta)
                                                    - 540
                                                    * cos(10 * phi)
                                                    * cos(3 * theta)
                                                    - 2325
                                                    * cos(10 * phi)
                                                    * cos(4 * theta)
                                                    + 2850
                                                    * cos(10 * phi)
                                                    * cos(5 * theta)
                                                    + 2100
                                                    * cos(10 * phi)
                                                    * cos(6 * theta)
                                                    - 3010
                                                    * cos(10 * phi)
                                                    * cos(7 * theta)
                                                    - 406
                                                    * cos(10 * phi)
                                                    * cos(8 * theta)
                                                    + 1350
                                                    * cos(10 * phi)
                                                    * cos(9 * theta)
                                                    - 188
                                                    * cos(10 * phi)
                                                    * cos(10 * theta)
                                                    - 230
                                                    * cos(10 * phi)
                                                    * cos(11 * theta)
                                                    + 69
                                                    * cos(10 * phi)
                                                    * cos(12 * theta)
                                                    + 1638 * cos(10 * phi)
                                                )
                                                / (4194304 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(969)
                                                * (
                                                    462 * sin(theta)
                                                    + 3996 * sin(2 * theta)
                                                    - 1530 * sin(3 * theta)
                                                    - 465 * sin(4 * theta)
                                                    - 1875 * sin(5 * theta)
                                                    - 2590 * sin(6 * theta)
                                                    + 5145 * sin(7 * theta)
                                                    + 868 * sin(8 * theta)
                                                    - 3429 * sin(9 * theta)
                                                    + 550 * sin(10 * theta)
                                                    + 759 * sin(11 * theta)
                                                    - 253 * sin(12 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                else:
                                    if m <= -7:
                                        if m <= -8:
                                            return (
                                                5
                                                * sqrt(2261)
                                                * (
                                                    528 * 1j * sin(8 * phi) * cos(theta)
                                                    - 888
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(2 * theta)
                                                    + 2160
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(3 * theta)
                                                    + 4185
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(4 * theta)
                                                    - 1800
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(5 * theta)
                                                    + 1140
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(6 * theta)
                                                    - 5560
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(7 * theta)
                                                    - 1346
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(8 * theta)
                                                    + 6696
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(9 * theta)
                                                    - 1276
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(10 * theta)
                                                    - 2024
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(11 * theta)
                                                    + 759
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(12 * theta)
                                                    - 2574 * 1j * sin(8 * phi)
                                                    - 528 * cos(8 * phi) * cos(theta)
                                                    + 888
                                                    * cos(8 * phi)
                                                    * cos(2 * theta)
                                                    - 2160
                                                    * cos(8 * phi)
                                                    * cos(3 * theta)
                                                    - 4185
                                                    * cos(8 * phi)
                                                    * cos(4 * theta)
                                                    + 1800
                                                    * cos(8 * phi)
                                                    * cos(5 * theta)
                                                    - 1140
                                                    * cos(8 * phi)
                                                    * cos(6 * theta)
                                                    + 5560
                                                    * cos(8 * phi)
                                                    * cos(7 * theta)
                                                    + 1346
                                                    * cos(8 * phi)
                                                    * cos(8 * theta)
                                                    - 6696
                                                    * cos(8 * phi)
                                                    * cos(9 * theta)
                                                    + 1276
                                                    * cos(8 * phi)
                                                    * cos(10 * theta)
                                                    + 2024
                                                    * cos(8 * phi)
                                                    * cos(11 * theta)
                                                    - 759
                                                    * cos(8 * phi)
                                                    * cos(12 * theta)
                                                    + 2574 * cos(8 * phi)
                                                )
                                                / (4194304 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(2261)
                                                * (
                                                    330 * sin(theta)
                                                    + 2220 * sin(2 * theta)
                                                    - 270 * sin(3 * theta)
                                                    + 1395 * sin(4 * theta)
                                                    - 2025 * sin(5 * theta)
                                                    - 870 * sin(6 * theta)
                                                    - 805 * sin(7 * theta)
                                                    - 556 * sin(8 * theta)
                                                    + 3969 * sin(9 * theta)
                                                    - 946 * sin(10 * theta)
                                                    - 1771 * sin(11 * theta)
                                                    + 759 * sin(12 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(714)
                                            * (
                                                660 * 1j * sin(6 * phi) * cos(theta)
                                                - 4440
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(2 * theta)
                                                + 4140
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(3 * theta)
                                                + 3255
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(4 * theta)
                                                + 3750
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(5 * theta)
                                                + 5380
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(6 * theta)
                                                - 5510
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(7 * theta)
                                                + 722
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(8 * theta)
                                                - 12654
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(9 * theta)
                                                + 4180
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(10 * theta)
                                                + 9614
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(11 * theta)
                                                - 4807
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(12 * theta)
                                                - 4290 * 1j * sin(6 * phi)
                                                - 660 * cos(6 * phi) * cos(theta)
                                                + 4440 * cos(6 * phi) * cos(2 * theta)
                                                - 4140 * cos(6 * phi) * cos(3 * theta)
                                                - 3255 * cos(6 * phi) * cos(4 * theta)
                                                - 3750 * cos(6 * phi) * cos(5 * theta)
                                                - 5380 * cos(6 * phi) * cos(6 * theta)
                                                + 5510 * cos(6 * phi) * cos(7 * theta)
                                                - 722 * cos(6 * phi) * cos(8 * theta)
                                                + 12654 * cos(6 * phi) * cos(9 * theta)
                                                - 4180 * cos(6 * phi) * cos(10 * theta)
                                                - 9614 * cos(6 * phi) * cos(11 * theta)
                                                + 4807 * cos(6 * phi) * cos(12 * theta)
                                                + 4290 * cos(6 * phi)
                                            )
                                            / (4194304 * sqrt(pi))
                                        )
                            else:
                                if m <= -3:
                                    if m <= -4:
                                        if m <= -5:
                                            return (
                                                5
                                                * sqrt(51)
                                                * (
                                                    2310 * sin(theta)
                                                    + 11100 * sin(2 * theta)
                                                    + 2430 * sin(3 * theta)
                                                    + 13175 * sin(4 * theta)
                                                    - 6575 * sin(5 * theta)
                                                    + 5250 * sin(6 * theta)
                                                    - 17955 * sin(7 * theta)
                                                    - 1596 * sin(8 * theta)
                                                    - 12825 * sin(9 * theta)
                                                    + 7942 * sin(10 * theta)
                                                    + 24035 * sin(11 * theta)
                                                    - 14421 * sin(12 * theta)
                                                )
                                                * exp(-5 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(6)
                                                * (
                                                    9240
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(theta)
                                                    - 137640
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(2 * theta)
                                                    + 72360
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(3 * theta)
                                                    - 37045
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(4 * theta)
                                                    + 144500
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(5 * theta)
                                                    + 49980
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(6 * theta)
                                                    + 135660
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(7 * theta)
                                                    + 40698
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(8 * theta)
                                                    - 34884
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(9 * theta)
                                                    - 71060
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(10 * theta)
                                                    - 326876
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(11 * theta)
                                                    + 245157
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(12 * theta)
                                                    - 90090 * 1j * sin(4 * phi)
                                                    - 9240 * cos(4 * phi) * cos(theta)
                                                    + 137640
                                                    * cos(4 * phi)
                                                    * cos(2 * theta)
                                                    - 72360
                                                    * cos(4 * phi)
                                                    * cos(3 * theta)
                                                    + 37045
                                                    * cos(4 * phi)
                                                    * cos(4 * theta)
                                                    - 144500
                                                    * cos(4 * phi)
                                                    * cos(5 * theta)
                                                    - 49980
                                                    * cos(4 * phi)
                                                    * cos(6 * theta)
                                                    - 135660
                                                    * cos(4 * phi)
                                                    * cos(7 * theta)
                                                    - 40698
                                                    * cos(4 * phi)
                                                    * cos(8 * theta)
                                                    + 34884
                                                    * cos(4 * phi)
                                                    * cos(9 * theta)
                                                    + 71060
                                                    * cos(4 * phi)
                                                    * cos(10 * theta)
                                                    + 326876
                                                    * cos(4 * phi)
                                                    * cos(11 * theta)
                                                    - 245157
                                                    * cos(4 * phi)
                                                    * cos(12 * theta)
                                                    + 90090 * cos(4 * phi)
                                                )
                                                / (8388608 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(6)
                                            * (
                                                6930 * sin(theta)
                                                + 19980 * sin(2 * theta)
                                                + 15930 * sin(3 * theta)
                                                + 31155 * sin(4 * theta)
                                                + 11475 * sin(5 * theta)
                                                + 27370 * sin(6 * theta)
                                                - 11305 * sin(7 * theta)
                                                + 9044 * sin(8 * theta)
                                                - 49419 * sin(9 * theta)
                                                - 7106 * sin(10 * theta)
                                                - 81719 * sin(11 * theta)
                                                + 81719 * sin(12 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        if m <= -2:
                                            return (
                                                5
                                                * (
                                                    2772
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(theta)
                                                    - 98568
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(2 * theta)
                                                    + 24300
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(3 * theta)
                                                    - 72075
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(4 * theta)
                                                    + 63750
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(5 * theta)
                                                    - 35700
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(6 * theta)
                                                    + 113050
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(7 * theta)
                                                    - 4522
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(8 * theta)
                                                    + 156978
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(9 * theta)
                                                    - 14212
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(10 * theta)
                                                    + 163438
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(11 * theta)
                                                    - 245157
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(12 * theta)
                                                    - 54054 * 1j * sin(2 * phi)
                                                    - 2772 * cos(2 * phi) * cos(theta)
                                                    + 98568
                                                    * cos(2 * phi)
                                                    * cos(2 * theta)
                                                    - 24300
                                                    * cos(2 * phi)
                                                    * cos(3 * theta)
                                                    + 72075
                                                    * cos(2 * phi)
                                                    * cos(4 * theta)
                                                    - 63750
                                                    * cos(2 * phi)
                                                    * cos(5 * theta)
                                                    + 35700
                                                    * cos(2 * phi)
                                                    * cos(6 * theta)
                                                    - 113050
                                                    * cos(2 * phi)
                                                    * cos(7 * theta)
                                                    + 4522
                                                    * cos(2 * phi)
                                                    * cos(8 * theta)
                                                    - 156978
                                                    * cos(2 * phi)
                                                    * cos(9 * theta)
                                                    + 14212
                                                    * cos(2 * phi)
                                                    * cos(10 * theta)
                                                    - 163438
                                                    * cos(2 * phi)
                                                    * cos(11 * theta)
                                                    + 245157
                                                    * cos(2 * phi)
                                                    * cos(12 * theta)
                                                    + 54054 * cos(2 * phi)
                                                )
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -5
                                                * sqrt(154)
                                                * (1j * sin(phi) - cos(phi))
                                                * (
                                                    1386 * sin(theta)
                                                    + 1332 * sin(2 * theta)
                                                    + 4050 * sin(3 * theta)
                                                    + 2325 * sin(4 * theta)
                                                    + 6375 * sin(5 * theta)
                                                    + 2550 * sin(6 * theta)
                                                    + 8075 * sin(7 * theta)
                                                    + 1292 * sin(8 * theta)
                                                    + 8721 * sin(9 * theta)
                                                    - 3230 * sin(10 * theta)
                                                    + 7429 * sin(11 * theta)
                                                    - 22287 * sin(12 * theta)
                                                )
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(6006)
                                            * (
                                                2664 * cos(2 * theta)
                                                + 2325 * cos(4 * theta)
                                                + 1700 * cos(6 * theta)
                                                + 646 * cos(8 * theta)
                                                - 1292 * cos(10 * theta)
                                                - 7429 * cos(12 * theta)
                                                + 1386
                                            )
                                            / (4194304 * sqrt(pi))
                                        )
                        else:
                            if m <= 6:
                                if m <= 3:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                5
                                                * sqrt(154)
                                                * (
                                                    1386 * sin(theta)
                                                    - 1332 * sin(2 * theta)
                                                    + 4050 * sin(3 * theta)
                                                    - 2325 * sin(4 * theta)
                                                    + 6375 * sin(5 * theta)
                                                    - 2550 * sin(6 * theta)
                                                    + 8075 * sin(7 * theta)
                                                    - 1292 * sin(8 * theta)
                                                    + 8721 * sin(9 * theta)
                                                    + 3230 * sin(10 * theta)
                                                    + 7429 * sin(11 * theta)
                                                    + 22287 * sin(12 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * (
                                                    2772
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(theta)
                                                    + 98568
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(2 * theta)
                                                    + 24300
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(3 * theta)
                                                    + 72075
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(4 * theta)
                                                    + 63750
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(5 * theta)
                                                    + 35700
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(6 * theta)
                                                    + 113050
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(7 * theta)
                                                    + 4522
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(8 * theta)
                                                    + 156978
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(9 * theta)
                                                    + 14212
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(10 * theta)
                                                    + 163438
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(11 * theta)
                                                    + 245157
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(12 * theta)
                                                    + 54054 * 1j * sin(2 * phi)
                                                    + 2772 * cos(2 * phi) * cos(theta)
                                                    + 98568
                                                    * cos(2 * phi)
                                                    * cos(2 * theta)
                                                    + 24300
                                                    * cos(2 * phi)
                                                    * cos(3 * theta)
                                                    + 72075
                                                    * cos(2 * phi)
                                                    * cos(4 * theta)
                                                    + 63750
                                                    * cos(2 * phi)
                                                    * cos(5 * theta)
                                                    + 35700
                                                    * cos(2 * phi)
                                                    * cos(6 * theta)
                                                    + 113050
                                                    * cos(2 * phi)
                                                    * cos(7 * theta)
                                                    + 4522
                                                    * cos(2 * phi)
                                                    * cos(8 * theta)
                                                    + 156978
                                                    * cos(2 * phi)
                                                    * cos(9 * theta)
                                                    + 14212
                                                    * cos(2 * phi)
                                                    * cos(10 * theta)
                                                    + 163438
                                                    * cos(2 * phi)
                                                    * cos(11 * theta)
                                                    + 245157
                                                    * cos(2 * phi)
                                                    * cos(12 * theta)
                                                    + 54054 * cos(2 * phi)
                                                )
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -5
                                            * sqrt(6)
                                            * (
                                                -6930 * sin(theta)
                                                + 19980 * sin(2 * theta)
                                                - 15930 * sin(3 * theta)
                                                + 31155 * sin(4 * theta)
                                                - 11475 * sin(5 * theta)
                                                + 27370 * sin(6 * theta)
                                                + 11305 * sin(7 * theta)
                                                + 9044 * sin(8 * theta)
                                                + 49419 * sin(9 * theta)
                                                - 7106 * sin(10 * theta)
                                                + 81719 * sin(11 * theta)
                                                + 81719 * sin(12 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= 5:
                                        if m <= 4:
                                            return (
                                                5
                                                * sqrt(6)
                                                * (
                                                    9240 * cos(theta)
                                                    + 137640 * cos(2 * theta)
                                                    + 72360 * cos(3 * theta)
                                                    + 37045 * cos(4 * theta)
                                                    + 144500 * cos(5 * theta)
                                                    - 49980 * cos(6 * theta)
                                                    + 135660 * cos(7 * theta)
                                                    - 40698 * cos(8 * theta)
                                                    - 34884 * cos(9 * theta)
                                                    + 71060 * cos(10 * theta)
                                                    - 326876 * cos(11 * theta)
                                                    - 245157 * cos(12 * theta)
                                                    + 90090
                                                )
                                                * exp(4 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -5
                                                * sqrt(51)
                                                * (
                                                    -2310 * sin(theta)
                                                    + 11100 * sin(2 * theta)
                                                    - 2430 * sin(3 * theta)
                                                    + 13175 * sin(4 * theta)
                                                    + 6575 * sin(5 * theta)
                                                    + 5250 * sin(6 * theta)
                                                    + 17955 * sin(7 * theta)
                                                    - 1596 * sin(8 * theta)
                                                    + 12825 * sin(9 * theta)
                                                    + 7942 * sin(10 * theta)
                                                    - 24035 * sin(11 * theta)
                                                    - 14421 * sin(12 * theta)
                                                )
                                                * exp(5 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(714)
                                            * (
                                                660 * cos(theta)
                                                + 4440 * cos(2 * theta)
                                                + 4140 * cos(3 * theta)
                                                - 3255 * cos(4 * theta)
                                                + 3750 * cos(5 * theta)
                                                - 5380 * cos(6 * theta)
                                                - 5510 * cos(7 * theta)
                                                - 722 * cos(8 * theta)
                                                - 12654 * cos(9 * theta)
                                                - 4180 * cos(10 * theta)
                                                + 9614 * cos(11 * theta)
                                                + 4807 * cos(12 * theta)
                                                + 4290
                                            )
                                            * exp(6 * 1j * phi)
                                            / (4194304 * sqrt(pi))
                                        )
                            else:
                                if m <= 9:
                                    if m <= 8:
                                        if m <= 7:
                                            return (
                                                -5
                                                * sqrt(2261)
                                                * (
                                                    -330 * sin(theta)
                                                    + 2220 * sin(2 * theta)
                                                    + 270 * sin(3 * theta)
                                                    + 1395 * sin(4 * theta)
                                                    + 2025 * sin(5 * theta)
                                                    - 870 * sin(6 * theta)
                                                    + 805 * sin(7 * theta)
                                                    - 556 * sin(8 * theta)
                                                    - 3969 * sin(9 * theta)
                                                    - 946 * sin(10 * theta)
                                                    + 1771 * sin(11 * theta)
                                                    + 759 * sin(12 * theta)
                                                )
                                                * exp(7 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(2261)
                                                * (
                                                    528 * cos(theta)
                                                    + 888 * cos(2 * theta)
                                                    + 2160 * cos(3 * theta)
                                                    - 4185 * cos(4 * theta)
                                                    - 1800 * cos(5 * theta)
                                                    - 1140 * cos(6 * theta)
                                                    - 5560 * cos(7 * theta)
                                                    + 1346 * cos(8 * theta)
                                                    + 6696 * cos(9 * theta)
                                                    + 1276 * cos(10 * theta)
                                                    - 2024 * cos(11 * theta)
                                                    - 759 * cos(12 * theta)
                                                    + 2574
                                                )
                                                * exp(8 * 1j * phi)
                                                / (4194304 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(969)
                                            * (
                                                462 * sin(theta)
                                                - 3996 * sin(2 * theta)
                                                - 1530 * sin(3 * theta)
                                                + 465 * sin(4 * theta)
                                                - 1875 * sin(5 * theta)
                                                + 2590 * sin(6 * theta)
                                                + 5145 * sin(7 * theta)
                                                - 868 * sin(8 * theta)
                                                - 3429 * sin(9 * theta)
                                                - 550 * sin(10 * theta)
                                                + 759 * sin(11 * theta)
                                                + 253 * sin(12 * theta)
                                            )
                                            * exp(9 * 1j * phi)
                                            / (2097152 * sqrt(pi))
                                        )
                                else:
                                    if m <= 11:
                                        if m <= 10:
                                            return (
                                                5
                                                * sqrt(7106)
                                                * (
                                                    420 * cos(theta)
                                                    - 888 * cos(2 * theta)
                                                    + 540 * cos(3 * theta)
                                                    - 2325 * cos(4 * theta)
                                                    - 2850 * cos(5 * theta)
                                                    + 2100 * cos(6 * theta)
                                                    + 3010 * cos(7 * theta)
                                                    - 406 * cos(8 * theta)
                                                    - 1350 * cos(9 * theta)
                                                    - 188 * cos(10 * theta)
                                                    + 230 * cos(11 * theta)
                                                    + 69 * cos(12 * theta)
                                                    + 1638
                                                )
                                                * exp(10 * 1j * phi)
                                                / (4194304 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(81719)
                                                * (
                                                    42 * sin(theta)
                                                    - 444 * sin(2 * theta)
                                                    - 270 * sin(3 * theta)
                                                    + 465 * sin(4 * theta)
                                                    + 375 * sin(5 * theta)
                                                    - 210 * sin(6 * theta)
                                                    - 245 * sin(7 * theta)
                                                    + 28 * sin(8 * theta)
                                                    + 81 * sin(9 * theta)
                                                    + 10 * sin(10 * theta)
                                                    - 11 * sin(11 * theta)
                                                    - 3 * sin(12 * theta)
                                                )
                                                * exp(11 * 1j * phi)
                                                / (2097152 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            5
                                            * sqrt(490314)
                                            * (
                                                168 * cos(theta)
                                                - 888 * cos(2 * theta)
                                                - 360 * cos(3 * theta)
                                                + 465 * cos(4 * theta)
                                                + 300 * cos(5 * theta)
                                                - 140 * cos(6 * theta)
                                                - 140 * cos(7 * theta)
                                                + 14 * cos(8 * theta)
                                                + 36 * cos(9 * theta)
                                                + 4 * cos(10 * theta)
                                                - 4 * cos(11 * theta)
                                                - cos(12 * theta)
                                                + 546
                                            )
                                            * exp(12 * 1j * phi)
                                            / (8388608 * sqrt(pi))
                                        )
                    else:
                        if m <= 0:
                            if m <= -7:
                                if m <= -10:
                                    if m <= -12:
                                        if m <= -13:
                                            return (
                                                3
                                                * sqrt(1448655)
                                                * (
                                                    1980 * sin(theta)
                                                    - 528 * sin(2 * theta)
                                                    - 1353 * sin(3 * theta)
                                                    + 660 * sin(4 * theta)
                                                    + 605 * sin(5 * theta)
                                                    - 440 * sin(6 * theta)
                                                    - 154 * sin(7 * theta)
                                                    + 176 * sin(8 * theta)
                                                    + 10 * sin(9 * theta)
                                                    - 40 * sin(10 * theta)
                                                    + 5 * sin(11 * theta)
                                                    + 4 * sin(12 * theta)
                                                    - sin(13 * theta)
                                                )
                                                * exp(-13 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(222870)
                                                * (
                                                    1980 * cos(theta)
                                                    - 1056 * cos(2 * theta)
                                                    - 4059 * cos(3 * theta)
                                                    + 2640 * cos(4 * theta)
                                                    + 3025 * cos(5 * theta)
                                                    - 2640 * cos(6 * theta)
                                                    - 1078 * cos(7 * theta)
                                                    + 1408 * cos(8 * theta)
                                                    + 90 * cos(9 * theta)
                                                    - 400 * cos(10 * theta)
                                                    + 55 * cos(11 * theta)
                                                    + 48 * cos(12 * theta)
                                                    - 13 * cos(13 * theta)
                                                )
                                                * exp(-12 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -11:
                                            return (
                                                3
                                                * sqrt(111435)
                                                * (
                                                    4356 * sin(theta)
                                                    - 528 * sin(2 * theta)
                                                    + 1353 * sin(3 * theta)
                                                    - 2508 * sin(4 * theta)
                                                    - 4477 * sin(5 * theta)
                                                    + 5192 * sin(6 * theta)
                                                    + 2618 * sin(7 * theta)
                                                    - 4048 * sin(8 * theta)
                                                    - 298 * sin(9 * theta)
                                                    + 1496 * sin(10 * theta)
                                                    - 229 * sin(11 * theta)
                                                    - 220 * sin(12 * theta)
                                                    + 65 * sin(13 * theta)
                                                )
                                                * exp(-11 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(222870)
                                                * (
                                                    -1188 * cos(theta)
                                                    + 528 * cos(2 * theta)
                                                    + 1353 * cos(3 * theta)
                                                    - 264 * cos(4 * theta)
                                                    + 605 * cos(5 * theta)
                                                    - 1496 * cos(6 * theta)
                                                    - 1078 * cos(7 * theta)
                                                    + 2112 * cos(8 * theta)
                                                    + 186 * cos(9 * theta)
                                                    - 1080 * cos(10 * theta)
                                                    + 187 * cos(11 * theta)
                                                    + 200 * cos(12 * theta)
                                                    - 65 * cos(13 * theta)
                                                )
                                                * exp(-10 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                else:
                                    if m <= -8:
                                        if m <= -9:
                                            return (
                                                3
                                                * sqrt(9690)
                                                * (
                                                    10692 * sin(theta)
                                                    + 528 * sin(2 * theta)
                                                    + 12177 * sin(3 * theta)
                                                    - 9636 * sin(4 * theta)
                                                    - 7381 * sin(5 * theta)
                                                    - 2376 * sin(6 * theta)
                                                    - 7238 * sin(7 * theta)
                                                    + 21648 * sin(8 * theta)
                                                    + 2454 * sin(9 * theta)
                                                    - 17112 * sin(10 * theta)
                                                    + 3427 * sin(11 * theta)
                                                    + 4140 * sin(12 * theta)
                                                    - 1495 * sin(13 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(10659)
                                                * (
                                                    -5940 * cos(theta)
                                                    + 2112 * cos(2 * theta)
                                                    + 2337 * cos(3 * theta)
                                                    + 2400 * cos(4 * theta)
                                                    + 5885 * cos(5 * theta)
                                                    - 4960 * cos(6 * theta)
                                                    + 98 * cos(7 * theta)
                                                    - 6912 * cos(8 * theta)
                                                    - 1230 * cos(9 * theta)
                                                    + 11040 * cos(10 * theta)
                                                    - 2645 * cos(11 * theta)
                                                    - 3680 * cos(12 * theta)
                                                    + 1495 * cos(13 * theta)
                                                )
                                                * exp(-8 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(149226)
                                            * (
                                                1980 * sin(theta)
                                                + 528 * sin(2 * theta)
                                                + 3567 * sin(3 * theta)
                                                - 1380 * sin(4 * theta)
                                                + 1045 * sin(5 * theta)
                                                - 3400 * sin(6 * theta)
                                                - 1658 * sin(7 * theta)
                                                - 112 * sin(8 * theta)
                                                - 470 * sin(9 * theta)
                                                + 6440 * sin(10 * theta)
                                                - 1955 * sin(11 * theta)
                                                - 3220 * sin(12 * theta)
                                                + 1495 * sin(13 * theta)
                                            )
                                            * exp(-7 * 1j * phi)
                                            / (16777216 * sqrt(pi))
                                        )
                            else:
                                if m <= -3:
                                    if m <= -5:
                                        if m <= -6:
                                            return (
                                                -3
                                                * sqrt(106590)
                                                * (
                                                    -1980 * cos(theta)
                                                    + 528 * cos(2 * theta)
                                                    - 369 * cos(3 * theta)
                                                    + 1272 * cos(4 * theta)
                                                    + 1243 * cos(5 * theta)
                                                    + 552 * cos(6 * theta)
                                                    + 1190 * cos(7 * theta)
                                                    - 1984 * cos(8 * theta)
                                                    + 54 * cos(9 * theta)
                                                    - 3128 * cos(10 * theta)
                                                    + 1357 * cos(11 * theta)
                                                    + 2760 * cos(12 * theta)
                                                    - 1495 * cos(13 * theta)
                                                )
                                                * exp(-6 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(2805)
                                                * (
                                                    9900 * sin(theta)
                                                    + 5808 * sin(2 * theta)
                                                    + 22755 * sin(3 * theta)
                                                    + 516 * sin(4 * theta)
                                                    + 19745 * sin(5 * theta)
                                                    - 17176 * sin(6 * theta)
                                                    + 5054 * sin(7 * theta)
                                                    - 32528 * sin(8 * theta)
                                                    - 2318 * sin(9 * theta)
                                                    - 17480 * sin(10 * theta)
                                                    + 16169 * sin(11 * theta)
                                                    + 43700 * sin(12 * theta)
                                                    - 28405 * sin(13 * theta)
                                                )
                                                * exp(-5 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -4:
                                            return (
                                                -3
                                                * sqrt(5610)
                                                * (
                                                    -17820 * cos(theta)
                                                    + 3168 * cos(2 * theta)
                                                    - 10701 * cos(3 * theta)
                                                    + 10512 * cos(4 * theta)
                                                    - 473 * cos(5 * theta)
                                                    + 16112 * cos(6 * theta)
                                                    + 6118 * cos(7 * theta)
                                                    + 12160 * cos(8 * theta)
                                                    + 2774 * cos(9 * theta)
                                                    - 6992 * cos(10 * theta)
                                                    - 8303 * cos(11 * theta)
                                                    - 34960 * cos(12 * theta)
                                                    + 28405 * cos(13 * theta)
                                                )
                                                * exp(-4 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(33)
                                                * (
                                                    53460 * sin(theta)
                                                    + 64944 * sin(2 * theta)
                                                    + 140589 * sin(3 * theta)
                                                    + 88740 * sin(4 * theta)
                                                    + 172975 * sin(5 * theta)
                                                    + 38760 * sin(6 * theta)
                                                    + 131138 * sin(7 * theta)
                                                    - 98192 * sin(8 * theta)
                                                    + 29070 * sin(9 * theta)
                                                    - 297160 * sin(10 * theta)
                                                    - 37145 * sin(11 * theta)
                                                    - 445740 * sin(12 * theta)
                                                    + 482885 * sin(13 * theta)
                                                )
                                                * exp(-3 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                else:
                                    if m <= -1:
                                        if m <= -2:
                                            return (
                                                3
                                                * sqrt(3)
                                                * (
                                                    196020 * cos(theta)
                                                    - 17424 * cos(2 * theta)
                                                    + 166419 * cos(3 * theta)
                                                    - 67320 * cos(4 * theta)
                                                    + 113135 * cos(5 * theta)
                                                    - 142120 * cos(6 * theta)
                                                    + 49742 * cos(7 * theta)
                                                    - 227392 * cos(8 * theta)
                                                    + 3230 * cos(9 * theta)
                                                    - 297160 * cos(10 * theta)
                                                    + 37145 * cos(11 * theta)
                                                    - 297160 * cos(12 * theta)
                                                    + 482885 * cos(13 * theta)
                                                )
                                                * exp(-2 * 1j * phi)
                                                / (4194304 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(15)
                                                * (1j * sin(phi) - cos(phi))
                                                * (
                                                    13068 * sin(theta)
                                                    + 52272 * sin(2 * theta)
                                                    + 36531 * sin(3 * theta)
                                                    + 100980 * sin(4 * theta)
                                                    + 51425 * sin(5 * theta)
                                                    + 142120 * sin(6 * theta)
                                                    + 49742 * sin(7 * theta)
                                                    + 170544 * sin(8 * theta)
                                                    + 17442 * sin(9 * theta)
                                                    + 178296 * sin(10 * theta)
                                                    - 81719 * sin(11 * theta)
                                                    + 148580 * sin(12 * theta)
                                                    - 482885 * sin(13 * theta)
                                                )
                                                / (8388608 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(2730)
                                            * (
                                                13068 * cos(theta)
                                                + 12177 * cos(3 * theta)
                                                + 10285 * cos(5 * theta)
                                                + 7106 * cos(7 * theta)
                                                + 1938 * cos(9 * theta)
                                                - 7429 * cos(11 * theta)
                                                - 37145 * cos(13 * theta)
                                            )
                                            / (8388608 * sqrt(pi))
                                        )
                        else:
                            if m <= 7:
                                if m <= 4:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                3
                                                * sqrt(15)
                                                * (
                                                    -13068 * sin(theta)
                                                    + 52272 * sin(2 * theta)
                                                    - 36531 * sin(3 * theta)
                                                    + 100980 * sin(4 * theta)
                                                    - 51425 * sin(5 * theta)
                                                    + 142120 * sin(6 * theta)
                                                    - 49742 * sin(7 * theta)
                                                    + 170544 * sin(8 * theta)
                                                    - 17442 * sin(9 * theta)
                                                    + 178296 * sin(10 * theta)
                                                    + 81719 * sin(11 * theta)
                                                    + 148580 * sin(12 * theta)
                                                    + 482885 * sin(13 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(3)
                                                * (
                                                    196020 * cos(theta)
                                                    + 17424 * cos(2 * theta)
                                                    + 166419 * cos(3 * theta)
                                                    + 67320 * cos(4 * theta)
                                                    + 113135 * cos(5 * theta)
                                                    + 142120 * cos(6 * theta)
                                                    + 49742 * cos(7 * theta)
                                                    + 227392 * cos(8 * theta)
                                                    + 3230 * cos(9 * theta)
                                                    + 297160 * cos(10 * theta)
                                                    + 37145 * cos(11 * theta)
                                                    + 297160 * cos(12 * theta)
                                                    + 482885 * cos(13 * theta)
                                                )
                                                * exp(2 * 1j * phi)
                                                / (4194304 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 3:
                                            return (
                                                -3
                                                * sqrt(33)
                                                * (
                                                    53460 * sin(theta)
                                                    - 64944 * sin(2 * theta)
                                                    + 140589 * sin(3 * theta)
                                                    - 88740 * sin(4 * theta)
                                                    + 172975 * sin(5 * theta)
                                                    - 38760 * sin(6 * theta)
                                                    + 131138 * sin(7 * theta)
                                                    + 98192 * sin(8 * theta)
                                                    + 29070 * sin(9 * theta)
                                                    + 297160 * sin(10 * theta)
                                                    - 37145 * sin(11 * theta)
                                                    + 445740 * sin(12 * theta)
                                                    + 482885 * sin(13 * theta)
                                                )
                                                * exp(3 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(5610)
                                                * (
                                                    17820 * cos(theta)
                                                    + 3168 * cos(2 * theta)
                                                    + 10701 * cos(3 * theta)
                                                    + 10512 * cos(4 * theta)
                                                    + 473 * cos(5 * theta)
                                                    + 16112 * cos(6 * theta)
                                                    - 6118 * cos(7 * theta)
                                                    + 12160 * cos(8 * theta)
                                                    - 2774 * cos(9 * theta)
                                                    - 6992 * cos(10 * theta)
                                                    + 8303 * cos(11 * theta)
                                                    - 34960 * cos(12 * theta)
                                                    - 28405 * cos(13 * theta)
                                                )
                                                * exp(4 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                else:
                                    if m <= 6:
                                        if m <= 5:
                                            return (
                                                -3
                                                * sqrt(2805)
                                                * (
                                                    9900 * sin(theta)
                                                    - 5808 * sin(2 * theta)
                                                    + 22755 * sin(3 * theta)
                                                    - 516 * sin(4 * theta)
                                                    + 19745 * sin(5 * theta)
                                                    + 17176 * sin(6 * theta)
                                                    + 5054 * sin(7 * theta)
                                                    + 32528 * sin(8 * theta)
                                                    - 2318 * sin(9 * theta)
                                                    + 17480 * sin(10 * theta)
                                                    + 16169 * sin(11 * theta)
                                                    - 43700 * sin(12 * theta)
                                                    - 28405 * sin(13 * theta)
                                                )
                                                * exp(5 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(106590)
                                                * (
                                                    1980 * cos(theta)
                                                    + 528 * cos(2 * theta)
                                                    + 369 * cos(3 * theta)
                                                    + 1272 * cos(4 * theta)
                                                    - 1243 * cos(5 * theta)
                                                    + 552 * cos(6 * theta)
                                                    - 1190 * cos(7 * theta)
                                                    - 1984 * cos(8 * theta)
                                                    - 54 * cos(9 * theta)
                                                    - 3128 * cos(10 * theta)
                                                    - 1357 * cos(11 * theta)
                                                    + 2760 * cos(12 * theta)
                                                    + 1495 * cos(13 * theta)
                                                )
                                                * exp(6 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -3
                                            * sqrt(149226)
                                            * (
                                                1980 * sin(theta)
                                                - 528 * sin(2 * theta)
                                                + 3567 * sin(3 * theta)
                                                + 1380 * sin(4 * theta)
                                                + 1045 * sin(5 * theta)
                                                + 3400 * sin(6 * theta)
                                                - 1658 * sin(7 * theta)
                                                + 112 * sin(8 * theta)
                                                - 470 * sin(9 * theta)
                                                - 6440 * sin(10 * theta)
                                                - 1955 * sin(11 * theta)
                                                + 3220 * sin(12 * theta)
                                                + 1495 * sin(13 * theta)
                                            )
                                            * exp(7 * 1j * phi)
                                            / (16777216 * sqrt(pi))
                                        )
                            else:
                                if m <= 10:
                                    if m <= 9:
                                        if m <= 8:
                                            return (
                                                3
                                                * sqrt(10659)
                                                * (
                                                    5940 * cos(theta)
                                                    + 2112 * cos(2 * theta)
                                                    - 2337 * cos(3 * theta)
                                                    + 2400 * cos(4 * theta)
                                                    - 5885 * cos(5 * theta)
                                                    - 4960 * cos(6 * theta)
                                                    - 98 * cos(7 * theta)
                                                    - 6912 * cos(8 * theta)
                                                    + 1230 * cos(9 * theta)
                                                    + 11040 * cos(10 * theta)
                                                    + 2645 * cos(11 * theta)
                                                    - 3680 * cos(12 * theta)
                                                    - 1495 * cos(13 * theta)
                                                )
                                                * exp(8 * 1j * phi)
                                                / (8388608 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(9690)
                                                * (
                                                    10692 * sin(theta)
                                                    - 528 * sin(2 * theta)
                                                    + 12177 * sin(3 * theta)
                                                    + 9636 * sin(4 * theta)
                                                    - 7381 * sin(5 * theta)
                                                    + 2376 * sin(6 * theta)
                                                    - 7238 * sin(7 * theta)
                                                    - 21648 * sin(8 * theta)
                                                    + 2454 * sin(9 * theta)
                                                    + 17112 * sin(10 * theta)
                                                    + 3427 * sin(11 * theta)
                                                    - 4140 * sin(12 * theta)
                                                    - 1495 * sin(13 * theta)
                                                )
                                                * exp(9 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(222870)
                                            * (
                                                1188 * cos(theta)
                                                + 528 * cos(2 * theta)
                                                - 1353 * cos(3 * theta)
                                                - 264 * cos(4 * theta)
                                                - 605 * cos(5 * theta)
                                                - 1496 * cos(6 * theta)
                                                + 1078 * cos(7 * theta)
                                                + 2112 * cos(8 * theta)
                                                - 186 * cos(9 * theta)
                                                - 1080 * cos(10 * theta)
                                                - 187 * cos(11 * theta)
                                                + 200 * cos(12 * theta)
                                                + 65 * cos(13 * theta)
                                            )
                                            * exp(10 * 1j * phi)
                                            / (8388608 * sqrt(pi))
                                        )
                                else:
                                    if m <= 12:
                                        if m <= 11:
                                            return (
                                                -3
                                                * sqrt(111435)
                                                * (
                                                    4356 * sin(theta)
                                                    + 528 * sin(2 * theta)
                                                    + 1353 * sin(3 * theta)
                                                    + 2508 * sin(4 * theta)
                                                    - 4477 * sin(5 * theta)
                                                    - 5192 * sin(6 * theta)
                                                    + 2618 * sin(7 * theta)
                                                    + 4048 * sin(8 * theta)
                                                    - 298 * sin(9 * theta)
                                                    - 1496 * sin(10 * theta)
                                                    - 229 * sin(11 * theta)
                                                    + 220 * sin(12 * theta)
                                                    + 65 * sin(13 * theta)
                                                )
                                                * exp(11 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(222870)
                                                * (
                                                    1980 * cos(theta)
                                                    + 1056 * cos(2 * theta)
                                                    - 4059 * cos(3 * theta)
                                                    - 2640 * cos(4 * theta)
                                                    + 3025 * cos(5 * theta)
                                                    + 2640 * cos(6 * theta)
                                                    - 1078 * cos(7 * theta)
                                                    - 1408 * cos(8 * theta)
                                                    + 90 * cos(9 * theta)
                                                    + 400 * cos(10 * theta)
                                                    + 55 * cos(11 * theta)
                                                    - 48 * cos(12 * theta)
                                                    - 13 * cos(13 * theta)
                                                )
                                                * exp(12 * 1j * phi)
                                                / (16777216 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -3
                                            * sqrt(1448655)
                                            * (
                                                1980 * sin(theta)
                                                + 528 * sin(2 * theta)
                                                - 1353 * sin(3 * theta)
                                                - 660 * sin(4 * theta)
                                                + 605 * sin(5 * theta)
                                                + 440 * sin(6 * theta)
                                                - 154 * sin(7 * theta)
                                                - 176 * sin(8 * theta)
                                                + 10 * sin(9 * theta)
                                                + 40 * sin(10 * theta)
                                                + 5 * sin(11 * theta)
                                                - 4 * sin(12 * theta)
                                                - sin(13 * theta)
                                            )
                                            * exp(13 * 1j * phi)
                                            / (16777216 * sqrt(pi))
                                        )
            else:
                if l <= 15:
                    if l <= 14:
                        if m <= 0:
                            if m <= -7:
                                if m <= -11:
                                    if m <= -13:
                                        if m <= -14:
                                            return (
                                                3
                                                * sqrt(98025655)
                                                * (
                                                    528
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(theta)
                                                    + 3333
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(2 * theta)
                                                    - 1188
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(3 * theta)
                                                    - 1958
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(4 * theta)
                                                    + 1100
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(5 * theta)
                                                    + 759
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(6 * theta)
                                                    - 616
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(7 * theta)
                                                    - 164
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(8 * theta)
                                                    + 216
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(9 * theta)
                                                    + 5
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(10 * theta)
                                                    - 44
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(11 * theta)
                                                    + 6
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(12 * theta)
                                                    + 4
                                                    * 1j
                                                    * sin(14 * phi)
                                                    * cos(13 * theta)
                                                    - 1j
                                                    * sin(14 * phi)
                                                    * cos(14 * theta)
                                                    - 1980 * 1j * sin(14 * phi)
                                                    - 528 * cos(14 * phi) * cos(theta)
                                                    - 3333
                                                    * cos(14 * phi)
                                                    * cos(2 * theta)
                                                    + 1188
                                                    * cos(14 * phi)
                                                    * cos(3 * theta)
                                                    + 1958
                                                    * cos(14 * phi)
                                                    * cos(4 * theta)
                                                    - 1100
                                                    * cos(14 * phi)
                                                    * cos(5 * theta)
                                                    - 759
                                                    * cos(14 * phi)
                                                    * cos(6 * theta)
                                                    + 616
                                                    * cos(14 * phi)
                                                    * cos(7 * theta)
                                                    + 164
                                                    * cos(14 * phi)
                                                    * cos(8 * theta)
                                                    - 216
                                                    * cos(14 * phi)
                                                    * cos(9 * theta)
                                                    - 5
                                                    * cos(14 * phi)
                                                    * cos(10 * theta)
                                                    + 44
                                                    * cos(14 * phi)
                                                    * cos(11 * theta)
                                                    - 6
                                                    * cos(14 * phi)
                                                    * cos(12 * theta)
                                                    - 4
                                                    * cos(14 * phi)
                                                    * cos(13 * theta)
                                                    + cos(14 * phi) * cos(14 * theta)
                                                    + 1980 * cos(14 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(14003665)
                                                * (
                                                    264 * sin(theta)
                                                    + 3333 * sin(2 * theta)
                                                    - 1782 * sin(3 * theta)
                                                    - 3916 * sin(4 * theta)
                                                    + 2750 * sin(5 * theta)
                                                    + 2277 * sin(6 * theta)
                                                    - 2156 * sin(7 * theta)
                                                    - 656 * sin(8 * theta)
                                                    + 972 * sin(9 * theta)
                                                    + 25 * sin(10 * theta)
                                                    - 242 * sin(11 * theta)
                                                    + 36 * sin(12 * theta)
                                                    + 26 * sin(13 * theta)
                                                    - 7 * sin(14 * theta)
                                                )
                                                * exp(-13 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -12:
                                            return (
                                                sqrt(84021990)
                                                * (
                                                    1056
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(theta)
                                                    + 3333
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(2 * theta)
                                                    + 792
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(3 * theta)
                                                    + 5874
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(4 * theta)
                                                    - 6600
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(5 * theta)
                                                    - 7337
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(6 * theta)
                                                    + 8624
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(7 * theta)
                                                    + 3116
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(8 * theta)
                                                    - 5328
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(9 * theta)
                                                    - 155
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(10 * theta)
                                                    + 1672
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(11 * theta)
                                                    - 274
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(12 * theta)
                                                    - 216
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(13 * theta)
                                                    + 63
                                                    * 1j
                                                    * sin(12 * phi)
                                                    * cos(14 * theta)
                                                    - 4620 * 1j * sin(12 * phi)
                                                    - 1056 * cos(12 * phi) * cos(theta)
                                                    - 3333
                                                    * cos(12 * phi)
                                                    * cos(2 * theta)
                                                    - 792
                                                    * cos(12 * phi)
                                                    * cos(3 * theta)
                                                    - 5874
                                                    * cos(12 * phi)
                                                    * cos(4 * theta)
                                                    + 6600
                                                    * cos(12 * phi)
                                                    * cos(5 * theta)
                                                    + 7337
                                                    * cos(12 * phi)
                                                    * cos(6 * theta)
                                                    - 8624
                                                    * cos(12 * phi)
                                                    * cos(7 * theta)
                                                    - 3116
                                                    * cos(12 * phi)
                                                    * cos(8 * theta)
                                                    + 5328
                                                    * cos(12 * phi)
                                                    * cos(9 * theta)
                                                    + 155
                                                    * cos(12 * phi)
                                                    * cos(10 * theta)
                                                    - 1672
                                                    * cos(12 * phi)
                                                    * cos(11 * theta)
                                                    + 274
                                                    * cos(12 * phi)
                                                    * cos(12 * theta)
                                                    + 216
                                                    * cos(12 * phi)
                                                    * cos(13 * theta)
                                                    - 63
                                                    * cos(12 * phi)
                                                    * cos(14 * theta)
                                                    + 4620 * cos(12 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1077205)
                                                * (
                                                    3432 * sin(theta)
                                                    + 36663 * sin(2 * theta)
                                                    - 13662 * sin(3 * theta)
                                                    - 11748 * sin(4 * theta)
                                                    - 8250 * sin(5 * theta)
                                                    - 23529 * sin(6 * theta)
                                                    + 40964 * sin(7 * theta)
                                                    + 19024 * sin(8 * theta)
                                                    - 39204 * sin(9 * theta)
                                                    - 1325 * sin(10 * theta)
                                                    + 16214 * sin(11 * theta)
                                                    - 2964 * sin(12 * theta)
                                                    - 2574 * sin(13 * theta)
                                                    + 819 * sin(14 * theta)
                                                )
                                                * exp(-11 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                else:
                                    if m <= -9:
                                        if m <= -10:
                                            return (
                                                sqrt(1077205)
                                                * (
                                                    6864
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(theta)
                                                    - 3333
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(2 * theta)
                                                    + 22572
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(3 * theta)
                                                    + 64614
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(4 * theta)
                                                    - 34980
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(5 * theta)
                                                    - 759
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(6 * theta)
                                                    - 47432
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(7 * theta)
                                                    - 36572
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(8 * theta)
                                                    + 99576
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(9 * theta)
                                                    + 4091
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(10 * theta)
                                                    - 58300
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(11 * theta)
                                                    + 12090
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(12 * theta)
                                                    + 11700
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(13 * theta)
                                                    - 4095
                                                    * 1j
                                                    * sin(10 * phi)
                                                    * cos(14 * theta)
                                                    - 36036 * 1j * sin(10 * phi)
                                                    - 6864 * cos(10 * phi) * cos(theta)
                                                    + 3333
                                                    * cos(10 * phi)
                                                    * cos(2 * theta)
                                                    - 22572
                                                    * cos(10 * phi)
                                                    * cos(3 * theta)
                                                    - 64614
                                                    * cos(10 * phi)
                                                    * cos(4 * theta)
                                                    + 34980
                                                    * cos(10 * phi)
                                                    * cos(5 * theta)
                                                    + 759
                                                    * cos(10 * phi)
                                                    * cos(6 * theta)
                                                    + 47432
                                                    * cos(10 * phi)
                                                    * cos(7 * theta)
                                                    + 36572
                                                    * cos(10 * phi)
                                                    * cos(8 * theta)
                                                    - 99576
                                                    * cos(10 * phi)
                                                    * cos(9 * theta)
                                                    - 4091
                                                    * cos(10 * phi)
                                                    * cos(10 * theta)
                                                    + 58300
                                                    * cos(10 * phi)
                                                    * cos(11 * theta)
                                                    - 12090
                                                    * cos(10 * phi)
                                                    * cos(12 * theta)
                                                    - 11700
                                                    * cos(10 * phi)
                                                    * cos(13 * theta)
                                                    + 4095
                                                    * cos(10 * phi)
                                                    * cos(14 * theta)
                                                    + 36036 * cos(10 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1292646)
                                                * (
                                                    3432 * sin(theta)
                                                    + 29997 * sin(2 * theta)
                                                    - 5742 * sin(3 * theta)
                                                    + 11748 * sin(4 * theta)
                                                    - 21450 * sin(5 * theta)
                                                    - 19987 * sin(6 * theta)
                                                    + 6468 * sin(7 * theta)
                                                    - 8528 * sin(8 * theta)
                                                    + 42012 * sin(9 * theta)
                                                    + 2305 * sin(10 * theta)
                                                    - 39930 * sin(11 * theta)
                                                    + 9620 * sin(12 * theta)
                                                    + 10530 * sin(13 * theta)
                                                    - 4095 * sin(14 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -8:
                                            return (
                                                sqrt(9367)
                                                * (
                                                    27456
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(theta)
                                                    - 136653
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(2 * theta)
                                                    + 147312
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(3 * theta)
                                                    + 229086
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(4 * theta)
                                                    + 39600
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(5 * theta)
                                                    + 236049
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(6 * theta)
                                                    - 327712
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(7 * theta)
                                                    - 46412
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(8 * theta)
                                                    - 258336
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(9 * theta)
                                                    - 25645
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(10 * theta)
                                                    + 586960
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(11 * theta)
                                                    - 170430
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(12 * theta)
                                                    - 215280
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(13 * theta)
                                                    + 94185
                                                    * 1j
                                                    * sin(8 * phi)
                                                    * cos(14 * theta)
                                                    - 180180 * 1j * sin(8 * phi)
                                                    - 27456 * cos(8 * phi) * cos(theta)
                                                    + 136653
                                                    * cos(8 * phi)
                                                    * cos(2 * theta)
                                                    - 147312
                                                    * cos(8 * phi)
                                                    * cos(3 * theta)
                                                    - 229086
                                                    * cos(8 * phi)
                                                    * cos(4 * theta)
                                                    - 39600
                                                    * cos(8 * phi)
                                                    * cos(5 * theta)
                                                    - 236049
                                                    * cos(8 * phi)
                                                    * cos(6 * theta)
                                                    + 327712
                                                    * cos(8 * phi)
                                                    * cos(7 * theta)
                                                    + 46412
                                                    * cos(8 * phi)
                                                    * cos(8 * theta)
                                                    + 258336
                                                    * cos(8 * phi)
                                                    * cos(9 * theta)
                                                    + 25645
                                                    * cos(8 * phi)
                                                    * cos(10 * theta)
                                                    - 586960
                                                    * cos(8 * phi)
                                                    * cos(11 * theta)
                                                    + 170430
                                                    * cos(8 * phi)
                                                    * cos(12 * theta)
                                                    + 215280
                                                    * cos(8 * phi)
                                                    * cos(13 * theta)
                                                    - 94185
                                                    * cos(8 * phi)
                                                    * cos(14 * theta)
                                                    + 180180 * cos(8 * phi)
                                                )
                                                / (134217728 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1442518)
                                                * (
                                                    3432 * sin(theta)
                                                    + 23331 * sin(2 * theta)
                                                    + 594 * sin(3 * theta)
                                                    + 22428 * sin(4 * theta)
                                                    - 16650 * sin(5 * theta)
                                                    + 483 * sin(6 * theta)
                                                    - 23996 * sin(7 * theta)
                                                    - 12464 * sin(8 * theta)
                                                    + 7452 * sin(9 * theta)
                                                    - 1265 * sin(10 * theta)
                                                    + 48070 * sin(11 * theta)
                                                    - 17940 * sin(12 * theta)
                                                    - 26910 * sin(13 * theta)
                                                    + 13455 * sin(14 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                            else:
                                if m <= -3:
                                    if m <= -5:
                                        if m <= -6:
                                            return (
                                                sqrt(309111)
                                                * (
                                                    6864
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(theta)
                                                    - 76659
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(2 * theta)
                                                    + 47916
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(3 * theta)
                                                    + 16554
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(4 * theta)
                                                    + 68700
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(5 * theta)
                                                    + 76751
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(6 * theta)
                                                    + 2744
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(7 * theta)
                                                    + 51004
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(8 * theta)
                                                    - 130824
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(9 * theta)
                                                    - 115
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(10 * theta)
                                                    - 156860
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(11 * theta)
                                                    + 86710
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(12 * theta)
                                                    + 161460
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(13 * theta)
                                                    - 94185
                                                    * 1j
                                                    * sin(6 * phi)
                                                    * cos(14 * theta)
                                                    - 60060 * 1j * sin(6 * phi)
                                                    - 6864 * cos(6 * phi) * cos(theta)
                                                    + 76659
                                                    * cos(6 * phi)
                                                    * cos(2 * theta)
                                                    - 47916
                                                    * cos(6 * phi)
                                                    * cos(3 * theta)
                                                    - 16554
                                                    * cos(6 * phi)
                                                    * cos(4 * theta)
                                                    - 68700
                                                    * cos(6 * phi)
                                                    * cos(5 * theta)
                                                    - 76751
                                                    * cos(6 * phi)
                                                    * cos(6 * theta)
                                                    - 2744
                                                    * cos(6 * phi)
                                                    * cos(7 * theta)
                                                    - 51004
                                                    * cos(6 * phi)
                                                    * cos(8 * theta)
                                                    + 130824
                                                    * cos(6 * phi)
                                                    * cos(9 * theta)
                                                    + 115
                                                    * cos(6 * phi)
                                                    * cos(10 * theta)
                                                    + 156860
                                                    * cos(6 * phi)
                                                    * cos(11 * theta)
                                                    - 86710
                                                    * cos(6 * phi)
                                                    * cos(12 * theta)
                                                    - 161460
                                                    * cos(6 * phi)
                                                    * cos(13 * theta)
                                                    + 94185
                                                    * cos(6 * phi)
                                                    * cos(14 * theta)
                                                    + 60060 * cos(6 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1545555)
                                                * (
                                                    3432 * sin(theta)
                                                    + 16665 * sin(2 * theta)
                                                    + 5346 * sin(3 * theta)
                                                    + 23140 * sin(4 * theta)
                                                    - 4090 * sin(5 * theta)
                                                    + 15801 * sin(6 * theta)
                                                    - 21756 * sin(7 * theta)
                                                    + 1968 * sin(8 * theta)
                                                    - 32292 * sin(9 * theta)
                                                    - 1219 * sin(10 * theta)
                                                    - 12650 * sin(11 * theta)
                                                    + 17940 * sin(12 * theta)
                                                    + 44850 * sin(13 * theta)
                                                    - 31395 * sin(14 * theta)
                                                )
                                                * exp(-5 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -4:
                                            return (
                                                sqrt(32538)
                                                * (
                                                    13728
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(theta)
                                                    - 296637
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(2 * theta)
                                                    + 111672
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(3 * theta)
                                                    - 135458
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(4 * theta)
                                                    + 247000
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(5 * theta)
                                                    + 40641
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(6 * theta)
                                                    + 312816
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(7 * theta)
                                                    + 121524
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(8 * theta)
                                                    + 188784
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(9 * theta)
                                                    + 24035
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(10 * theta)
                                                    - 192280
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(11 * theta)
                                                    - 170430
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(12 * theta)
                                                    - 681720
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(13 * theta)
                                                    + 596505
                                                    * 1j
                                                    * sin(4 * phi)
                                                    * cos(14 * theta)
                                                    - 180180 * 1j * sin(4 * phi)
                                                    - 13728 * cos(4 * phi) * cos(theta)
                                                    + 296637
                                                    * cos(4 * phi)
                                                    * cos(2 * theta)
                                                    - 111672
                                                    * cos(4 * phi)
                                                    * cos(3 * theta)
                                                    + 135458
                                                    * cos(4 * phi)
                                                    * cos(4 * theta)
                                                    - 247000
                                                    * cos(4 * phi)
                                                    * cos(5 * theta)
                                                    - 40641
                                                    * cos(4 * phi)
                                                    * cos(6 * theta)
                                                    - 312816
                                                    * cos(4 * phi)
                                                    * cos(7 * theta)
                                                    - 121524
                                                    * cos(4 * phi)
                                                    * cos(8 * theta)
                                                    - 188784
                                                    * cos(4 * phi)
                                                    * cos(9 * theta)
                                                    - 24035
                                                    * cos(4 * phi)
                                                    * cos(10 * theta)
                                                    + 192280
                                                    * cos(4 * phi)
                                                    * cos(11 * theta)
                                                    + 170430
                                                    * cos(4 * phi)
                                                    * cos(12 * theta)
                                                    + 681720
                                                    * cos(4 * phi)
                                                    * cos(13 * theta)
                                                    - 596505
                                                    * cos(4 * phi)
                                                    * cos(14 * theta)
                                                    + 180180 * cos(4 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1479)
                                                * (
                                                    113256 * sin(theta)
                                                    + 329967 * sin(2 * theta)
                                                    + 280962 * sin(3 * theta)
                                                    + 552156 * sin(4 * theta)
                                                    + 282150 * sin(5 * theta)
                                                    + 581647 * sin(6 * theta)
                                                    + 40964 * sin(7 * theta)
                                                    + 386384 * sin(8 * theta)
                                                    - 456228 * sin(9 * theta)
                                                    + 41515 * sin(10 * theta)
                                                    - 1105610 * sin(11 * theta)
                                                    - 113620 * sin(12 * theta)
                                                    - 1533870 * sin(13 * theta)
                                                    + 1789515 * sin(14 * theta)
                                                )
                                                * exp(-3 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                else:
                                    if m <= -1:
                                        if m <= -2:
                                            return (
                                                sqrt(29)
                                                * (
                                                    226512
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(theta)
                                                    - 11108889
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(2 * theta)
                                                    + 1999404
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(3 * theta)
                                                    - 8887362
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(4 * theta)
                                                    + 5329500
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(5 * theta)
                                                    - 5638611
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(6 * theta)
                                                    + 9749432
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(7 * theta)
                                                    - 2171852
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(8 * theta)
                                                    + 14441976
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(9 * theta)
                                                    - 37145
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(10 * theta)
                                                    + 17978180
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(11 * theta)
                                                    - 2897310
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(12 * theta)
                                                    + 17383860
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(13 * theta)
                                                    - 30421755
                                                    * 1j
                                                    * sin(2 * phi)
                                                    * cos(14 * theta)
                                                    - 5945940 * 1j * sin(2 * phi)
                                                    - 226512 * cos(2 * phi) * cos(theta)
                                                    + 11108889
                                                    * cos(2 * phi)
                                                    * cos(2 * theta)
                                                    - 1999404
                                                    * cos(2 * phi)
                                                    * cos(3 * theta)
                                                    + 8887362
                                                    * cos(2 * phi)
                                                    * cos(4 * theta)
                                                    - 5329500
                                                    * cos(2 * phi)
                                                    * cos(5 * theta)
                                                    + 5638611
                                                    * cos(2 * phi)
                                                    * cos(6 * theta)
                                                    - 9749432
                                                    * cos(2 * phi)
                                                    * cos(7 * theta)
                                                    + 2171852
                                                    * cos(2 * phi)
                                                    * cos(8 * theta)
                                                    - 14441976
                                                    * cos(2 * phi)
                                                    * cos(9 * theta)
                                                    + 37145
                                                    * cos(2 * phi)
                                                    * cos(10 * theta)
                                                    - 17978180
                                                    * cos(2 * phi)
                                                    * cos(11 * theta)
                                                    + 2897310
                                                    * cos(2 * phi)
                                                    * cos(12 * theta)
                                                    - 17383860
                                                    * cos(2 * phi)
                                                    * cos(13 * theta)
                                                    + 30421755
                                                    * cos(2 * phi)
                                                    * cos(14 * theta)
                                                    + 5945940 * cos(2 * phi)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(377)
                                                * (1j * sin(phi) - cos(phi))
                                                * (
                                                    113256 * sin(theta)
                                                    + 109989 * sin(2 * theta)
                                                    + 333234 * sin(3 * theta)
                                                    + 199716 * sin(4 * theta)
                                                    + 532950 * sin(5 * theta)
                                                    + 245157 * sin(6 * theta)
                                                    + 696388 * sin(7 * theta)
                                                    + 211888 * sin(8 * theta)
                                                    + 802332 * sin(9 * theta)
                                                    + 37145 * sin(10 * theta)
                                                    + 817190 * sin(11 * theta)
                                                    - 445740 * sin(12 * theta)
                                                    + 668610 * sin(13 * theta)
                                                    - 2340135 * sin(14 * theta)
                                                )
                                                / (67108864 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(79170)
                                            * (
                                                109989 * cos(2 * theta)
                                                + 99858 * cos(4 * theta)
                                                + 81719 * cos(6 * theta)
                                                + 52972 * cos(8 * theta)
                                                + 7429 * cos(10 * theta)
                                                - 74290 * cos(12 * theta)
                                                - 334305 * cos(14 * theta)
                                                + 56628
                                            )
                                            / (134217728 * sqrt(pi))
                                        )
                        else:
                            if m <= 7:
                                if m <= 4:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                sqrt(377)
                                                * (
                                                    113256 * sin(theta)
                                                    - 109989 * sin(2 * theta)
                                                    + 333234 * sin(3 * theta)
                                                    - 199716 * sin(4 * theta)
                                                    + 532950 * sin(5 * theta)
                                                    - 245157 * sin(6 * theta)
                                                    + 696388 * sin(7 * theta)
                                                    - 211888 * sin(8 * theta)
                                                    + 802332 * sin(9 * theta)
                                                    - 37145 * sin(10 * theta)
                                                    + 817190 * sin(11 * theta)
                                                    + 445740 * sin(12 * theta)
                                                    + 668610 * sin(13 * theta)
                                                    + 2340135 * sin(14 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (67108864 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(29)
                                                * (
                                                    226512 * cos(theta)
                                                    + 11108889 * cos(2 * theta)
                                                    + 1999404 * cos(3 * theta)
                                                    + 8887362 * cos(4 * theta)
                                                    + 5329500 * cos(5 * theta)
                                                    + 5638611 * cos(6 * theta)
                                                    + 9749432 * cos(7 * theta)
                                                    + 2171852 * cos(8 * theta)
                                                    + 14441976 * cos(9 * theta)
                                                    + 37145 * cos(10 * theta)
                                                    + 17978180 * cos(11 * theta)
                                                    + 2897310 * cos(12 * theta)
                                                    + 17383860 * cos(13 * theta)
                                                    + 30421755 * cos(14 * theta)
                                                    + 5945940
                                                )
                                                * exp(2 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 3:
                                            return (
                                                -sqrt(1479)
                                                * (
                                                    -113256 * sin(theta)
                                                    + 329967 * sin(2 * theta)
                                                    - 280962 * sin(3 * theta)
                                                    + 552156 * sin(4 * theta)
                                                    - 282150 * sin(5 * theta)
                                                    + 581647 * sin(6 * theta)
                                                    - 40964 * sin(7 * theta)
                                                    + 386384 * sin(8 * theta)
                                                    + 456228 * sin(9 * theta)
                                                    + 41515 * sin(10 * theta)
                                                    + 1105610 * sin(11 * theta)
                                                    - 113620 * sin(12 * theta)
                                                    + 1533870 * sin(13 * theta)
                                                    + 1789515 * sin(14 * theta)
                                                )
                                                * exp(3 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(32538)
                                                * (
                                                    13728 * cos(theta)
                                                    + 296637 * cos(2 * theta)
                                                    + 111672 * cos(3 * theta)
                                                    + 135458 * cos(4 * theta)
                                                    + 247000 * cos(5 * theta)
                                                    - 40641 * cos(6 * theta)
                                                    + 312816 * cos(7 * theta)
                                                    - 121524 * cos(8 * theta)
                                                    + 188784 * cos(9 * theta)
                                                    - 24035 * cos(10 * theta)
                                                    - 192280 * cos(11 * theta)
                                                    + 170430 * cos(12 * theta)
                                                    - 681720 * cos(13 * theta)
                                                    - 596505 * cos(14 * theta)
                                                    + 180180
                                                )
                                                * exp(4 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                                else:
                                    if m <= 6:
                                        if m <= 5:
                                            return (
                                                -sqrt(1545555)
                                                * (
                                                    -3432 * sin(theta)
                                                    + 16665 * sin(2 * theta)
                                                    - 5346 * sin(3 * theta)
                                                    + 23140 * sin(4 * theta)
                                                    + 4090 * sin(5 * theta)
                                                    + 15801 * sin(6 * theta)
                                                    + 21756 * sin(7 * theta)
                                                    + 1968 * sin(8 * theta)
                                                    + 32292 * sin(9 * theta)
                                                    - 1219 * sin(10 * theta)
                                                    + 12650 * sin(11 * theta)
                                                    + 17940 * sin(12 * theta)
                                                    - 44850 * sin(13 * theta)
                                                    - 31395 * sin(14 * theta)
                                                )
                                                * exp(5 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(309111)
                                                * (
                                                    6864 * cos(theta)
                                                    + 76659 * cos(2 * theta)
                                                    + 47916 * cos(3 * theta)
                                                    - 16554 * cos(4 * theta)
                                                    + 68700 * cos(5 * theta)
                                                    - 76751 * cos(6 * theta)
                                                    + 2744 * cos(7 * theta)
                                                    - 51004 * cos(8 * theta)
                                                    - 130824 * cos(9 * theta)
                                                    + 115 * cos(10 * theta)
                                                    - 156860 * cos(11 * theta)
                                                    - 86710 * cos(12 * theta)
                                                    + 161460 * cos(13 * theta)
                                                    + 94185 * cos(14 * theta)
                                                    + 60060
                                                )
                                                * exp(6 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            sqrt(1442518)
                                            * (
                                                3432 * sin(theta)
                                                - 23331 * sin(2 * theta)
                                                + 594 * sin(3 * theta)
                                                - 22428 * sin(4 * theta)
                                                - 16650 * sin(5 * theta)
                                                - 483 * sin(6 * theta)
                                                - 23996 * sin(7 * theta)
                                                + 12464 * sin(8 * theta)
                                                + 7452 * sin(9 * theta)
                                                + 1265 * sin(10 * theta)
                                                + 48070 * sin(11 * theta)
                                                + 17940 * sin(12 * theta)
                                                - 26910 * sin(13 * theta)
                                                - 13455 * sin(14 * theta)
                                            )
                                            * exp(7 * 1j * phi)
                                            / (134217728 * sqrt(pi))
                                        )
                            else:
                                if m <= 11:
                                    if m <= 9:
                                        if m <= 8:
                                            return (
                                                sqrt(9367)
                                                * (
                                                    27456 * cos(theta)
                                                    + 136653 * cos(2 * theta)
                                                    + 147312 * cos(3 * theta)
                                                    - 229086 * cos(4 * theta)
                                                    + 39600 * cos(5 * theta)
                                                    - 236049 * cos(6 * theta)
                                                    - 327712 * cos(7 * theta)
                                                    + 46412 * cos(8 * theta)
                                                    - 258336 * cos(9 * theta)
                                                    + 25645 * cos(10 * theta)
                                                    + 586960 * cos(11 * theta)
                                                    + 170430 * cos(12 * theta)
                                                    - 215280 * cos(13 * theta)
                                                    - 94185 * cos(14 * theta)
                                                    + 180180
                                                )
                                                * exp(8 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1292646)
                                                * (
                                                    3432 * sin(theta)
                                                    - 29997 * sin(2 * theta)
                                                    - 5742 * sin(3 * theta)
                                                    - 11748 * sin(4 * theta)
                                                    - 21450 * sin(5 * theta)
                                                    + 19987 * sin(6 * theta)
                                                    + 6468 * sin(7 * theta)
                                                    + 8528 * sin(8 * theta)
                                                    + 42012 * sin(9 * theta)
                                                    - 2305 * sin(10 * theta)
                                                    - 39930 * sin(11 * theta)
                                                    - 9620 * sin(12 * theta)
                                                    + 10530 * sin(13 * theta)
                                                    + 4095 * sin(14 * theta)
                                                )
                                                * exp(9 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 10:
                                            return (
                                                sqrt(1077205)
                                                * (
                                                    6864 * cos(theta)
                                                    + 3333 * cos(2 * theta)
                                                    + 22572 * cos(3 * theta)
                                                    - 64614 * cos(4 * theta)
                                                    - 34980 * cos(5 * theta)
                                                    + 759 * cos(6 * theta)
                                                    - 47432 * cos(7 * theta)
                                                    + 36572 * cos(8 * theta)
                                                    + 99576 * cos(9 * theta)
                                                    - 4091 * cos(10 * theta)
                                                    - 58300 * cos(11 * theta)
                                                    - 12090 * cos(12 * theta)
                                                    + 11700 * cos(13 * theta)
                                                    + 4095 * cos(14 * theta)
                                                    + 36036
                                                )
                                                * exp(10 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1077205)
                                                * (
                                                    3432 * sin(theta)
                                                    - 36663 * sin(2 * theta)
                                                    - 13662 * sin(3 * theta)
                                                    + 11748 * sin(4 * theta)
                                                    - 8250 * sin(5 * theta)
                                                    + 23529 * sin(6 * theta)
                                                    + 40964 * sin(7 * theta)
                                                    - 19024 * sin(8 * theta)
                                                    - 39204 * sin(9 * theta)
                                                    + 1325 * sin(10 * theta)
                                                    + 16214 * sin(11 * theta)
                                                    + 2964 * sin(12 * theta)
                                                    - 2574 * sin(13 * theta)
                                                    - 819 * sin(14 * theta)
                                                )
                                                * exp(11 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                else:
                                    if m <= 13:
                                        if m <= 12:
                                            return (
                                                sqrt(84021990)
                                                * (
                                                    1056 * cos(theta)
                                                    - 3333 * cos(2 * theta)
                                                    + 792 * cos(3 * theta)
                                                    - 5874 * cos(4 * theta)
                                                    - 6600 * cos(5 * theta)
                                                    + 7337 * cos(6 * theta)
                                                    + 8624 * cos(7 * theta)
                                                    - 3116 * cos(8 * theta)
                                                    - 5328 * cos(9 * theta)
                                                    + 155 * cos(10 * theta)
                                                    + 1672 * cos(11 * theta)
                                                    + 274 * cos(12 * theta)
                                                    - 216 * cos(13 * theta)
                                                    - 63 * cos(14 * theta)
                                                    + 4620
                                                )
                                                * exp(12 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(14003665)
                                                * (
                                                    264 * sin(theta)
                                                    - 3333 * sin(2 * theta)
                                                    - 1782 * sin(3 * theta)
                                                    + 3916 * sin(4 * theta)
                                                    + 2750 * sin(5 * theta)
                                                    - 2277 * sin(6 * theta)
                                                    - 2156 * sin(7 * theta)
                                                    + 656 * sin(8 * theta)
                                                    + 972 * sin(9 * theta)
                                                    - 25 * sin(10 * theta)
                                                    - 242 * sin(11 * theta)
                                                    - 36 * sin(12 * theta)
                                                    + 26 * sin(13 * theta)
                                                    + 7 * sin(14 * theta)
                                                )
                                                * exp(13 * 1j * phi)
                                                / (134217728 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            3
                                            * sqrt(98025655)
                                            * (
                                                528 * cos(theta)
                                                - 3333 * cos(2 * theta)
                                                - 1188 * cos(3 * theta)
                                                + 1958 * cos(4 * theta)
                                                + 1100 * cos(5 * theta)
                                                - 759 * cos(6 * theta)
                                                - 616 * cos(7 * theta)
                                                + 164 * cos(8 * theta)
                                                + 216 * cos(9 * theta)
                                                - 5 * cos(10 * theta)
                                                - 44 * cos(11 * theta)
                                                - 6 * cos(12 * theta)
                                                + 4 * cos(13 * theta)
                                                + cos(14 * theta)
                                                + 1980
                                            )
                                            * exp(14 * 1j * phi)
                                            / (268435456 * sqrt(pi))
                                        )
                    else:
                        if m <= 0:
                            if m <= -8:
                                if m <= -12:
                                    if m <= -14:
                                        if m <= -15:
                                            return (
                                                15
                                                * sqrt(16500246)
                                                * (
                                                    7293 * sin(theta)
                                                    - 1716 * sin(2 * theta)
                                                    - 5291 * sin(3 * theta)
                                                    + 2288 * sin(4 * theta)
                                                    + 2717 * sin(5 * theta)
                                                    - 1716 * sin(6 * theta)
                                                    - 923 * sin(7 * theta)
                                                    + 832 * sin(8 * theta)
                                                    + 169 * sin(9 * theta)
                                                    - 260 * sin(10 * theta)
                                                    + sin(11 * theta)
                                                    + 48 * sin(12 * theta)
                                                    - 7 * sin(13 * theta)
                                                    - 4 * sin(14 * theta)
                                                    + sin(15 * theta)
                                                )
                                                * exp(-15 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(13750205)
                                                * (
                                                    7293 * cos(theta)
                                                    - 3432 * cos(2 * theta)
                                                    - 15873 * cos(3 * theta)
                                                    + 9152 * cos(4 * theta)
                                                    + 13585 * cos(5 * theta)
                                                    - 10296 * cos(6 * theta)
                                                    - 6461 * cos(7 * theta)
                                                    + 6656 * cos(8 * theta)
                                                    + 1521 * cos(9 * theta)
                                                    - 2600 * cos(10 * theta)
                                                    + 11 * cos(11 * theta)
                                                    + 576 * cos(12 * theta)
                                                    - 91 * cos(13 * theta)
                                                    - 56 * cos(14 * theta)
                                                    + 15 * cos(15 * theta)
                                                )
                                                * exp(-14 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -13:
                                            return (
                                                3
                                                * sqrt(948290)
                                                * (
                                                    94809 * sin(theta)
                                                    - 12012 * sin(2 * theta)
                                                    + 15873 * sin(3 * theta)
                                                    - 38896 * sin(4 * theta)
                                                    - 95095 * sin(5 * theta)
                                                    + 97812 * sin(6 * theta)
                                                    + 76609 * sin(7 * theta)
                                                    - 94016 * sin(8 * theta)
                                                    - 24843 * sin(9 * theta)
                                                    + 48100 * sin(10 * theta)
                                                    - 227 * sin(11 * theta)
                                                    - 13104 * sin(12 * theta)
                                                    + 2261 * sin(13 * theta)
                                                    + 1508 * sin(14 * theta)
                                                    - 435 * sin(15 * theta)
                                                )
                                                * exp(-13 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(406410)
                                                * (
                                                    -51051 * cos(theta)
                                                    + 20592 * cos(2 * theta)
                                                    + 68783 * cos(3 * theta)
                                                    - 18304 * cos(4 * theta)
                                                    + 13585 * cos(5 * theta)
                                                    - 48048 * cos(6 * theta)
                                                    - 58149 * cos(7 * theta)
                                                    + 93184 * cos(8 * theta)
                                                    + 29913 * cos(9 * theta)
                                                    - 67600 * cos(10 * theta)
                                                    + 363 * cos(11 * theta)
                                                    + 23424 * cos(12 * theta)
                                                    - 4459 * cos(13 * theta)
                                                    - 3248 * cos(14 * theta)
                                                    + 1015 * cos(15 * theta)
                                                )
                                                * exp(-12 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                else:
                                    if m <= -10:
                                        if m <= -11:
                                            return (
                                                sqrt(135470)
                                                * (
                                                    561561 * sin(theta)
                                                    - 1716 * sin(2 * theta)
                                                    + 523809 * sin(3 * theta)
                                                    - 418704 * sin(4 * theta)
                                                    - 529815 * sin(5 * theta)
                                                    + 108108 * sin(6 * theta)
                                                    - 277823 * sin(7 * theta)
                                                    + 832832 * sin(8 * theta)
                                                    + 364533 * sin(9 * theta)
                                                    - 1015300 * sin(10 * theta)
                                                    + 6397 * sin(11 * theta)
                                                    + 470448 * sin(12 * theta)
                                                    - 100107 * sin(13 * theta)
                                                    - 80388 * sin(14 * theta)
                                                    + 27405 * sin(15 * theta)
                                                )
                                                * exp(-11 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(176111)
                                                * (
                                                    51051 * cos(theta)
                                                    - 17160 * cos(2 * theta)
                                                    - 32967 * cos(3 * theta)
                                                    - 10560 * cos(4 * theta)
                                                    - 52041 * cos(5 * theta)
                                                    + 49896 * cos(6 * theta)
                                                    + 18389 * cos(7 * theta)
                                                    + 25088 * cos(8 * theta)
                                                    + 25623 * cos(9 * theta)
                                                    - 100040 * cos(10 * theta)
                                                    + 781 * cos(11 * theta)
                                                    + 67392 * cos(12 * theta)
                                                    - 16317 * cos(13 * theta)
                                                    - 14616 * cos(14 * theta)
                                                    + 5481 * cos(15 * theta)
                                                )
                                                * exp(-10 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -9:
                                            return (
                                                sqrt(1056666)
                                                * (
                                                    153153 * sin(theta)
                                                    + 22308 * sin(2 * theta)
                                                    + 240537 * sin(3 * theta)
                                                    - 111408 * sin(4 * theta)
                                                    - 3135 * sin(5 * theta)
                                                    - 163548 * sin(6 * theta)
                                                    - 178423 * sin(7 * theta)
                                                    + 143808 * sin(8 * theta)
                                                    - 32227 * sin(9 * theta)
                                                    + 328500 * sin(10 * theta)
                                                    - 3595 * sin(11 * theta)
                                                    - 382320 * sin(12 * theta)
                                                    + 108045 * sin(13 * theta)
                                                    + 109620 * sin(14 * theta)
                                                    - 45675 * sin(15 * theta)
                                                )
                                                * exp(-9 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(1232777)
                                                * (
                                                    -51051 * cos(theta)
                                                    + 13728 * cos(2 * theta)
                                                    + 3663 * cos(3 * theta)
                                                    + 25344 * cos(4 * theta)
                                                    + 47025 * cos(5 * theta)
                                                    - 9504 * cos(6 * theta)
                                                    + 28187 * cos(7 * theta)
                                                    - 63488 * cos(8 * theta)
                                                    - 12519 * cos(9 * theta)
                                                    - 28000 * cos(10 * theta)
                                                    + 715 * cos(11 * theta)
                                                    + 103680 * cos(12 * theta)
                                                    - 35595 * cos(13 * theta)
                                                    - 41760 * cos(14 * theta)
                                                    + 19575 * cos(15 * theta)
                                                )
                                                * exp(-8 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                            else:
                                if m <= -4:
                                    if m <= -6:
                                        if m <= -7:
                                            return (
                                                sqrt(107198)
                                                * (
                                                    357357 * sin(theta)
                                                    + 121836 * sin(2 * theta)
                                                    + 743589 * sin(3 * theta)
                                                    - 131472 * sin(4 * theta)
                                                    + 460845 * sin(5 * theta)
                                                    - 604692 * sin(6 * theta)
                                                    - 140651 * sin(7 * theta)
                                                    - 584384 * sin(8 * theta)
                                                    - 322023 * sin(9 * theta)
                                                    + 425500 * sin(10 * theta)
                                                    + 4945 * sin(11 * theta)
                                                    + 1341360 * sin(12 * theta)
                                                    - 601335 * sin(13 * theta)
                                                    - 840420 * sin(14 * theta)
                                                    + 450225 * sin(15 * theta)
                                                )
                                                * exp(-7 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -3
                                                * sqrt(589589)
                                                * (
                                                    -51051 * cos(theta)
                                                    + 10296 * cos(2 * theta)
                                                    - 19129 * cos(3 * theta)
                                                    + 28864 * cos(4 * theta)
                                                    + 20425 * cos(5 * theta)
                                                    + 27816 * cos(6 * theta)
                                                    + 36139 * cos(7 * theta)
                                                    - 11776 * cos(8 * theta)
                                                    + 17641 * cos(9 * theta)
                                                    - 69000 * cos(10 * theta)
                                                    + 115 * cos(11 * theta)
                                                    - 66240 * cos(12 * theta)
                                                    + 45885 * cos(13 * theta)
                                                    + 80040 * cos(14 * theta)
                                                    - 50025 * cos(15 * theta)
                                                )
                                                * exp(-6 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -5:
                                            return (
                                                sqrt(2526810)
                                                * (
                                                    51051 * sin(theta)
                                                    + 32604 * sin(2 * theta)
                                                    + 125763 * sin(3 * theta)
                                                    + 19888 * sin(4 * theta)
                                                    + 133019 * sin(5 * theta)
                                                    - 54180 * sin(6 * theta)
                                                    + 73059 * sin(7 * theta)
                                                    - 154560 * sin(8 * theta)
                                                    - 897 * sin(9 * theta)
                                                    - 190900 * sin(10 * theta)
                                                    + 1495 * sin(11 * theta)
                                                    - 49680 * sin(12 * theta)
                                                    + 118335 * sin(13 * theta)
                                                    + 280140 * sin(14 * theta)
                                                    - 210105 * sin(15 * theta)
                                                )
                                                * exp(-5 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                -sqrt(45942)
                                                * (
                                                    -561561 * cos(theta)
                                                    + 75504 * cos(2 * theta)
                                                    - 389499 * cos(3 * theta)
                                                    + 263296 * cos(4 * theta)
                                                    - 118085 * cos(5 * theta)
                                                    + 454608 * cos(6 * theta)
                                                    + 123753 * cos(7 * theta)
                                                    + 494592 * cos(8 * theta)
                                                    + 189267 * cos(9 * theta)
                                                    + 230000 * cos(10 * theta)
                                                    - 7015 * cos(11 * theta)
                                                    - 397440 * cos(12 * theta)
                                                    - 287385 * cos(13 * theta)
                                                    - 1120560 * cos(14 * theta)
                                                    + 1050525 * cos(15 * theta)
                                                )
                                                * exp(-4 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                else:
                                    if m <= -2:
                                        if m <= -3:
                                            return (
                                                3
                                                * sqrt(806)
                                                * (
                                                    561561 * sin(theta)
                                                    + 698412 * sin(2 * theta)
                                                    + 1526657 * sin(3 * theta)
                                                    + 1066736 * sin(4 * theta)
                                                    + 2045065 * sin(5 * theta)
                                                    + 825132 * sin(6 * theta)
                                                    + 1916929 * sin(7 * theta)
                                                    - 195776 * sin(8 * theta)
                                                    + 1119157 * sin(9 * theta)
                                                    - 1966500 * sin(10 * theta)
                                                    - 24035 * sin(11 * theta)
                                                    - 4090320 * sin(12 * theta)
                                                    - 321195 * sin(13 * theta)
                                                    - 5322660 * sin(14 * theta)
                                                    + 6653325 * sin(15 * theta)
                                                )
                                                * exp(-3 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(31)
                                                * (
                                                    21900879 * cos(theta)
                                                    - 1472328 * cos(2 * theta)
                                                    + 19380933 * cos(3 * theta)
                                                    - 5738304 * cos(4 * theta)
                                                    + 14712555 * cos(5 * theta)
                                                    - 12324312 * cos(6 * theta)
                                                    + 8715889 * cos(7 * theta)
                                                    - 20360704 * cos(8 * theta)
                                                    + 2880267 * cos(9 * theta)
                                                    - 28405000 * cos(10 * theta)
                                                    + 2185 * cos(11 * theta)
                                                    - 33981120 * cos(12 * theta)
                                                    + 6745095 * cos(13 * theta)
                                                    - 31935960 * cos(14 * theta)
                                                    + 59879925 * cos(15 * theta)
                                                )
                                                * exp(-2 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= -1:
                                            return (
                                                -sqrt(7378)
                                                * (1j * sin(phi) - cos(phi))
                                                * (
                                                    184041 * sin(theta)
                                                    + 736164 * sin(2 * theta)
                                                    + 523809 * sin(3 * theta)
                                                    + 1434576 * sin(4 * theta)
                                                    + 774345 * sin(5 * theta)
                                                    + 2054052 * sin(6 * theta)
                                                    + 859313 * sin(7 * theta)
                                                    + 2545088 * sin(8 * theta)
                                                    + 664677 * sin(9 * theta)
                                                    + 2840500 * sin(10 * theta)
                                                    - 24035 * sin(11 * theta)
                                                    + 2831760 * sin(12 * theta)
                                                    - 1789515 * sin(13 * theta)
                                                    + 2281140 * sin(14 * theta)
                                                    - 8554275 * sin(15 * theta)
                                                )
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(110670)
                                                * (
                                                    184041 * cos(theta)
                                                    + 174603 * cos(3 * theta)
                                                    + 154869 * cos(5 * theta)
                                                    + 122759 * cos(7 * theta)
                                                    + 73853 * cos(9 * theta)
                                                    - 2185 * cos(11 * theta)
                                                    - 137655 * cos(13 * theta)
                                                    - 570285 * cos(15 * theta)
                                                )
                                                / (268435456 * sqrt(pi))
                                            )
                        else:
                            if m <= 8:
                                if m <= 4:
                                    if m <= 2:
                                        if m <= 1:
                                            return (
                                                sqrt(7378)
                                                * (
                                                    -184041 * sin(theta)
                                                    + 736164 * sin(2 * theta)
                                                    - 523809 * sin(3 * theta)
                                                    + 1434576 * sin(4 * theta)
                                                    - 774345 * sin(5 * theta)
                                                    + 2054052 * sin(6 * theta)
                                                    - 859313 * sin(7 * theta)
                                                    + 2545088 * sin(8 * theta)
                                                    - 664677 * sin(9 * theta)
                                                    + 2840500 * sin(10 * theta)
                                                    + 24035 * sin(11 * theta)
                                                    + 2831760 * sin(12 * theta)
                                                    + 1789515 * sin(13 * theta)
                                                    + 2281140 * sin(14 * theta)
                                                    + 8554275 * sin(15 * theta)
                                                )
                                                * exp(1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(31)
                                                * (
                                                    21900879 * cos(theta)
                                                    + 1472328 * cos(2 * theta)
                                                    + 19380933 * cos(3 * theta)
                                                    + 5738304 * cos(4 * theta)
                                                    + 14712555 * cos(5 * theta)
                                                    + 12324312 * cos(6 * theta)
                                                    + 8715889 * cos(7 * theta)
                                                    + 20360704 * cos(8 * theta)
                                                    + 2880267 * cos(9 * theta)
                                                    + 28405000 * cos(10 * theta)
                                                    + 2185 * cos(11 * theta)
                                                    + 33981120 * cos(12 * theta)
                                                    + 6745095 * cos(13 * theta)
                                                    + 31935960 * cos(14 * theta)
                                                    + 59879925 * cos(15 * theta)
                                                )
                                                * exp(2 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 3:
                                            return (
                                                -3
                                                * sqrt(806)
                                                * (
                                                    561561 * sin(theta)
                                                    - 698412 * sin(2 * theta)
                                                    + 1526657 * sin(3 * theta)
                                                    - 1066736 * sin(4 * theta)
                                                    + 2045065 * sin(5 * theta)
                                                    - 825132 * sin(6 * theta)
                                                    + 1916929 * sin(7 * theta)
                                                    + 195776 * sin(8 * theta)
                                                    + 1119157 * sin(9 * theta)
                                                    + 1966500 * sin(10 * theta)
                                                    - 24035 * sin(11 * theta)
                                                    + 4090320 * sin(12 * theta)
                                                    - 321195 * sin(13 * theta)
                                                    + 5322660 * sin(14 * theta)
                                                    + 6653325 * sin(15 * theta)
                                                )
                                                * exp(3 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(45942)
                                                * (
                                                    561561 * cos(theta)
                                                    + 75504 * cos(2 * theta)
                                                    + 389499 * cos(3 * theta)
                                                    + 263296 * cos(4 * theta)
                                                    + 118085 * cos(5 * theta)
                                                    + 454608 * cos(6 * theta)
                                                    - 123753 * cos(7 * theta)
                                                    + 494592 * cos(8 * theta)
                                                    - 189267 * cos(9 * theta)
                                                    + 230000 * cos(10 * theta)
                                                    + 7015 * cos(11 * theta)
                                                    - 397440 * cos(12 * theta)
                                                    + 287385 * cos(13 * theta)
                                                    - 1120560 * cos(14 * theta)
                                                    - 1050525 * cos(15 * theta)
                                                )
                                                * exp(4 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                else:
                                    if m <= 6:
                                        if m <= 5:
                                            return (
                                                -sqrt(2526810)
                                                * (
                                                    51051 * sin(theta)
                                                    - 32604 * sin(2 * theta)
                                                    + 125763 * sin(3 * theta)
                                                    - 19888 * sin(4 * theta)
                                                    + 133019 * sin(5 * theta)
                                                    + 54180 * sin(6 * theta)
                                                    + 73059 * sin(7 * theta)
                                                    + 154560 * sin(8 * theta)
                                                    - 897 * sin(9 * theta)
                                                    + 190900 * sin(10 * theta)
                                                    + 1495 * sin(11 * theta)
                                                    + 49680 * sin(12 * theta)
                                                    + 118335 * sin(13 * theta)
                                                    - 280140 * sin(14 * theta)
                                                    - 210105 * sin(15 * theta)
                                                )
                                                * exp(5 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(589589)
                                                * (
                                                    51051 * cos(theta)
                                                    + 10296 * cos(2 * theta)
                                                    + 19129 * cos(3 * theta)
                                                    + 28864 * cos(4 * theta)
                                                    - 20425 * cos(5 * theta)
                                                    + 27816 * cos(6 * theta)
                                                    - 36139 * cos(7 * theta)
                                                    - 11776 * cos(8 * theta)
                                                    - 17641 * cos(9 * theta)
                                                    - 69000 * cos(10 * theta)
                                                    - 115 * cos(11 * theta)
                                                    - 66240 * cos(12 * theta)
                                                    - 45885 * cos(13 * theta)
                                                    + 80040 * cos(14 * theta)
                                                    + 50025 * cos(15 * theta)
                                                )
                                                * exp(6 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 7:
                                            return (
                                                -sqrt(107198)
                                                * (
                                                    357357 * sin(theta)
                                                    - 121836 * sin(2 * theta)
                                                    + 743589 * sin(3 * theta)
                                                    + 131472 * sin(4 * theta)
                                                    + 460845 * sin(5 * theta)
                                                    + 604692 * sin(6 * theta)
                                                    - 140651 * sin(7 * theta)
                                                    + 584384 * sin(8 * theta)
                                                    - 322023 * sin(9 * theta)
                                                    - 425500 * sin(10 * theta)
                                                    + 4945 * sin(11 * theta)
                                                    - 1341360 * sin(12 * theta)
                                                    - 601335 * sin(13 * theta)
                                                    + 840420 * sin(14 * theta)
                                                    + 450225 * sin(15 * theta)
                                                )
                                                * exp(7 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                sqrt(1232777)
                                                * (
                                                    51051 * cos(theta)
                                                    + 13728 * cos(2 * theta)
                                                    - 3663 * cos(3 * theta)
                                                    + 25344 * cos(4 * theta)
                                                    - 47025 * cos(5 * theta)
                                                    - 9504 * cos(6 * theta)
                                                    - 28187 * cos(7 * theta)
                                                    - 63488 * cos(8 * theta)
                                                    + 12519 * cos(9 * theta)
                                                    - 28000 * cos(10 * theta)
                                                    - 715 * cos(11 * theta)
                                                    + 103680 * cos(12 * theta)
                                                    + 35595 * cos(13 * theta)
                                                    - 41760 * cos(14 * theta)
                                                    - 19575 * cos(15 * theta)
                                                )
                                                * exp(8 * 1j * phi)
                                                / (268435456 * sqrt(pi))
                                            )
                            else:
                                if m <= 12:
                                    if m <= 10:
                                        if m <= 9:
                                            return (
                                                sqrt(1056666)
                                                * (
                                                    -153153 * sin(theta)
                                                    + 22308 * sin(2 * theta)
                                                    - 240537 * sin(3 * theta)
                                                    - 111408 * sin(4 * theta)
                                                    + 3135 * sin(5 * theta)
                                                    - 163548 * sin(6 * theta)
                                                    + 178423 * sin(7 * theta)
                                                    + 143808 * sin(8 * theta)
                                                    + 32227 * sin(9 * theta)
                                                    + 328500 * sin(10 * theta)
                                                    + 3595 * sin(11 * theta)
                                                    - 382320 * sin(12 * theta)
                                                    - 108045 * sin(13 * theta)
                                                    + 109620 * sin(14 * theta)
                                                    + 45675 * sin(15 * theta)
                                                )
                                                * exp(9 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                5
                                                * sqrt(176111)
                                                * (
                                                    51051 * cos(theta)
                                                    + 17160 * cos(2 * theta)
                                                    - 32967 * cos(3 * theta)
                                                    + 10560 * cos(4 * theta)
                                                    - 52041 * cos(5 * theta)
                                                    - 49896 * cos(6 * theta)
                                                    + 18389 * cos(7 * theta)
                                                    - 25088 * cos(8 * theta)
                                                    + 25623 * cos(9 * theta)
                                                    + 100040 * cos(10 * theta)
                                                    + 781 * cos(11 * theta)
                                                    - 67392 * cos(12 * theta)
                                                    - 16317 * cos(13 * theta)
                                                    + 14616 * cos(14 * theta)
                                                    + 5481 * cos(15 * theta)
                                                )
                                                * exp(10 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        if m <= 11:
                                            return (
                                                -sqrt(135470)
                                                * (
                                                    561561 * sin(theta)
                                                    + 1716 * sin(2 * theta)
                                                    + 523809 * sin(3 * theta)
                                                    + 418704 * sin(4 * theta)
                                                    - 529815 * sin(5 * theta)
                                                    - 108108 * sin(6 * theta)
                                                    - 277823 * sin(7 * theta)
                                                    - 832832 * sin(8 * theta)
                                                    + 364533 * sin(9 * theta)
                                                    + 1015300 * sin(10 * theta)
                                                    + 6397 * sin(11 * theta)
                                                    - 470448 * sin(12 * theta)
                                                    - 100107 * sin(13 * theta)
                                                    + 80388 * sin(14 * theta)
                                                    + 27405 * sin(15 * theta)
                                                )
                                                * exp(11 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(406410)
                                                * (
                                                    51051 * cos(theta)
                                                    + 20592 * cos(2 * theta)
                                                    - 68783 * cos(3 * theta)
                                                    - 18304 * cos(4 * theta)
                                                    - 13585 * cos(5 * theta)
                                                    - 48048 * cos(6 * theta)
                                                    + 58149 * cos(7 * theta)
                                                    + 93184 * cos(8 * theta)
                                                    - 29913 * cos(9 * theta)
                                                    - 67600 * cos(10 * theta)
                                                    - 363 * cos(11 * theta)
                                                    + 23424 * cos(12 * theta)
                                                    + 4459 * cos(13 * theta)
                                                    - 3248 * cos(14 * theta)
                                                    - 1015 * cos(15 * theta)
                                                )
                                                * exp(12 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                else:
                                    if m <= 14:
                                        if m <= 13:
                                            return (
                                                -3
                                                * sqrt(948290)
                                                * (
                                                    94809 * sin(theta)
                                                    + 12012 * sin(2 * theta)
                                                    + 15873 * sin(3 * theta)
                                                    + 38896 * sin(4 * theta)
                                                    - 95095 * sin(5 * theta)
                                                    - 97812 * sin(6 * theta)
                                                    + 76609 * sin(7 * theta)
                                                    + 94016 * sin(8 * theta)
                                                    - 24843 * sin(9 * theta)
                                                    - 48100 * sin(10 * theta)
                                                    - 227 * sin(11 * theta)
                                                    + 13104 * sin(12 * theta)
                                                    + 2261 * sin(13 * theta)
                                                    - 1508 * sin(14 * theta)
                                                    - 435 * sin(15 * theta)
                                                )
                                                * exp(13 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                3
                                                * sqrt(13750205)
                                                * (
                                                    7293 * cos(theta)
                                                    + 3432 * cos(2 * theta)
                                                    - 15873 * cos(3 * theta)
                                                    - 9152 * cos(4 * theta)
                                                    + 13585 * cos(5 * theta)
                                                    + 10296 * cos(6 * theta)
                                                    - 6461 * cos(7 * theta)
                                                    - 6656 * cos(8 * theta)
                                                    + 1521 * cos(9 * theta)
                                                    + 2600 * cos(10 * theta)
                                                    + 11 * cos(11 * theta)
                                                    - 576 * cos(12 * theta)
                                                    - 91 * cos(13 * theta)
                                                    + 56 * cos(14 * theta)
                                                    + 15 * cos(15 * theta)
                                                )
                                                * exp(14 * 1j * phi)
                                                / (536870912 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            -15
                                            * sqrt(16500246)
                                            * (
                                                7293 * sin(theta)
                                                + 1716 * sin(2 * theta)
                                                - 5291 * sin(3 * theta)
                                                - 2288 * sin(4 * theta)
                                                + 2717 * sin(5 * theta)
                                                + 1716 * sin(6 * theta)
                                                - 923 * sin(7 * theta)
                                                - 832 * sin(8 * theta)
                                                + 169 * sin(9 * theta)
                                                + 260 * sin(10 * theta)
                                                + sin(11 * theta)
                                                - 48 * sin(12 * theta)
                                                - 7 * sin(13 * theta)
                                                + 4 * sin(14 * theta)
                                                + sin(15 * theta)
                                            )
                                            * exp(15 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                else:
                    if m <= 0:
                        if m <= -8:
                            if m <= -12:
                                if m <= -14:
                                    if m <= -15:
                                        if m <= -16:
                                            return (
                                                15
                                                * sqrt(4321493)
                                                * (
                                                    1716
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(theta)
                                                    + 12584
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(2 * theta)
                                                    - 4004
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(3 * theta)
                                                    - 8008
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(4 * theta)
                                                    + 4004
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(5 * theta)
                                                    + 3640
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(6 * theta)
                                                    - 2548
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(7 * theta)
                                                    - 1092
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(8 * theta)
                                                    + 1092
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(9 * theta)
                                                    + 168
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(10 * theta)
                                                    - 308
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(11 * theta)
                                                    + 8
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(12 * theta)
                                                    + 52
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(13 * theta)
                                                    - 8
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(14 * theta)
                                                    - 4
                                                    * 1j
                                                    * sin(16 * phi)
                                                    * cos(15 * theta)
                                                    + 1j
                                                    * sin(16 * phi)
                                                    * cos(16 * theta)
                                                    - 7293 * 1j * sin(16 * phi)
                                                    - 1716 * cos(16 * phi) * cos(theta)
                                                    - 12584
                                                    * cos(16 * phi)
                                                    * cos(2 * theta)
                                                    + 4004
                                                    * cos(16 * phi)
                                                    * cos(3 * theta)
                                                    + 8008
                                                    * cos(16 * phi)
                                                    * cos(4 * theta)
                                                    - 4004
                                                    * cos(16 * phi)
                                                    * cos(5 * theta)
                                                    - 3640
                                                    * cos(16 * phi)
                                                    * cos(6 * theta)
                                                    + 2548
                                                    * cos(16 * phi)
                                                    * cos(7 * theta)
                                                    + 1092
                                                    * cos(16 * phi)
                                                    * cos(8 * theta)
                                                    - 1092
                                                    * cos(16 * phi)
                                                    * cos(9 * theta)
                                                    - 168
                                                    * cos(16 * phi)
                                                    * cos(10 * theta)
                                                    + 308
                                                    * cos(16 * phi)
                                                    * cos(11 * theta)
                                                    - 8
                                                    * cos(16 * phi)
                                                    * cos(12 * theta)
                                                    - 52
                                                    * cos(16 * phi)
                                                    * cos(13 * theta)
                                                    + 8
                                                    * cos(16 * phi)
                                                    * cos(14 * theta)
                                                    + 4
                                                    * cos(16 * phi)
                                                    * cos(15 * theta)
                                                    - cos(16 * phi) * cos(16 * theta)
                                                    + 7293 * cos(16 * phi)
                                                )
                                                / (1073741824 * sqrt(pi))
                                            )
                                        else:
                                            return (
                                                15
                                                * sqrt(8642986)
                                                * (
                                                    429 * sin(theta)
                                                    + 6292 * sin(2 * theta)
                                                    - 3003 * sin(3 * theta)
                                                    - 8008 * sin(4 * theta)
                                                    + 5005 * sin(5 * theta)
                                                    + 5460 * sin(6 * theta)
                                                    - 4459 * sin(7 * theta)
                                                    - 2184 * sin(8 * theta)
                                                    + 2457 * sin(9 * theta)
                                                    + 420 * sin(10 * theta)
                                                    - 847 * sin(11 * theta)
                                                    + 24 * sin(12 * theta)
                                                    + 169 * sin(13 * theta)
                                                    - 28 * sin(14 * theta)
                                                    - 15 * sin(15 * theta)
                                                    + 4 * sin(16 * theta)
                                                )
                                                * exp(-15 * 1j * phi)
                                                / (1073741824 * sqrt(pi))
                                            )
                                    else:
                                        return (
                                            15
                                            * sqrt(139403)
                                            * (
                                                3003 * 1j * sin(14 * phi) * cos(theta)
                                                + 12584
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(2 * theta)
                                                + 1001
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(3 * theta)
                                                + 16016
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(4 * theta)
                                                - 17017
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(5 * theta)
                                                - 25480
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(6 * theta)
                                                + 26117
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(7 * theta)
                                                + 15288
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(8 * theta)
                                                - 19929
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(9 * theta)
                                                - 3864
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(10 * theta)
                                                + 8701
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(11 * theta)
                                                - 272
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(12 * theta)
                                                - 2093
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(13 * theta)
                                                + 376
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(14 * theta)
                                                + 217
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(15 * theta)
                                                - 62
                                                * 1j
                                                * sin(14 * phi)
                                                * cos(16 * theta)
                                                - 14586 * 1j * sin(14 * phi)
                                                - 3003 * cos(14 * phi) * cos(theta)
                                                - 12584 * cos(14 * phi) * cos(2 * theta)
                                                - 1001 * cos(14 * phi) * cos(3 * theta)
                                                - 16016 * cos(14 * phi) * cos(4 * theta)
                                                + 17017 * cos(14 * phi) * cos(5 * theta)
                                                + 25480 * cos(14 * phi) * cos(6 * theta)
                                                - 26117 * cos(14 * phi) * cos(7 * theta)
                                                - 15288 * cos(14 * phi) * cos(8 * theta)
                                                + 19929 * cos(14 * phi) * cos(9 * theta)
                                                + 3864 * cos(14 * phi) * cos(10 * theta)
                                                - 8701 * cos(14 * phi) * cos(11 * theta)
                                                + 272 * cos(14 * phi) * cos(12 * theta)
                                                + 2093 * cos(14 * phi) * cos(13 * theta)
                                                - 376 * cos(14 * phi) * cos(14 * theta)
                                                - 217 * cos(14 * phi) * cos(15 * theta)
                                                + 62 * cos(14 * phi) * cos(16 * theta)
                                                + 14586 * cos(14 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= -13:
                                        return (
                                            3
                                            * sqrt(1394030)
                                            * (
                                                6435 * sin(theta)
                                                + 81796 * sin(2 * theta)
                                                - 29029 * sin(3 * theta)
                                                - 40040 * sin(4 * theta)
                                                - 5005 * sin(5 * theta)
                                                - 45500 * sin(6 * theta)
                                                + 75803 * sin(7 * theta)
                                                + 58968 * sin(8 * theta)
                                                - 94185 * sin(9 * theta)
                                                - 21420 * sin(10 * theta)
                                                + 55055 * sin(11 * theta)
                                                - 1928 * sin(12 * theta)
                                                - 16393 * sin(13 * theta)
                                                + 3220 * sin(14 * theta)
                                                + 2015 * sin(15 * theta)
                                                - 620 * sin(16 * theta)
                                            )
                                            * exp(-13 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(48070)
                                            * (
                                                19305 * 1j * sin(12 * phi) * cos(theta)
                                                + 12584
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(2 * theta)
                                                + 51051
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(3 * theta)
                                                + 200200
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(4 * theta)
                                                - 115115
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(5 * theta)
                                                - 54600
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(6 * theta)
                                                - 69433
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(7 * theta)
                                                - 121212
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(8 * theta)
                                                + 274365
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(9 * theta)
                                                + 78120
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(10 * theta)
                                                - 237545
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(11 * theta)
                                                + 9528
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(12 * theta)
                                                + 90857
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(13 * theta)
                                                - 19720
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(14 * theta)
                                                - 13485
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(15 * theta)
                                                + 4495
                                                * 1j
                                                * sin(12 * phi)
                                                * cos(16 * theta)
                                                - 109395 * 1j * sin(12 * phi)
                                                - 19305 * cos(12 * phi) * cos(theta)
                                                - 12584 * cos(12 * phi) * cos(2 * theta)
                                                - 51051 * cos(12 * phi) * cos(3 * theta)
                                                - 200200
                                                * cos(12 * phi)
                                                * cos(4 * theta)
                                                + 115115
                                                * cos(12 * phi)
                                                * cos(5 * theta)
                                                + 54600 * cos(12 * phi) * cos(6 * theta)
                                                + 69433 * cos(12 * phi) * cos(7 * theta)
                                                + 121212
                                                * cos(12 * phi)
                                                * cos(8 * theta)
                                                - 274365
                                                * cos(12 * phi)
                                                * cos(9 * theta)
                                                - 78120
                                                * cos(12 * phi)
                                                * cos(10 * theta)
                                                + 237545
                                                * cos(12 * phi)
                                                * cos(11 * theta)
                                                - 9528 * cos(12 * phi) * cos(12 * theta)
                                                - 90857
                                                * cos(12 * phi)
                                                * cos(13 * theta)
                                                + 19720
                                                * cos(12 * phi)
                                                * cos(14 * theta)
                                                + 13485
                                                * cos(12 * phi)
                                                * cos(15 * theta)
                                                - 4495 * cos(12 * phi) * cos(16 * theta)
                                                + 109395 * cos(12 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                            else:
                                if m <= -10:
                                    if m <= -11:
                                        return (
                                            15
                                            * sqrt(67298)
                                            * (
                                                6435 * sin(theta)
                                                + 69212 * sin(2 * theta)
                                                - 15301 * sin(3 * theta)
                                                + 12584 * sin(4 * theta)
                                                - 37037 * sin(5 * theta)
                                                - 56420 * sin(6 * theta)
                                                + 35035 * sin(7 * theta)
                                                - 6552 * sin(8 * theta)
                                                + 63063 * sin(9 * theta)
                                                + 26892 * sin(10 * theta)
                                                - 103697 * sin(11 * theta)
                                                + 4936 * sin(12 * theta)
                                                + 53911 * sin(13 * theta)
                                                - 13108 * sin(14 * theta)
                                                - 9889 * sin(15 * theta)
                                                + 3596 * sin(16 * theta)
                                            )
                                            * exp(-11 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            15
                                            * sqrt(33649)
                                            * (
                                                3575 * 1j * sin(10 * phi) * cos(theta)
                                                - 12584
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(2 * theta)
                                                + 16445
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(3 * theta)
                                                + 38896
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(4 * theta)
                                                - 5005
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(5 * theta)
                                                + 25480
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(6 * theta)
                                                - 42679
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(7 * theta)
                                                - 21112
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(8 * theta)
                                                - 2093
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(9 * theta)
                                                - 12520
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(10 * theta)
                                                + 73953
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(11 * theta)
                                                - 4464
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(12 * theta)
                                                - 57681
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(13 * theta)
                                                + 16008
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(14 * theta)
                                                + 13485
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(15 * theta)
                                                - 5394
                                                * 1j
                                                * sin(10 * phi)
                                                * cos(16 * theta)
                                                - 24310 * 1j * sin(10 * phi)
                                                - 3575 * cos(10 * phi) * cos(theta)
                                                + 12584 * cos(10 * phi) * cos(2 * theta)
                                                - 16445 * cos(10 * phi) * cos(3 * theta)
                                                - 38896 * cos(10 * phi) * cos(4 * theta)
                                                + 5005 * cos(10 * phi) * cos(5 * theta)
                                                - 25480 * cos(10 * phi) * cos(6 * theta)
                                                + 42679 * cos(10 * phi) * cos(7 * theta)
                                                + 21112 * cos(10 * phi) * cos(8 * theta)
                                                + 2093 * cos(10 * phi) * cos(9 * theta)
                                                + 12520
                                                * cos(10 * phi)
                                                * cos(10 * theta)
                                                - 73953
                                                * cos(10 * phi)
                                                * cos(11 * theta)
                                                + 4464 * cos(10 * phi) * cos(12 * theta)
                                                + 57681
                                                * cos(10 * phi)
                                                * cos(13 * theta)
                                                - 16008
                                                * cos(10 * phi)
                                                * cos(14 * theta)
                                                - 13485
                                                * cos(10 * phi)
                                                * cos(15 * theta)
                                                + 5394 * cos(10 * phi) * cos(16 * theta)
                                                + 24310 * cos(10 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= -9:
                                        return (
                                            15
                                            * sqrt(124982)
                                            * (
                                                5005 * sin(theta)
                                                + 44044 * sin(2 * theta)
                                                - 3003 * sin(3 * theta)
                                                + 32648 * sin(4 * theta)
                                                - 29491 * sin(5 * theta)
                                                - 15540 * sin(6 * theta)
                                                - 21707 * sin(7 * theta)
                                                - 30520 * sin(8 * theta)
                                                + 40761 * sin(9 * theta)
                                                - 644 * sin(10 * theta)
                                                + 53361 * sin(11 * theta)
                                                - 4824 * sin(12 * theta)
                                                - 78039 * sin(13 * theta)
                                                + 25404 * sin(14 * theta)
                                                + 24273 * sin(15 * theta)
                                                - 10788 * sin(16 * theta)
                                            )
                                            * exp(-9 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(62491)
                                            * (
                                                10010 * 1j * sin(8 * phi) * cos(theta)
                                                - 88088
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(2 * theta)
                                                + 62062
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(3 * theta)
                                                + 70840
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(4 * theta)
                                                + 56210
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(5 * theta)
                                                + 135800
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(6 * theta)
                                                - 73402
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(7 * theta)
                                                + 48188
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(8 * theta)
                                                - 190750
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(9 * theta)
                                                - 40600
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(10 * theta)
                                                - 34650
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(11 * theta)
                                                + 13320
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(12 * theta)
                                                + 305370
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(13 * theta)
                                                - 121800
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(14 * theta)
                                                - 134850
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(15 * theta)
                                                + 67425
                                                * 1j
                                                * sin(8 * phi)
                                                * cos(16 * theta)
                                                - 85085 * 1j * sin(8 * phi)
                                                - 10010 * cos(8 * phi) * cos(theta)
                                                + 88088 * cos(8 * phi) * cos(2 * theta)
                                                - 62062 * cos(8 * phi) * cos(3 * theta)
                                                - 70840 * cos(8 * phi) * cos(4 * theta)
                                                - 56210 * cos(8 * phi) * cos(5 * theta)
                                                - 135800 * cos(8 * phi) * cos(6 * theta)
                                                + 73402 * cos(8 * phi) * cos(7 * theta)
                                                - 48188 * cos(8 * phi) * cos(8 * theta)
                                                + 190750 * cos(8 * phi) * cos(9 * theta)
                                                + 40600 * cos(8 * phi) * cos(10 * theta)
                                                + 34650 * cos(8 * phi) * cos(11 * theta)
                                                - 13320 * cos(8 * phi) * cos(12 * theta)
                                                - 305370
                                                * cos(8 * phi)
                                                * cos(13 * theta)
                                                + 121800
                                                * cos(8 * phi)
                                                * cos(14 * theta)
                                                + 134850
                                                * cos(8 * phi)
                                                * cos(15 * theta)
                                                - 67425 * cos(8 * phi) * cos(16 * theta)
                                                + 85085 * cos(8 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                        else:
                            if m <= -4:
                                if m <= -6:
                                    if m <= -7:
                                        return (
                                            sqrt(374946)
                                            * (
                                                45045 * sin(theta)
                                                + 308308 * sin(2 * theta)
                                                + 37037 * sin(3 * theta)
                                                + 366520 * sin(4 * theta)
                                                - 152075 * sin(5 * theta)
                                                + 142100 * sin(6 * theta)
                                                - 352163 * sin(7 * theta)
                                                - 125832 * sin(8 * theta)
                                                - 232575 * sin(9 * theta)
                                                - 140700 * sin(10 * theta)
                                                + 317625 * sin(11 * theta)
                                                + 13080 * sin(12 * theta)
                                                + 672945 * sin(13 * theta)
                                                - 356700 * sin(14 * theta)
                                                - 471975 * sin(15 * theta)
                                                + 269700 * sin(16 * theta)
                                            )
                                            * exp(-7 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(40755)
                                            * (
                                                27027 * 1j * sin(6 * phi) * cos(theta)
                                                - 440440
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(2 * theta)
                                                + 201201
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(3 * theta)
                                                - 38192
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(4 * theta)
                                                + 354431
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(5 * theta)
                                                + 318360
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(6 * theta)
                                                + 228781
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(7 * theta)
                                                + 374808
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(8 * theta)
                                                - 268065
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(9 * theta)
                                                + 135240
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(10 * theta)
                                                - 823515
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(11 * theta)
                                                + 16560
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(12 * theta)
                                                - 650325
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(13 * theta)
                                                + 560280
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(14 * theta)
                                                + 930465
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(15 * theta)
                                                - 620310
                                                * 1j
                                                * sin(6 * phi)
                                                * cos(16 * theta)
                                                - 306306 * 1j * sin(6 * phi)
                                                - 27027 * cos(6 * phi) * cos(theta)
                                                + 440440 * cos(6 * phi) * cos(2 * theta)
                                                - 201201 * cos(6 * phi) * cos(3 * theta)
                                                + 38192 * cos(6 * phi) * cos(4 * theta)
                                                - 354431 * cos(6 * phi) * cos(5 * theta)
                                                - 318360 * cos(6 * phi) * cos(6 * theta)
                                                - 228781 * cos(6 * phi) * cos(7 * theta)
                                                - 374808 * cos(6 * phi) * cos(8 * theta)
                                                + 268065 * cos(6 * phi) * cos(9 * theta)
                                                - 135240
                                                * cos(6 * phi)
                                                * cos(10 * theta)
                                                + 823515
                                                * cos(6 * phi)
                                                * cos(11 * theta)
                                                - 16560 * cos(6 * phi) * cos(12 * theta)
                                                + 650325
                                                * cos(6 * phi)
                                                * cos(13 * theta)
                                                - 560280
                                                * cos(6 * phi)
                                                * cos(14 * theta)
                                                - 930465
                                                * cos(6 * phi)
                                                * cos(15 * theta)
                                                + 620310
                                                * cos(6 * phi)
                                                * cos(16 * theta)
                                                + 306306 * cos(6 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= -5:
                                        return (
                                            sqrt(81510)
                                            * (
                                                99099 * sin(theta)
                                                + 484484 * sin(2 * theta)
                                                + 187187 * sin(3 * theta)
                                                + 738584 * sin(4 * theta)
                                                + 4235 * sin(5 * theta)
                                                + 644420 * sin(6 * theta)
                                                - 445165 * sin(7 * theta)
                                                + 282072 * sin(8 * theta)
                                                - 924945 * sin(9 * theta)
                                                - 48300 * sin(10 * theta)
                                                - 982905 * sin(11 * theta)
                                                + 63480 * sin(12 * theta)
                                                - 130065 * sin(13 * theta)
                                                + 680340 * sin(14 * theta)
                                                + 1550775 * sin(15 * theta)
                                                - 1240620 * sin(16 * theta)
                                            )
                                            * exp(-5 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(570570)
                                            * (
                                                4719 * 1j * sin(4 * phi) * cos(theta)
                                                - 138424
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(2 * theta)
                                                + 39325
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(3 * theta)
                                                - 80344
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(4 * theta)
                                                + 92323
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(5 * theta)
                                                - 8680
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(6 * theta)
                                                + 134113
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(7 * theta)
                                                + 44436
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(8 * theta)
                                                + 127995
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(9 * theta)
                                                + 46920
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(10 * theta)
                                                + 41745
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(11 * theta)
                                                - 13800
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(12 * theta)
                                                - 130065
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(13 * theta)
                                                - 80040
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(14 * theta)
                                                - 310155
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(15 * theta)
                                                + 310155
                                                * 1j
                                                * sin(4 * phi)
                                                * cos(16 * theta)
                                                - 80223 * 1j * sin(4 * phi)
                                                - 4719 * cos(4 * phi) * cos(theta)
                                                + 138424 * cos(4 * phi) * cos(2 * theta)
                                                - 39325 * cos(4 * phi) * cos(3 * theta)
                                                + 80344 * cos(4 * phi) * cos(4 * theta)
                                                - 92323 * cos(4 * phi) * cos(5 * theta)
                                                + 8680 * cos(4 * phi) * cos(6 * theta)
                                                - 134113 * cos(4 * phi) * cos(7 * theta)
                                                - 44436 * cos(4 * phi) * cos(8 * theta)
                                                - 127995 * cos(4 * phi) * cos(9 * theta)
                                                - 46920 * cos(4 * phi) * cos(10 * theta)
                                                - 41745 * cos(4 * phi) * cos(11 * theta)
                                                + 13800 * cos(4 * phi) * cos(12 * theta)
                                                + 130065
                                                * cos(4 * phi)
                                                * cos(13 * theta)
                                                + 80040 * cos(4 * phi) * cos(14 * theta)
                                                + 310155
                                                * cos(4 * phi)
                                                * cos(15 * theta)
                                                - 310155
                                                * cos(4 * phi)
                                                * cos(16 * theta)
                                                + 80223 * cos(4 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                            else:
                                if m <= -2:
                                    if m <= -3:
                                        return (
                                            sqrt(8778)
                                            * (
                                                306735 * sin(theta)
                                                + 899756 * sin(2 * theta)
                                                + 797511 * sin(3 * theta)
                                                + 1573000 * sin(4 * theta)
                                                + 935935 * sin(5 * theta)
                                                + 1829100 * sin(6 * theta)
                                                + 542087 * sin(7 * theta)
                                                + 1557192 * sin(8 * theta)
                                                - 470925 * sin(9 * theta)
                                                + 793500 * sin(10 * theta)
                                                - 2030325 * sin(11 * theta)
                                                - 140760 * sin(12 * theta)
                                                - 3771885 * sin(13 * theta)
                                                - 200100 * sin(14 * theta)
                                                - 4652325 * sin(15 * theta)
                                                + 6203100 * sin(16 * theta)
                                            )
                                            * exp(-3 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(33)
                                            * (
                                                306735 * 1j * sin(2 * phi) * cos(theta)
                                                - 19794632
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(2 * theta)
                                                + 2719717
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(3 * theta)
                                                - 16736720
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(4 * theta)
                                                + 7322315
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(5 * theta)
                                                - 12103000
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(6 * theta)
                                                + 13640081
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(7 * theta)
                                                - 6680856
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(8 * theta)
                                                + 20877675
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(9 * theta)
                                                - 1835400
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(10 * theta)
                                                + 27760425
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(11 * theta)
                                                - 104880
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(12 * theta)
                                                + 32126055
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(13 * theta)
                                                - 7603800
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(14 * theta)
                                                + 29464725
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(15 * theta)
                                                - 58929450
                                                * 1j
                                                * sin(2 * phi)
                                                * cos(16 * theta)
                                                - 10428990 * 1j * sin(2 * phi)
                                                - 306735 * cos(2 * phi) * cos(theta)
                                                + 19794632
                                                * cos(2 * phi)
                                                * cos(2 * theta)
                                                - 2719717
                                                * cos(2 * phi)
                                                * cos(3 * theta)
                                                + 16736720
                                                * cos(2 * phi)
                                                * cos(4 * theta)
                                                - 7322315
                                                * cos(2 * phi)
                                                * cos(5 * theta)
                                                + 12103000
                                                * cos(2 * phi)
                                                * cos(6 * theta)
                                                - 13640081
                                                * cos(2 * phi)
                                                * cos(7 * theta)
                                                + 6680856
                                                * cos(2 * phi)
                                                * cos(8 * theta)
                                                - 20877675
                                                * cos(2 * phi)
                                                * cos(9 * theta)
                                                + 1835400
                                                * cos(2 * phi)
                                                * cos(10 * theta)
                                                - 27760425
                                                * cos(2 * phi)
                                                * cos(11 * theta)
                                                + 104880
                                                * cos(2 * phi)
                                                * cos(12 * theta)
                                                - 32126055
                                                * cos(2 * phi)
                                                * cos(13 * theta)
                                                + 7603800
                                                * cos(2 * phi)
                                                * cos(14 * theta)
                                                - 29464725
                                                * cos(2 * phi)
                                                * cos(15 * theta)
                                                + 58929450
                                                * cos(2 * phi)
                                                * cos(16 * theta)
                                                + 10428990 * cos(2 * phi)
                                            )
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= -1:
                                        return (
                                            -3
                                            * sqrt(110)
                                            * (1j * sin(phi) - cos(phi))
                                            * (
                                                920205 * sin(theta)
                                                + 899756 * sin(2 * theta)
                                                + 2719717 * sin(3 * theta)
                                                + 1673672 * sin(4 * theta)
                                                + 4393389 * sin(5 * theta)
                                                + 2178540 * sin(6 * theta)
                                                + 5845749 * sin(7 * theta)
                                                + 2226952 * sin(8 * theta)
                                                + 6959225 * sin(9 * theta)
                                                + 1529500 * sin(10 * theta)
                                                + 7571025 * sin(11 * theta)
                                                - 471960 * sin(12 * theta)
                                                + 7413705 * sin(13 * theta)
                                                - 5322660 * sin(14 * theta)
                                                + 5892945 * sin(15 * theta)
                                                - 23571780 * sin(16 * theta)
                                            )
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(1870)
                                            * (
                                                1799512 * cos(2 * theta)
                                                + 1673672 * cos(4 * theta)
                                                + 1452360 * cos(6 * theta)
                                                + 1113476 * cos(8 * theta)
                                                + 611800 * cos(10 * theta)
                                                - 157320 * cos(12 * theta)
                                                - 1520760 * cos(14 * theta)
                                                - 5892945 * cos(16 * theta)
                                                + 920205
                                            )
                                            / (1073741824 * sqrt(pi))
                                        )
                    else:
                        if m <= 8:
                            if m <= 4:
                                if m <= 2:
                                    if m <= 1:
                                        return (
                                            3
                                            * sqrt(110)
                                            * (
                                                920205 * sin(theta)
                                                - 899756 * sin(2 * theta)
                                                + 2719717 * sin(3 * theta)
                                                - 1673672 * sin(4 * theta)
                                                + 4393389 * sin(5 * theta)
                                                - 2178540 * sin(6 * theta)
                                                + 5845749 * sin(7 * theta)
                                                - 2226952 * sin(8 * theta)
                                                + 6959225 * sin(9 * theta)
                                                - 1529500 * sin(10 * theta)
                                                + 7571025 * sin(11 * theta)
                                                + 471960 * sin(12 * theta)
                                                + 7413705 * sin(13 * theta)
                                                + 5322660 * sin(14 * theta)
                                                + 5892945 * sin(15 * theta)
                                                + 23571780 * sin(16 * theta)
                                            )
                                            * exp(1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(33)
                                            * (
                                                306735 * cos(theta)
                                                + 19794632 * cos(2 * theta)
                                                + 2719717 * cos(3 * theta)
                                                + 16736720 * cos(4 * theta)
                                                + 7322315 * cos(5 * theta)
                                                + 12103000 * cos(6 * theta)
                                                + 13640081 * cos(7 * theta)
                                                + 6680856 * cos(8 * theta)
                                                + 20877675 * cos(9 * theta)
                                                + 1835400 * cos(10 * theta)
                                                + 27760425 * cos(11 * theta)
                                                + 104880 * cos(12 * theta)
                                                + 32126055 * cos(13 * theta)
                                                + 7603800 * cos(14 * theta)
                                                + 29464725 * cos(15 * theta)
                                                + 58929450 * cos(16 * theta)
                                                + 10428990
                                            )
                                            * exp(2 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= 3:
                                        return (
                                            -sqrt(8778)
                                            * (
                                                -306735 * sin(theta)
                                                + 899756 * sin(2 * theta)
                                                - 797511 * sin(3 * theta)
                                                + 1573000 * sin(4 * theta)
                                                - 935935 * sin(5 * theta)
                                                + 1829100 * sin(6 * theta)
                                                - 542087 * sin(7 * theta)
                                                + 1557192 * sin(8 * theta)
                                                + 470925 * sin(9 * theta)
                                                + 793500 * sin(10 * theta)
                                                + 2030325 * sin(11 * theta)
                                                - 140760 * sin(12 * theta)
                                                + 3771885 * sin(13 * theta)
                                                - 200100 * sin(14 * theta)
                                                + 4652325 * sin(15 * theta)
                                                + 6203100 * sin(16 * theta)
                                            )
                                            * exp(3 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(570570)
                                            * (
                                                4719 * cos(theta)
                                                + 138424 * cos(2 * theta)
                                                + 39325 * cos(3 * theta)
                                                + 80344 * cos(4 * theta)
                                                + 92323 * cos(5 * theta)
                                                + 8680 * cos(6 * theta)
                                                + 134113 * cos(7 * theta)
                                                - 44436 * cos(8 * theta)
                                                + 127995 * cos(9 * theta)
                                                - 46920 * cos(10 * theta)
                                                + 41745 * cos(11 * theta)
                                                + 13800 * cos(12 * theta)
                                                - 130065 * cos(13 * theta)
                                                + 80040 * cos(14 * theta)
                                                - 310155 * cos(15 * theta)
                                                - 310155 * cos(16 * theta)
                                                + 80223
                                            )
                                            * exp(4 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                            else:
                                if m <= 6:
                                    if m <= 5:
                                        return (
                                            -sqrt(81510)
                                            * (
                                                -99099 * sin(theta)
                                                + 484484 * sin(2 * theta)
                                                - 187187 * sin(3 * theta)
                                                + 738584 * sin(4 * theta)
                                                - 4235 * sin(5 * theta)
                                                + 644420 * sin(6 * theta)
                                                + 445165 * sin(7 * theta)
                                                + 282072 * sin(8 * theta)
                                                + 924945 * sin(9 * theta)
                                                - 48300 * sin(10 * theta)
                                                + 982905 * sin(11 * theta)
                                                + 63480 * sin(12 * theta)
                                                + 130065 * sin(13 * theta)
                                                + 680340 * sin(14 * theta)
                                                - 1550775 * sin(15 * theta)
                                                - 1240620 * sin(16 * theta)
                                            )
                                            * exp(5 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            sqrt(40755)
                                            * (
                                                27027 * cos(theta)
                                                + 440440 * cos(2 * theta)
                                                + 201201 * cos(3 * theta)
                                                + 38192 * cos(4 * theta)
                                                + 354431 * cos(5 * theta)
                                                - 318360 * cos(6 * theta)
                                                + 228781 * cos(7 * theta)
                                                - 374808 * cos(8 * theta)
                                                - 268065 * cos(9 * theta)
                                                - 135240 * cos(10 * theta)
                                                - 823515 * cos(11 * theta)
                                                - 16560 * cos(12 * theta)
                                                - 650325 * cos(13 * theta)
                                                - 560280 * cos(14 * theta)
                                                + 930465 * cos(15 * theta)
                                                + 620310 * cos(16 * theta)
                                                + 306306
                                            )
                                            * exp(6 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= 7:
                                        return (
                                            -sqrt(374946)
                                            * (
                                                -45045 * sin(theta)
                                                + 308308 * sin(2 * theta)
                                                - 37037 * sin(3 * theta)
                                                + 366520 * sin(4 * theta)
                                                + 152075 * sin(5 * theta)
                                                + 142100 * sin(6 * theta)
                                                + 352163 * sin(7 * theta)
                                                - 125832 * sin(8 * theta)
                                                + 232575 * sin(9 * theta)
                                                - 140700 * sin(10 * theta)
                                                - 317625 * sin(11 * theta)
                                                + 13080 * sin(12 * theta)
                                                - 672945 * sin(13 * theta)
                                                - 356700 * sin(14 * theta)
                                                + 471975 * sin(15 * theta)
                                                + 269700 * sin(16 * theta)
                                            )
                                            * exp(7 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(62491)
                                            * (
                                                10010 * cos(theta)
                                                + 88088 * cos(2 * theta)
                                                + 62062 * cos(3 * theta)
                                                - 70840 * cos(4 * theta)
                                                + 56210 * cos(5 * theta)
                                                - 135800 * cos(6 * theta)
                                                - 73402 * cos(7 * theta)
                                                - 48188 * cos(8 * theta)
                                                - 190750 * cos(9 * theta)
                                                + 40600 * cos(10 * theta)
                                                - 34650 * cos(11 * theta)
                                                - 13320 * cos(12 * theta)
                                                + 305370 * cos(13 * theta)
                                                + 121800 * cos(14 * theta)
                                                - 134850 * cos(15 * theta)
                                                - 67425 * cos(16 * theta)
                                                + 85085
                                            )
                                            * exp(8 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                        else:
                            if m <= 12:
                                if m <= 10:
                                    if m <= 9:
                                        return (
                                            15
                                            * sqrt(124982)
                                            * (
                                                5005 * sin(theta)
                                                - 44044 * sin(2 * theta)
                                                - 3003 * sin(3 * theta)
                                                - 32648 * sin(4 * theta)
                                                - 29491 * sin(5 * theta)
                                                + 15540 * sin(6 * theta)
                                                - 21707 * sin(7 * theta)
                                                + 30520 * sin(8 * theta)
                                                + 40761 * sin(9 * theta)
                                                + 644 * sin(10 * theta)
                                                + 53361 * sin(11 * theta)
                                                + 4824 * sin(12 * theta)
                                                - 78039 * sin(13 * theta)
                                                - 25404 * sin(14 * theta)
                                                + 24273 * sin(15 * theta)
                                                + 10788 * sin(16 * theta)
                                            )
                                            * exp(9 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            15
                                            * sqrt(33649)
                                            * (
                                                3575 * cos(theta)
                                                + 12584 * cos(2 * theta)
                                                + 16445 * cos(3 * theta)
                                                - 38896 * cos(4 * theta)
                                                - 5005 * cos(5 * theta)
                                                - 25480 * cos(6 * theta)
                                                - 42679 * cos(7 * theta)
                                                + 21112 * cos(8 * theta)
                                                - 2093 * cos(9 * theta)
                                                + 12520 * cos(10 * theta)
                                                + 73953 * cos(11 * theta)
                                                + 4464 * cos(12 * theta)
                                                - 57681 * cos(13 * theta)
                                                - 16008 * cos(14 * theta)
                                                + 13485 * cos(15 * theta)
                                                + 5394 * cos(16 * theta)
                                                + 24310
                                            )
                                            * exp(10 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= 11:
                                        return (
                                            -15
                                            * sqrt(67298)
                                            * (
                                                -6435 * sin(theta)
                                                + 69212 * sin(2 * theta)
                                                + 15301 * sin(3 * theta)
                                                + 12584 * sin(4 * theta)
                                                + 37037 * sin(5 * theta)
                                                - 56420 * sin(6 * theta)
                                                - 35035 * sin(7 * theta)
                                                - 6552 * sin(8 * theta)
                                                - 63063 * sin(9 * theta)
                                                + 26892 * sin(10 * theta)
                                                + 103697 * sin(11 * theta)
                                                + 4936 * sin(12 * theta)
                                                - 53911 * sin(13 * theta)
                                                - 13108 * sin(14 * theta)
                                                + 9889 * sin(15 * theta)
                                                + 3596 * sin(16 * theta)
                                            )
                                            * exp(11 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            3
                                            * sqrt(48070)
                                            * (
                                                19305 * cos(theta)
                                                - 12584 * cos(2 * theta)
                                                + 51051 * cos(3 * theta)
                                                - 200200 * cos(4 * theta)
                                                - 115115 * cos(5 * theta)
                                                + 54600 * cos(6 * theta)
                                                - 69433 * cos(7 * theta)
                                                + 121212 * cos(8 * theta)
                                                + 274365 * cos(9 * theta)
                                                - 78120 * cos(10 * theta)
                                                - 237545 * cos(11 * theta)
                                                - 9528 * cos(12 * theta)
                                                + 90857 * cos(13 * theta)
                                                + 19720 * cos(14 * theta)
                                                - 13485 * cos(15 * theta)
                                                - 4495 * cos(16 * theta)
                                                + 109395
                                            )
                                            * exp(12 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                            else:
                                if m <= 14:
                                    if m <= 13:
                                        return (
                                            3
                                            * sqrt(1394030)
                                            * (
                                                6435 * sin(theta)
                                                - 81796 * sin(2 * theta)
                                                - 29029 * sin(3 * theta)
                                                + 40040 * sin(4 * theta)
                                                - 5005 * sin(5 * theta)
                                                + 45500 * sin(6 * theta)
                                                + 75803 * sin(7 * theta)
                                                - 58968 * sin(8 * theta)
                                                - 94185 * sin(9 * theta)
                                                + 21420 * sin(10 * theta)
                                                + 55055 * sin(11 * theta)
                                                + 1928 * sin(12 * theta)
                                                - 16393 * sin(13 * theta)
                                                - 3220 * sin(14 * theta)
                                                + 2015 * sin(15 * theta)
                                                + 620 * sin(16 * theta)
                                            )
                                            * exp(13 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            15
                                            * sqrt(139403)
                                            * (
                                                3003 * cos(theta)
                                                - 12584 * cos(2 * theta)
                                                + 1001 * cos(3 * theta)
                                                - 16016 * cos(4 * theta)
                                                - 17017 * cos(5 * theta)
                                                + 25480 * cos(6 * theta)
                                                + 26117 * cos(7 * theta)
                                                - 15288 * cos(8 * theta)
                                                - 19929 * cos(9 * theta)
                                                + 3864 * cos(10 * theta)
                                                + 8701 * cos(11 * theta)
                                                + 272 * cos(12 * theta)
                                                - 2093 * cos(13 * theta)
                                                - 376 * cos(14 * theta)
                                                + 217 * cos(15 * theta)
                                                + 62 * cos(16 * theta)
                                                + 14586
                                            )
                                            * exp(14 * 1j * phi)
                                            / (536870912 * sqrt(pi))
                                        )
                                else:
                                    if m <= 15:
                                        return (
                                            -15
                                            * sqrt(8642986)
                                            * (
                                                -429 * sin(theta)
                                                + 6292 * sin(2 * theta)
                                                + 3003 * sin(3 * theta)
                                                - 8008 * sin(4 * theta)
                                                - 5005 * sin(5 * theta)
                                                + 5460 * sin(6 * theta)
                                                + 4459 * sin(7 * theta)
                                                - 2184 * sin(8 * theta)
                                                - 2457 * sin(9 * theta)
                                                + 420 * sin(10 * theta)
                                                + 847 * sin(11 * theta)
                                                + 24 * sin(12 * theta)
                                                - 169 * sin(13 * theta)
                                                - 28 * sin(14 * theta)
                                                + 15 * sin(15 * theta)
                                                + 4 * sin(16 * theta)
                                            )
                                            * exp(15 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
                                    else:
                                        return (
                                            15
                                            * sqrt(4321493)
                                            * (
                                                1716 * cos(theta)
                                                - 12584 * cos(2 * theta)
                                                - 4004 * cos(3 * theta)
                                                + 8008 * cos(4 * theta)
                                                + 4004 * cos(5 * theta)
                                                - 3640 * cos(6 * theta)
                                                - 2548 * cos(7 * theta)
                                                + 1092 * cos(8 * theta)
                                                + 1092 * cos(9 * theta)
                                                - 168 * cos(10 * theta)
                                                - 308 * cos(11 * theta)
                                                - 8 * cos(12 * theta)
                                                + 52 * cos(13 * theta)
                                                + 8 * cos(14 * theta)
                                                - 4 * cos(15 * theta)
                                                - cos(16 * theta)
                                                + 7293
                                            )
                                            * exp(16 * 1j * phi)
                                            / (1073741824 * sqrt(pi))
                                        )
