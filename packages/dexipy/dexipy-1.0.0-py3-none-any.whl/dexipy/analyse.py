"""
The module `dexipy.analyse` implements functions for the analysis of decision alternatives.
"""

import sys
from copy import deepcopy
from typing import Any, Sequence, Optional
import dexipy.utils as utl
from dexipy.types import DexiAlternative, DexiAltData
from dexipy.dexi import DexiModel, DexiAttribute
from dexipy.dexi import value_text, subtree_order, subtree_attributes
from dexipy.eval import get_alt_value, get_alternatives, scale_value, compare_two_alternatives
from dexipy.values import dexi_value_as_set

def _print_selective_explanation(atts: list[str],
                                 vals: list[str],
                                 head: str) -> None:
    """A helper function to print out results of `selective_explanation()`.

    Args:
        alt (DexiAlternative):
            A single DEXi alternative.
            Assumed to be fully evaluated and containing item "name".
        atts (list[str]):
            Text to be displayed in the first column.
            Assumed to contain attribute IDs or attribute structure information.
        vals (list[str]):
            Text to be displayed in the second column.
            Normally contains strings representing attribute values.
        head (str): Introductory heading text.

    Raises:
        ValueError: When `atts` and `vals` are of different lengths.
    """
    if len(atts) != len(vals):
        raise ValueError("Arguments 'atts' and 'vals' must be of same length")
    print(head + "\n")
    if len(atts) <= 1:
        print("None\n")
    else:
        print("\n".join(utl.table_lines([atts, vals], align = "l", def_align = "r")))
        print("\n")

def selective_explanation(model: DexiModel,
            alternatives: Optional[DexiAltData] = None,
            root: Optional[DexiAttribute] = None,
            prune: list[str] = [],
            text: bool = True,
            structure: bool = True
            ) -> None:
    """*Selective Explanation*:
    Displays subtrees of `alternatives`' values in which values are particularly
    weak (`DexiQuality.BAD`) and particularly strong (`DexiQuality.GOOD`).

    Args:
        model (DexiModel): A `DexiModel` object. Required.
        alternatives (Optional[DexiAltSelect], optional):
            A single `DexiAlternative` or a list
            of alternatives (`DexiAlternatives`).
            Alternatives are assumed to be previously fully evaluated.
            Defaults to None, which selects `model.alternatives`.
        root (Optional[DexiAttribute], optional):
            The topmost (root) attribute for displaying results.
            Defaults to None, which selects `model.root`.
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
            or to extend them with tree-structure information (True).
            Defaults to True.

    Raises:
        ValueError: When `model` or `root` are undefined.
    """
    if model is None:
        raise ValueError("Undefined model")
    alts = get_alternatives(alternatives, model)
    if root is None:
        root = model.root
    if root is None:
        raise ValueError("Undefined model root")

    att_order = subtree_order(root, prune)

    for alt in alts:
        badatts = ["atribute"]
        goodatts = ["attribute"]
        badvals = [str(alt["name"])]
        goodvals = [str(alt["name"])]
        for attid in att_order:
            if attid == root.id:
                continue
            (att, scl) = model.att_and_scale(attid)
            if att is None or scl is None:
                continue
            value = scale_value(get_alt_value(alt, att.id), scl)
            if scl.has_bad(value):
                badatts.append(att.structure() + attid if structure else attid)
                badvals.append(str(value_text(value, scl)) if text else str(value))
            if scl.has_good(value):
                goodatts.append(att.structure() + attid if structure else attid)
                goodvals.append(str(value_text(value, scl)) if text else str(value))
        print("Alternative " + str(alt["name"]) + "\n")
        _print_selective_explanation(badatts, badvals, "Weak points")
        _print_selective_explanation(goodatts, goodvals, "Strong points")

