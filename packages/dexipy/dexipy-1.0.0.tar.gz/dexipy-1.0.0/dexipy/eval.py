"""
The module `dexipy.eval` implements classess and functions
for the evaluation of decision alternatives.
"""

import sys
import csv
from typing import Any, Optional, Iterable
from copy import copy, deepcopy
from dexipy.types import CallableOperator, CallableNorm
from dexipy.types import DexiValue, DexiValueType
from dexipy.types import DexiAlternative, DexiAlternatives, DexiAltData
from dexipy.dexi import DexiModel, DexiAttribute, DexiFunction, DexiDiscretizeFunction
from dexipy.dexi import scale_value, bounded_scale_value
from dexipy.dexi import att_names, alt_name
from dexipy.dexi import compare_values_on_scale
import dexipy.utils as utl
import dexipy.values as vls

def evaluation_order(att: DexiAttribute, prune: list[str] = []) -> list[str]:
    """Determine the evaluation order of attributes. Interpreted as a sequence,
    the order guarantees that whenever some attribute is reached as a next candidate for
    evaluation, all the affecting attributes have already been evaluated.

    Args:
        att (DexiAttribute): The starting point of evaluation.
        prune (list[str], optional):
            A list of attribute IDs at which to prune the evaluation.
            The evaluation will treat them as if they were basic attributes,
            not looking to any descendant attributes. Defaults to [].

    Returns:
        list[str]: A list of attribute IDs in the evaluation order.
    """
    result: list[str] = []

    def add_to_order(att: DexiAttribute) -> None:
        attid = att.id
        if not attid in result:
            if not attid in prune:
                if att.link is not None:
                    add_to_order(att.link)
                else:
                    for inp in att.inputs:
                        add_to_order(inp)
            result.append(attid)

    add_to_order(att)
    return result

class DexiEvalParameters:
    """A class defining evaluation parameters.

     Please see :ref:`evaluation` for more information about the evaluation process
     and evaluation methods used in DEXiPy.

    Args:
        method (str): Method name.
            One of the strings "set", "prob", "fuzzy", "fuzzynorm".
        and_op (CallableOperator):
            Conjunctive aggregation function.
        or_op (CallableOperator):
            Disjunctive aggregation function.
        norm (CallableNorm):
            Normalization function.
    """
    def __init__(self,
                 method: str,
                 and_op: CallableOperator,
                 or_op: CallableOperator,
                 norm: CallableNorm):
        self.method = method
        self.and_op = and_op
        self.or_op = or_op
        self.norm = norm

class DexiEvalMethods:
    """A class defining default :py:class:`dexipy.eval.DexiEvalParameters`
   for the evaluation methods implemented in DEXiPy.

    The default parameters are set as follows::

        import dexipy.utils as utl
        self.set_method(DexiEvalParameters("set", lambda x: 0, lambda x: 1, utl.norm_none))
        self.set_method(DexiEvalParameters("prob", utl.prod, sum, utl.norm_sum))
        self.set_method(DexiEvalParameters("fuzzy", min, max, utl.norm_none))
        self.set_method(DexiEvalParameters("fuzzynorm", min, max, utl.norm_max))
   """

    _eval_methods: dict[str, DexiEvalParameters] = {}

    def __init__(self):
        self.set_method(DexiEvalParameters("set", lambda x: 0, lambda x: 1, utl.norm_none))
        self.set_method(DexiEvalParameters("prob", utl.prod, sum, utl.norm_sum))
        self.set_method(DexiEvalParameters("fuzzy", min, max, utl.norm_none))
        self.set_method(DexiEvalParameters("fuzzynorm", min, max, utl.norm_max))

    @classmethod
    def set_method(cls, method: DexiEvalParameters) -> None:
        """Sets default evaluation parameters for `method`.

        Args:
            method (DexiEvalParameters):
                Evaluation parameters with defined method name `method.method`.
        """
        cls._eval_methods[method.method] = method

    @classmethod
    def get_method(cls, method: str) -> DexiEvalParameters:
        """Gets default evaluation parameters for `method`.

        Args:
            method (str): Method name.

        Raises:
            ValueError:
                When method parameters have not been previously defined
                for the given method name.

        Returns:
            DexiEvalParameters: Default parameters of the given method.
        """
        if not method in cls._eval_methods:
            raise ValueError(f'Unknown evaluation method name: "{method}"' )
        return cls._eval_methods[method]

