```python
from numbers import Number

def divide(a: Number, b: Number) -> float:
    """
    Divides a by b.

    Args:
        a (Number): Numerator.
        b (Number): Denominator.

    Returns:
        float: Result of division.

    Raises:
        TypeError: If inputs are not numbers.
        ZeroDivisionError: If division by zero is attempted.
    """
    if not isinstance(a, Number) or not isinstance(b, Number):
        raise TypeError("Inputs must be numeric types.")
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return float(a) / float(b)


if __name__ == "__main__":
    test_cases = [
        (10, 2),     # 5.0
        (7, 0),      # Division by zero
        (5.5, 2.2),  # 2.5
        ('3', 2)     # TypeError
    ]

    for a, b in test_cases:
        try:
            result = divide(a, b)
            print(f"{a} / {b} = {result}")
        except Exception as e:
            print(f"Error: {e}")
```