```python
import math

def calculate_root(number, n=2):
    """
    Calculate the n-th real root of a number.

    Parameters:
        number (int or float): The number to compute the root of.
        n (int): The degree of the root (default is 2, square root).

    Returns:
        float: The calculated n-th root of the number.

    Raises:
        ValueError: If n is not a positive integer.
        ValueError: If number is negative and n is even (result would be complex).
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Root degree 'n' must be a positive integer (n > 0).")
    if number == 0:
        return 0.0

    if number < 0:
        if n % 2 == 0:
            raise ValueError(
                f"Cannot calculate even root ({n}) of a negative number ({number}). Result would be complex."
            )
        # Use math.copysign for correct root sign and improved numerical stability
        return -((-number) ** (1.0 / n))
    return number ** (1.0 / n)

def _run_tests():
    test_cases = [
        (4, 2, 2.0),
        (27, 3, 3.0),
        (16, 4, 2.0),
        (0, 2, 0.0),
        (1, 5, 1.0),
        (-27, 3, -3.0),
        (64, 6, 2.0),
        (81, 4, 3.0),
    ]
    for num, n, expected in test_cases:
        result = calculate_root(num, n)
        assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=0.0), f"Failed for ({num}, {n}), got {result}, expected {expected}"
    
    # Test error cases
    error_cases = [
        {"args": (-16, 2), "err": ValueError},
        {"args": (16, 0), "err": ValueError},
        {"args": (16, -2), "err": ValueError},
        {"args": (25, 2.5), "err": ValueError},
    ]
    for case in error_cases:
        try:
            calculate_root(*case["args"])
            assert False, f"Expected {case['err']} for args {case['args']}"
        except Exception as e:
            assert isinstance(e, case["err"]), f"Wrong exception {type(e)} for args {case['args']}"

    print("All tests passed.")

if __name__ == "__main__":
    _run_tests()
```