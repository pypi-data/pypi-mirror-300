"""
Module `dexipy.utils` contains a collection of helper functions used in DEXiPy.
"""

from typing import Any, Optional, Iterable, Sequence
from sys import float_info
import itertools
from dexipy.types import BoundAssoc

def objlen(obj: Any) -> int:
    """Returns length of any object type.

    Args:
        obj (Any): An object.

    Returns:
        int: `len(obj)` if object's length is defined, or 0 otherwise.
    """
    try:
        return len(obj)
    except:
        return 0

def table_lines(columns: list[list[str]], align: str = "", def_align: str = "l") -> list[str]:
    """A general-purpose function for making a table from a list of column strings.

    Args:
        columns (list[list[str]]):
            A list of columns. Each column is a list of strings.
        align (str, optional):
            A string consisting of letters in ("l", "c", "r") that indicate
            the justification of the corresponding columns . Defaults to "".
        def_align (str, optional):
            Default aligning character for columns not specified in `align`.
            Defaults to "l".

    Returns:
        list[str]: A list of table lines that can be joined for printing.
    """
    result: list[str] = []
    ncol = len(columns)
    acol = pad_list(list(align), ncol, def_align)
    nlin = max(len(col) for col in columns)
    widths = [col_width(col) for col in columns]
    for i in range(nlin):
        line = " ".join(
            aligned(col[i] if 0 <= i < len(col) else "", widths[c], acol[c])
                for c, col in enumerate(columns)
            )
        result.append(line)
    return result

def round_float(val: int | float, decimals: Optional[int] = None) -> float:
    """Rounds a float number to the required number of decimals.

    Args:
        val (float):
            An int or float number.
        decimals (Optional[int], optional):
            The required number of decimals.
            No rounding takes place if None. Defaults to None.

    Returns:
        float: Rounded float value.
    """
    assert isinstance(val, (int, float)), f"Value {val} is not int or float"
    if isinstance(val, int):
        return val
    return val if decimals is None else round(val, decimals)

def round_float_list(values: list[int | float], decimals: Optional[int] = None) -> list[float]:
    """Rounds all list elements to the required number of decimals.
    A vectorized version of :py:func:`dexipy.utils.round_float`.

    Args:
        values (list[float]):
            List of floats.
        decimals (Optional[int], optional):
            The required number of decimals.
            No rounding takes place if None. Defaults to None.

    Returns:
        list[float]: A list of rounded values.
    """
    return values if decimals is None else [round(val, decimals) for val in values]

def rule_values(vals: str, add: int = 0) -> tuple[int, ...]:
    """Convert a DEXi rule values string to a tuple of integers to be used in DEXiPy.

    In `.dxi` files, values of decision rules are encoded using character strings,
    where each individual character encodes some function value. The encoding is zero-based,
    so that the character `"0"` represents the lowest ordinal number on the corresponding
    discrete scale.

    Args:
        vals (str):
            A value string as used in `.dxi` files.
        add (int, optional):
            An optional integer value to be added to elements of the resulting tuple.
            Defaults to 0.

    Returns:
        tuple[int, ...]: A tuple of integers, of the same length as `vals`.

    Example:
       >>> rule_values("05A")
       (0, 5, 17)
    """
    return tuple((ord(ch) - ord("0") + add) for ch in vals)

def values_to_str(vals: Iterable[int], add: int = 0) -> str:
    """Converts numbers to a DEXi string. A reverse operation of :py:func:`rule_values`.

    Args:
        vals (Iterable[int]):
            An iterable of integers to be converted to characters.
        add (int, optional):
            An optional integer value to be added to `vals` before conversion.
            Defaults to 0.

    Returns:
        str: A string of the same length as `vals`.

    Example:
        >>> values_to_str((0, 5, 17))
        '05A'
    """
    return "".join((chr(val + ord("0") + add)) for val in vals)