def _plus_minus_setup(alternative: DexiAlternative,
                      attributes: Sequence[DexiAttribute]) -> dict[str, Any]:
    """A helper function for `plus_minus()`.
    
    Prepares a data table with useful information about involved `attribues`
    and corresponding `alternative` values.

    Args:
        alternative (DexiAlternative):
            A single DEXi alternative.
        attributes (Sequence[DexiAttribute]):
            DexiAttributes involved in `plus_minus()` analysis.

    Returns:
        dict[str, Any]: A data table, i.e., a dictionary with the following columns:

        - result["ids"]: str: Attribute IDs.
        - result["structs"]: str: Attribute structure + IDs.
        - result["evals"]: DexiValue: Evaluation results.
        - result["sets"]: DexiValue: Evaluation results, reprsented a sets.
        - result["counts"]: int: Scale sizes of the correponding attributes.
        - result["low_bounds"]: int: Lower bounds of the corresponding sets.
        - result["high_bounds"]: int: Uppor bounds of the corresponding sets.
        - result["low_diffs"]: int: Admissible negative decrease of attribute values.
        - result["high_diffs"]: int: Admissible positive increase of attribute values.

        All columns are of length equal to `len(attributes)`.
        Column items correspond to consecutive elements of `attributes`.
    """
    ids = [att.id for att in attributes]
    evals = [scale_value(get_alt_value(alternative, att.id), att.scale) for att in attributes]
    setvals = [dexi_value_as_set(val) for val in evals]
    structs = [att.structure() + att.id for att in attributes]
    counts = [-1 if att.scale is None else att.scale.count() for att in attributes]
    low_bounds = [None if val is None else min(val) for val in setvals]
    high_bounds = [None if val is None else max(val) for val in setvals]
    low_diffs = low_bounds
    high_diffs = [None if hb is None else c - hb for c, hb in zip(counts, high_bounds)]
    result: dict[str, Any] = {}
    result["ids"] = ids
    result["structs"] = structs
    result["evals"] = evals
    result["sets"] = setvals
    result["counts"] = counts
    result["low_bounds"] = low_bounds
    result["high_bounds"] = high_bounds
    result["low_diffs"] = low_diffs
    result["high_diffs"] = high_diffs
    return result

def plus_minus(model: DexiModel,
               alternative: DexiAlternative,
               target: Optional[DexiAttribute] = None,
               minus: int = sys.maxsize,
               plus: int = sys.maxsize,
               text: bool = True,
               structure: bool = True
               ) -> None:
    """*Plus Minus Analysis*: Investigate the effects of changing
    single attributes' values on the evaluation of `alternative`.
    The values of discrete basic attributes ("input attributes") are changed,
    one attribute at a time,
    by a particular number of steps downwards (`minus`) and upwards (`plus`),
    while observing the changes of the `target` attribute values.

    Args:
        model (DexiModel):
            A `DexiModel` object. Required.
        alternative (DexiAlternative): A single `DexiAlternative`.
            Assumed to be previously evaluated using `evaluate()`.
        target (Optional[DexiAttribute], optional):
            A `DexiAttribute` on which effects are observed.
            Defaults to None, which selects `model.root`.
        minus (int, optional):
            The maximum number of downward steps to be made
            for each input attribute. Defaults to `sys.maxsize`.
            The actual `minus` value is further determined with respect to
            `alternative` values and involved attributes' scales.
        plus (int, optional):
            The maximum number of upward steps to be made
            for each input attribute. Defaults to `sys.maxsize`.
            The actual `plus` value is further determined with respect to
            `alternative` values and involved attributes' scales.
        text (bool, optional):
            Whether to display results textually (True)
            or using internal value representation (False).
            Defaults to True.
        structure (bool, optional):
            Whether to display only attribute IDs in the first column
            (False) or to extend them with tree-structure information. Defaults to True.

    Raises:
        ValueError:
            When `model` is None,
            when `target` is None or does not have a scale defined, and
            when `alternative` is not a single DEXi alternative.

    Returns:
        Optional[list[list[str]]]: A data table containing the following columns of strings:

        - First column: Attribute IDs, optionally extended with `structure` information.
        - For `-minus` to `-1`: Columns containing evaluation values of `target`
          when decreasing attribute values by the corresponding number of steps.
        - Middle column: Original `alternative` values assigned to the corresponding attributes.
        - For `+1` to `+plus`: Columns containing evaluation values of `target`
          when increasing attribute values by the corresponding number of steps.

    Limitations:
        Only basic attributes with defined discrete scales participate in the analysis.
    """
    # Check arguments
    if model is None:
        raise ValueError("Undefined model")
    if target is None:
        target = model.first()
    if not isinstance(alternative, dict):
        raise ValueError("Only single `alternative` is allowed")
    if target is None or target.scale is None:
        raise ValueError("Undefined target attribute")
    attributes = [att for att in model.attributes
                  if att.scale is not None and att.scale.is_discrete() and
                     att.is_basic() and not att.is_link() and att.affects(target)]

    # Setup data
    data = _plus_minus_setup(alternative, attributes)
    target_value = alternative[target.id]
    target_string = str(value_text(target_value, target.scale) if text else str(target_value))

    # Calculate `minus` and `plus` bounds
    ldiff = [n for n in data["low_diffs"] if n is not None]
    hdiff = [n for n in data["high_diffs"] if n is not None]
    if len(ldiff) == 0 or len(hdiff) == 0:
        print("All involved values are None")
        return
    minus = min(abs(minus), max(ldiff))
    plus = min(abs(plus), max(hdiff))

    # Initialize table
    idcolumn = ["Attribute", target.id]
    idcolumn.extend(data["structs"] if structure else data["ids"])
    table = [idcolumn]

    # Build table columns
    for pm in range(-minus, plus + 1):
        pm_str = str(pm)
        if pm > 0:
            pm_str = "+" + pm_str
        column: list[str] = [str(alternative["name"]), target_string] if pm == 0 else [pm_str, ""]
        for idx, att in enumerate(attributes):
            alt = deepcopy(alternative)
            value = data["evals"][idx]
            if value is None:
                entry = str(None)
            elif pm == 0:
                entry = str(value_text(value, att.scale)) if text else str(value)
            else:
                bound = data["low_bounds"][idx] if pm < 0 else data["low_bounds"][idx]
                value = bound + pm
                if 0 <= value < data["counts"][idx]:
                    alt[att.id] = value
                    evalalt = model.evaluate(alt, root = target, method = "set")
                    evalresult = get_alt_value(evalalt, target.id)
                    if evalresult == target_value:
                        entry = ""
                    else:
                        entry = \
                            str(value_text(evalresult, target.scale)) if text \
                            else str(evalresult)
                elif value == -1:
                    entry = '['
                elif value == data["counts"][idx]:
                    entry = ']'
                else:
                    entry = ""
            column.append(entry)
        table.append(column)

    print("\n".join(utl.table_lines(table)))

