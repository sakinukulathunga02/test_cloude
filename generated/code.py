```python
from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Optional, Union

Number = Union[int, float, Decimal]


def is_numeric(val: Any) -> bool:
    """Check if value is numeric (int, float, Decimal) or a numeric string."""
    if isinstance(val, (int, float, Decimal)):
        return True
    if isinstance(val, (str, bytes)):
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False
    return False


def to_number(val: Any) -> Number:
    """Converts val to number. Tries int, float, then Decimal."""
    if isinstance(val, (int, float, Decimal)):
        return val
    if isinstance(val, bytes):
        try:
            val = val.decode()
        except Exception:
            raise ValueError(f"Cannot decode bytes {val!r} to string for conversion.")
    if isinstance(val, str):
        val_strip = val.strip()
        try:
            return int(val_strip)
        except ValueError:
            pass
        try:
            return float(val_strip)
        except ValueError:
            pass
        try:
            return Decimal(val_strip)
        except (InvalidOperation, ValueError):
            pass
    raise ValueError(f"Cannot convert {val!r} to a number.")


def _flatten(items: Any) -> Iterable:
    """Recursively flattens nested iterables except for str/bytes."""
    if isinstance(items, (str, bytes)):
        yield items
    elif isinstance(items, Iterable):
        for item in items:
            yield from _flatten(item)
    else:
        yield items


def sum_advanced(
    *args: Any,
    filter_fn: Optional[Callable[[Number], bool]] = None,
    handle_invalid: str = "ignore",  # 'ignore', 'error'
    parse_numeric_strings: bool = True
) -> Number:
    """
    Advanced summation function.

    Args:
        *args: Numbers or (possibly nested) iterables of numbers.
        filter_fn: Optional function: number -> bool.
        handle_invalid: 'ignore' skips invalid/non-numeric entries; 'error' raises ValueError.
        parse_numeric_strings: If True, numeric strings/bytes are parsed and included in sum.

    Returns:
        The sum of all valid numbers after flattening/validation/filtering.

    Raises:
        ValueError: If invalid input is found and handle_invalid is 'error'.
    """
    if not args:
        return 0

    result: Number = 0

    for item in _flatten(args):
        # Optionally skip non-numeric str/bytes
        if isinstance(item, (str, bytes)) and not parse_numeric_strings:
            if handle_invalid == "error":
                raise ValueError(f"Non-numeric string/bytes found: {item!r}")
            continue

        if is_numeric(item):
            try:
                number = to_number(item)
            except ValueError:
                if handle_invalid == "error":
                    raise
                continue
            if filter_fn and not filter_fn(number):
                continue
            result += number
        else:
            if handle_invalid == "error":
                raise ValueError(f"Non-numeric value found: {item!r}")

    return result


# ---------------------- Unit tests ----------------------
import unittest

class TestSumAdvanced(unittest.TestCase):
    def test_basic_numbers(self):
        self.assertEqual(sum_advanced(1, 2, 3), 6)
        self.assertEqual(sum_advanced(1.5, 2.5), 4.0)
        self.assertEqual(sum_advanced(Decimal('1.1'), 2), Decimal('3.1'))

    def test_collections(self):
        self.assertEqual(sum_advanced([1, 2, 3]), 6)
        self.assertEqual(sum_advanced((1, 2), {3, 4}), 10)
        self.assertEqual(sum_advanced([1, [2, 3], [4, [5, 6]]]), 21)

    def test_nested_collections(self):
        data = [1, [2, [3, [4, 5]], 6], 7]
        self.assertEqual(sum_advanced(data), 28)

    def test_strings(self):
        self.assertEqual(sum_advanced("2", "3.5"), 5.5)
        self.assertEqual(sum_advanced("2", 1), 3)
        self.assertEqual(sum_advanced(["1", 2, "3.5"]), 6.5)

    def test_ignore_invalid(self):
        self.assertEqual(sum_advanced([1, '2', 'x', None, 3]), 6)
        self.assertEqual(sum_advanced({'a': 1, 2: 2}, handle_invalid='ignore'), 2)

    def test_error_on_invalid(self):
        with self.assertRaises(ValueError):
            sum_advanced(1, 'xyz', handle_invalid='error')
        with self.assertRaises(ValueError):
            sum_advanced('a', handle_invalid='error')

    def test_filter_fn(self):
        self.assertEqual(
            sum_advanced([1, -2, 3, -4], filter_fn=lambda x: x > 0),
            4
        )
        self.assertEqual(
            sum_advanced([1, 2, 3, 4], filter_fn=lambda x: x % 2 == 0),
            6
        )

    def test_parse_numeric_strings(self):
        self.assertEqual(sum_advanced('2.2', '3.3', parse_numeric_strings=True), 5.5)
        self.assertEqual(sum_advanced('two', 1, parse_numeric_strings=True), 1)
        with self.assertRaises(ValueError):
            sum_advanced('2.2', 'three', parse_numeric_strings=False, handle_invalid='error')

    def test_empty(self):
        self.assertEqual(sum_advanced(), 0)
        self.assertEqual(sum_advanced([], ()), 0)

    def test_large_numbers(self):
        numbers = [10**6] * 1000
        self.assertEqual(sum_advanced(numbers), 10**9)

    def test_bytes(self):
        self.assertEqual(sum_advanced([b"123", 2], parse_numeric_strings=True), 125)
        self.assertEqual(sum_advanced([b"123", 2], parse_numeric_strings=False), 2)

    def test_custom_types(self):
        class MyNum:
            def __int__(self):
                return 5
            def __float__(self):
                return 5.0
        # Since MyNum is not recognized as numeric, it's ignored
        self.assertEqual(sum_advanced(MyNum()), 0)

if __name__ == "__main__":
    unittest.main()
```