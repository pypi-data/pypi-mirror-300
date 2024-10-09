"""
Module `dexipy.values` contains helper classes and functions for handling DEXi values.
"""

from typing import Any, Optional
from statistics import mean
from dexipy.types import DexiValue, DexiValueType, DexiOrder
import dexipy.utils as utl
import dexipy.dexi as dxi

def dexi_value_type(value: Any) -> DexiValueType:
    """Determines the `DexiValueType` of the argument.

    Args:
        value (Any): Value object to be checked.

    Returns:
        DexiValueType: Enumeration of the argument's DEXi value type.
    """
    if value is None:
        return DexiValueType.NONE
    val_type = type(value)
    if val_type is int:
        return DexiValueType.INT
    if val_type is str:
        return DexiValueType.STR
    if val_type is float:
        return DexiValueType.FLOAT
    if val_type is set:
        return DexiValueType.SET
    if val_type is tuple:
        return DexiValueType.TUPLE
    if val_type is list:
        return DexiValueType.LIST
    if val_type is dict:
        return DexiValueType.DICT
    return DexiValueType.ERROR

def check_dexi_value(value: Any) -> bool:
    """Checks the data object and determines whether or not it represents a `DexiValue`.

    Only the data structure is checked. Even if the structure is correct, `value`
    can still contain elements that may not be correct in the context of some specific
    `DexiScale`. For instance, the object may contain value indices not
    found in the scale definition.

    Args:
        value (Any): Value object to be checked.

    Returns:
        bool: Whether or not the object's structure is valid for representing a `DexiValue`.
    """
    val_type = dexi_value_type(value)
    if val_type in [
            DexiValueType.ERROR, DexiValueType.STR, DexiValueType.TUPLE, DexiValueType.DICT
        ]:
        return False
    if val_type == DexiValueType.SET:
        return all(isinstance(val, int) for val in value)
    if val_type == DexiValueType.LIST:
        return all(isinstance(val, (int, float)) for val in value)
    return True

def check_dexi_value_specification(value: Any) -> bool:
    """Checks the data object and determines whether or not it represents
    a `DexiValueSpecification`.

    Only the data structure is checked. Even if the structure is correct, `value`
    can still contain elements that may not be correct in the context of some specific
    `DexiScale`. For instance, the object may contain value names or indices not
    found in the scale definition.

    Args:
        value (Any): Value object to be checked.

    Returns:
        bool:
            Whether or not the object's structure is valid for representing
            a `DexiValue`.
    """
    val_type = dexi_value_type(value)
    if val_type == DexiValueType.ERROR:
        return False
    if val_type in [DexiValueType.SET, DexiValueType.TUPLE]:
        return all(isinstance(val, (int, str)) for val in value)
    if val_type == DexiValueType.LIST:
        return all(isinstance(val, (int, float)) for val in value)
    if val_type == DexiValueType.DICT:
        return all(isinstance(key, (int, str)) and isinstance(val, (int, float))
                   for key, val in value.items())
    return True

def dexi_value_as_set(value: DexiValue, strict: bool = False) -> Optional[set[int]]:
    """Converts a `DexiValue` object to a set.

    Args:
        value (DexiValue): A `DexiValue`.
        strict (bool, optional): Defines the conversion from value distributions.
           When True, only distributions that clearly represent sets, i.e., contain only
           0.0 or 1.0 elements, are converted. When False, all elements with non-zero values
           are considered set members, too.
           Defaults to False.

    Returns:
        Optional[set[int]]:
            Resulting value set. None if `value` cannot be interpreted as a set.

    Examples:
       >>> dexi_value_as_set([0, 1, 0.5, 1], strict = True) # returns None
       >>> dexi_value_as_set([0, 1, 0.0, 1], strict = True)
       {1, 3}
       >>> dexi_value_as_set([0, 1, 0.5, 1], strict = False)
       {1, 2, 3}
    """
    if isinstance(value, int):
        return {value}
    if isinstance(value, (set, tuple)):
        if any(not isinstance(val, int) for val in value):
            return None
        return set(value)
    if isinstance(value, dict):
        value = utl.dict_to_list(value)
    if isinstance(value, list):
        return utl.distr_to_strict_set(value) if strict else utl.distr_to_set(value)
    return None

