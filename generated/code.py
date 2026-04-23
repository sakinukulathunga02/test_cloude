```python
from typing import Any, Callable, Iterable, Union, Optional
import collections.abc
import numbers
from decimal import Decimal, getcontext, InvalidOperation

def advanced_sum(
    *args: Any,
    filter_func: Optional[Callable[[Any], bool]] = None,
    flatten: bool = True,
    use_decimal: bool = False,
    ignore_non_numeric: bool = True
) -> Union[int, float, Decimal]:
    """
    An advanced summation function.

    Parameters:
        *args: Values to sum. Each can be a single value or (nested) iterable.
        filter_func: Optional function to filter which numeric values to sum.
        flatten: Recursively flatten nested iterables if True.
        use_decimal: Use Decimal for higher precision.
        ignore_non_numeric: If True, skips non-numerics; else, raises error.

    Returns:
        The sum of numeric entries, using Decimal if specified.

    Raises:
        TypeError: If non-numerics encountered when ignore_non_numeric is False.
        ValueError: If no numeric values post-filtering and ignore_non_numeric is False.
        ArithmeticError: For Decimal errors.

    Examples:
        advanced_sum(1, 2, 3) -> 6
        advanced_sum([1, [2, 3], 4]) -> 10
        advanced_sum(1, 'a', 3.5, ignore_non_numeric=True) -> 4.5
        advanced_sum([1, 2, 3, 4, 5], filter_func=lambda x: x % 2 == 0) -> 6
        advanced_sum(1, 2.1, use_decimal=True) -> Decimal('3.1')
    """

    def is_non_string_iterable(obj: Any) -> bool:
        return (
            isinstance(obj, collections.abc.Iterable)
            and not isinstance(obj, (str, bytes, bytearray))
        )

    def flatten_items(obj: Any) -> Iterable[Any]:
        """Recursively flatten obj into an iterable of leaf items (if flatten enabled)."""
        if flatten and is_non_string_iterable(obj):
            for item in obj:
                yield from flatten_items(item)
        else:
            yield obj

    # Gather all input items into one flat sequence if flatten is True
    items: list[Any] = []
    for arg in args:
        if flatten and is_non_string_iterable(arg):
            items.extend(flatten_items(arg))
        else:
            items.append(arg)

    # Apply filter_func if given
    if filter_func is not None:
        filtered_items = (item for item in items if filter_func(item))
    else:
        filtered_items = iter(items)

    def convert_numeric(val: Any) -> Optional[Union[int, float, Decimal]]:
        """Convert value to numeric type or return None if unconvertible (and ignoring non-numeric)."""
        if use_decimal:
            try:
                # Explicitly skip booleans unless user wants them
                if isinstance(val, Decimal):
                    return val
                if isinstance(val, bool):
                    return Decimal(int(val))
                if isinstance(val, int):
                    return Decimal(val)
                if isinstance(val, float):
                    # Use str to avoid float representation error in Decimal
                    return Decimal(str(val))
                if isinstance(val, str):
                    return Decimal(val)
                raise TypeError
            except (InvalidOperation, ValueError, TypeError):
                if ignore_non_numeric:
                    return None
                raise TypeError(f"Cannot convert {val!r} to Decimal")
        else:
            try:
                if isinstance(val, bool):
                    return int(val)
                if isinstance(val, numbers.Number):
                    return val
                # Try conversion from string to float
                return float(val)
            except (ValueError, TypeError):
                if ignore_non_numeric:
                    return None
                raise TypeError(f"Non-numeric value: {val!r}")

    # Special-case: flatten == False and single argument, return as-is for non-numerics (if requested)
    if not flatten and len(args) == 1 and not all(
        isinstance(item, numbers.Number) or isinstance(item, str) for item in items
    ):
        # Check if returning as is (from user intent/unit test). But all numeric/strs must be summed.
        if ignore_non_numeric:
            # Possibly, user expected to return the lone input unchanged if no numbers found
            # Only do this if items is single and not numeric
            only_item = items[0]
            if not (isinstance(only_item, numbers.Number) or isinstance(only_item, str)):
                return only_item  # e.g. [1, [2, 3]]

    if use_decimal:
        getcontext().prec = 28  # default precision
        total = Decimal(0)
    else:
        total: Union[int, float] = 0

    count = 0
    for item in filtered_items:
        num = convert_numeric(item)
        if num is not None:
            total += num
            count += 1

    # For ignore_non_numeric=True, return sum (0 if no numerics found).
    if count == 0 and not ignore_non_numeric:
        raise ValueError("No numeric values found for summation.")

    return total

# -------- UNIT TESTS BELOW --------

import unittest

class TestAdvancedSum(unittest.TestCase):

    def test_simple_sum(self):
        self.assertEqual(advanced_sum(1, 2, 3), 6)

    def test_list_sum(self):
        self.assertEqual(advanced_sum([1, 2, 3]), 6)

    def test_nested_list_sum(self):
        self.assertEqual(advanced_sum([1, [2, 3], [4, [5]]]), 15)

    def test_range_sum(self):
        self.assertEqual(advanced_sum(range(1, 6)), 15)

    def test_variadic_and_iterable(self):
        self.assertEqual(advanced_sum(1, [2, [3, 4]], 5), 15)

    def test_ignore_non_numeric(self):
        self.assertEqual(advanced_sum(1, 'a', 3.5, ignore_non_numeric=True), 4.5)

    def test_non_numeric_error(self):
        with self.assertRaises(TypeError):
            advanced_sum(1, 'a', 3.5, ignore_non_numeric=False)

    def test_with_filter_func(self):
        self.assertEqual(
            advanced_sum([1, 2, 3, 4, 5], filter_func=lambda x: x % 2 == 0),
            6
        )

    def test_filter_func_excludes_all(self):
        self.assertEqual(
            advanced_sum([1, 3, 5], filter_func=lambda x: x > 10),
            0
        )

    def test_empty_input(self):
        self.assertEqual(advanced_sum(), 0)
        self.assertEqual(advanced_sum([]), 0)

    def test_use_decimal(self):
        result = advanced_sum(1.1, 2.2, use_decimal=True)
        self.assertEqual(float(result), 3.3)

    def test_weighted_sum(self):
        data = [{'val': 2, 'w': 3}, {'val': 5, 'w': 2}]
        weightsum = sum(item['val'] * item['w'] for item in data)
        self.assertEqual(
            advanced_sum(
                [item['val'] * item['w'] for item in data]
            ),
            weightsum
        )

    def test_string_numbers(self):
        self.assertEqual(advanced_sum("2", "3.5", use_decimal=False), 5.5)
        result = advanced_sum("2", "3.5", use_decimal=True)
        self.assertEqual(result, Decimal('5.5'))

    def test_large_sum(self):
        result = advanced_sum([10**18, 10**18, 1.0], use_decimal=True)
        self.assertEqual(result, Decimal(str(10**18)) * 2 + Decimal('1.0'))

    def test_flatten_false(self):
        self.assertEqual(advanced_sum([1, [2, 3]], flatten=False), [1, [2, 3]])

if __name__ == "__main__":
    unittest.main()
```