EvalMethods = DexiEvalMethods()
"""A :py:class:`dexipy.eval.DexiEvalMethods` object containing default
evaluation parameters for all methods implemented in DEXiPy."""

def eval_parameters(method: str,
                   and_op: Optional[CallableOperator] = None,
                   or_op: Optional[CallableOperator] = None,
                   norm: Optional[CallableNorm] = None) -> DexiEvalParameters:
    """Fetches default evaluation parameters from `EvalMethods` and
    optionally modifies them considering non-None arguments of this function.

    Args:
        method (str): Method name. Required.
        and_op (Optional[CallableOperator], optional):
            If not None, set the conjuntive aggregation function.
            Defaults to None.
        or_op (Optional[CallableOperator], optional):
            If not None, set the disjuntive aggregation function.
            Defaults to None.
        norm (Optional[CallableNorm], optional):
            If not None, set the normalization function.
            Defaults to None.

    Returns:
        DexiEvalParameters: Fetched and optionally modified evaluation parameters.
    """
    result = copy(EvalMethods.get_method(method))
    if and_op is not None:
        result.and_op = and_op
    if or_op is not None:
        result.or_op = or_op
    if norm is not None:
        result.norm = norm
    return result

def get_alt_value(alt: Any, attid: str) -> DexiValue:
    """Returns ``alt[attid]``.

    Args:
        alt (Any): Expected a `DexiAlternative`.
        attid (str): Value ID, a key in the `alt` dictionary.

    Returns:
        DexiValue: Alternative value corresponding to ID, or None if not found.
    """
    try:
        return alt[attid]
    except:
        return None

def _evaluate_as_set(funct: DexiFunction, inp_values: list[DexiValue]) -> DexiValue:
    """Evaluate `inp_values`, interpreted as sets, by `funct`.

    Args:
        funct (DexiFunction): A `DexiFunction` or derived object.
        inp_values (list[DexiValue]):
            List of DexiValues, representing function arguments.

    Returns:
        DexiValue: Result of evaluation, represented as a set.
    """
    inp_vals = tuple(vls.dexi_value_as_set(val) for val in inp_values)
    if None in inp_vals or set() in inp_vals:
        return None
    inp_args = utl.cartesian_product(*inp_vals)
    result = set()
    for args in inp_args:
        value = funct.evaluate(args)
        if value is None:
            return None
        value = vls.dexi_value_as_set(value)
        if value is None:
            return None
        result.update(value)
    if result == set():
        return None
    return result

def _evaluate_as_distribution(funct: DexiFunction,
                              inp_values: list[DexiValue],
                              eval_param: DexiEvalParameters) -> DexiValue:
    """Evaluate `inp_values`, interpreted as distributions, by `funct`.

    Args:
        funct (DexiFunction): A `DexiFunction` or derived object.
        inp_values (list[DexiValue]):
            List of DexiValues, representing function arguments.
        eval_param (DexiEvalParameters): Parameters of evaluation.

    Returns:
        DexiValue: Result of evaluation, represented as a distribution.
    """
    inp_distrs = tuple(vls.dexi_value_as_distr(val) for val in inp_values)
    if None in inp_distrs or [] in inp_distrs:
        return None
    args_mem = utl.cartesian_product(*inp_distrs)
    args_idx = utl.cartesian_product(*(tuple(range(utl.objlen(distr))) for distr in inp_distrs))
    ands = [eval_param.and_op(mem) for mem in args_mem]
    assert len(args_mem) == len(args_idx) == len(ands), "Internal error: Length error"
    result: list[float] = []
    if funct.attribute is not None and funct.attribute.scale is not None:
        result = [0.0] * funct.attribute.scale.count()
    for idx, mem in enumerate(args_mem):
        if ands[idx] == 0:
            continue
        args = args_idx[idx]
        value = funct.evaluate(args)
        if value is None:
            return None
        as_set = vls.dexi_value_as_set(value)
        nval = utl.objlen(as_set)
        if  nval == 0:
            return None
        as_distr = vls.dexi_value_as_distr(value)
        as_distr = eval_param.norm(as_distr)
        for i, el in enumerate(as_distr):
            if i >= len(result):
                result = utl.pad_list(result, i + 1, 0.0)
            result[i] = eval_param.or_op([result[i], eval_param.and_op([ands[idx], el])])
    return result