def dexi_value_as_distr(value: DexiValue) -> Optional[list[float]]:
    """Converts a `DexiValue` object to a value distribution.

    Args:
        value (DexiValue): A `DexiValue`.

    Returns:
        Optional[list[float]]:
            `value` represented in terms of a value distribution,
            or None if it cannot be interpreted.

    Examples:
       >>> dexi_value_as_distr(2)
       [0.0, 0.0, 1.0]
       >>> dexi_value_as_distr({1, 2})
       [0.0, 1.0, 1.0]
       >>> dexi_value_as_distr({0: 0.5, 2: 1.0})
       [0.5, 0.0, 1.0]
       >>> dexi_value_as_distr((1, 1, 2, 2))
       [0.0, 1.0, 1.0]
    """
    if isinstance(value, int):
        value = {value}
    if isinstance(value, tuple):
        value = set(value)
    if isinstance(value, set):
        return utl.set_to_distr(value)
    if isinstance(value, dict):
        value = utl.dict_to_list(value)
    if isinstance(value, list):
        return value
    return None

def reduce_set(value: DexiValue) -> DexiValue:
    """Reduces a `DexiValue`, represented as a set,
    to a smaller data representation, if possible.

    Typical reductions:
       * an empty set to None: ``{} -> None``
       * a single-element tuple or set to int: ``(1,) -> {1} -> 1`` or ``{"low"} -> "low"``

    Args:
        value (Any): A `DexiValue`.

    Returns:
        DexiValue:
            Reduced representation of `value`, or `value` itself
            if no reduction is possible.

    Examples:
       >>> reduce_set(set()) # returns None
       >>> reduce_set({1})
       1
       >>> reduce_set({1, 2}) # no reduction
       {1, 2}
       >>> reduce_set(0.1) # no reduction
       0.1
    """
    if not isinstance(value, set):
        return value
    if len(value) == 0:
        return None
    if len(value) == 1:
        (element,) = value
        if isinstance(element, (str, int)):
            return element
    return value

def reduce_dexi_value(value: DexiValue) -> DexiValue:
    """Reduce a `DexiValue` to a smaller and possibly more comprehensible
    data representation, if possible.

    Typical reductions:
       * a tuple to set: ``(1, 1, 2, 2) -> {1, 2}``
       * a single-element tuple or set to int: ``(1,) -> {1} -> 1``
       * a distribution to set, if possible: ``[1.0, 0.0, 1.0] -> {0, 2}``

    Args:
        value (DexiValue): A `DexiValue`.

    Returns:
        DexiValue: Reduced representation of `value`, or `value` itself
        if no reduction is possible.

    Examples:
       >>> reduce_dexi_value((1, 1, 2, 2))
       {1, 2}
       >>> reduce_dexi_value({1})
       1
       >>> reduce_dexi_value([1.0, 0.0, 1.0])
       {0, 2}
       >>> reduce_dexi_value([1.0, 0.5, 1.0]) # no reduction
       [1.0, 0.5, 1.0]
       >>> reduce_dexi_value({1: 1.0})
       1
    """
    if isinstance(value, (tuple, set)):
        return reduce_set(set(value))
    if isinstance(value, list):
        as_set = utl.distr_to_strict_set(value)
        if isinstance(as_set, set):
            return reduce_set(as_set)
    if isinstance(value, dict):
        as_distr = dexi_value_as_distr(value)
        if as_distr is not None:
            return reduce_dexi_value(as_distr)
    return value

