```python
import math
import cmath
import unittest
from typing import Union

Number = Union[int, float]
ResultType = Union[float, complex]


def calculate_root(number: Number, n: int = 2) -> ResultType:
    """
    Calculates the n-th root of a number.

    Args:
        number (int | float): The number to find the root of.
        n (int): The degree of the root. Defaults to 2 (square root).

    Returns:
        float | complex: The n-th root of the number.

    Raises:
        ValueError: If n <= 0 or n is not an integer.
        TypeError: If input types are invalid.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Root degree 'n' must be a positive integer.")
    if not isinstance(number, (int, float)):
        raise TypeError("Input 'number' must be an integer or float.")

    if n == 1:
        return float(number)

    # Handle zero: 0 ** (1/n) == 0 for n > 0
    if number == 0:
        return 0.0

    # Odd root of negative numbers is real
    if number < 0:
        if n % 2 == 0:
            # Even root of negative number: complex result
            # Use polar form for correct result
            root = cmath.exp(cmath.log(number) / n)
            # Remove insignificant real/imaginary parts due to floating-point errors
            real = 0.0 if math.isclose(root.real, 0.0, abs_tol=1e-12) else root.real
            imag = 0.0 if math.isclose(root.imag, 0.0, abs_tol=1e-12) else root.imag
            return complex(real, imag)
        else:  # Odd root: real result
            return -(-number) ** (1 / n)

    # Normal (real) root
    return float(number) ** (1 / n)


class TestCalculateRoot(unittest.TestCase):
    def test_square_root(self):
        self.assertAlmostEqual(calculate_root(9, 2), 3.0)
        self.assertAlmostEqual(calculate_root(16), 4.0)
        self.assertAlmostEqual(calculate_root(0, 2), 0.0)

    def test_cube_root(self):
        self.assertAlmostEqual(calculate_root(8, 3), 2.0)
        self.assertAlmostEqual(calculate_root(-27, 3), -3.0)

    def test_nth_root(self):
        self.assertAlmostEqual(calculate_root(32, 5), 2.0)

    def test_root_one(self):
        self.assertEqual(calculate_root(5, 1), 5.0)

    def test_even_root_negative(self):
        result = calculate_root(-16, 2)
        self.assertIsInstance(result, complex)
        self.assertAlmostEqual(result.real, 0.0, places=7)
        self.assertAlmostEqual(result.imag, 4.0, places=7)

    def test_invalid_n(self):
        with self.assertRaises(ValueError):
            calculate_root(9, 0)
        with self.assertRaises(ValueError):
            calculate_root(9, -4)
        with self.assertRaises(ValueError):
            calculate_root(9, 2.5)

    def test_invalid_number_type(self):
        with self.assertRaises(TypeError):
            calculate_root("a", 2)

    def test_zero_root_degree(self):
        with self.assertRaises(ValueError):
            calculate_root(10, 0)

    def test_non_integer_n(self):
        with self.assertRaises(ValueError):
            calculate_root(4, 2.0)
        with self.assertRaises(ValueError):
            calculate_root(8, "3")  # type: ignore

    def test_zero_base_various_n(self):
        self.assertEqual(calculate_root(0, 5), 0.0)
        self.assertEqual(calculate_root(0, 7), 0.0)

if __name__ == "__main__":
    unittest.main()
```