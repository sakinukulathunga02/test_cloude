```python
import math
import cmath
from typing import Union

def calculate_root(number: Union[int, float], degree: Union[int, float]) -> Union[float, complex]:
    """
    Calculate the nth root of a number.

    Parameters:
        number (int or float): The base number whose root is to be computed.
        degree (int or float): The degree of the root (e.g., 2 for square root).

    Returns:
        float or complex: The calculated root. Returns complex if the root is not real.

    Raises:
        TypeError: If number or degree is not numeric.
        ValueError: If degree is zero, or if root is not defined for the given input.

    Examples:
        >>> calculate_root(9, 2)
        3.0
        >>> calculate_root(-8, 3)
        -2.0
        >>> calculate_root(-16, 4)
        (1.4142135623730951+1.4142135623730951j)
        >>> calculate_root(16, -2)
        0.25
        >>> calculate_root('a', 2)
        Traceback (most recent call last):
            ...
        TypeError: number and degree must be numeric (int or float)
        >>> calculate_root(9, 0)
        Traceback (most recent call last):
            ...
        ValueError: Root degree cannot be zero
    """
    # Input validation
    if not isinstance(number, (int, float)):
        raise TypeError("number and degree must be numeric (int or float)")
    if not isinstance(degree, (int, float)):
        raise TypeError("number and degree must be numeric (int or float)")
    if degree == 0:
        raise ValueError("Root degree cannot be zero")

    # Special handling for zero input
    if number == 0:
        if degree < 0:
            return math.inf if degree % 2 == 1 else complex(math.inf, 0)
        return 0.0

    is_integer_degree = float(degree).is_integer()
    integer_degree = int(degree) if is_integer_degree else None

    # Handle negative degree: inverse root
    if degree < 0:
        # Negative degree means reciprocal of the positive root
        pos_root = calculate_root(number, -degree)
        try:
            return 1 / pos_root
        except ZeroDivisionError:
            return math.inf if number != 0 else float('nan')

    # Positive degree
    if number >= 0:
        return number ** (1/degree)
    else:
        # Negative number
        if is_integer_degree and integer_degree % 2 == 1:
            # Odd integer root of negative number is real
            root = abs(number) ** (1/degree)
            return -root
        else:
            # Even root of negative number or non-integer degree: complex result
            return cmath.exp(cmath.log(number) / degree)

# ---- Unit tests ----
if __name__ == "__main__":
    import unittest

    class TestCalculateRoot(unittest.TestCase):
        def test_positive_square(self):
            self.assertAlmostEqual(calculate_root(4, 2), 2.0)
            self.assertAlmostEqual(calculate_root(27, 3), 3.0)

        def test_negative_number_odd_degree(self):
            self.assertAlmostEqual(calculate_root(-8, 3), -2.0)
            self.assertAlmostEqual(calculate_root(-27, 3), -3.0)

        def test_negative_number_even_degree(self):
            res = calculate_root(-16, 4)
            self.assertIsInstance(res, complex)
            self.assertAlmostEqual(res.real, 1.4142135623730951)
            self.assertAlmostEqual(res.imag, 1.4142135623730951)

        def test_negative_degree(self):
            self.assertAlmostEqual(calculate_root(16, -2), 0.25)

        def test_zero(self):
            self.assertEqual(calculate_root(0, 2), 0.0)
            self.assertEqual(calculate_root(0, 3), 0.0)
            self.assertEqual(calculate_root(0, -3), math.inf)
            inf = calculate_root(0, -2)
            self.assertTrue(math.isinf(inf) or
                            (isinstance(inf, complex) and math.isinf(inf.real)))

        def test_non_integer_degree(self):
            self.assertAlmostEqual(calculate_root(27, 1.5), 9.0)

        def test_invalid_inputs(self):
            with self.assertRaises(TypeError):
                calculate_root("string", 2)
            with self.assertRaises(TypeError):
                calculate_root(4, "string")
            with self.assertRaises(ValueError):
                calculate_root(4, 0)

    unittest.main()
```