def aggregate_value(value: DexiValue, aggregate: str = "mean", interpret: str = "distribution"
                    ) -> Optional[int | float]:
    """Aggregates `value` to a single number or None.

    Args:
        value (DexiValue):
            A `DexiValue` (internal representation without strings).
        aggregate (str, optional):
            One of  "min", "max" or "mean".
            Determines aggregation operation in the case that `value` is a set or distribution.
            Defaults to "mean".
        interpret (str):
            Whether to interpret value distributions as sets ("set") or
            distributions ("distribution").
            Defaults to "distribution".

    Returns:
        Optional[int | float]: Aggregated value or None.
    """
    assert aggregate in ["min", "max", "mean"], \
        'Parameter "aggregate" must be one of: "min", "max", "mean"'
    assert interpret in ["set", "distribution"], \
        'Parameter "interpret" must be "set" or "distribution"'
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if utl.objlen(value) == 0:
        return None
    if isinstance(value, list) and interpret == "set":
        value = dexi_value_as_set(value)
    if isinstance(value, (set, tuple)):
        if aggregate == "min":
            return min(value)
        if aggregate == "max":
            return max(value)
        return mean(value)
    if isinstance(value, list):
        if aggregate == "mean":
            return sum(i * value[i] for i in range(len(value)))
        setval = dexi_value_as_set(value)
        assert setval is not None
        if aggregate == "min":
            return min(setval)
        if aggregate == "max":
            return max(setval)
    return None

def compare_values(value1: DexiValue, value2: DexiValue) -> Optional[int]:
    """Compare two DEXi values.

    Args:
        value1 (DexiValue): First value.
        value2 (DexiValue): Second value.

    Returns:
        Optional[int]: 0 if values are equal, -1 if `value1 < value2`, +1 if `value1 > value2`
        and None if values are incomparable. Values are incomparable if they are not of `DexiValue`
        type or if they represent two overlapping sets.
    """
    if value1 is None or value2 is None:
        return None
    if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
        return 0 if value1 == value2 else 1 if value1 > value2 else -1
    value1 = dexi_value_as_set(value1)
    value2 = dexi_value_as_set(value2)
    if value1 is None or value2 is None:
        return None
    if value1 == value2:
        return 0
    if len(value1) == 0 or len(value2) == 0:
        return None
    l1 = min(value1)
    h1 = max(value1)
    l2 = min(value2)
    h2 = max(value2)
    return -1 if h1 < l2 else 1 if h2 < l1 else None

def compare_values_by_preference(value1: DexiValue, value2: DexiValue, order: Optional[DexiOrder]
                                 ) -> Optional[int]:
    """Compare two DEXi values, considering preference `order`. 

    Args:
        value1 (DexiValue): First value.
        value2 (DexiValue): Second value.
        order (Optional[DexiOrder]): Preference order.

    Returns:
        Optional[int]:
            Returns result of :py:func:`dexipy.values.compare_values`,
            interpreted in the context of preference order. 
            When order is None, results are retained.
            Results `0` (equal values) and `None` (incomparable values) are retained
            for any order.
            Results `-1` and `+1` are retained when `order` is ascending and
            reversed when `order` is descending.
            When `order` is `DexiOrder.NONE`, non-equal values return None.
    """
    comp = compare_values(value1, value2)
    if order is None:
        return comp
    if comp is None or comp == 0:
        return comp
    if order is DexiOrder.ASCENDING:
        return comp
    if order is DexiOrder.DESCENDING:
        # pylint: disable-next=invalid-unary-operand-type
        return -comp
    if order is DexiOrder.NONE:
        return None
    return None

def distr_to_dexi_string(value: list) -> str:
    """Convert a value distribution to a string that can be imported
    by DEXi/DEXiWin software.

    Args:
        value (list): Value distribution.

    Returns:
        str: DEXi representation of `value`.
    """
    result = ""
    for idx, val in enumerate(value):
        if val != 0.0:
            if result != "":
                result = result + ";"
            result = result + str(idx + 1) + "/" + str(val)
    return result

