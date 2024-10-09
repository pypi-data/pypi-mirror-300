"""
Module `dexipy.dexi` is the main DEXiPy module.
It defines all the main classess that constitute a DEXi model and
exposes all functions that are usually used to read DEXi models,
and evaluate and analyze decision alternatives.
"""

from __future__ import annotations
from typing import Any, Sequence, Optional, Iterable
import sys
import math
import keyword as kwd
from copy import deepcopy
from dexipy.types import BoundAssoc, DexiOrder, DexiQuality, DexiValue
from dexipy.types import DexiAlternative, DexiAlternatives, DexiAltData
import dexipy.utils as utl
import dexipy.values as vls

# also imports dexipy.parse, dexipy.eval and dexipy.analyse (partial),
# but later or inline, to avoid circular imports

def dexi_value_qualities(value: DexiValue, scale: Optional[DexiScale]
                        ) -> Optional[Sequence[Optional[DexiQuality]]]:
    """Returns a list of DexiQuality items for `value` interpreted as a set.

    Args:
        value (DexiValue): A `DexiValue`.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.

    Returns:
        Optional[Sequence[Optional[DexiQuality]]]:
            A list of `DexiQuality` items corresponding to `value` items,
            where `value` is interpreted as a value set on `scale`.
    """
    val = vls.dexi_value_as_set(value)
    if val is None or scale is None:
        return None
    return [scale.value_quality(v) for v in val]

def dexi_value_has_quality(value: DexiValue, scale: Optional[DexiScale], quality: DexiQuality
                          ) -> bool:
    """Determines whether `value`, interpreted on `scale`,
    has at least one element of given `quality`.

    Args:
        value (DexiValue): A `DexiValue`.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.
        quality (DexiQuality): Required `DexiQuality`.

    Returns:
        bool: Whether or not `value` contains an item of given `quality`.
    """
    if value is None or scale is None:
        return False
    qualities = dexi_value_qualities(value, scale)
    if qualities is None:
        return False
    return quality in qualities

def dexi_value_has_bad(value: DexiValue, scale: Optional[DexiScale]) -> bool:
    """Determines whether `value`, interpreted on `scale`,
    has at least one element of `DexiQuality.BAD`.

    Args:
        value (DexiValue): A `DexiValue`.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.
 
    Returns:
        bool: Whether or not `value` contains an item of given `DexiQuality.BAD`.
    """
    return dexi_value_has_quality(value, scale, DexiQuality.BAD)

def dexi_value_has_none(value: DexiValue, scale: Optional[DexiScale]) -> bool:
    """Determines whether `value`, interpreted on `scale`,
    has at least one element of `DexiQuality.NONE`.

    Args:
        value (DexiValue): A `DexiValue`.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.
 
    Returns:
        bool: Whether or not `value` contains an item of given `DexiQuality.NONE`.
    """
    return dexi_value_has_quality(value, scale, DexiQuality.NONE)

def dexi_value_has_good(value: DexiValue, scale: Optional[DexiScale]) -> bool:
    """Determines whether `value`, interpreted on `scale`,
    has at least one element of `DexiQuality.GOOD`.

    Args:
        value (DexiValue): A `DexiValue`.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.
 
    Returns:
        bool: Whether or not `value` contains an item of given `DexiQuality.GOOD`.
    """
    return dexi_value_has_quality(value, scale, DexiQuality.GOOD)

def compare_values_on_scale(value1: DexiValue, value2: DexiValue,
                            scale: Optional[DexiScale],
                            force: bool = False) -> Optional[int]:
    """Compare DEXi  values `value1` and `value2` considering `scale.order`.

    Args:
        value1 (DexiValue): First value.
        value2 (DexiValue): Second value.
        scale (Optional[DexiScale]): A `DexiScale` or derived object.
        force (bool, optional):
            Considered when `scale` or `scale.order` are None.
            When `force` is True, comparison is enforced,
            assuming ascending preference order.
            When False, None is returned in such cases.
            Defaults to False.

    Returns:
        Optional[int]:
            Returns result of :py:func:`dexipy.values.compare_values_by_preference`,
            considering `scale.order`. 
    """
    if scale is None or scale.order is None:
        return vls.compare_values(value1, value2) if force else None
    return vls.compare_values_by_preference(value1, value2, scale.order)

class DexiScale:
    """`DexiScale` is a base class for representing DEXi value scales.

    A value scale defines the type and set of values that can be assigned to some
    :py:class:`dexipy.dexi.DexiAttribute`.

    :py:class:`dexipy.dexi.DexiScale` defines attributes and methods common to all scales.
    Normally, this class should not be created itself, but only through derived scale classes,
    :py:class:`dexipy.dexi.DexiContinuousScale` and :py:class:`dexipy.dexi.DexiDiscreteScale`.

    Args:
        order (DexiOrder):
            Preferential order of the scale.
            Defaults to DexiOrder.ASCENDING.
    """

    _order = {DexiOrder.DESCENDING: "-", DexiOrder.NONE: "*", DexiOrder.ASCENDING: "+"}

    @classmethod
    def equal_scales(cls, scl1, scl2) -> bool:
        """Checks whether of not two scales are equal.

        Args:
            scl1 (Any): First scale.
            scl2 (Any): Second scale.

        Returns:
            bool:
                Returns True if both scales are None or both are
                not None and ``scl1.equals(scl2)``.
                Returns False for non-scale arguments.
        """
        if scl1 is None:
            return scl2 is None
        if scl2 is None:
            return False
        return isinstance(scl1, DexiScale) and isinstance(scl2, DexiScale) and scl1.equal(scl2)

    def __init__(self, order: DexiOrder = DexiOrder.ASCENDING):
        self.order: DexiOrder = order

    def scale_str(self) -> str:
        """Returns a short string representing the scale to be used in DEXi model printouts.

        Returns:
            str: A short string representation of this scale.
        """
        return self._order[self.order]

    def equal(self, scl: Optional[DexiScale]) -> bool:
        """Checks whether or not this scale is equal to another scale `scl`.

        Args:
            scl (Optional[DexiScale]):
                Expected a :py:class:`dexipy.dexi.DexiScale` object.

        Returns:
            bool: Is this scale equal to `scl`?
        """
        return isinstance(scl, DexiScale) and self.order == scl.order

    def is_discrete(self) -> bool:
        """Returns True is this scale is discrete.

        Returns:
            bool: Is this scale discrete?
        """
        return False

    def is_continuous(self) -> bool:
        """Returns True is this scale is continuous.

        Returns:
            bool: Is this scale continous?
        """
        return False

    def count(self) -> int:
        """Returns the number of discrete values of this scale.

        Returns:
            int: The number of values or 0 for non-discrete scales.
        """
        return 0

    # pylint: disable-next=unused-argument
    def value_index(self, value: Any) -> Optional[int]:
        """Returns the index of `value` in the scale.

        Returns:
            Optional[int]: Integer index or None for non-discrete scales.
        """
        return None

    # pylint: disable-next=unused-argument
    def value_quality(self, value: Any) -> Optional[DexiQuality]:
        """Returns the quality (value class) of `value`.

        Args:
            value (Any): Some scale value, usually a number or string.

        Returns:
            Optional[DexiQuality]: Value quality.
        """
        return None

    def value_qualities(self, value: DexiValue) -> Optional[Sequence[Optional[DexiQuality]]]:
        """Returns a list of DexiQuality items for `value` interpreted as a set on this scale."""
        return dexi_value_qualities(value, self)

    def has_quality(self, value: DexiValue, quality: DexiQuality) -> bool:
        """Determines whether or not `value`, interpreted as a set on this scale,
        contains at least one element of given `quality`"""
        return dexi_value_has_quality(value, self, quality)

    def has_bad(self, value: DexiValue) -> bool:
        """Determines whether or not `value`, interpreted as a set on this scale,
        contains at least one element of DexiQuality.BAD"""
        return dexi_value_has_bad(value, self)

    def has_none(self, value: DexiValue) -> bool:
        """Determines whether or not `value`, interpreted as a set on this scale,
        contains at least one element of DexiQuality.NONE"""
        return dexi_value_has_none(value, self)

    def has_good(self, value: DexiValue) -> bool:
        """Determines whether or not `value`, interpreted as a set on this scale,
        contains at least one element of DexiQuality.GOOD"""
        return dexi_value_has_good(value, self)

    def full_range(self) -> Optional[set[int]]:
        """Returns the full range of admissible values for this scale.

        Returns:
            Optional[set[int]]: A set of all values or None for non-discrete scales.
        """
        return None

class DexiContinuousScale(DexiScale):
    """`DexiContinuousScale` is a scale class representing continuous scales in DEXi.

     Args:
        order (DexiOrder, optional):
            Preferential order of the scale. Defaults to `DexiOrder.ASCENDING`.
        lpoint (float):
            Defines the interval [-Infinity, lpoint]. All float values lying
            in this interval are considered to be of a `DexiQuality.BAD` quality
            (for `order = DexiOrder.ASCENDING`)
            or `DexiQuality.GOOD` quality (for `order = DexiOrder.DESCENDING`).
        hpoint (float): Defines the interval [hpoint, +Infinity]. All float values lying
            in this interval are considered to be of a `DexiQuality.GOOD` quality
            (for order = `DexiOrder.ASCENDING`)
            or `DexiQuality.BAD` quality (for `order = DexiOrder.DESCENDING`).
    """

    def __init__(self,
                 order: DexiOrder = DexiOrder.ASCENDING,
                 lpoint: float = -math.inf,
                 hpoint: float = math.inf
                ):
        super().__init__(order = order)
        self.lpoint: float = lpoint
        self.hpoint: float = hpoint

    def scale_str(self) -> str:
        return f"{self.lpoint}:{self.hpoint} ({super().scale_str()})"

    def equal(self, scl: Optional[DexiScale]) -> bool:
        return \
            isinstance(scl, DexiContinuousScale) and super().equal(scl) \
            and self.lpoint == scl.lpoint and self.hpoint == scl.hpoint

    def is_continuous(self) -> bool:
        return True

    def value_quality(self, value: float) -> DexiQuality:
        if self.order == DexiOrder.ASCENDING:
            return \
                DexiQuality.BAD if value < self.lpoint \
                else DexiQuality.GOOD if value > self.hpoint \
                else DexiQuality.NONE
        if self.order == DexiOrder.DESCENDING:
            return \
                DexiQuality.BAD if value > self.hpoint \
                else DexiQuality.GOOD if value < self.lpoint \
                else DexiQuality.NONE
        return DexiQuality.NONE