def set_to_distr(valset: int | set[int], length: int = 0) -> Optional[list[float]]:
    """Converts a set to a value distribution.

    Args:
        valset (int | set[int]):
            A value to be converted.
        length (int, optional):
            The required length of the distribution. Defaults to 0.

    Returns:
        list[float]: Set converted to a list of floats.
        The minimal length of the list is `length`, but it may be extended if `valset`
        contains elements larger than `length - 1`.
        
    Examples:
       >>> set_to_distr(1)
       [0.0, 1.0]
       >>> set_to_distr(1, 5)
       [0.0, 1.0, 0.0, 0.0, 0.0]
       >>> set_to_distr({1,2}, 4)
       [0.0, 1.0, 1.0, 0.0]
    """
    if isinstance(valset, int):
        valset = {valset}
    if len(valset) == 0:
        return length * [0.0]
    if all(isinstance(val, int) for val in valset):
        dlen = max(length, max(valset) + 1)
        result = dlen * [0.0]
        for el in valset:
            if el >= 0:
                result[el] = 1.0
        return result
    return None

def distr_to_set(distr: list[float], eps: float = float_info.epsilon) -> set[int]:
    """Converts a DEXi value distribution to a DEXi value set.

    Args:
        distr (list[float]):
            A distribution to be converted.
        eps (float, optional):
            Threshold for determining whether a distribution element
            can be considered a member of the resulting set.
            Defaults to `float_info.epsilon`.

    Returns:
        set[int]:
            The set, composed of indices of `distr` elements greater than `eps`.

    Examples:
       >>> distr_to_set([0.0, 0.5, 1.0, 0.0])
       {1, 2}
       >>> distr_to_set([0.0, 0.5, 1.0, 0.0], 0.5)
       {2}
    """
    return {i for i, el in enumerate(distr) if el > eps}

def distr_to_strict_set(distr: list[float], eps: float = float_info.epsilon) -> Optional[set[int]]:
    """Converts a DEXi value distribution to a DEXi value set.
    Only distributions that strictly represent sets, i.e., they contain only 0.0 and 1.0 entries,
    are converted.

    Args:
        distr (list[float]):
            A distribution to be converted.
        eps (float, optional):
            Allowed tolerance around distribution values,
            so that they can be considered 0.0 or 1.0.
            Defaults to `float_info.epsilon`.

    Returns:
        Optional[set[int]]:
            The set, composed of indices of `distr` elements that differ from 0.0 or 1.0
            for at most `eps`. None is returned if `distr` contains values that are not
            sufficiently close to 0.0 or 1.0.

    Examples:
       >>> distr_to_strict_set([0.0, 0.5, 1.0, 0.0]) # returns None
       >>> distr_to_strict_set([0.0, 1.0, 1.0, 0.0])
       {1, 2}
       >>> distr_to_strict_set([0.0, 0.9, 1.1, 0.0]) # returns None
       >>> distr_to_strict_set([0.0, 0.9, 1.1, 0.0], 0.1)
       {1, 2}
    """
    result = set()
    for i, el in enumerate(distr):
        if 1.0 - eps <= el <= 1.0 + eps:
            result.add(i)
        elif not 0.0 - eps <= el <= 0.0 + eps:
            return None
    return result

def dict_to_list(distr: dict[int, float]) -> list[float]:
    """Converts a dictionary-form value distribution to a list-form one.
    Example: ``{1: 0.7, 2: 0.2}`` is converted to ``[0.0, 0.7, 0.2]``.

    Args:
        distr (dict[int, float]):
            A dictionary-form value distribution to be converted.

    Returns:
        list[float]: A list-form value distribution.

    Examples:
       >>> dict_to_list({1: 0.7, 2: 0.2})
       [0.0, 0.7, 0.2]
    """
    max_val = max(-1, max(distr.keys()))
    result = [0.0] * (max_val + 1)
    for idx, val in distr.items():
        if idx >= 0:
            result[idx] = val
    return result