def export_dexi_value(value: DexiValue) -> str:
    """Formats `value` so that it can be imported to DEXi/DEXiWin software.

    Args:
        value (DexiValue):
            A `DexiValue` to be formatted.
            Internal (non-text) representation of values is assumed.

    Returns:
        str: String representation of `value`.

    Raises:
        ValueError: When `value` is not a `DexiValue` or is represented in a way
            that cannot be interpreted without model context.

    """
    if value is None:
        return "<undefined>"
    if isinstance(value, tuple):
        value = set(value)
    if isinstance(value, int):
        return str(value + 1)
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        return str(value)
    if isinstance(value, set):
        return ";".join(export_dexi_value(v) for v in value)
    if isinstance(value, dict):
        value = utl.dict_to_list(value)
    if isinstance(value, list):
        return distr_to_dexi_string(value)
    raise ValueError(f"Cannot export value {str(value)}")

class DexiValues:
    """A wrapper class around a `DexiValue` data element.
    An object of this class contains a `value` of type :py:attr:`dexipy.values.DexiValues`,
    on which methods operate.

    Args:
       value (DexiValue): A `DexiValue` element stored internally and operated upon by methods.
    """

    def __init__(self, value: DexiValue):
        """Create a `DexiValues` object.

        Args:
            value (Any): A `DexiValue` to be operated upon.
        """
        self.value = value

    def value_type(self) -> Optional[DexiValueType]:
        """Determine the value type of `self.value`."""
        return dexi_value_type(self.value)

    def check_value(self) -> bool:
        """Check whether or not `self.value` contains valid `DexiValue` data."""
        return check_dexi_value(self.value)

    def as_set(self, strict: bool = False) -> Optional[set[int]]:
        """Convert `self.value` to a set, if possible.
        See :py:meth:`dexipy.values.dexi_value_as_set` for details.

        Args:
            strict (bool, optional):
               Defines the conversion when `self.value` is a value distribution.
               When True, only distributions that clearly represent sets, i.e., contain only
               0.0 or 1.0 elements, are converted. When False, all elements with non-zero values
               are considered set members.
               Defaults to False.
        """
        return dexi_value_as_set(self.value, strict = strict)

    def as_distr(self) -> Optional[list[float]]:
        """Convert `self.value` to a value distribution, if possible."""
        return dexi_value_as_distr(self.value)

    def reduce(self) -> DexiValue:
        """Reduces the data representation of `self.value`, if possible.
        See :py:meth:`dexipy.values.reduce_dexi_value` for details.
        """
        return reduce_dexi_value(self.value)

    def reduce_value(self) -> None:
        """Returns a reduced data representation of `self.value`."""
        self.value = reduce_dexi_value(self.value)

    def val_str(self, scale: Any, none: Optional[str] = None,
                reduce: bool = False, decimals: Optional[int] = None, use_dict: bool = True
                ) -> Optional[str]:
        """Returns a string representation of `self.value`.
        See :py:func:`dexipy.dexi.value_text` for more details.

        Args:
            scale (Any):
                Expected a :py:class:`dexipy.dexi.DexiScale` or
                :py:class:`dexipy.dexi.DexiAttribute` object.
            none (Optional[str], optional):
                An optional string that is returned when the value cannot be interpreted.
                Defaults to None.
            reduce (bool, optional):
                Whether or not the value is reduced (see :py:func:`reduce_dexi_value`)
                prior to processing. Defaults to False.
            decimals (Optional[int], optional):
                The number of decimals used to display float numbers. Defaults to None.
            use_dict (bool, optional):
                Whether or not the dictionary-form is used for
                displaying value distributions (rather than list-form).
                Defaults to True.
        """
        return dxi.value_text(
                self.value, scale,
                none = none, reduce = reduce, decimals = decimals, use_dict = use_dict
                )
