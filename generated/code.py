```python
from numbers import Real
from typing import Union

def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Divides a by b and returns the result.

    Args:
        a (int or float): Numerator.
        b (int or float): Denominator.

    Returns:
        float: The result of the division.

    Raises:
        ValueError: If b is zero.
        TypeError: If a or b are not real numbers.
    """
    if not isinstance(a, Real):
        raise TypeError("Numerator 'a' must be a real number.")
    if not isinstance(b, Real):
        raise TypeError("Denominator 'b' must be a real number.")
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return float(a) / float(b)


# Unit tests
import unittest

class TestDivideFunction(unittest.TestCase):
    def test_divide_normal(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(9.0, 3), 3.0)
        self.assertAlmostEqual(divide(7, 3), 2.3333333333333335)

    def test_divide_negative(self):
        self.assertEqual(divide(-10, 2), -5.0)
        self.assertEqual(divide(10, -2), -5.0)
        self.assertEqual(divide(-10, -2), 5.0)

    def test_divide_zero_numerator(self):
        self.assertEqual(divide(0, 1), 0.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(5, 0)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            divide("10", 2)
        with self.assertRaises(TypeError):
            divide(10, "2")
        with self.assertRaises(TypeError):
            divide(None, 2)
        with self.assertRaises(TypeError):
            divide(10, None)
        with self.assertRaises(TypeError):
            divide(complex(3, 2), 1)

if __name__ == "__main__":
    unittest.main()
```