def norm_sum(vals: list[float], req_sum: float = 1.0) -> list[float]:
    """Normalizes a list of float values so that ``sum(vals) == req_sum``.

    Args:
        vals (list[float]):
            A list of values.
        req_sum (float, optional):
            The required sum of the resulting list. Defaults to 1.0.

    Returns:
        list[float]: Normalized list. Returns the original list if ``sum(vals) == 0``.

    Examples:
       >>> norm_sum([0.1, 0.2, 0.5])
       [0.125, 0.25, 0.625]
       >>> norm_sum([0.1, -0.2, 0.5])
       [0.25, -0.5, 1.25]
       >>> norm_sum([0.1, 0.2, 0.5], 2)
       [0.25, 0.5, 1.25]
    """
    try:
        val_sum = sum(vals)
        result = [req_sum * val / val_sum for val in vals]
    except:
        result = vals
    return result

def norm_max(vals: list[float], req_max: float = 1.0) -> list[float]:
    """Normalizes a list of float values so that ``max(values) == req_max``.

    Args:
        vals (list[float]):
            A list of values.
        req_max (float, optional):
            The required maximum of the resulting list. Defaults to 1.0.

    Returns:
        list[float]:
            Normalized list. Returns the original list if ``max(vals) == 0``.

    Examples:
       >>> norm_max([0.1, 0.2, 0.4])
       [0.25, 0.5, 1.0]
       >>> norm_max([0.1, -0.2, 0.4])
       [0.25, -0.5, 1.0]
       >>> norm_max([0.1, -0.2, 0.4], 2)
       [0.5, -1.0, 2.0]
    """
    try:
        val_max = max(vals)
        result = [val * req_max / val_max for val in vals]
    except:
        result = vals
    return result

def norm_none(vals: list[float]) -> list[float]:
    """A no-normalization function that can be used in place of other normalization functions.

    Args:
        vals (list[float]):
            A list of values.

    Returns:
        list[float]:
            The original list of values. No normalization is performed.
    """
    return vals

def is_in_range(x: float,
                lb: float, hb: float,
                la: Optional[BoundAssoc] = BoundAssoc.UP, ha: Optional[BoundAssoc] = BoundAssoc.DOWN
               ) -> bool:
    """Checks whether or not the argument `x` lies in the interval bounded by `lb` and `hb`,
    considering the corresponding bound associations `la` and `ha`.

    Args:
        x (float):
            An integer or floating point value.
        lb (float):
            Lower interval bound.
        hb (float):
            Upper interval bound.
        la (BoundAssoc, optional):
            Bound association of `lb`. Defaults to BoundAssoc.UP.
        ha (BoundAssoc, optional):
            Bound association of `hb`. Defaults to BoundAssoc.DOWN.

    Returns:
        bool:
            Whether or not `x` lies in the specified interval.

    Examples:
       >>> is_in_range(0.5, 0, 1)
       True
       >>> is_in_range(0.0, 0, 1, BoundAssoc.UP, BoundAssoc.DOWN)
       True
       >>> is_in_range(0.0, 0, 1, BoundAssoc.DOWN, BoundAssoc.DOWN)
       False
       >>> is_in_range(1.0, 0, 1, BoundAssoc.DOWN, BoundAssoc.DOWN)
       True
       >>> is_in_range(1.0, 0, 1, BoundAssoc.DOWN, BoundAssoc.UP)
       False
    """
    if la is None:
        la = BoundAssoc.UP
    if ha is None:
        ha = BoundAssoc.DOWN
    return (lb < x < hb) or (x == lb and la == BoundAssoc.UP) or (x == hb and ha == BoundAssoc.DOWN)

def prod(iterable: Iterable[int | float]) -> float:
    """Calculates the product of arguments.

    Args:
        iterable (Iterable[int | float]):
            A sequence of integer or float numbers.

    Returns:
        int | float:
            Product of arguments.
    """
    p = 1.0
    for n in iterable:
        p *= n
    return p

