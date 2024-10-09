"""
Module `dexipy.types` defines type aliases and enumeration classess
that are used throughout DEXiPy.
"""

from enum import Enum
from typing import Callable

class BoundAssoc(Enum):
    """Enumeration associated with bounds that discretize continuous scales.

    Args:
        Enum (int): indicates the interval to which some corresponding bound :math:`b` belongs.
    """

    DOWN = -1
    """Indicates that :math:`b` belongs to the interval :math:`[..., b]`."""

    UP = 1
    """Indicates that :math:`b` belongs to the interval :math:`[b, ...]`."""

# Internal representation of DEXi values
DexiValue = None | float | set[int] | list[float]
"""Type alias: Admissible DEXi values that can be interpreted without knowing the
`DexiScale` or `DexiModel` context.
Used to represent DEXi values internally.
"""

# Internal representation of alternatives.
DexiAlternative = dict[str, DexiValue | str]
"""Type alias: Internal representation of a single decision alternative:
   ``dict[str, DexiValue | str]``.
   String value is allowed only with non-attribute entries,
   such as alternative "name" or "description".
"""

DexiAlternatives = list[DexiAlternative]
"""Type alias: Internal representation of multiple decision alternatives as
   ``list[DexiAlternative]``.
"""

DexiAltData = DexiAlternative | DexiAlternatives
"""Type alias: General internal representation of a single or multiple alternatives:
    ``DexiAlternative | DexiAlternatives``.
"""

DexiValueSpecification = \
    DexiValue | str | set[int | str] | tuple[int | str, ...] | dict[int | str, float]
"""Type alias: Admissible DEXi values for user interaction.
In addition to `DexiValue`, it accepts strings, tuples and
value distributions represented by dictionaries.
Requires a `DexiScale` or `DexiModel` context to be interpreted or
converted to `DexiValue`.
"""

class DexiValueType(Enum):
    """Enumeration of :py:type:`DexiValueSpecification` data types."""

    NONE = 0
    STR = 1
    INT = 2
    FLOAT = 3
    SET = 4
    TUPLE = 5
    LIST = 6
    DICT = 7
    ERROR = -1

CallableNorm = Callable[..., list[float]]
"""Type alias: Callable normalization functions that accept and return a list of floats."""

CallableOperator = Callable[[list[float]], float]
"""Type alias: Callable `and_op` and `or_op` operator functions that accept
a list of floats and return a single float."""

class DexiOrder(Enum):
    """ Enumeration of `DexiScale` preferential order.

    Args:
        Enum (int): Preferential order.
    """
    DESCENDING = -1
    """Scale values are ordered from "good" to "bad" ones."""

    NONE = 0
    """Scale values are not ordered by preference."""

    ASCENDING = 1
    """Scale values are ordered from "bad" to "good" ones (default)."""

class DexiQuality(Enum):
    """Enumeration of `DexiScale` value quality classes.

    Args:
        Enum (int): Scale value quality class.
    """

    BAD = -1
    """A "bad" value class, indicating an undesired value."""

    NONE = 0
    """A "neutral" value class, neither particularly "good" or "bad"."""

    GOOD = 1
    """A "good" value class, indicating a desired value."""

class DexiEvalMethod(Enum):
    """Enumeration od DEXiPy evaluation methods.

    Args:
        Enum (int): Evaluation method.
    """
    SET = 1
    """Evaluation using sets (default)."""

    PROB = 2
    """Evaluation interpreting DEXi values as probability distributions."""

    FUZZY = 3
    """Evaluation interpreting DEXi values as fuzzy set memberships (possibility distributions)."""

    FUZZYNORM = 4
    """Similar to `FUZZY`, but enforcing fuzzy normalization
    (the maximum distribution element must be equal to 1.0)."""