def _evaluate_aggregate(att: DexiAttribute,
                        alt: DexiAlternative,
                        eval_param: DexiEvalParameters) -> DexiValue:
    """Evaluate `alt` at an aggregate attribute `att`.

    Args:
        att (DexiAttribute): A `DexiAttribute`.
        alt (DexiAlternative): A `DexiAlternative`.
        eval_param (DexiEvalParameters): Parameters of evaluation.

    Returns:
        DexiValue: Evaluation result.
    """
    funct = att.funct
    if funct is None:
        return None
    inputs = att.inputs
    inp_ids = att_names(inputs)

    inp_values = [get_alt_value(alt, id) for id in inp_ids]
    if None in inp_values:
        return None
    inp_types = [vls.dexi_value_type(val) for val in inp_values]
    if DexiValueType.NONE in inp_types or None in inp_types:
        return None

    if isinstance(funct, DexiDiscretizeFunction):
        value = funct.evaluate(inp_values[0])
    elif eval_param.method == "set":
        multi_valued = any(inp != DexiValueType.INT for inp in inp_types)
        if multi_valued:
            value = _evaluate_as_set(funct, inp_values)
        else:
            value = funct.evaluate(inp_values)
    else:
        value = _evaluate_as_distribution(funct, inp_values, eval_param)
    return value

def get_alternatives(alternatives: Optional[DexiAltData],
                     model: Optional[DexiModel] = None) -> list[DexiAlternative]:
    """Makes a proper list of alternatives from `alternatives`.

    Args:
        alternatives (Optional[DexiAltData]):
            Alternative(s) specification, which might be None or
            contain a single alternative or a list of alternatives.
            None selects `model.alternatives`, but only if `model` is not None.
        model (Optional[DexiModel], optional):
            A `DexiModel` object. Defaults to None.

    Returns:
        list[DexiAlternative]:
            List of DEXi alternatives
            (may be empty, but not None or does not contain None).
    """
    if alternatives is None:
        if model is None:
            return []
        alternatives = model.alternatives
    return alternatives if isinstance(alternatives, list) else [alternatives]

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
    """
    This is the main implementation of the evaluation method in DEXiPy.

    While it is possible to call this function directly, it is also possible to
    avoid importing :py:mod:`dexipy.eval` and run evaluations using
    :py:func:`dexipy.dexi.evaluate` or :py:meth:`dexipy.dexi.DexiModel.evaluate`.

    Please see :ref:`evaluation` for more information about the evaluation process
    and evaluation methods used in DEXiPy.

    Args:
        model (DexiModel):
            A `DexiModel` object. Required.
        alternatives (Optional[DexiAltSelect], optional):
            A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
            Defaults to None, which selects `model.alternatives`.
        method (str, optional):
            One of the strings "set", "prob", "fuzzy", "fuzzynorm" that select
            the evaluation method. Defaults to "set".
        root (Optional[DexiAttribute], optional):
            The topmost (root) attribute of the evaluation.
            Defaults to None, which selects `model.root`.
        prune (list[str], optional):
            List of attribute IDs at which the evaluation is "pruned".
            This means that input attributes below some pruned attribute are not evaluated
            and the pruned attribute is treated as an input (basic) attribute for this evaluation.
            Defaults to [].
        pre_check (bool, optional):
            Whether `alternatives` are checked by
            :py:meth:`dexipy.dexi.DexiModel.check_alternatives` prior to evaluation.
            Defaults to False.
        bounding (bool, optional):
            Whether or not the evaluation keeps calculated values within
            bounds prescribed by the corresponding scales. Defaults to False.
        in_place (bool, optional):
            If True, evaluation modifies `alternatives` in place,
            otherwise a deep copy is made and returned by the method. Defaults to False.
        eval_param (Optional[eval.DexiEvalParameters], optional):
            Optional :py:class:`dexipy.eval.DexiEvalParameters`, which may customize
            the normalization and aggregation methods used in the evaluation.
            Defaults to None.

    Returns:
        DexiAltData: Returns a list of evaluated alternatives.
    """
    if eval_param is None:
        eval_param = EvalMethods.get_method(method)
    alts = get_alternatives(alternatives, model)
    if not in_place:
        alts = deepcopy(alts)

    if root is None:
        root = model.root
    if root is None:
        raise ValueError("Undefined model root")

    pruning = len(prune) > 0
    full_order = evaluation_order(root)
    eval_order = full_order
    if pruning:
        eval_order = evaluation_order(root, prune)
        diff = set(full_order).difference(set(eval_order))
        for attid in model.non_root_ids:
            if attid in diff:
                for alt in alts:
                    alt[attid] = None

    if pre_check:
        check = model.check_alternatives(alts)
        if check["errors"] != []:
            raise ValueError(utl.check_str(check, warnings = True))

    for alt in alts:
        for attid in eval_order:
            if model.root is None or attid == model.root.id:
                continue
            (att, scl) = model.att_and_scale(attid)
            if att is None:
                continue
            if scl is None:
                value = None
            elif att.link is not None:
                value = get_alt_value(alt, att.link.id)
            elif att.is_basic() or attid in prune:
                value = scale_value(get_alt_value(alt, attid), scl)
            elif att.is_aggregate():
                value = _evaluate_aggregate(att, alt, eval_param)
            else:
                value = None
            if bounding:
                value = bounded_scale_value(value, scl)
            if eval_param.method != "set" and isinstance(value, list):
                value = eval_param.norm(value)
            value = vls.reduce_dexi_value(value)
            alt[attid] = value

    if isinstance(alternatives, list):
        return alts
    return alts[0]

