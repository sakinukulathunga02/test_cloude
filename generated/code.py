```python
import math
import unittest

def calculate_root(number, root_degree=2):
    """
    Calculate the nth root of a number.

    Parameters:
        number (float or int): The number to calculate the root for.
        root_degree (int): The degree of the root. Default is 2 (square root).

    Returns:
        float: The calculated root.

    Raises:
        ValueError: If root_degree is not integer >= 2,
                    or if number is negative and root_degree is even,
                    or if inputs are invalid.
    Examples:
        >>> calculate_root(9)
        3.0
        >>> calculate_root(27, 3)
        3.0
        >>> calculate_root(16, 4)
        2.0
    """
    if not isinstance(root_degree, int) or root_degree < 2:
        raise ValueError("root_degree must be an integer >= 2.")
    if not isinstance(number, (int, float)):
        raise ValueError("number must be an int or float.")
    if math.isnan(number):
        raise ValueError("number must not be NaN.")
    if number < 0:
        if root_degree % 2 == 0:
            raise ValueError("Cannot calculate even root of negative number (in real numbers).")
        else:
            return -((-number) ** (1 / root_degree))
    if number == 0:
        return 0.0
    return number ** (1 / root_degree)

class TestCalculateRoot(unittest.TestCase):
    def test_square_root(self):
        self.assertAlmostEqual(calculate_root(9), 3.0)
        self.assertAlmostEqual(calculate_root(16), 4.0)
        self.assertAlmostEqual(calculate_root(0), 0.0)
        self.assertAlmostEqual(calculate_root(2), math.sqrt(2))

    def test_nth_root(self):
        self.assertAlmostEqual(calculate_root(27, 3), 3.0)
        self.assertAlmostEqual(calculate_root(32, 5), 2.0)
        self.assertAlmostEqual(calculate_root(81, 4), 3.0)
        self.assertAlmostEqual(calculate_root(243, 5), 3.0)
        self.assertAlmostEqual(calculate_root(10_000, 4), 10.0)

    def test_negative_input_even_root(self):
        with self.assertRaises(ValueError):
            calculate_root(-16, 2)
        with self.assertRaises(ValueError):
            calculate_root(-32, 4)

    def test_negative_input_odd_root(self):
        self.assertAlmostEqual(calculate_root(-27, 3), -3.0)
        self.assertAlmostEqual(calculate_root(-32, 5), -2.0)
        self.assertAlmostEqual(calculate_root(-8, 5), -8**(1/5))

    def test_invalid_root_degree(self):
        with self.assertRaises(ValueError):
            calculate_root(16, -2)
        with self.assertRaises(ValueError):
            calculate_root(16, 0)
        with self.assertRaises(ValueError):
            calculate_root(16, 1.5)
        with self.assertRaises(ValueError):
            calculate_root(16, float('nan'))
        with self.assertRaises(ValueError):
            calculate_root(16, None)

    def test_invalid_number(self):
        with self.assertRaises(ValueError):
            calculate_root("a number", 2)
        with self.assertRaises(ValueError):
            calculate_root(None, 2)
        with self.assertRaises(ValueError):
            calculate_root(float('nan'), 2)

    def test_float_degrees(self):
        with self.assertRaises(ValueError):
            calculate_root(16, 2.0)

    def test_large_numbers(self):
        self.assertAlmostEqual(calculate_root(1e8, 8), 10.0)
        self.assertAlmostEqual(calculate_root(-1e9, 9), -10.0)

if __name__ == "__main__":
    unittest.main()
```