def compare_alternatives(model: DexiModel,
                         alternative: DexiAlternative,
                         alternatives: Optional[DexiAltData] = None,
                         root: Optional[DexiAttribute] = None,
                         prune: list[str] = [],
                         compare: bool = True,
                         deep: bool = True,
                         text: bool = True,
                         structure: bool = True
            ) -> None:
    """*Compare Alternatives*: Compare `alternative` with each of `alternatives`.
    Display only values that differ and, optionally when ``compare = True``, include
    preference-relational operators.

    Args:
        model (DexiModel):
            A `DexiModel` object. Required.
        alternative (DexiAlternative):
            A single DEXi alternative to be compared with `alternatives`.
        alternatives (Optional[DexiAltSelect], optional):
            A single `DexiAlternative` or a list
            of alternatives (`DexiAlternatives`).
            Alternatives are assumed to be previously fully evaluated.
            Defaults to None, which selects `model.alternatives`.
        root (Optional[DexiAttribute], optional):
            The topmost (root) attribute for displaying results.
            Defaults to None, which selects `model.root`.
        prune (list[str], optional): List of attribute IDs at which the display is "pruned",
            skipping their subordinate attributes.
            Defaults to [].
        compare (bool, optional):
            Whether to display preference comparison operators "=", "<", ">", "<=", ">=".
            Defaults to True.
        deep (bool, optional):Whether of not "deep" comparison
            (see :py:meth:`dexipy.eval.compare_two_alternatives`)
            is carried out. Defaults to True.
        text (bool, optional):
            Whether to display results textually (True) or using internal
            value representation (False). Defaults to True.
        structure (bool, optional):
            Whether to display only attribute IDs in the first column (False)
            or to extend them with tree-structure information (True).
            Defaults to True.

    Raises:
        ValueError:
            When `model`, `alternative` or `alternatives` are None,
            when `alternative` is not a single alternative, or when `root` is undefined.

    Returns:
        None and prints out the resulting alternative comparison table.
    """
    if model is None:
        raise ValueError("Undefined model")
    if alternative is None or not isinstance(alternative, dict):
        raise ValueError("A single source alternative is required for comparison")
    alts = get_alternatives(alternatives, model)
    if root is None:
        root = model.root
    if root is None:
        raise ValueError("Undefined model root")

    attributes = subtree_attributes(root, prune)
    attributes = [att for att in attributes if att != model.root]
    ids = [att.id for att in attributes]
    att_column: list[str] = ["Attribute"]
    if structure:
        att_column.extend(att.structure() + att.id for att in attributes)
    else:
        att_column.extend(ids)

    alt_column: list[str] = [str(alternative["name"])]
    for att in attributes:
        value = get_alt_value(alternative, att.id)
        valstr: str = str(value_text(value, att.scale)) if text else str(value)
        alt_column.append(valstr)

    table: list[list[str]] = [att_column, alt_column]

    for alt in alts:
        alt_column = [str(alt["name"])]
        compalt = compare_two_alternatives(alternative, alt, attributes, deep = deep)
        for idx, att in enumerate(attributes):
            value = get_alt_value(alt, att.id)
            comp = compalt[idx]
            valstr = \
                "" if comp is None or -1 < comp < +1 \
                else str(value_text(value, att.scale)) if text \
                else str(value)
            if compare:
                valstr = utl.compare_operator(comp) + " " + valstr
            alt_column.append(valstr)
        table.append(alt_column)

    print("\n".join(utl.table_lines(table)))