def compare_two_alternatives(alt1: DexiAlternative,
                             alt2: DexiAlternative,
                             attributes: list[DexiAttribute],
                             deep: bool = True
                             ) -> list[Optional[float]]:
    """Compare two alternatives `alt1` and `alt2` with respect to `attributes`.

    Args:
        alt1 (DexiAlternative): First alternative.
        alt2 (DexiAlternative): Second alternative.
        attributes (list[DexiAttribute]): List of `DexiAttribute` objects.
        deep (bool, optional):
            When True and compared values are equal,
            subordinate attributes are additionally investigated for possible
            preferential differences. Defaults to True.

    Returns:
        list[float]:
            Float vector of the same length as `attributes`.
            Each element represents the comparison result w.r.t. the corresponding attribute.
            Possible element values are:

            - 0: Values are equal.
            - -1: `alt1`'s value is worse than `alt2`'s.
            - +1: `alt1`'s value is better than `alt2`'s.
            - None: Values are incomparable.

            When `deep = True`, the so-called deep comparison is performed:
            when the compared attribute's values are equal,
            subordinate attributes are checked for differences, possibly returning:

            * -0.5: indicates the weak preference relation "<=".
            * +0.5: indicates the weak preference relation ">=".
    """
    result: list[Optional[float]] = []
    for att in attributes:
        value1 = get_alt_value(alt1, att.id)
        value2 = get_alt_value(alt2, att.id)
        comp: Optional[float] = compare_values_on_scale(value1, value2, att.scale, force = True)
        if deep and comp is not None and comp == 0 and att.is_aggregate():
            compdeep = [compare_values_on_scale(
                get_alt_value(alt1, inp.id), get_alt_value(alt2, inp.id),
                inp.scale, force = True) \
                    for inp in att.inputs]
            if not None in compdeep:
                if all(c <= 0 for c in compdeep if c is not None) and \
                   any(c < 0 for c in compdeep if c is not None):
                    comp = -0.5
                elif all(c >= 0 for c in compdeep if c is not None) and \
                    any(c > 0 for c in compdeep if c is not None):
                    comp = +0.5
        result.append(comp)
    return result

