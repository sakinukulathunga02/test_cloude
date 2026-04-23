```python
from typing import Union


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiplies two numbers.

    Args:
        a (int or float): First number.
        b (int or float): Second number.

    Returns:
        int or float: The product of a and b.

    Raises:
        TypeError: If the inputs are not int or float.
    """
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        raise TypeError("Both inputs must be numeric (int or float).")
    return a * b


def to_number(s: str) -> Union[int, float]:
    """
    Converts a string to an int or float.

    Args:
        s (str): Input string.

    Returns:
        int or float: Numerical representation of the string.

    Raises:
        ValueError: If the string cannot be converted to a number.
    """
    try:
        return int(s)
    except ValueError:
        return float(s)


def main() -> None:
    print("Multiplication Feature\n")
    try:
        a_str = input("Enter first number: ").strip()
        b_str = input("Enter second number: ").strip()

        a = to_number(a_str)
        b = to_number(b_str)

        product = multiply(a, b)
        print(f"\nResult: {a} * {b} = {product}")
    except ValueError:
        print("Error: Please enter valid numbers (e.g., 2, 2.5).")
    except TypeError as te:
        print(f"Type Error: {te}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
```