def cartesian_product(*dimensions):
    """Constructs the cartesian product of ranges,
    tuples or sets submitted as the function arguments.

    Uses `itertools.product`.

    Returns:
        List of all possible combinations of values of `dimensions`.

    Examples:
       >>> cartesian_product((0, 1), (2, 3, 4))
       [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]
       >>> cartesian_product({"a", "b"}, (2, 3, 4))
       [('a', 2), ('a', 3), ('a', 4), ('b', 2), ('b', 3), ('b', 4)]
       >>> cartesian_product(range(2), range(3))
       [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    """
    return list(itertools.product(*dimensions))

def unique_names(names: list[str], reserved: list[str] = [], start: int = 0) -> list[str]:
    """Converts a list of strings to a list of unique ID strings.

    Args:
        names (list[str]):
            A list of strings to be converted to IDs.
        reserved (list[str], optional):
            Reserved strings that should not be used as IDs.
            Defaults to [].
        start (int, optional):
            To make IDs unique, indices of the form `_<int>` are added
            to the original strings.
            This argument defines the starting index, which corresponds to the first
            appearance of some string and is incremented before each subsequent occurence.
            Defaults to 0.

    Returns:
        list[str]: A list of unique IDs, of the same length as `names`.

    Examples:
       >>> unique_names(["name", "state", "name", "city", "name", "zip", "zip"])
       ['name', 'state', 'name_1', 'city', 'name_2', 'zip', 'zip_1']
       >>> unique_names(["name", "name", "city", "name", "zip", "zip"], reserved = ["name"])
       ['name_1', 'name_2', 'city', 'name_3', 'zip', 'zip_1']
    """
    state = {}
    names = reserved + names
    result = []
    for n in names:
        if n not in result:
            result.append(n)
            state[n] = start
        else:
            if not n in state:
                state[n] = start
            while True:
                state[n] += 1
                newname = n + "_" + str(state[n])
                if newname not in result:
                    result.append(newname)
                    break
    del result[:len(reserved)]
    return result

def name_to_id(name: str, replace: str = "_") -> str:
    """Replaces all non-alphanumeric characters in `name` with `replace`.

    Args:
        name (str):
            Some string.
        replace (str, optional):
            Replacement string. Defaults to "_".

    Returns:
        str: Converted string.

    Example:
       >>> name_to_id("Some #string 1")
       'Some__string_1'
    """
    return "".join([c if c.isalnum() else replace for c in name])

def names_to_ids(names: list[str], replace: str = "_") -> list[str]:
    """A vectorized version of :py:func:`dexipy.utils.name_to_id`.

    Args:
        names (list[str]):
            List of strings.
        replace (str, optional):
            Replacement string. Defaults to "_".

    Returns:
        list[str]:
            Converted list of strings, of the same length as `names`.
    """
    return [name_to_id(name, replace) for name in names]

def pad_list(lst: list[Any], newlen: int, pad: Any) -> list[Any]:
    """Pads a list to the required length, adding `pad` elements if necessary.

    Args:
        lst (list[Any]):
            List of objects of any type.
        newlen (int):
            The required length of the resulting list.
        pad (Any):
            Elements to be added if necessary.

    Returns:
        list[Any]:
            A list obtained from `lst`, padded or trimmed to the required length.
    """
    return lst[:newlen] if len(lst) >= newlen else lst + ([pad] * (newlen - len(lst)))

def col_width(column: None | list[str]) -> int:
    """Calculates the maximum width of strings in `column`.

    Args:
        column (None | list[str]):
            A list of strings.

    Returns:
        int: Maximum string length.
    """
    if column is None or len(column) == 0:
        return 0
    return max(len(el) for el in column)

def aligned(s: str, width: int = -1, align: str = "l") -> str:
    """Pads and/or aligns the string.

    Args:
        s (str):
            Some input string.
        width (int, optional):
            The required length of the resulting string.
            Defaults to -1, not affecting string length.
        align (str, optional):
            A one-character string in ``("l", "c", "r")``, requesting
            a left, centered or right justification, respectively.
            Any other value returns the original string.
            Defaults to "l".

    Returns:
        str: Padded and justified string.
    """
    if width <= 0:
        return s
    if align == "r":
        return s.rjust(width)
    if align == "l":
        return s.ljust(width)
    if align == "c":
        return s.center(width)
    return s