def export_alternatives(model: DexiModel,
                        alternatives: Optional[DexiAltData] = None
                        ) -> list[list[str]]:
    """Export alternatives: Convert `alternatives`' data to a data table,
    prepared to be written out by :py:func:`dexipy.eval.write_alternatives`

    Args:
        model (DexiModel): A `DexiModel` object.
        alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.

    Raises:
        ValueError: When `model` is undefined.

    Returns:
        list[list[str]]: Data table containing rows of strings to be written out.
    """
    if model is None:
        raise ValueError("Undefined model")
    alts = get_alternatives(alternatives, model)

    head = ["name"]
    for idx, alt in enumerate(alts):
        head.append(str(idx) if alt["name"] is None else str(alt["name"]))
    data = [head]
    for att in model.attributes:
        if att != model.root:
            row = [". " * (att.level() - 1) + str(att.name)]
            for alt in alts:
                value = get_alt_value(alt, att.id)
                row.append(vls.export_dexi_value(value))
            data.append(row)
    return data

def write_alternatives(model: DexiModel,
                        alternatives: Optional[DexiAltData] = None,
                        filename: Optional[str] = "",
                        **fmtparams
                        ) -> None:
    """Write `alternatives` to a file,
    which can be subsequently imported in `DEXi/DEXiWin` software.

    In order to successfully import the output of this function in DEXi/DEXiWin software,
    the formats of this export and DEXi/DEXiWin's settings must be properly
    configured and matched.
    In DEXi/DEXiWin, see "Import/Export" settings and make sure that they are set as follows:

    - Option values: "Base 1"
    - Attributes: "All"
    - Orientation: "Attributes \\ Alternatives" or "normal"
    - CSV Format: "Invariant" (DEXiWin only)

    When importing in the "csv" format, make sure that you write alternatives using the parameters:

    ``write_alternatives(model, alternatives, filename, delimiter = ',')``

    For importing in the "tab" format, use the parameters:

    ``write_alternatives(model, alternatives, filename, delimiter = '\\t')``

    If `alternatives` contain value distributions,
    they can be imported only by DEXiWin and not by DEXi.

    Args:
        model (DexiModel): A `DexiModel` object.
        alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.
        filename (Optional[str], optional):
            File name for writing out the data.
            None or "" mean that data is written to the console.
            Defaults to "".

    Returns:
        None: Writes out `alternatives`' data to a file or console.
    """
    data = export_alternatives(model, alternatives)
    if filename is None or filename == "":  # write to console
        csvfile = sys.stdout
        writer = csv.writer(csvfile, **fmtparams)
        writer.writerows(data)
    else:
        with open(filename, 'w', newline = "", encoding = "utf-8") as csvfile:
            writer = csv.writer(csvfile, **fmtparams)
            writer.writerows(data)

def alternatives_value_ranges(alternatives: DexiAlternatives,
                              attributes: list[str],
                              defined_ranges: dict[str, tuple[float, float]] = {}
                             ) -> dict[str, tuple[float, float]]:
    """A helper function for determining attribute value ranges in `alternatives`.
    Particularly needed for continues attributes.

    Args:
        alternatives (DexiAlternatives): Aggregated DEXi alternatives.
        attributes (list[str]): Attribute IDs.
        defined_ranges (dict[str, tuple[float, float]], optional):
            Dictionary of attributes' lower and upper range bounds that are already known.
            Attributes already listed in `defined_ranges` are not considered here and
            their ranges are just included in the output.
            Defaults to {}.

    Returns:
        dict[str, tuple[float, float]]:
            A dictionary, indexed by attribute IDs, containing (`lower`, `upper`) bound tuples.
    """
    result: dict[str, tuple[float, float]] = defined_ranges
    def_keys = defined_ranges.keys()
    for att in attributes:
        if att not in def_keys:
            values = [get_alt_value(alt, att) for alt in alternatives]
            vals = [v for v in values if v is not None and isinstance(v, (int, float))]
            if len(vals) > 0:
                result[att] = (min(vals), max(vals))
    return result