class DexiDiscreteScale(DexiScale):
    """`DexiDiscreteScale` is a scale class representing qualitative (symbolic, discrete, verbal)
    scales in DEXi. Such scales are typical for DEXi models and are the only scale type supported
    by the DEXi Classic software.

    An attribute associated with a discrete scale can take values from a finite (and usually small)
    set of string values contained in `self.values`. Additionally, each of these values is
    associated with :py:class:`dexipy.types.DexiQuality`.
    The latter are contained in the list `self.quality`,
    which is of the same length as `self.values`.

    Args:
        order (DexiOrder, optional):
            Preferential order of the scale. Defaults to `DexiOrder.ASCENDING`.
        values (list[str]):
            A list of qualitative scale values.
            Example: ``self.values = ["low", "medium", "high"]``.
        descriptions (list[str], optional):
            A list of textual descriptions of the corresponding `self.values`.
            If necessary, the list is internally paddedd with empty strings
            to the same length as `self.values`.
        quality (list[DexiQuality], optional):
            A list of qualities, corresponding to `self.values`.
            Should be of the same length as `self.values`.
            Defaults to [], which assigns default qualities using
            :py:meth:`dexipy.dexi.DexiDiscreteScale.default_quality`.
    """

    @classmethod
    def default_quality(cls, order: DexiOrder, nvals: int) -> list[DexiQuality]:
        """Makes a default list of value qualities.

        Args:
            order (DexiOrder): Preferential order of the scale.
            nvals (int): The number of discrete scale values.

        Returns:
            list[DexiQuality]: A list of length `nvals` of value qualities.
            The list depends on `order` as follows:

               * DexiOrder.ASCENDING: Returns ``[DexiQuality.BAD, ...,  DexiQuality.GOOD]``
               * DexiOrder.DESCENDING: Returns ``[DexiQuality.GOOD, ...,  DexiQuality.BAD]``
               * DexiOrder.NONE: Returns ``[...]``

            Here,  ``...`` denotes a sufficiently long sequence of ``DexiQuality.NONE``.
        """
        quality = [DexiQuality.NONE] * nvals
        if order == DexiOrder.NONE or nvals <= 1:
            return quality
        if order == DexiOrder.ASCENDING:
            quality[0] = DexiQuality.BAD
            quality[-1] = DexiQuality.GOOD
        else:
            quality[0] = DexiQuality.GOOD
            quality[-1] = DexiQuality.BAD
        return quality

    def __init__(self, values: list[str],
                order: DexiOrder = DexiOrder.ASCENDING,
                descriptions: list[str] = [],
                quality: list[DexiQuality] = []
                ):
        super().__init__(order = order)
        self.values: list[str] = values
        self.nvals: int = self.count()
        self.descriptions: list[str] = utl.pad_list(descriptions, self.nvals, "")
        if quality is None or len(quality) == 0:
            self.quality: list[DexiQuality] = \
                DexiDiscreteScale.default_quality(self.order, self.nvals)
        else:
            self.quality = utl.pad_list(quality, self.nvals, DexiQuality.NONE)

    def count(self) -> int:
        return len(self.values)

    def scale_str(self) -> str:
        return "; ".join(self.values) + " (" + super().scale_str()+ ")"

    def equal(self, scl: Optional[DexiScale]) -> bool:
        return \
            isinstance(scl, DexiDiscreteScale) and \
            super().equal(scl) and \
            self.values == scl.values and \
            self.descriptions == scl.descriptions and \
            self.quality == scl.quality

    def is_discrete(self) -> bool:
        return True

    def value_index(self, value: str) -> int:
        """Returns the index of value in the scale.

        Args:
            value (str): Some string.

        Raises:
            ValueError: When `value` was not found.

        Returns:
            int: Index of `value` in `self.values`.
        """
        return self.values.index(value)

    def value_index_or_none(self, value: str) -> Optional[int]:
        """Returns the index of value in the scale or None if not found.

        Args:
            value (str): Some string.

        Returns:
            Optional[int]: Index of `value` in `self.values` or None if `value` was not found.
        """
        try:
            return self.value_index(value)
        except:
            return None

    def value_quality(self, value: int| str) -> Optional[DexiQuality]:
        try:
            idx = value if isinstance(value, int) else self.value_index_or_none(str(value))
            return None if idx is None else self.quality[idx]
        except:
            return None

    def full_range(self) -> set[int]:
        return set(range(self.count()))

def scale_of(obj: Any) -> Optional[DexiScale]:
    """Returns a DEXi scale related to `obj`.

    Args:
        obj (Any):
            Expected are :py:class:`dexipy.dexi.DexiScale` or
            :py:class:`dexipy.dexi.DexiAttribute` objects.

    Returns:
        Optional[DexiScale]:
            Returns `obj` if `obj` is a :py:class:`dexipy.dexi.DexiScale` object.
            Returns `obj.scale` if `obj` is :py:class:`dexipy.dexi.DexiAttribute`.
            Returns None for other object types.
    """
    if isinstance(obj, DexiScale):
        return obj
    if isinstance(obj, DexiAttribute):
        return obj.scale
    return None