def check_str(check: dict[str, list[str]], errors: bool = True, warnings: bool = False) -> str:
    """Makes a string, suitable for printing, from an error/warning dictionary.

    Args:
        check (dict[str, list[str]]):
            A dictionary in the form ``{"errors": [...], "warnings": [...]}``.
        errors (bool, optional):
            Should this function consider errors? Defaults to True.
        warnings (bool, optional):
            Should this function consider warnings? Defaults to False.

    Returns:
        str: A string containing error and warning messages, formatted for printing.
    """
    result = ""
    if errors and check["errors"] != []:
        result = "Errors\n" + "\n".join(check["errors"]) + "\n"
    if warnings and check["warnings"] != []:
        result = result + "Warnings:\n" + "\n".join(check["warnings"]) + "\n"
    return result

def compare_operator(comp: Optional[float],
                     none: str = "",
                     eq: str = "=",
                     lt: str = "<",
                     le: str = "<=",
                     gt: str = ">",
                     ge: str = ">=") -> str:
    """Converts a float value comparison value to a string operator.

    Args:
        comp (Optional[float]):
            Result of comparison of two variables.
            Expected values are: None, -1, -0.5, 0, +0.5, +1.
        none (str, optional):
            String representation of None (incomparable values). Defaults to "".
        zero (str, optional):
            String representation of 0 (equal values). Defaults to "=".
        lt (str, optional):
            String representation of -1 (lower_than). Defaults to "<".
        le (str, optional):
            String representation of -0.5 (lower_than or equal). Defaults to "<=".
        gt (str, optional):
            String representation of +1 (greater_than). Defaults to ">".
        ge (str, optional):
            String representation of +0.5 (greater_than or equal). Defaults to ">=".

    Returns:
        str: String representation of `comp`. Returns "?" for an unexpected argument value.
    """
    if comp is None:
        return none
    if comp == 0:
        return eq
    if comp == -1:
        return lt
    if comp == +1:
        return gt
    if comp == -0.5:
        return le
    if comp == +0.5:
        return ge
    return "?"

def lin_map(x: float, imin: float, imax: float, omin: float = 0.0, omax: float = 1.0) -> float:
    """Map value :math:`x` linearly from interval :math:`[imin:imax]` to :math:`[omax:omax]`.

    Args:
        x (float):
            Value to be mapped.
        imin (float):
            Lower bound of the input range.
        imax (float):
            Upper bound of the input range.
        omin (float, optional):
            Lower bound of the output range. Defaults to 0.0.
        omax (float, optional):
            Upper bound of the output range. Defaults to 1.0.

    Returns:
        float: Mapped value.

    Raises:
        ZeroDivisionError: when :math:`imin = imax`.

    """
    k = (omax - omin) / (imax - imin)
    n = omin - k * imin
    return k * x + n

def lin_map_values(values: Sequence[float],
                   imin: float, imax: float, omin: float = 0.0, omax: float = 1.0
                   ) -> list[float]:
    """Map values :math:`x` linearly from interval :math:`[imin:imax]` to :math:`[omax:omax]`,
    using :py:func:`lin_map`.

    Args:
        values (Sequence[float]):
            Values to be mapped.
        imin (float):
            Lower bound of the input range.
        imax (float):
            Upper bound of the input range.
        omin (float, optional):
            Lower bound of the output range. Defaults to 0.0.
        omax (float, optional):
            Upper bound of the output range. Defaults to 1.0.

    Returns:
        list[float]: Mapped value.

    Raises:
        ZeroDivisionError: when :math:`imin = imax`.

    """
    return [lin_map(x, imin, imax, omin, omax) for x in values]