def aggregate_alternatives(model: DexiModel,
                           alternatives: Optional[DexiAltData] = None,
                           attributes: Optional[Iterable[Optional[DexiAttribute | str | int]]]=None,
                           name: str = "name",
                           aggregate: str = "mean",
                           interpret: str = "distribution"
                          ) -> DexiAlternatives:
    """Aggregate `alternatives` so as to contain only numeric data (or None).
    Value sets and distributions are converted by :py:func:`dexipy.values.aggregate_value`.

    Args:
       model (DexiModel): A `DexiModel` object.
       alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.
       attributes (Optional[Iterable[Optional[DexiAttribute | str | int]]], optional):
            A sequence of DexiAttributes, attribute IDs or indices.
            Defaults to None, which selects `model.attributes`.
       name (str):
            Name of DexiAlternative element that contains alternatives' name.
            Defaults to "name".
       aggregate (str, optional):
            One of "min", "max" or "mean".
            Determines aggregation operation for sets and distributions.
            Defaults to "mean".
       interpret (str, optional):
            One of "set" or "distribution".
            Determines whether to interpret value distributions as sets or distributions.
            Defaults to "distribution".

    Returns:
        list[dict[str, Optional[float]]] (subtype of `DexiAlternatives`):
            A list of aggregated alternatives.
            Sublist entries are guaranteed to contain None, int or float values.
    """
    assert alternatives is not None, "Undefined alternatives"
    assert model is not None, "Undefined model"
    alts = get_alternatives(alternatives, model)
    atts = model.attributes if attributes is None else model.attribute_list(attributes)

    result: DexiAlternatives = []

    for idx, alt in enumerate(alts):
        calt: DexiAlternative = {}
        calt[name] = alt_name(alt, "Alt" + str(idx + 1), name)
        for att in atts:
            value = get_alt_value(alt, att.id)
            calt[att.id] = vls.aggregate_value(value, aggregate, interpret)
        result.append(calt)

    return result

def convert_alternatives(model: DexiModel,
                         alternatives: Optional[DexiAltData] = None,
                         attributes:  Optional[Iterable[Optional[DexiAttribute | str | int]]]=None,
                         name: str = "name",
                         aggregate: Optional[str] = "mean",
                         interpret: str = "distribution",
                         scale_values: bool = True,
                         omin: float = 0,
                         omax: float = 1,
                         defined_ranges: dict[str, tuple[float, float]] = {},
                         reverse_descending: bool = True,
                         shift: float = 0
                        ) -> DexiAlternatives:
    """Converts `alternatives`' data, generally performing four steps:
        1. Aggregating DEXi values to single numbers,
           using :py:func:`dexipy,eval.aggregate_alternatives`.
        2. Scaling those numbers to a given numeric interval.
        3. Reversing values corresponding to descending DexiAttributes.
        4. Shifting values by a small amount (aimed at avoiding overlapped chart lines).

    Steps 2-4 are optional.

    Args:
        model (DexiModel):
            A `DexiModel` object.
        alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.
        attributes ( Optional[Iterable[Optional[DexiAttribute | str | int]]], optional):
            A sequence of `DexiAttribute`s, attribute IDs or indices.
            Defaults to None, which selects `model.attributes`.
        name (str):
            Name of `DexiAlternative` element that contains alternatives' name.
            Defaults to "name".
        aggregate (Optional[str], optional):
            One of  "min", "max" or "mean".
            Determines aggregation operation for sets and distributions.
            Defaults to "mean".
        interpret (str, optional):
            One of "set" or "distribution".
            Determines whether to interpret value distributions as sets or distributions.
            Defaults to "distribution".
        scale_values (bool, optional):
            Whether or not to scale values to the [`omin`, `omax`] interval.
            Defaults to True.
        omin (float, optional):
            Lower output bound for value scaling. Defaults to 0.
        omax (float, optional):
            Upper output bound for value scaling. Defaults to 1.
        defined_ranges (dict[str, tuple[float, float]], optional):
            A dictionary of pre-determined value ranges.
            Applicable to continuous attributes.
            Continuous attribute ranges, which are not specified in `defined_ranges`,
            are determined from `alternatives` data.
            Discrete attribute ranges are always determined from their scales.
            Defaults to {}.
        reverse_descending (bool, optional):
            Whether or not to reverse values of descending attributes.
            Defaults to True.
        shift (float, optional):
            Used to "shift" numerical values by a small amount to avoid overlapping lines in charts. 
            Defaults to 0.

    Returns:
        DexiAlternatives: A list of converted `alternatives`.
    """

    # Check arguments and prepare data
    assert model is not None, "DexiModel is required"
    assert aggregate in ["min", "max", "mean"], \
        'Parameter `aggregate` must be one of: "min", "max", "mean"'
    assert interpret in ["set", "distribution"], \
        'Parameter `interpret` must be one of: "set" or "distribution"'
    if alternatives is None:
        alternatives = model.alternatives
    assert alternatives is not None, "Undefined alternatives"

    alts = get_alternatives(alternatives, model)
    atts = model.attributes if attributes is None else model.attribute_list(attributes)

    # Stage 1: Aggregate alternatives
    data: DexiAlternatives = aggregate_alternatives(
        model, alts, atts, name = name, aggregate = aggregate, interpret = interpret)

    # Stage 2: Value mapping
    if scale_values:
        cont_atts = [att.id for att in atts if att.is_continuous()]
        ranges = alternatives_value_ranges(data, cont_atts, defined_ranges = defined_ranges)
        for idx, alt in enumerate(data):
            for att in atts:
                if att.id == name:
                    continue
                if att.scale is None:
                    continue
                value = alt[att.id]
                if value is None:
                    continue
                if att.is_continuous():
                    if (att.id not in ranges.keys() or (ranges[att.id] is None)):
                        continue
                if att.is_discrete():
                    lower, upper = 0.0, float(att.scale.count() - 1)
                elif att.is_continuous():
                    lower, upper = ranges[att.id]
                else:
                    continue
                assert isinstance(value, (int, float)), \
                    f"Non-numeric value {value} assigned to continuous attribute {att.id}"
                value = utl.lin_map(value, lower, upper, omin, omax)
                if reverse_descending and att.is_descending():
                    value = utl.lin_map(value, omin, omax, omax, omin)
                data[idx][att.id] = value

    # Stage 3: Value shifting
    if shift != 0:
        shake = 0.0
        for idx, alt in enumerate(data):
            for att in atts:
                if att.id == name:
                    continue
                value = alt[att.id]
                if value is None:
                    continue
                if isinstance(value, (int, float)):
                    value += shake
                data[idx][att.id] = value
            shake -= shift

    return data