def scale_value(value: DexiValue, scale: Any) -> DexiValue:
    """Checks and interprets `value` on `scale`.

    Args:
        value (DexiValue): Normally, a :ref:`DEXi value <dexivalues>` is expected.
        scale (Any): A :py:class:`dexipy.dexi.DexiScale` object.

    Raises:
        ValueError:
            When scale is undefined, when `value` does not contain a valid `DexiValue`
            or `value` cannot be interpreted on `scale`.

    Returns:
        DexiValue: An interpreted `value`. The interpretation includes:

        * replacing the value ``"*"`` by the actual
          :py:meth:`dexipy.dexi.DexiScale.full_range` of the scale,
        * interpreting ``""`` and ``"undef..."`` as None,
        * float values are admissible only with continuous scales,
          otherwise they are interpreted as None,
        * all value-name strings that occur in value sets, lists and dictionaries,
          are replaced by the corresponding numeric indices.
    """
    scale = scale_of(scale)
    if scale is None:
        raise ValueError("Scale is not defined")
    if value is None:
        return None
    if scale.is_continuous():
        assert isinstance(value, (int, float)), \
            f"Non-numeric value {value} assigned to continuous attribute"
        return float(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        if value == "*":
            return scale.full_range()
        if value == "" or value.lower().startswith("undef"):
            return None
        return scale.value_index(value)
    if isinstance(value, (set, tuple)):
        if isinstance(value, tuple):
            value = set(value)
        return set(val if isinstance(val, int) else scale.value_index(val) for val in value)
    if isinstance(value, list):
        return [float(val) for val in value]
    if isinstance(value, dict):
        indexed: dict[int, float]  = \
            {key if isinstance(key, int) else scale.value_index(key): float(val) \
                for key, val in value.items()
            }
        return utl.dict_to_list(indexed)
    raise ValueError(f"Cannot interpret value {value} on scale {scale.scale_str()}")

def bounded_scale_value(value: DexiValue, scale: Any) -> DexiValue:
    """A wrapper around :py:func:`dexipy.dexi.scale_value` that ensures that
    the resulting value lies within the bounds set up by `scale`.

    Args:
        value (DexiValue):
            A Dexi value specificatuion.
        scale (Any):
            Expected a :py:class:`dexipy.dexi.DexiScale` or
            :py:class:`dexipy.dexi.DexiAttribute` object.


    Raises:
        ValueError: When `value` cannot be interpreted or bound to `scale` limits.

    Returns:
        DexiValue: An interpreted value (see :py:func:`dexipy.dexi.scale_value`)
        and reduced to `scale` bounds.
    """
    scale = scale_of(scale)
    value = scale_value(value, scale)
    if value is None:
        return None
    if scale.is_continuous():
        return value
    nvals = scale.count()
    if isinstance(value, int):
        return 0 if value < 0 else nvals - 1 if value >= nvals else value
    if isinstance(value, set):
        return set(val for val in value if 0 <= val < nvals)
    if isinstance(value, list):
        return value[:nvals]
    raise ValueError(f"Cannot bound value {value} to scale {scale.scale_str()}")

def value_text(value: DexiValue | str,
               scale: Any,
               none: Optional[str] = str(None),
               reduce: bool = False,
               decimals: Optional[int] = None,
               use_dict: bool = True) -> Optional[str]:
    """Represents `value` by a human-readable string that can be printed.

    Args:
        value (DexiValue | str):
            Normally a `DexiValue`.
            May also be string, which is returned as-is.
        scale (Any):
            Expected a :py:class:`dexipy.dexi.DexiScale` or
            :py:class:`dexipy.dexi.DexiAttribute` object.
        none (Optional[str], optional):
            An optional string that is returned when the value cannot be interpreted.
            Defaults to None.
        reduce (bool, optional):
            Whether or not the value is reduced
            (see :py:func:`dexipy.values.reduce_dexi_value`) prior to processing.
            Defaults to False.
        decimals (Optional[int], optional): The number of decimals used to display
            float numbers. Defaults to None.
        use_dict (bool, optional):
            Whether or not the dictionary-form is used for displaying
            value distributions (rather than list-form). Defaults to True.

    Returns:
        Optional[str]: A string representation of `value`.
    """
    if isinstance(value, str):
        return value
    scale = scale_of(scale)
    if value is None or scale is None:
        return none
    if reduce:
        value = vls.reduce_dexi_value(value)
    result: Any = value
    if scale.is_continuous():
        assert isinstance(value, (int, float)), \
            f"Non-numeric value {value} assigned to continuous attribute"
        result = utl.round_float(value, decimals)
    elif not isinstance(value, str):
        if isinstance(value, int):
            try:
                result = scale.values[value]
            except:
                result = "<Out of bounds>"
        elif isinstance(value, (set, tuple)):
            if isinstance(value, tuple):
                value = set(value)
            result = tuple(scale.values[val] if isinstance(val, int) else str(val) for val in value)
        elif isinstance(value, list):
            if use_dict:
                try:
                    result = {scale.values[idx]: val if decimals is None else round(val, decimals)
                                for idx, val in enumerate(value) if val > 0.0}
                except: # keep the list form
                    result = utl.round_float_list(value, decimals)
            else:
                result = utl.round_float_list(value, decimals)
        elif isinstance(value, dict):
            result = {value_text(key, scale, none): utl.round_float(val, decimals) \
                        for key, val in value.items()
                      }
    return str(result)

class DexiFunction:
    """`DexiFunction` is a base class for representing DEXi aggregation and
    discretization functions.

    Args:
        attribute (Optional[DexiAttribute], optional):
            A :py:class:`dexipy.dexi.DexiAttribute` to
            which this function is assigned. Defaults to None.
    """

    def __init__(self, attribute: Optional[DexiAttribute] = None):
        self.attribute = attribute

    def nargs(self) -> int:
        """Returns the number of function arguments.

        Returns:
            int: The number of this function's arguments.
        """
        return 0

    def nvals(self) -> int:
        """Returns this function size.

        Returns:
            int:
                The number of this function's decision rules.
                Returns 0 for function types that do not have rules.
        """
        return 0

    def funct_str(self) -> str:
        """Creates a short string for displaying information about the function in printouts.

        Returns:
            str: A short string, whose contents depends on this function's type.
        """
        return "Undefined"

    def value(self, args) -> DexiValue:
        """Returns the function value for given arguments.

        Args:
            args (Any): Expected is a single float number or a list of integer arguments
                passed to the function.

        Raises:
            ValueError: When function value cannot be determined for the given `args`.

        Returns:
            DexiValue: Function value for the given `args`.
        """
        raise ValueError(f"Undefined DexiFunction.value({args})")

    def evaluate(self, args) -> DexiValue:
        """A wrapper around :py:meth:`dexipy.dexi.DexiFunction.value` that returns
        None when :py:meth:`value` raises an error.

        Args:
            args (Any):
                Expected is a single float number or a list of integer arguments
                passed to the function.

        Returns:
            DexiValue: Function value for the given `args`,
            or None when the value cannot be determined for the given `args`.
        """
        try:
            return self.value(args)
        except:
            return None

class DexiTabularFunction(DexiFunction):
    """`DexiTabularFunction` represents the most common function type used in DEXi models.
    Functions of this type aggregate discrete attribute values according to *decision rules*,
    defined in terms of a *decision table*.

    A decision table contains as many decision rules as there are possible combinations of
    input attributes' values. For instance, if some attribute has two inputs whose
    discrete scales have three and four values, respectively, then the number of rules
    is equal to :math:`3 * 4 = 12`. Each rule defines the value of the attribute for one
    of the possible combinations of values of the attribute's inputs.
    For example, a decision rule ``(0, 1): 2`` maps the zeroth and first value of the first and
    second input attribute to value 2 of the output attribute. A decision table is
    represented as a dictionary of such rules. Thus, it can be interpreted as a lookup table
    that, given a vector of values of `attribute.inputs`, (i.e., function arguments)
    returns the corresponding output attribute value. In general, the output value can be any
    :ref:`DEXi value <dexivalues>`.

    Notes:
        * In order to properly define the context in which the newly created function operates,
          at least one of the arguments, `attribute` or `dim`, must be given.
        * Decision rules must be defined either directly by the `values` argument,
          or indirectly using the `low` and `high` strings.

    Args:
        attribute (Optional[DexiAttribute], optional):
            A :py:class:`dexipy.dexi.DexiAttribute` to which this function is assigned.
            Both the attribute and its inputs are required to be discrete
            (i.e., associated with :py:class:`dexipy.dexi.DexiDiscreteScale`.
            Defaults to None.
        dim (Any, optional):
            A list of integers, representing the size of the corresponding
            input attribute dimensions.
            Defaults to None.
        values (Optional[list[DexiValue]], optional):
            A decision table. Represented in the form of a dictionary that maps
            function arguments (represented as integer tuples) to function values
            (represented as :ref:`dexivalues`).
            Defaults to None.
        low (Optional[str], optional):
            A DEXi string representing lower bounds of function values in `.dxi` files.
            Defaults to None.
        high (Optional[str], optional):
            A DEXi string representing upper bounds of function values in `.dxi` files.
            When None, it is assumed that ``low == high``.
            Defaults to None.

    Raises:
        ValueError:
            * When at least one of the arguments `attribute` or `dim` is not given.
            * When `dim` is not a list of integers, has length different from
                `attribute.count()` or contains dimensions incompatible with input attributes.
            * When `low` and/or `high` are of length different than the expected number
                of decision rules.
    """
    def __init__(self,
                 attribute: Optional[DexiAttribute] = None,
                 dim: Any = None, # expected list[int], checked in the code
                 values: Optional[list[Optional[DexiValue]]] = None,
                 low: Optional[str] = None,
                 high: Optional[str] = None):
        super().__init__(attribute)
        if attribute is None and dim is None:
            raise ValueError("At least one of the arguments 'attribute' or 'dim' must be specified")
        self.attribute = attribute
        if attribute is None:
            if dim is not None:
                dim = tuple(dim)
        else:
            dim = attribute.dim()
        if dim is None or len(dim) == 0 or not all(isinstance(d, int) and d > 0 for d in dim):
            raise ValueError(f"Erroneus function dimensions: {dim}")
        self.dim = dim
        nargs = len(dim)
        nvals = int(utl.prod(dim))
        if attribute is not None:
            if attribute.count() != nargs or attribute.dim() != dim:
                raise ValueError(
                    f"Incompatible attribute {attribute.name} and function dimensions {dim}"
                )
        if values is not None:
            values = utl.pad_list(values, nvals, None)
        elif low is not None:
            if high is None:
                high = low
            if len(low) != nvals:
                raise ValueError(f"Length of 'low' is {len(low)}, expected {nvals}")
            if len(high) != nvals:
                raise ValueError(f"Length of 'high' is {len(high)}, expected {nvals}")
            lvals = utl.rule_values(low)
            hvals = utl.rule_values(high)
            values = [lvals[i] if lvals[i] == hvals[i] else set(range(lvals[i], hvals[i] + 1)) \
                        for i in range(nvals)
                     ]
        else:
            values = [None] * nvals
        assert values is not None, "Internal error: None values"
        ranges = tuple(set(range(dim[i])) for i in range(nargs))
        indices = utl.cartesian_product(*ranges)
        assert len(indices) == utl.objlen(values), "Internal error: Length error"
        self.values: dict[tuple[int, ...], DexiValue] = \
            {indices[i]: values[i] for i in range(nvals)}

    def funct_str(self) -> str:
        return str(self.nvals()) + " " + "x".join(str(d) for d in self.dim)

    def nargs(self) -> int:
        return len(self.dim)

    def nvals(self) -> int:
        """Returns the function space size
        (the total number of input attributes' value combinations).

        Returns:
            int: Size of the space defined by this function's input attributes.
        """
        return len(self.values)

    def value_vector(self) -> list[DexiValue]:
        """Returns the vector of this function's values.

        Returns:
            list[DexiValue]: A list of DEXi values, extracted from `self.values`, in the order
            determined using :py:func:`dexipy.utils.cartesian_product`.
        """
        ranges = tuple(set(range(self.dim[i])) for i in range(self.nargs()))
        indices = utl.cartesian_product(*ranges)
        return [self.values[idx] for idx in indices]

    def value(self, args: Iterable[int]) -> DexiValue:
        """Returns the function value for given arguments.

        Args:
            args (Iterable[int]): A vector of integer arguments passed to the function.

        Raises:
            ValueError: When function value cannot be determined for the given `args`.

        Returns:
            DexiValue: Function value for the given `args`.
        """
        return self.values[tuple(args)]

class DexiDiscretizeFunction(DexiFunction):
    """`DexiDiscretizeFunction` represents DEXi functions that discretize numerical values of
    continuous attributes to qualitative values of discrete attributes. A `DexiDiscretizeFunction`
    can be associated only with a discrete attribute that has exactly one continuous input.
    The function discretizes numeric values of the input attribute and maps them to
    discrete values of the parent attribute.
    This function type is supported in DEXi Suite software, but not in DEXi Classic.

    Objects of class `DexiDiscretizeFunction` define discretization rules in terms of three lists:
    `values`, `bounds` and `assoc`.
    Using `n = self.nvals()` to denote the length of `values`,
    the required lengths of `bounds` and `assoc` are `n - 1`,

    The list `bounds` refers to values of the input attribute and partitions its scale
    in `n` intervals
    ``[-Infinity, bound[0]], [bound[0], bound[1]], ..., [bound[n - 1], +Infinity]``.

    The list `values` defines the output DEXi values for each interval.

    The list `assoc` contains :py:class:`dexipy.types.BoundAssoc` elements that indicate to
    which interval, lower or higher, belong the corresponding `bounds`.

    When creating a `DexiDiscretizeFunction`, the determining argument is `bounds`.
    The remaining two arguments, `values` and `assoc` are padded to the correct length,
    possibly inserting None and `BoundAssoc.DOWN`, respectively.

    Args:
        attribute (Optional[DexiAttribute], optional):
            A :py:class:`dexipy.dexi.DexiAttribute` to which this function is assigned.
            The attribute is required to be discrete (i.e., associated with
            :py:class:`dexipy.dexi.DexiDiscreteScale`) and must have exactly
            one continuous attribute (i.e., associated with
            :py:class:`dexipy.dexi.DexiContinuousScale`).
            Defaults to None.
        bounds (list[float], optional):
            List of bounds. Defaults to [].
        assoc (list, optional):
            List of bound associations. Defaults to [].
        values (list[DexiValue], optional):
            List of output DEXi values corresponding to each interval induced by `bounds`.
            Defaults to [].
    """
    def __init__(self,
                 attribute: Optional[DexiAttribute] = None,
                 bounds: list[float] = [],
                 assoc: list[BoundAssoc] = [],
                 values: list[DexiValue] = []):
        super().__init__(attribute)
        self.attribute = attribute
        self.bounds: list[float] = bounds
        nvals = len(bounds) + 1
        self.values: list[DexiValue]  = utl.pad_list(values, nvals, None)
        self.assoc: list[BoundAssoc] = utl.pad_list(assoc, nvals - 1, BoundAssoc.DOWN)

    def funct_str(self) -> str:
        result = []
        for i, val in enumerate(self.values):
            result.append(str(val))
            if i < len(self.bounds):
                assoc = self.bound_assoc(i)
                result.append(
                    f"[{self.bounds[i]}>" if assoc == BoundAssoc.UP else f"<{self.bounds[i]}]"
                    )
        return " ".join(result)

    def bound_assoc(self,
                    idx: int,
                    default: Optional[BoundAssoc] = None
                    ) -> Optional[BoundAssoc]:
        """Returns association of the `idx`-th bound.

        Args:
            idx (int):
                A bound index.
            default (BoundAssoc, optional):
                An optional association returned for out-of-bound indices.
                Defaults to None.

        Returns:
            Optional[BoundAssoc]:
                Association of the `idx`-th bound or `default` when `idx` is
                out of bounds.
        """
        if default is None:
            default = BoundAssoc.DOWN
        try:
            return self.assoc[idx]
        except:
            return default

    def nargs(self) -> int:
        return 1

    def nvals(self) -> int:
        return len(self.values)

    def value(self, args: float) -> DexiValue:
        """Returns the function value for given arguments.

        Args:
            args (float): A single float function argument.

        Returns:
            DexiValue: Function value for the given argument.
        """

        nvals = self.nvals()
        if self.values is None or nvals == 0:
            return None
        if nvals == 1:
            return self.values[0]
        lb = -math.inf
        la: Optional[BoundAssoc] = BoundAssoc.UP
        for i in range(nvals):
            hb = self.bounds[i] if i < nvals - 1 else math.inf
            ha = self.bound_assoc(i, BoundAssoc.DOWN) if i < nvals - 1 else BoundAssoc.DOWN
            if utl.is_in_range(args, lb, hb, la, ha):
                return self.values[i]
            lb, la = hb, ha
        return None


class DexiAttribute:
    """`DexiAttribute` is a class representing DEXi attributes.

    In a DEXi model, attributes are variables that represent observed properties of decision
    alternatives. Attributes are structured in a tree, so each attribute may, but need not,
    have one or more direct descendants (lower-level attributes) in the tree.
    Attributes without descendants are called *basic* and serve as model inputs.
    Attributes with one or more descendants are called *aggregate* and represent model outputs.
    In order to represent attribute hierarchies (directed acyclic graphs) rather than plain trees,
    some attributes may be *linked*: two attributes of which one links to another one collectively
    represent, in a conceptual sense, a single attribute in the hierarchy.

    When completely defined, each attribute is associated with a value scale represented by a
    :py:class:`dexipy.dexi.DexiScale` object.
    It is also expected that a :py:class:`dexipy.dexi.DexiFunction` is defined for each aggregate
    attribute, where it serves for the  aggregation or discretization of the attribute's inputs to
    output values of that attribute.

    Args:
        name (str, optional):
            Attribute name. Defaults to "".
        description (str, optional):
            Attribute description. Defaults to "".
        id (Optional[str] optional):
            Attribute ID. By default equals to `name`,
            but may be adjusted for uniqueness in the model context.
            Automatically adjusted after reading a `DexiModel` with
            :py:func:`dexipy.parse.read_dexi`.
            Defaults to None.
        inputs (Sequence[DexiAttribute], optional):
            A vector of this attribute's input attributes.
            Defaults to None.
        parent (DexiAttribute | DexiModel, optional):
            This attribute's parent attribute in the DEXi model tree.
            By convention, ``model.root.parent == model``.
            Defaults to None.
        link (DexiAttribute, optional):
            An optional link to an alias of this attribute. Defaults to None.
        scale (DexiScale, optional):
            A scale associated with this attribute. Defaults to None.
        funct (DexiFunction, optional):
            An aggregation/discretization function associated with this attribute.
            Defaults to None.
    """

    # pylint: disable=redefined-builtin
    def __init__(self,
                 name: str = "",
                 description: str = "",
                 id: Optional[str] = None,
                 inputs: Optional[Sequence[DexiAttribute]] = None,
                 parent: Optional[DexiAttribute | DexiModel] = None,
                 link: Optional[DexiAttribute] = None,
                 scale: Optional[DexiScale] = None,
                 funct: Optional[DexiFunction] = None):
        self.name = name
        self.id = name if id is None else id
        self.description = description
        self.inputs = [] if inputs is None else inputs
        self.parent = parent
        self.link = link
        self.scale = scale
        self.funct = funct
        self._alternatives: list[Any] = []
    # pylint: enable=redefined-builtin

    def ninp(self) -> int:
        """Returns the number of input attributes of this attribute.

        Returns:
            int: The number of input attributes.
        """
        return utl.objlen(self.inputs)

    def count(self) -> int:
        """Returns the number of input attributes of this attribute.

        Returns:
            int: The number of input attributes.
        """
        return self.ninp()

    def dim(self) -> list[Optional[int]]:
        """Returns dimensions of this attribute's input attributes.

        Returns:
            list[Optional[int]]:
                A list of all input attribute's scale sizes.
                May contain None elements for undefined input scales.
        """
        return [inp.scale.count() if isinstance(inp, DexiAttribute) and inp.scale is not None \
                else None \
                for inp in self.inputs
               ]

    def is_basic(self, include_linked: bool = True) -> bool:
        """Checks if this attribute is basic.

        Args:
            include_linked (bool, optional):
                Whether a linked attribute is considered basic. Defaults to True.

        Returns:
            bool: Is this attribute basic?
        """
        if self.is_aggregate():
            return False
        if include_linked:
            return True
        return not self.is_link()

    def is_aggregate(self) -> bool:
        """Checks if this attribute is aggregate.

        Returns:
            bool: Is this attribute aggregate?
        """
        return self.ninp() > 0

    def has_order(self, order: DexiOrder) -> bool:
        """Checks if this attribute's scale has `order`.

        Returns:
            bool: If this attribute has a scale and `scale.order` equals to `order`.
        """
        return self.scale is not None and self.scale.order == order

    def is_descending(self) -> bool:
        """Checks if this attribute's scale is descending.

        Returns:
            bool: Is this attribute's scale descending?
        """
        return self.has_order(DexiOrder.DESCENDING)

    def is_ascending(self) -> bool:
        """Checks if this attribute's scale is ascending.

        Returns:
            bool: Is this attribute's scale ascending?
        """
        return self.has_order(DexiOrder.ASCENDING)

    def is_ordered(self) -> bool:
        """Checks if this attribute's scale is ordered.

        Returns:
            bool: Is this attribute's scale ordered?
        """
        return self.scale is not None and self.scale.order != DexiOrder.NONE

    def is_link(self) -> bool:
        """Checks if this attribute is linked.

        Returns:
            bool: Is this attribute linked, i.e., has a defined `self.link`?
        """
        return self.link is not None

    def is_discrete(self) -> bool:
        """Returns True is this attribute's scale is discrete.

        Returns:
            bool: Does this attribute have a discrete scale?
        """
        return False if self.scale is None else self.scale.is_discrete()

    def is_continuous(self) -> bool:
        """Returns True is this attribute's scale is continuous.

        Returns:
            bool: Does this attribute have a continuous scale?
        """
        return False if self.scale is None else self.scale.is_continuous()

    def level(self) -> int:
        """Returns the level of this attribute in the DEXi model.
        The level of `DexiModel.root` is 0.

        Returns:
            int: The level of this attribute.
        """
        att = self.parent
        lev = 0
        while att is not None and isinstance(att, DexiAttribute):
            att = att.parent
            lev += 1
        return lev

    def affects(self, attribute: DexiAttribute) -> bool:
        """Checks if this attribute affects `attribute`.
        An attribute is affected if it lies on the path from the affecting attribute
        to the model root.

        Args:
            attribute (DexiAttribute): An attribute checked for being affected.

        Returns:
            bool: Is `attribute` affected by this attribute?
        """
        att = self.parent
        while att is not None and isinstance(att, DexiAttribute):
            if att == attribute:
                return True
            att = att.parent
        return False

    def model(self) -> Optional[DexiModel]:
        """Returns a :py:class:`dexipy.dexi.DexiModel` to which this attribute belongs.

        Returns:
            Optional[DexiModel]: The model containing this attribute.
            None might be returned if this attribute is improperly "wired" (using `self.parent`)
            in the enclosing model.
        """
        att = self.parent
        while att is not None:
            if isinstance(att, DexiModel):
                return att
            att = att.parent
        return None

    def att_str(self) -> str:
        """Returns a string representation of the main non-empty attributes of this object.

        Returns:
            str: A string representation of a dictionary containing the non-empty values
            of `name`, `id`, `description`, `inputs`, `link`, `scale` and `funct`.
        """
        result = {"name": self.name}
        if self.id != "":
            result["id"] = self.id
        if self.description != "":
            result["description"] = self.description
        if self.ninp() > 0:
            result["inputs"] = ", ".join(inp.id for inp in self.inputs)
        if self.link is not None:
            result["link"] = self.link.id
        if self.scale is not None:
            result["scale"] = self.scale.scale_str()
        if self.funct is not None:
            result["funct"] = self.funct.funct_str()
        return str(result)

    def inp_index(self, inp: DexiAttribute) -> Optional[int]:
        """Returns the index of `inp` in `self.inputs`.

        Args:
            inp (DexiAttribute): An attribute.

        Returns:
            Optional[int]: Index of `inp`, or None if not found.
        """
        try:
            return self.inputs.index(inp)
        except:
            return None

    def tree_indent(self,
                    none: str = " ",
                    thru: str = "|",
                    link: str  = "*",
                    last: str = "+"
                    ) -> str:
        """Creates a string indicating the level of this attribute and its connections with
        other attributes in the model.
        In model printouts, such a string can be used in front of the attribute name or ID,
        achieving an indented output.

        Args:
            none (str, optional):
                String to indicate no connection at a given tree level. Defaults to " ".
            thru (str, optional):
                Vertical connection to attributes displayed below this one.
                Defaults to "|".
            link (str, optional):
                Horizontal connection to this attribute and vertical connection
                to attributes displayed below. Defaults to "*".
            last (str, optional):
                Horizontal connection to the attribute that occurs as
                last child of the parent attribute. Defaults to "+".

        Returns:
            str: An indentation string, including connections with other attributes.
        """
        result = ""
        if self.parent is None or not isinstance(self.parent, DexiAttribute):
            return result
        idx = self.parent.inp_index(self)
        result = none if idx is None else last if idx + 1 >= self.parent.ninp() else link
        att = self.parent
        while att.parent is not None and isinstance(att.parent, DexiAttribute):
            idx = att.parent.inp_index(att)
            el = none if idx is None or (idx + 1) >= att.parent.ninp() else thru
            result = el + result
            att = att.parent
        return result

    def structure(self) -> str:
        """Makes a specific indentation string used in DEXiPy to print DEXi model structure.

        This method calls :py:meth:`dexipy.dexi.DexiAttribute.tree_indent` with
        arguments that indent attributes by two characters per level.

        Returns:
            str: A DEXiPy indentation string, including connections with other attributes.
        """
        return self.tree_indent(none = "  ", thru = "| ", link = "|-", last = "+-")

def att_names(atts: Iterable[DexiAttribute], use_id: bool = True) -> list[str]:
    """Given a sequence of attributes, returns the list of names or IDs of that attribute.

    Args:
        atts (Iterable[DexiAttribute]): A sequence of attributes.
        use_id (bool, optional):
            Whether to use attribute IDs (True) or names (False).
            Defaults to True.

    Returns:
        list[str]: A list of attributes' IDs or names.
    """
    return [None if not isinstance(att, DexiAttribute) else att.id if use_id else att.name \
            for att in atts
           ]

def subtree_order(att: DexiAttribute, prune: list[str] = [], links: bool = True) -> list[str]:
    """Determine the depth-first order of attributes, starting at `att` and pruning at `prune`.

    Args:
        att (DexiAttribute):
            The starting point of making the subtree.
        prune (list[str], optional):
            A list of attribute IDs at which to prune the search.
            Defaults to [].
        links (bool, optional):
            Whether to include linked attributes. Defaults to True.

    Returns:
        list[str]: A list of attribute IDs.
    """
    result: list[str] = []

    def add_to_order(att: DexiAttribute) -> None:
        attid = att.id
        if not attid in result:
            if att.link is None or links:
                result.append(attid)
            if attid not in prune:
                for inp in att.inputs:
                    add_to_order(inp)

    add_to_order(att)
    return result

def subtree_attributes(att: DexiAttribute,
                       prune: list[str] = [],
                       links: bool = True
                       ) -> list[DexiAttribute]:
    """Determine the depth-first order of attributes, starting at `att`
    and pruning at `prune`.

    Args:
        att (DexiAttribute): The starting point of making the subtree.
        prune (list[str], optional):
            A list of attribute IDs at which to prune the search.
            Defaults to [].
        links (bool, optional): Whether to include linked attributes. Defaults to True.

    Returns:
        list[DexiAttribute]: A list of DexiAttribute objects.
    """
    result: list[DexiAttribute] = []

    def add_to_order(att: DexiAttribute) -> None:
        if not att in result:
            if att.link is None or links:
                result.append(att)
            if att.id not in prune:
                for inp in att.inputs:
                    add_to_order(inp)

    add_to_order(att)
    return result

class DexiModel:
    """`DexiModel` is the class that represents a DEXi model.

    In DEXiPy, `DexiModel` objects are normally created by reading from a `.dxi` file,
    previously developed by external DEXi/DEXiWin software.
    Reading models from files ensures that they are properly "wired" into
    a consistent structure of attributes, scales and functions.
    In principle, all fields of a `DexiModel` should be thus considered read-only.
    DEXiPy does not provide any explicit functionality for creating and changing DEXi models.
    Models can still be created and modified in Python, but without any
    integrity or consistency guarantees.

    Args:
        name (str, optional):
            Model name. Defaults to "".
        description (str, optional):
            An optional textual description of the model. Defaults to "".
        root (Optional[DexiAttribute], optional):
            The virtual root of all subtrees/hierarchies of attributes in the model.
            Defaults to None.
        linking (bool, optional):
            Indicates whether or not the model uses linked attributes,
            which are used in DEXi to represent hierarchies of attributes
            (i.e., directed acyclic graphs) rather than trees.
            Defaults to False.

    Attributes:
        attributes (list[DexiAttribute]):
            List of all model attributes, using the depth-first order.
        natt (int):
            Length of `self.attributes`.
        att_names (list[str]):
            List of attribute names in the model, in the order of `self.attributes`.
        att_ids (list[str]):
            List of attribute IDs in the model, in the order of `self.attributes`.
        basic (list[DexiAttribute]):
            List of all basic attributes.
        aggregate (list[DexiAttribute]):
            List of all aggregate attributes.
        links (list[DexiAttribute]):
            List of all linked attributes.
        non_root (list[DexiAttribute]):
            List of all `self.attributes` without `self.root`.
        basic_names (list[str]):
            List of all basic attributes's names.
        aggregate_names (list[str]):
            List of all aggregate attributes' names.
        links_names (list[str]):
            List of all linked attributes' names.
        non_root_names (list[str]):
            List of all `self.non_root` attributes' names.
        basic_ids (list[str]):
            List of all basic attributes's IDs.
        aggregate_ids (list[str]):
            List of all aggregate attributes' IDs.
        links_ids (list[str]):
            List of all linked attributes' IDs.
        non_root_ids (list[str]):
            List of all `self.non_root` attributes' IDs.
        alternatives (DexiAlternatives):
            A list of DEXi decision alternatives defined as part of the model.
    """

    def __init__(self,
                name: str = "",
                description: str = "",
                root: Optional[DexiAttribute] = None,
                linking: bool = False):
        self.name = name
        self.description = description
        self.root = root
        self.linking = linking
        self.alternatives: DexiAlternatives = []
        self.att_ids: list[str] = []
        self.non_root_ids: list[str] = []
        self.basic_ids: list[str] = []
        self.aggregate_ids: list[str] = []
        self.link_ids: list[str] = []
        self.setup()

    def propagate_ids(self) -> None:
        """Propagates `self.att_ids` to other `self.*_ids` lists and to IDs of
        individual attributes in the model.
        Should be explicitly called after a modification of `self.att_ids`.
        """
        self.non_root_ids = [att.id for att in self.non_root]
        self.basic_ids = [att.id for att in self.basic]
        self.aggregate_ids = [att.id for att in self.aggregate]
        self.link_ids = [att.id for att in self.links]
        for i, attid in enumerate(self.att_ids):
            self.attributes[i].id = attid

    def make_ids(self, max_len: Optional[int] = None, var_names: bool = False) -> None:
        """A helper method for creating attribute IDs from attribute names.
        Generated IDs are assigned to `self.att_ids` and propagated through the model.

        Args:
            max_len (Optional[int], optional):
                Maximum length of IDs (excluding `"_<idx>"` strings
                added to ensure the uniqueness of IDs).
                Defaults to None, which leaves the attribute name length intact.
            var_names (bool, optional):
                Whether or not IDs should be generated so that they conform with
                Python's syntax for variable names.
                This allows using attribute IDs as function arguments,
                for example with :py:meth:`dexipy.dexi.DexiModel.alternative`.
                Defaults to False.
        """
        names = self.att_names
        if max_len is not None:
            names = [name[:max_len] for name in names]
        if var_names:
            names = utl.names_to_ids(names)
            names = [
                    name if name.isidentifier() and not kwd.iskeyword(name) else "_" + name \
                        for name in names
                    ]
        self.att_ids = \
            utl.unique_names(names, reserved = ["name", "description", "structure", "alternative"])
        self.propagate_ids()

    def setup(self) -> None:
        """A helper method called as the last step when creating a `DexiModel`.

        This method assigns `self.root`, sets attributes' parents, generates attribute IDs and
        creates all model-level attribute lists.
        If `self.linking` is True, it also traverses the model and links attributes.

        When manually changing elements of a `DexiModel`, calling this method might
        (but need not) reestablish a consistent model structure.

        Raises:
            ValueError: When `self.root` is undefined or not of the DexiAttribute class.
        """
        if not isinstance(self.root, DexiAttribute):
            raise ValueError(f'Undefined or non-attribute root attribute in model "{self.name}"')
        self.root.parent = self
        self.parent_attributes(self.root)
        self.attributes = self.collect_attributes(self.root)
        self.non_root = self.attributes[1:]
        self.natt: int = len(self.attributes)
        self.att_names = [att.name for att in self.attributes]
        if self.linking:
            self.link_attributes()
        self.basic = [att for att in self.non_root if att.is_basic()]
        self.aggregate = [att for att in self.non_root if att.is_aggregate()]
        self.links = [att for att in self.non_root if att.is_link()]
        self.make_ids()

        #alternatives

        # pylint: disable=protected-access
        len_alt = max(len(att._alternatives) for att in self.attributes)
        self.root._alternatives = \
            utl.unique_names(utl.pad_list(self.root._alternatives, len_alt, ""))
        for i, altname in enumerate(self.root._alternatives):
            altvals: DexiAlternative = {"name": altname}
            for att in self.attributes:
                if att != self.root:
                    value = att._alternatives[i] if 0 <= i < len(att._alternatives) else None
                    altvals[att.id] = value
            self.alternatives.append(altvals)
        for att in self.attributes:
            att._alternatives = []
        # pylint: enable=protected-access

    def __str__(self) -> str:
        lines: list[str] = []
        lines.append("DEXi Model: " + self.name)
        if self.description is not None and self.description != "":
            lines.append("Description: " + self.description)
        indices: list[str] = ["index"]
        ids: list[str] = ["id"]
        struct: list[str] = ["structure"]
        links: list[str] = ["link"]
        scales: list[str] = ["scale"]
        functs: list[str] = ["funct"]
        for idx, att in enumerate(self.attributes):
            indices.append(str(idx))
            ids.append(att.id)
            struct.append((att.structure() + " " + att.name).lstrip())
            links.append("" if att.link is None else att.link.id)
            scales.append("" if att.scale is None else att.scale.scale_str())
            functs.append("" if att.funct is None else att.funct.funct_str())
        columns = [indices, ids, struct, links, scales, functs]
        if len(self.link_ids) == 0:
            del columns[3]
        lines = lines + utl.table_lines(columns, align = "rlllll")
        return "\n".join(lines)

    def collect_attributes(self, att: DexiAttribute) -> list[DexiAttribute]:
        """Returns a list of attributes, obtained by a recursive depth-first travesal
        of the subtree rooted at `att`.

        Args:
            att (DexiAttribute): The root attribute of traversal.

        Returns:
            list[DexiAttribute]: List of attributes found in the subtree rooted at `att`,
            including `att`.
        """
        atts = []

        def collect(att: DexiAttribute) -> None:
            atts.append(att)
            for inp in att.inputs:
                collect(inp)

        collect(att)
        return atts

    def parent_attributes(self, att: DexiAttribute) -> None:
        """Traverses the subtree of attributes rooted at `att` and sets
        the `parent` field of each attribute.

        Args:
            att (DexiAttribute): The root attribute of traversal.
        """
        def set_parent(
            att: DexiAttribute,
            parent: Optional[DexiAttribute | DexiModel]
            ) -> None:
            att.parent = parent
            for inp in att.inputs:
                set_parent(inp, att)

        set_parent(att, att.parent)

    def _link_candidates(self, name: str) -> list[DexiAttribute]:
        return [att for att in self.attributes if att.name == name and not att.is_link()]

    def _link_attribute_by_name(self, name: str) -> Optional[DexiAttribute]:
        bas: Optional[DexiAttribute] = None
        agg: Optional[DexiAttribute] = None
        agg_count = 1
        candidates = self._link_candidates(name)
        for att in candidates:
            if att.is_basic():
                bas = att
            else:
                agg = att
                agg_count += 1
        return agg if agg is not None and agg_count == 1 else bas

    def _link_attribute(self, att: DexiAttribute) -> None:
        att.link = None
        if att.is_aggregate():
            return
        link = self._link_attribute_by_name(att.name)
        if link is not None:
            if att == link or att.affects(link) or \
              not DexiScale.equal_scales(att.scale, link.scale):
                link = None
            att.link = link

    def link_attributes(self) -> None:
        """Carries out the linking of attributes.

        DEXi attributes that have the same names and value scales,
        and satisfy some other constraints to prevent making cycles in the model,
        are linked together so that they logically represent a single attribute.
        In this way, a tree of attributes is conceptually turned in a hierarchy
        (directed acyclic graph).
        """
        for att in self.attributes:
            att.link = None
        for att in self.attributes:
            if att != self.root:
                self._link_attribute(att)

    def att_stat(self) -> dict[str, int]:
        """Counts attributes of different types in the model.

        Returns:
            dict[str, int]:
                A dictionary of the form
                ``{"all": int, "basic": int, "aggregate": int, "link": int}``,
                containing counts of the corresponding attribute types.
        """
        return {
            "all": len(self.attributes),
            "basic": len(self.basic),
            "aggregate": len(self.aggregate),
            "link": len(self.links)
            }

    def att_index(self, attname: str, use_id: bool = True) -> Optional[int]:
        """Given an ID or name of an attribute, find its index in `self.attributes`.

        Args:
            attname (str):
                Attribute ID or name.
            use_id (bool, optional):
                Whether to search by attribute ID (True) or name (False).
                Defaults to True.

        Returns:
            Optional[int]:
                Attribute index or None if not found.
                When searching by name, attribute names may not be unique and
                only the first index is returned in this case.
        """
        try:
            atts = self.att_ids if use_id else self.att_names
            return atts.index(attname)
        except:
            return None

    def att_indices(self, attname: str) -> list[int]:
        """Returns the index of attribute named `attname` in `self.attributes`.

        Args:
            attname (str): Attribute name.

        Returns:
            list[int]:
                A list of attributes. May contain multiple attributes when
                attribute names are not unique.
        """
        return [i for i, att in enumerate(self.attributes) if att.name == attname]

    def attrib(self, find: Optional[DexiAttribute | str | int]) -> Optional[DexiAttribute]:
        """A general method for finding an attribute in the model.

        Args:
            find (Optional[DexiAttribute | str | int]): An attribute object, ID or index.

        Returns:
            Optional[DexiAttribute]: DexiAttribute object if found in the model, or None otherwise.
        """
        if find is None:
            return None
        att: Optional[DexiAttribute] = None
        try:
            if isinstance(find, DexiAttribute):
                att = find
            elif isinstance(find, str):
                idx = self.att_index(find)
                if idx is not None:
                    att = self.attributes[idx]
            else:
                att = self.attributes[find]
        except:
            pass
        return att

    def att_and_scale(self, find: Optional[DexiAttribute | str | int]
                      ) -> tuple[Optional[DexiAttribute], Optional[DexiScale]]:
        """Find an attribute and also return its scale.

        Args:
            find (Optional[DexiAttribute  |  str  |  int]): An attribute object, ID or index.

        Returns:
            tuple[Optional[DexiAttribute], Optional[DexiScale]]:
                A tuple consisting of DexiAttribute and DexiScale objects.
                If attribute has not been found, (None, None) is returned.
        """
        att = self.attrib(find)
        if att is None:
            return (None, None)
        return (att, att.scale)

    def find_attributes(self,
                        select: Iterable[Optional[DexiAttribute | str | int]],
                        exclude: list[DexiAttribute | str] = []
                        ) -> Optional[list[DexiAttribute] | list[Optional[DexiAttribute]]]:
        """A vectorized version of :py:meth:`dexipy.dexi.DexiModel.attrib`.
        Returns a list of attributes found in the model according to the `select` specification.

        Args:
            select (Iterable[Optional[DexiAttribute | str | int]]):
                A list of DEXiAttributes, attribute IDs or attribute indices.
            exclude (list[list[DexiAttribute | str]], optional):
                Exclude attributes elements from result.

        Returns:
            Optional[list[DexiAttribute] | list[Optional[DexiAttribute]]]:
                A list of DexiAttributes w.r.t. the correspoding `select` and
                `exclude` criteria.
                May contain None elements for not-found attributes.
        """
        return [self.attrib(sel) for sel in select if not sel in exclude]

    def attribute_list(self,
                        select: Iterable[Optional[DexiAttribute | str | int]],
                        exclude: list[DexiAttribute | str] = []
                        ) -> list[DexiAttribute]:
        """Wrapper around :py:meth:`find_attributes` that returns a clean list of attributes.

        Args:
            select (Iterable[Optional[DexiAttribute | str | int]]):
                A list of DEXiAttributes, attribute IDs or attribute indices.
            exclude (list[list[DexiAttribute | str]], optional):
                Exclude attributes elements from result.

        Returns:
            list[DexiAttribute]:
                A clean list of DexiAttributes w.r.t. the correspoding `select` and
                `exclude` criteria,
                without any None elements.
        """
        found = self.find_attributes(select, exclude)
        if found is None:
            return []
        return [att for att in found if att is not None]

    def first(self) -> Optional[DexiAttribute]:
        """Return first non-virtual model attribute, i.e., first descendant of `model.root`."""
        if self.root is None or self.root.count() == 0:
            return None
        return self.root.inputs[0]

    def evaluate(self,
            alternatives: Optional[DexiAltData] = None,
            method: str = "set",
            root: Optional[DexiAttribute] = None,
            prune: list[str] = [],
            pre_check: bool = False,
            bounding: bool = False,
            in_place: bool = False,
            eval_param: Optional[DexiEvalParameters] = None
            ) -> DexiAltData:
        """Evaluates decision alternative(s).

        See :ref:`evaluation` for more information about the evaluation process
        and evaluation methods used in DEXiPy.

        Args:
            alternatives (Optional[DexiAltData], optional):
                A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
                Defaults to None, which selects `self.alternatives`.
            method (str, optional):
                One of the strings "set", "prob", "fuzzy", "fuzzynorm" that
                select the evaluation method.
                Defaults to "set".
            root (Optional[DexiAttribute], optional):
                The topmost (root) attribute of the evaluation.
                Defaults to None, which selects `self.root`.
            prune (list[str], optional):
                List of attribute IDs at which the evaluation is "pruned".
                This means that input attributes below some pruned attribute are not evaluated and
                the pruned attribute is treated as an input (basic) attribute for this evaluation.
                Defaults to [].
            pre_check (bool, optional):
                Whether of not `alternatives` are checked by
                :py:meth:`dexipy.dexi.DexiModel.check_alternatives` prior to evaluation.
                Defaults to False.
            bounding (bool, optional):
                Whether or not the evaluation keeps calculated values within
                bounds prescribed by the corresponding scales. Defaults to False.
            in_place (bool, optional):
                If True, evaluation modifies `alternatives` in place,
                otherwise a copy is made and returned by the method.
                Defaults to False.
            eval_param (Optional[DexiEvalParameters], optional):
                Optional `DexiEvalParameters` that may
                customize the normalization and aggregation methods used in the evaluation.
                Defaults to None.

        Returns:
            DexiAltData:
                Returns an evaluated alternative or list of alternatives,
                depending on the type of the `alternatives` argument.
        """
        return evl.evaluate(
            self, alternatives, method, root, prune, pre_check, bounding, in_place, eval_param)

    def check_alternative(self,
                          alt: DexiAlternative,
                          aggregate: bool = False
                          ) -> dict[str, list[str]]:
        """Checks the data representing alternative `alt`,
        and reports found errors and warnings.

        Args:
            alt (DexiAlternative):
                A DEXi alternative.
            aggregate (bool, optional):
                Whether values of aggregate attributes are checked or not.
                The rationale for this argument is that :py:meth:`evaluate`, which
                typically follows checking,  overwrites values of aggregate attributes.
                Defaults to False.

        Returns:
            dict[str, list[str]]:
                A dictionary of the form
                ``{"errors": <list of error strings>, "warnings": <list of warning strings>}``.
        """
        errors: list[str] = []
        warnings: list[str] = []
        for key, val in alt.items():
            if key in self.att_ids:
                if isinstance(val, str):
                    errors.append(f"String value {val} assigned to model attribute {key}")
                    continue
                att = self.attrib(key)
                if att is None:
                    errors.append(f"Attribute {key} not found")
                    continue
                if att.scale is None:
                    warnings.append(f'Undefined scale of attribute "{key}"')
                elif aggregate or att.is_basic():
                    try:
                        scale_value(val, att.scale)
                    except (IndexError, ValueError, TypeError) as err:
                        errors.append(str(err))
                if aggregate and att.is_aggregate() and att.funct is None:
                    warnings.append(f'Undefined function of attribute "{key}"')
            elif isinstance(key, int):
                if not 0 <= key < self.natt:
                    errors.append(f"Attribute index [{key}] is out of range")
            elif key not in ["name", "description", "index"]:
                warnings.append(f'Unrecognized value key: "{key}"')
        return {"errors": errors, "warnings": warnings}

    def check_alternatives(self,
                          alternatives: Optional[DexiAltData] = None,
                          aggregate: bool = False
                          ) -> dict[str, list[str]]:
        """A vectorized version of :py:func:`dexipy.dexi.check_alternative`.
        May check a single alternative or a list of alternatives.

        Args:
            alternatives (Optional[DexiAltData], optional):
                A single alterative or a list of alternatives.
                Defaults to None, which selects `self.alternatives`.
            aggregate (bool, optional):
                Whether values of aggregate attributes are checked or not.
                Defaults to False.

        Raises:
            ValueError: When `alternatives` is not of a `DexiAltData` type.

        Returns:
            dict[str, list[str]]:
                A dictionary of the form
                ``{"errors": <list of error strings>, "warnings": <list of warning strings>}``.
        """
        if alternatives is None:
            alternatives = self.alternatives
        if isinstance(alternatives, dict):
            return self.check_alternative(alternatives, aggregate)
        if not isinstance(alternatives, list):
            raise ValueError("List of alternatives expected")
        errors: list[str] = []
        warnings: list[str] = []
        for idx, alt in enumerate(alternatives):
            altname = alt_name(alt, str(idx))
            check = self.check_alternative(alt, aggregate = aggregate)
            for err in check["errors"]:
                errors.append(f"Alternative {altname}: " + err)
            for warn in check["warnings"]:
                warnings.append(f"Alternative {altname}: " + warn)
        return {"errors": errors, "warnings": warnings}

    def deindex_alternative(self, alt: DexiAlternative) -> DexiAlternative:
        """Converts a `DexiAlternative` dictionary replacing all attribute indices
       with the corresponding attribute IDs.

        Args:
            alt (DexiAlternative):
                An alternative, represented by a dictionary.

        Returns:
            DexiAlternative:
                A dictionary with all numeric indices replaced with string IDs.
        """
        result: DexiAlternative = {}
        for att, val in alt.items():
            newatt = att
            if isinstance(att, int) and (0 <= att < len(self.att_ids)):
                newatt = self.att_ids[att]
            result[newatt] = val
        return result

    def textualize_alternative(self,
                               alt: DexiAlternative,
                               decimals: Optional[int] = None,
                               use_dict: bool = True
                               ) -> DexiAlternative:
        """Converts an internal representation of alternative `alt`, which typically uses
        numerical attribute and value indices, to a more comprehensible dictionary that
        uses string attribute IDs and value names.

        Args:
            alt (DexiAlternative):
                An alternative, represented by a dictionary.
            decimals (Optional[int], optional):
                The number of decimal places used to display floating-point numbers.
                Defaults to None.
            use_dict (bool, optional):
                Whether or not the dictionary-form is used for displaying
                value distributions (rather than list-form). Defaults to True.

        Returns:
            DexiAlternative:
                `alt` converted to an equivalent dictionary that uses strings instead of numbers.
        """
        result: DexiAlternative = {}
        for key, val in alt.items():
            att = self.attrib(key)
            if att is None or att.scale is None:
                result[key] = val
            else:
                result[att.id] = \
                    value_text(val, att.scale, decimals = decimals, use_dict = use_dict)
        return result

    def textualize_alternatives(self,
                                alts: DexiAltData,
                                decimals: Optional[int] = None, use_dict: bool = True
                                ) -> DexiAltData:
        """A vectorized version of :py:func:`dexipy.dexi.textualize_alternative`.
        May textualize a single alternative or a list of alternatives.

        Args:
            alts (DexiAltData):
                A single alterative or a list of alternatives.
                Defaults to None, which selects `self.alternatives`.
            decimals (Optional[int], optional):
                The number of decimal places used to display floating-point numbers.
                Defaults to None.
            use_dict (bool, optional):
                Whether or not the dictionary-form is used for displaying
                value distributions (rather than list-form). Defaults to True.

        Returns:
            DexiAltData:
                `alts` converted to an equivalent representation that uses strings
                instead of numbers.
        """
        if isinstance(alts, dict):
            return self.textualize_alternative(alts)
        return [self.textualize_alternative(alt, decimals = decimals, use_dict = use_dict) \
                    for alt in alts
               ]

    def alt_table(self,
                  alternatives: Optional[DexiAltData] = None,
                  alt_head: str = "alternative",
                  sel_att: list[str] = [],
                  basic: bool = False,
                  aggregate: bool = False,
                  structure: bool = False,
                  decimals: Optional[int] = None,
                  transpose: bool = False,
                  use_dict: bool = True,
                  text: bool = False,
                  none: str = "") -> str:
        """Creates a string that, when printed out, displays `alternatives` in a tabular form.

        Args:
            alternatives (Optional[DexiAltData], optional):
                A single alterative or a list of alternatives.
                Defaults to None, which selects `self.alternatives`.
            alt_head (str, optional):
                Text to be displayed in the topmost-left cell.
                Defaults to "alternative".
            sel_att (list[str], optional):
                A list of attribute IDs to be displayed.
                Defaults to [], which selects all non-root attributes,
                unless overriden by `basic` and `aggregate` arguments.
            basic (bool, optional):
                Selects all basic attributes for display.
                Considered only when ``sel_att == []``. Defaults to False.
            aggregate (bool, optional):
                Selects all aggregate attributes for display.
                Considered only when ``sel_att == []``. Defaults to False.
            structure (bool, optional):
                Whether attribute structure is displayed together with attribute names.
                Considered only when `transpose` is True. Defaults to False.
            decimals (Optional[int], optional):
                The number of decimal places used to display floating-point numbers.
                Defaults to None.
            transpose (bool, optional):
                Normally, the table displays attributes in rows and alternatives in columns.
                Setting this argument to True transposes the table.
                Defaults to False.
            use_dict (bool, optional):
                Whether or not the dictionary-form is used for displaying value
                distributions (rather than list-form).
                Defaults to True.
            text (bool, optional):
                Whether of not value cells are textualized using
                :py:meth:`dexipy.dexi.DexiModel.textualize_alternatives`.
                Defaults to False.
            none (str, optional):
                The string used to display None values.
                Defaults to "".

        Returns:
            str: A multi-line string representation of `alternatives`.
        """
        if alternatives is None:
            alternatives = self.alternatives
        if isinstance(alternatives, dict):
            alternatives = [alternatives]
        alts: DexiAltData = list(alternatives)
        if text:
            alts = self.textualize_alternatives(
                       alts, decimals = decimals, use_dict = use_dict
                   )
        if sel_att == []:
            if not aggregate and not basic: # default
                sel_att = self.non_root_ids
            else:
                if aggregate:
                    sel_att = self.aggregate_ids
                if basic:
                    sel_att = self.basic_ids
        att_text = []
        for att in sel_att:
            txt = att
            if structure:
                a = self.attrib(att)
                if a is not None:
                    txt = a.structure() + txt
            att_text.append(txt)
        cols = columnize(alts, alt_head, sel_att, att_text, transpose, none)
        return "\n".join(utl.table_lines(cols, align = "l", def_align = "r"))

    def alt_text(self, alternatives: Optional[DexiAltData] = None, **kwargs) -> str:
        """Creates a string that, when printed out, displays `alternatives` in
        a tabular and textualized form. It is meant as a convenient abbreviation
        for calling ``self.alt_table(alternatives, text = True, **kwargs)``.

        Args:
            alternatives (Optional[DexiAltData], optional):
                A single alterative or a list of alternatives.
                Defaults to None, which selects `self.alternatives`.
            **kwargs:
                Other arguments passed to :py:meth:`dexipy.dexi.DexiModel.alt_table`.

        Returns:
            str: A multi-line string representation of `alternatives`.
        """
        kwargs["text"] = True
        return self.alt_table(alternatives, **kwargs)

    def alternative(self,
               name: Optional[str] = None,
               description: Optional[str] = None,
               alt: Optional[DexiAlternative] = None,
               sel_att: list[str] = [],
               basic: bool = False,
               aggregate: bool = False,
               default: DexiValue = None,
               deindex: bool = False,
               values: Optional[DexiAlternative] = None,
               **kwargs) -> DexiAlternative:
        """Defines a new decision alternative.

        Args:
            name (Optional[str], optional):
                Name of the alternative. Defaults to None.
            description (Optional[str], optional):
                Textual description of the alternative. Defaults to None.
            alt (Optional[DexiAlternative], optional):
                A base alternative.
                If specified, all the values of `alt` are copied to the resulting alternative
                prior to adding or overwriting them with values specified in other arguments.
                Defaults to None.
            sel_att (list[str], optional):
                The list of attributes whose values are added to
                the resulting alternative and initialized to the None value.
                Defaults to [].
            basic (bool, optional):
                If True, add all basic attributes.
                Considered only when ``sel_att == []``. Defaults to False.
            aggregate (bool, optional):
                If True, add all aggregate attributes.
                Considered only when ``sel_att == []``. Defaults to False.
            default (DexiValue, optional):
                Default attribute value that is assigned
                unless it has been specified in other arguments. Defaults to None.
            deindex (bool, optional):
                Whether or not the resulting alternative data is deindexed
                after setup, using :py:func:`dexipy.dexi.deindex_alternative`.
                Defaults to False.
            values (Optional[DexiAlternative], optional):
                A dictionary of ``attribute_id: attribute_value`` or
                ``attribute_index: attribute_value`` elements, added to the resulting dictionary
                in addition to or overwriting values set by other arguments.
                Defaults to None.
            **kwargs:
                Keyword method arguments in the form ``attribute_id = attribute_value``.
                This form is possible only with attributes whose IDs match the Python's
                syntax for variable names.

        Returns:
            DexiAlternative:
                Alternative data represented as a dictionary consisting of
                ``attribute_id: attribute_value`` or ``attribute_index: attribute_value`` elements.
        """
        if alt is None:
            if sel_att == []:
                if basic == aggregate:
                    sel_att = self.non_root_ids
                elif aggregate:
                    sel_att = self.aggregate_ids
                else:
                    sel_att = self.basic_ids
            alt =  {id: default for id in sel_att} if alt is None else alt
        result = alternative(
                    name = name, description = description, alt = alt, values = values, **kwargs
                 )
        if deindex:
            result = self.deindex_alternative(result)
        return result

    def selective_explanation(self,
            alternatives: Optional[DexiAltData] = None,
            root: Optional[DexiAttribute] = None,
            prune: list[str] = [],
            text: bool = True,
            structure: bool = True
            ) -> None:
        """Selective Explanation

         Displays subtrees of `alternatives`' values in which values are particularly
         weak (`DexiQuality.BAD`) and particularly strong (`DexiQuality.GOOD`).

        Args:
            alternatives (Optional[DexiAltData], optional):
                A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
                Alternatives are assumed to be previously fully evaluated.
                Defaults to None, which selects all `self.alternatives`.
            root (Optional[DexiAttribute], optional):
                The topmost (root) attribute for displaying results.
                Defaults to None, which selects `self.root`.
            prune (list[str], optional):
                List of attribute IDs at which the display is "pruned",
                skipping their subordinate attributes.
                Defaults to [].
            text (bool, optional):
                Whether to display results textually (True) or
                using internal value representation (False).
                Defaults to True.
            structure (bool, optional):
                Whether to display only attribute IDs in the first column (False)
                or to extend them with tree-structure information.
                Defaults to True.

        Raises:
            ValueError: When `model`, `root` or `alternatives` are undefined.
        """
        # pylint: disable-next=import-outside-toplevel
        from dexipy.analyse import selective_explanation
        selective_explanation(self, alternatives, root, prune, text, structure)

    def plus_minus(self,
                   alt: DexiAlternative,
                   target: Optional[DexiAttribute] = None,
                   minus: int = sys.maxsize,
                   plus: int = sys.maxsize,
                   text: bool = True,
                   structure: bool = True
                   ) -> None:
        """Plus Minus Analysis

        Investigate the effects of changing single attributes' values
        on the evaluation of `alt`.
        The values of discrete basic attributes ("input attributes") are changed,
        one attribute at a time,
        by a particular number of steps downwards (`minus`) and upwards (`plus`),
        while observing the changes of the `target` attribute values.

        Args:
            alt (DexiAlternative): A single `DexiAlternative`.
                Assumed to be previously evaluated using :py:meth:`evaluate`.
            target (DexiAttribute, optional):
                A `DexiAttribute` on which effects are observed.
                Defaults to None, which selects self.root.
            minus (int, optional):
                The maximum number of downward steps to be made
                for each input attribute. Defaults to sys.maxsize.
                The actual `minus` value is further determined with respect to
                `alternative` values and involved attributes' scales.
            plus (int, optional):
                The maximum number of upward steps to be made
                for each input attribute. Defaults to sys.maxsize.
                The actual `plus` value is further determined with respect to
                `alternative` values and involved attributes' scales.
            text (bool, optional):
                Whether to display results textually (True)
                or using internal value representation (False).
                Defaults to True.
            structure (bool, optional):
                Whether to display only attribute IDs in the first column (False)
                or to extend them with tree-structure information. Defaults to True.

        Raises:
            ValueError: When `target` is None or does not have a scale defined.
            ValueError: When `alt` is not a single `DexiAlternative`.

        Returns:
            Optional[list[list[str]]]:
                A data table containing the following columns of strings:

                - First column: Attribute IDs, optionally extended with `structure` information.
                - For `-minus` to `-1`: Columns containing evaluation values of `target`
                  when decreasing attribute values by the corresponding number of steps.
                - Middle column:
                  Original `alternative` values assigned to the corresponding attributes.
                - For `+1` to `+plus`: Columns containing evaluation values of `target`
                  when increasing attribute values by the corresponding number of steps.

        Limitations:
            Only basic attributes with defined discrete scales participate in the analysis.
        """
        # pylint: disable-next=import-outside-toplevel
        from dexipy.analyse import plus_minus
        plus_minus(self, alt, target, minus, plus, text, structure)

    def compare_alternatives(self,
                             alt: DexiAlternative,
                             alternatives: Optional[DexiAltData] = None,
                             root: Optional[DexiAttribute] = None,
                             prune: list[str] = [],
                             compare: bool = True,
                             deep: bool = True,
                             text: bool = True,
                             structure: bool = True
                            ) -> None:
        """Compare Alternatives

        Compare `alt` with each of `alternatives`.
        Display only values that differ and, optionally when `compare = True`, include
        preference-relational operators.

        Args:
            alt (DexiAlternative):
                A single `DexiAlternative` to be compared with `alternatives`.
            alternatives (Optional[DexiAltData], optional):
                A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
                Alternatives are assumed to be previously fully evaluated.
                Defaults to None, which selects all `self.alternatives`.
            root (Optional[DexiAttribute], optional):
                The topmost (root) attribute for displaying results.
                Defaults to None, which selects `self.root`.
            prune (list[str], optional):
                List of attribute IDs at which the display is "pruned",
                skipping their subordinate attributes.
                Defaults to [].
            compare (bool, optional):
                Whether or not to display preference comparison operators
                "=", "<", ">", "<=", ">=". Defaults to True.
            deep (bool, optional):
                Whether or not "deep" comparison
                (see :py:meth:`dexipy.eval.compare_two_alternatives`) is carried out.
                Defaults to True.
            text (bool, optional):
                Whether to display results textually (True) or
                using internal value representation (False).
                Defaults to True.
            structure (bool, optional):
                Whether to display only attribute IDs in the first column (False)
                or to extend them with tree-structure information. Defaults to True.

        Raises:
            ValueError:
                When `alt` or `alternatives` are None, when `alt`
                is not a single alternative, and when `root` is undefined.

        Returns:
            None and prints out the resulting alternative comparison table.
        """
        # pylint: disable-next=import-outside-toplevel
        from dexipy.analyse import compare_alternatives
        compare_alternatives(self,
             alt, alternatives, root, prune, compare, deep, text, structure
        )

def alternative(name: Optional[str] = None,
                description: Optional[str] = None,
                alt: Optional[DexiAlternative] = None,
                values: Optional[DexiAlternative] = None,
                **kwargs) -> DexiAlternative:
    """Defines a new decision alternative.

    Args:
        name (Optional[str], optional):
            Name of the alternative. Defaults to None.
        description (Optional[str], optional):
            Textual description of the alternative. Defaults to None.
        alt (Optional[DexiAlternative], optional):
            A base alternative.
            If specified, all the values of `alt` are copied to the resulting alternative
            prior to adding or overwriting them with `values`. Defaults to None.
        values (Optional[DexiAlternative], optional):
            A dictionary of ``attribute_id: attribute_value``
            or ``attribute_index: attribute_value`` elements, added to the resulting dictionary.
            Defaults to None.
        **kwargs:
            Keyword function arguments in the form ``attribute_id = attribute_value``.
            This form is possible only with attributes whose IDs match Python's
            syntax for variable names.

    Raises:
        ValueError: When `alt` is not a dictionary.

    Returns:
        DexiAlternative:
            Alternative data represented as a dictionary consisting of
            ``attribute_id: attribute_value`` or ``attribute_index: attribute_value`` elements.
    """
    result: DexiAlternative = {} if alt is None else deepcopy(alt)
    if name is not None:
        result["name"] = name
    if description is not None:
        result["description"] = description
    if values is not None:
        if not isinstance(values, dict):
            raise ValueError(f"Values argument {values}: Expecting a dictionary")
        result.update(values)
    for att, val in kwargs.items():
        result[att] = val
    return result

def alt_name(alt: DexiAlternative,
             default: str = "",
             name: str = "name") -> str:
    """Extracts alternative name from DexiAlternative data.

    Args:
        alt (DexiAlternative): A DEXi alternative.
        default (str, optional): Name returned when no name has been found. Defaults to "".
        name (str, optional): Key string for finding alternative name. Defaults to "name".

    Returns:
        str: Name of the alternative, or `default` if not found.
    """
    return str(alt[name]) if name in alt.keys() else str(default)

def columnize(alternatives: DexiAltData,
              alt_head: str = "alternative",
              sel_att: list[str] = [],
              att_text: Optional[list[str]] = None,
              transpose: bool = False,
              none: str = "") -> list[list[str]]:
    """A helper function that "columnizes" DexiAltData.
    A suitable list of columns is produced for further processing.

    Args:
        alternatives (DexiAltData):
            A DEXi alternative or a list of DEXi alternatives.
        alt_head (str, optional):
            Text to be included as the first element of the first column.
            Defaults to "alternative".
        sel_att (list[str], optional):
            A list of selected attribute IDs.
            Any remaining IDs in `alternatives` are ignored. Defaults to [].
        att_text (list[str], optional):
            A text to be displayed for each corresponding item in `sel_att`.
            Considered only if not None, `sel_att` is defined, lengths of `sel_att` and
            `att_text` are equal and `transpose` is False.
            Defaults to None.
        transpose (bool, optional):
            Normally, columns correspond to alternatives.
            Setting `transpose` to True makes columns corresponding to attributes.
            Defaults to False.
        none (str, optional):
            A string to display None values. Defaults to "".

    Returns:
        list[list[str]]: List of columns. Each column is a list of strings.
        All columns are padded to the same length.
    """
    if isinstance(alternatives, dict):
        alternatives = [alternatives]
    if att_text is None:
        att_text = sel_att
    if len(att_text) != len(sel_att):
        raise ValueError("Arguments 'sel_att' and 'att_text' must be of the same length")
    attkeys = sel_att
    if attkeys == []:
        att_text = None
        for alt in alternatives:
            for key in alt.keys():
                if key not in attkeys:
                    attkeys.append(str(key))
    result: list[list[str]] = []
    if transpose:
        result.append(
            [alt_head] + [alt_name(alt, str(idx)) for idx, alt in enumerate(alternatives)]
        )
        for att in attkeys:
            result.append(
                [att] + [str(alt[att]) if att in alt.keys() else none for alt in alternatives]
            )
    else:
        if att_text is None:
            result.append([alt_head] + attkeys)
        else:
            result.append([alt_head] + att_text)
        for idx, alt in enumerate(alternatives):
            result.append(
                [alt_name(alt, str(idx))] +
                [str(alt[att]) if att in alt.keys() else none for att in attkeys]
                )
    return result

def alt_lines(alternatives: DexiAltData,
              alt_head: str = "alternative",
              sel_att: list[str] = [],
              transpose: bool = False,
              none: str = ""
              ) -> list[str]:
    """Makes a list of strings that represent `alternative` in a tabular form.

    Args:
        alternatives (DexiAltData):
            A DEXi alternative or a list of DEXi alternatives.
        alt_head (str, optional):
            Text to be included as the top-left element of the table.
            Defaults to "alternative".
        sel_att (list[str], optional):
            A list of selected attribute IDs.
            Any remaining IDs in `alternatives` are ignored.
            Defaults to [], which selects all attributes.
        transpose (bool, optional):
            Normally, table columns correspond to alternatives.
            Setting `transpose` to True makes columns corresponding to attributes.
            Defaults to False.
        none (str, optional): A string to display None values. Defaults to "".

    Returns:
        list[str]: A list of lines that can be joined together and printed.
    """
    return utl.table_lines(
        columnize(alternatives, alt_head, sel_att, sel_att, transpose, none),
        align = "l", def_align = "r")

# pylint: disable-next=wrong-import-position
import dexipy.parse as prs

def read_dexi(filename: str) -> DexiModel:
    """Reads a DEXi model from a `.dxi` file.

    Args:
        filename (str): File name.

    Returns:
        DexiModel: DEXi model read from the file.
    """
    return prs.read_dexi(filename)

def read_dexi_from_string(xml: str) -> DexiModel:
    """Reads a DEXi model from a `xml` string.

    Args:
        xml (str): XML string representation of a DEXi model, conforming to the format
            used in `.dxi` files.

    Returns:
        DexiModel: DEXi model read from the string.
    """
    return prs.read_dexi_from_string(xml)

# pylint: disable-next=wrong-import-position
import dexipy.eval as evl
# pylint: disable-next=wrong-import-position
from dexipy.eval import DexiEvalParameters

def evaluate(model: DexiModel,
             alternatives: Optional[DexiAltData] = None,
             method: str = "set",
             root: Optional[DexiAttribute] = None,
             prune: list[str] = [],
             pre_check: bool = False,
             bounding: bool = False,
             in_place: bool = False,
             eval_param: Optional[DexiEvalParameters] = None
            ) -> DexiAltData:
    """Evaluates decision alternative(s).

    Please see :ref:`evaluation` for more information about the evaluation process and
    evaluation methods used in DEXiPy.

    Args:
        model (DexiModel):
            A `DexiModel`. Required.
        alternatives (Optional[DexiAltData], optional):
            A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
            Defaults to None, which selects `model.alternatives`.
        method (str, optional): One of the strings "set", "prob", "fuzzy", "fuzzynorm"
            that select the evaluation method. Defaults to "set".
        root (Optional[DexiAttribute], optional):
            The topmost (root) attribute of the evaluation.
            Defaults to None, which selects `model.root`.
        prune (list[str], optional):
            List of attribute IDs at which the evaluation is "pruned".
            This means that input attributes below some pruned attribute are not evaluated
            and the pruned attribute is treated as an input (basic) attribute for this evaluation.
            Defaults to [].
        pre_check (bool, optional):
            Whether or not `alternatives` are checked by
            :py:meth:`dexipy.dexi.DexiModel.check_alternatives` prior to evaluation.
            Defaults to False.
        bounding (bool, optional):
            Whether or not the evaluation keeps calculated values within
            bounds prescribed by the corresponding scales. Defaults to False.
        in_place (bool, optional):
            If True, evaluation modifies `alternatives` in place,
            otherwise a copy is made and returned by the method. Defaults to False.
        eval_param (Optional[DexiEvalParameters], optional):
            Optional `DexiEvalParameters`, that may customize
            the normalization and aggregation methods used in the evaluation.
            Defaults to None.

    Returns:
        DexiAltData: Returns an evaluated alternative or list of alternatives,
        depending on the type of the `alternatives` argument.
    """
    return evl.evaluate(
        model, alternatives, method, root, prune, pre_check, bounding, in_place, eval_param
        )
