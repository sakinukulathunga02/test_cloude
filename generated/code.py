```python
from typing import Iterable, Optional, Callable, Any, Union, Dict, List, Tuple
import math
import json
import logging

# Configure logger only if not already configured externally
logger = logging.getLogger("advanced_sum")
if not logger.handlers:
    logging.basicConfig(level=logging.WARNING)

class AdvancedSumError(Exception):
    """Custom exception for errors in advanced_sum."""
    pass

def advanced_sum(
    values: Iterable[Any],
    *,
    weights: Optional[Iterable[Union[int, float]]] = None,
    filter_func: Optional[Callable[[Any], bool]] = None,
    skip_non_numeric: bool = True,
    ignore_nan: bool = True,
    ignore_null: bool = True,
    ignore_negative: bool = False,
    numeric_types: Tuple[type, ...] = (int, float),
    output_format: str = "number",  # Options: 'number', 'json', 'str'
    round_result: Optional[int] = None,
    raise_on_error: bool = False,
    log_errors: bool = False,
    max_items: Optional[int] = None,  # For very large input
) -> Union[int, float, str, Dict[str, Any], None]:
    """
    Calculate an advanced sum over an iterable.

    Args:
        values: The values to sum; any iterable.
        weights: Optional iterable of weights (must match length of filtered values).
        filter_func: Optional function to filter values (should return True if value is included).
        skip_non_numeric: If True, skips non-numeric items; else, error/warn.
        ignore_nan: If True, skips math.nan/float('nan').
        ignore_null: If True, skips None.
        ignore_negative: If True, negative numbers are skipped.
        numeric_types: Tuple of numeric types to accept.
        output_format: 'number', 'json', or 'str'.
        round_result: If set, rounds the result to this many decimals.
        raise_on_error: If True, raises on errors, otherwise returns None.
        log_errors: If True, logs errors/warnings.
        max_items: If set, processes up to max_items values after filtering.

    Returns:
        The result in required format, or None on error if not raising.
    """
    def error(msg: str):
        if log_errors:
            logger.warning(msg)
        if raise_on_error:
            raise AdvancedSumError(msg)

    # Validate iterable
    if not hasattr(values, '__iter__'):
        error("Input 'values' is not iterable.")
        return None

    # Prepare processed input as list for multiple scans, supports generator input
    try:
        values_list = list(values)
    except Exception as ex:
        error(f"Cannot convert values to list: {ex}")
        return None

    # Filtering and validation
    filtered_vals: List[Any] = []
    original_indices: List[int] = []

    for idx, v in enumerate(values_list):
        if max_items is not None and len(filtered_vals) >= max_items:
            break
        if filter_func and not filter_func(v):
            continue
        if ignore_null and v is None:
            continue

        is_num = isinstance(v, numeric_types)
        if not is_num:
            if not skip_non_numeric:
                error(f"Non-numeric value at index {idx}: {v!r}")
                return None
            continue

        if ignore_nan and isinstance(v, float) and math.isnan(v):
            continue

        if ignore_negative and isinstance(v, numeric_types) and v < 0:
            continue

        filtered_vals.append(v)
        original_indices.append(idx)

    if not filtered_vals:
        error("No valid values to sum after filtering.")
        return 0 if raise_on_error else None

    # Prepare and validate weights
    weights_list: Optional[List[Union[int, float]]] = None
    if weights is not None:
        try:
            input_weights = list(weights)
        except Exception as ex:
            error(f"Cannot convert weights to list: {ex}")
            return None

        if len(input_weights) == len(values_list):
            weights_filtered = [input_weights[i] for i in original_indices]
        elif len(input_weights) == len(filtered_vals):
            weights_filtered = input_weights
        else:
            error(f"Weights length ({len(input_weights)}) does not match filtered data ({len(filtered_vals)}).")
            return None

        # Check for valid weight values
        for wi, w in enumerate(weights_filtered):
            if w is None or not isinstance(w, numeric_types) or (ignore_nan and isinstance(w, float) and math.isnan(w)):
                error(f"Invalid weight at filtered index {wi}: {w!r}")
                return None
        weights_list = weights_filtered

    # Perform sum
    try:
        if weights_list is not None:
            result = sum(v * w for v, w in zip(filtered_vals, weights_list))
        else:
            result = sum(filtered_vals)
    except OverflowError as oe:
        error(f"Overflow detected: {oe}")
        return None
    except Exception as ex:
        error(f"Error during summation: {ex}")
        return None

    # Optional rounding
    if round_result is not None:
        try:
            result = round(result, round_result)
        except Exception as ex:
            error(f"Error rounding result: {ex}")
            return None

    # Output formatting
    if output_format == "json":
        out = {
            "result": result,
            "count": len(filtered_vals),
            "weights_used": weights_list is not None,
        }
        try:
            return json.dumps(out)
        except Exception as ex:
            error(f"Error serializing to JSON: {ex}")
            return None
    elif output_format == "str":
        return str(result)
    elif output_format == "number":
        return result
    else:
        error(f"Unknown output_format: {output_format!r}")
        return None

# ===================
# Example Usage:
if __name__ == "__main__":
    # Simple sum
    print(advanced_sum([1, 2, 3, 4]))
    # Weighted sum, ignore negative numbers
    print(advanced_sum([1, -2, 3, 4], weights=[0.5, 1.5, 0.7, 1.0], ignore_negative=True, output_format='json'))
    # Custom filter (include only odd numbers)
    print(advanced_sum([1, 2, 3, None, 'a'], filter_func=lambda x: isinstance(x, int) and x % 2 == 1))
    # Handle NaN and non-numeric values
    print(advanced_sum([5, 2.3, float('nan'), None, "oops"], output_format='str'))
    # Edge case: all filtered out (should warn and return None or 0)
    print(advanced_sum(["a", None, float('nan')], log_errors=True))
    # Max items for huge data
    big_list = list(range(1000000))
    print(advanced_sum(big_list, max_items=10, output_format="json"))
    # Error raising mode
    try:
        advanced_sum([1, None, "string"], skip_non_numeric=False, raise_on_error=True)
    except AdvancedSumError as e:
        print(f"Caught error as expected: {e}")
```