def columnize_alternatives(alternatives: Optional[DexiAltData] = None,
                           model: Optional[DexiModel] = None,
                           attributes:  Optional[Iterable[Optional[DexiAttribute | str]]] = None
                          ) -> dict[str, list]:
    """'Columnizes' `alternatives` to a dictionary of columns that is suitable for importing data to
    other packahes, such as Panda's `DataFrame`. Data is columnized "as-is", without any checking,
    which is left to the recipient.

    Args:
        alternatives (Optional[DexiAltData], optional):
            A single `DexiAlternative` or a list of `DexiAlternatives`.
            Defaults to None, which invokes :py:func:`dexipy.eval.get_alternatives`
            to make the list.
        model (Optional[DexiModel], optional):
            A `DexiModel`. Defaults to None.
        attributes (Optional[Iterable[Optional[DexiAttribute | str]]], optional):
            The list of attributes to be columnized.
            When present, it can contain `DexiAttribute`s
            (which need a defined `model`, otherwise `AssertionError` is raised)
            or attribute IDs (strings that are not checked against `model`).
            When None: if 'model` is defined, then `model.non_root_ids`, otherwise
            attribute names are determined from `alternatives` themselves.
            Defaults to None.

    Returns:
        dict[str, list]: A dictionary composed of data columns.
            Keys are attribute IDs and other column headings (such as "name").
            Individual columns are lists, all of length equal to the number of `alternatives`,
            containing corresponding values extracted from `alternatives`.
    """
    # Prepare
    alts = get_alternatives(alternatives, model)
    keys = []
    if attributes is None:
        if model is None:
            # determine the union of keys from `alts`
            for alt in alts:
                for key in alt.keys():
                    if key not in keys:
                        keys.append(key)
        else:
            # take attributes from `model`
            keys = model.non_root_ids
    else:
        if model is None:
            keys = [att for att in attributes if isinstance(att, str)]
        else:
            keys = model.non_root_ids

    # Convert data
    data: dict[str, list] = {key: [] for key in keys}
    for alt in alts:
        for key in keys:
            data[key].append(None if key not in alt.keys() else alt[key])

    return data
