```python
import math
from typing import Union

def calculate_root(number: float, degree: float = 2) -> Union[float, complex]:
    """
    Calculates the nth root of a given number.

    Args:
        number (float): The number to take the root of.
        degree (float): The degree of the root (default is 2 for square root).

    Returns:
        float or complex: The calculated root.

    Raises:
        ValueError: If degree is zero or not finite/real.
    """
    if not isinstance(degree, (int, float)) or not math.isfinite(degree):
        raise ValueError("Root degree must be a finite real number.")
    if not isinstance(number, (int, float)):
        raise ValueError("Number must be a real number.")
    if degree == 0:
        raise ValueError("Root degree cannot be zero.")

    # Handle integer-degree roots for correct negative/odd root semantics
    is_integer_degree = isinstance(degree, int) or (isinstance(degree, float) and degree.is_integer())
    if is_integer_degree:
        int_degree = int(degree)
        if number < 0 and int_degree % 2 == 1:
            # Odd roots of negative number: real result
            root = -((-number) ** (1 / int_degree))
            return root
        elif number < 0 and int_degree % 2 == 0:
            # Even root of negative: complex result
            root = complex(number) ** (1 / int_degree)
            return root
        else:
            # Positive number or zero
            return number ** (1 / int_degree)
    else:
        # Non-integer root degree; use complex for negative input
        if number < 0:
            return complex(number) ** (1 / degree)
        return number ** (1 / degree)

# Unit tests
if __name__ == "__main__":
    test_cases = [
        (27, 3, 3),
        (16, 2, 4),
        (81, 4, 3),
        (-8, 3, -2),
        (0, 5, 0),
        (10, 1, 10),
        (-16, 2, complex(0, 4)),
        # Non-integer degree, negative input
        (-16, 2.5, complex(-1.454427098, 3.356399723)),  # Approximate complex result
    ]

    for number, degree, expected in test_cases:
        result = calculate_root(number, degree)
        if isinstance(expected, complex):
            assert (
                abs(result.real - expected.real) < 1e-6
                and abs(result.imag - expected.imag) < 1e-6
            ), f"Failed for {number}^{1/degree}: expected {expected}, got {result}"
        else:
            assert abs(result - expected) < 1e-9, (
                f"Failed for {number}^{1/degree}: expected {expected}, got {result}"
            )

    # Test: Invalid degree
    for invalid_degree in [0, float('inf'), float('nan'), 'a']:
        try:
            calculate_root(10, invalid_degree)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Failed to raise ValueError for degree={invalid_degree}")

    # Test: Invalid number type
    try:
        calculate_root('a', 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Failed to raise ValueError for number='a'")

    print("All tests passed.")
```