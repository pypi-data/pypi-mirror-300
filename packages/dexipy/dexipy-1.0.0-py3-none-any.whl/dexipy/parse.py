"""The module `dexipy.parse` implements parsing and reading of `.dxi` files.

The only functions interesting for public use are :py:func:`dexipy.parse.read_dexi` and
:py:func:`dexipy.parse.read_dexi_from_string`; both are aliased in the module
:py:mod:`dexipy.dexi`.

For more information, please refer to
:py:func:`dexipy.dexi.read_dexi` and :py:func:`dexipy.dexi.read_dexi_from_string` .
"""

from typing import Any, Sequence, Optional
import xml.etree.ElementTree as ET
import dexipy.utils as utl
from dexipy.types import BoundAssoc, DexiOrder, DexiQuality, DexiValue
from dexipy.dexi import DexiModel, DexiAttribute
from dexipy.dexi import DexiScale, DexiContinuousScale, DexiDiscreteScale
from dexipy.dexi import DexiFunction, DexiTabularFunction, DexiDiscretizeFunction

def _dexi_bool(x: str) -> bool:
    try:
        return x.upper() in ("TRUE", "T", "1")
    except AttributeError:
        return False

def _dexi_vector(x: str) -> list[float]:
    flts = [float(s) for s in x.split(";")]
    return [int(flt) if flt.is_integer() else flt for flt in flts]

def _dexi_value(x: Optional[str], add: int = 0) -> DexiValue | str:
    if x is None:
        return None
    x = x.lower()
    if x == "":
        return None
    if x == "*":
        return "*"
    if x.startswith("undef"):
        return None
    if x.startswith("{") and x.endswith("}"):
        valset: Sequence[int] = [int(val) + add for val in _dexi_vector(x[1:-1])]
        return set(valset)
    if x.startswith("<") and x.endswith(">"):
        return _dexi_vector(x[1:-1])
    lh = x.split(":")
    if len(lh) == 1:
        return int(lh[0]) + add
    l = int(lh[0]) + add
    h = int(lh[1]) + add
    return set(range(l, h + 1))

def _dexi_option_value(x: Optional[str]) -> DexiValue | str:
    if x is None:
        return None
    x = x.lower()
    if x in ("", "*"):
        return "*"
    if x.startswith("undef"):
        return None
    vals = utl.rule_values(x)
    return vals[0] if len(vals) == 1 else set(vals)

def _parse_dexi_continuous_scale(scl_xml: ET.Element,
                                order: DexiOrder = DexiOrder.ASCENDING
                                ) -> DexiContinuousScale:
    low_point = float(scl_xml.findtext("LOW", default = "-inf"))
    high_point = float(scl_xml.findtext("HIGH", default = "+inf"))
    return DexiContinuousScale(order = order, lpoint = low_point, hpoint = high_point)

def _parse_dexi_discrete_scale(scl_xml: list[ET.Element],
                              order: DexiOrder = DexiOrder.ASCENDING
                              ) -> DexiDiscreteScale:
    values: list[str] = []
    descrs: list[str] = []
    quals: list[DexiQuality] = []
    for val_xml in scl_xml:
        values.append(val_xml.findtext("NAME", default = ""))
        descrs.append(val_xml.findtext("DESCRIPTION", default = ""))
        qual = val_xml.findtext("GROUP", default = "NONE").upper()
        quality = \
            DexiQuality.GOOD if qual == "GOOD" \
            else DexiQuality.BAD if qual == "BAD" \
            else DexiQuality.NONE
        quals.append(quality)
    return DexiDiscreteScale(order = order, values = values, descriptions = descrs, quality = quals)

def _parse_dexi_scale(att_xml: ET.Element) -> Optional[DexiScale]:
    scl_xml = att_xml.find("SCALE")
    if scl_xml is None:
        return None
    order_text: str = scl_xml.findtext("ORDER", default = "ASC").upper()
    order: DexiOrder = \
        DexiOrder.DESCENDING if order_text == "DESC" \
        else DexiOrder.NONE if order_text == "NONE" \
        else DexiOrder.ASCENDING
    xml = scl_xml.find("CONTINUOUS")
    if xml is not None:
        return _parse_dexi_continuous_scale(xml, order)
    xmls = scl_xml.findall("SCALEVALUE")
    if xmls is not None and len(xmls) > 0:
        return _parse_dexi_discrete_scale(xmls, order)
    return None

def _parse_dexi_tabular_funct_def(att_xml: ET.Element) -> Optional[dict[str, Any]]:
    fnc_xml = att_xml.find("FUNCTION")
    if fnc_xml is not None:
        low = fnc_xml.findtext("LOW", default = "")
        high = fnc_xml.findtext("HIGH", default = low)
        return {"low": low, "high": high}
    tab_xml = att_xml.find("TABLE")
    if tab_xml is not None:
        values: list[DexiValue | str] = []
        rul_xml = tab_xml.findall("RULE")
        for val_xml in rul_xml:
            val = _dexi_value(val_xml.text)
            values.append(val)
        return {"values": values}
    return None

def _parse_dexi_discretize_funct_def(att_xml: ET.Element) -> Optional[dict[str, Any]]:
    fnc_xml = att_xml.find("DISCRETIZE")
    if fnc_xml is None or len(fnc_xml) == 0:
        return None
    values_xml = fnc_xml.findall("VALUE")
    values: list[DexiValue | str] = []
    for val_xml in values_xml:
        val = _dexi_value(val_xml.text)
        values.append(val)
    bounds_xml = fnc_xml.findall("BOUND")
    bounds: list[float] = []
    assoc: list[BoundAssoc] = []
    for bnd_xml in bounds_xml:
        bnd = float(str(bnd_xml.text))
        attrib = bnd_xml.attrib
        asc_text = attrib["Associate"] if "Associate" in attrib else "down"
        asc = BoundAssoc.UP if asc_text.upper() == "UP" else BoundAssoc.DOWN
        bounds.append(bnd)
        assoc.append(asc)
    values = utl.pad_list(values, len(bounds) + 1, None)
    return {"values": values, "bounds": bounds, "assoc": assoc}

def _parse_dexi_alternative_names(att_xml: ET.Element) -> list[str]:
    names: list[str] = []
    for el in att_xml:
        if el.tag == "OPTION":
            txt = el.text
            names.append("" if txt is None else txt)
        elif el.tag == "ALTERNATIVE":
            txt = el.findtext("NAME", default = "")
            names.append("" if txt is None else txt)
    return names

def _parse_dexi_alternative_values(att_xml: ET.Element) -> list[DexiValue | str]:
    values = []
    for el in att_xml:
        if el.tag == "OPTION":
            values.append(_dexi_option_value(el.text))
        elif el.tag == "ALTERNATIVE":
            values.append(_dexi_value(el.text))
    return values

def _parse_dexi_attributes(xml: ET.Element,
                          def_name: str = "",
                          alt_values: bool = True) -> DexiAttribute:
    name = xml.findtext("NAME", default = def_name)
    description = xml.findtext("DESCRIPTION", default = "")


    scale: Optional[DexiScale] = _parse_dexi_scale(xml)
    tab_funct_def = _parse_dexi_tabular_funct_def(xml)
    disc_funct_def = _parse_dexi_discretize_funct_def(xml)

    inp_xmls = xml.findall("ATTRIBUTE")
    inp_list: list[DexiAttribute] =  []
    for inp_xml in inp_xmls:
        inp = _parse_dexi_attributes(inp_xml)
        inp_list.append(inp)
    att = DexiAttribute(name, description, inputs = inp_list, scale = scale)

    # parents
    for inp in att.inputs:
        inp.parent = att

    # function
    funct: Optional[DexiFunction] = None
    if scale is not None:
        if tab_funct_def is not None and isinstance(scale, DexiDiscreteScale):
            if "values" in tab_funct_def:
                funct = DexiTabularFunction(att, values = tab_funct_def["values"])
            else:
                funct = DexiTabularFunction(att,
                                            low = tab_funct_def["low"],
                                            high = tab_funct_def["high"])
        elif disc_funct_def is not None and isinstance(scale, DexiDiscreteScale):
            funct = DexiDiscretizeFunction(att,
                                           values = disc_funct_def["values"],
                                           bounds = disc_funct_def["bounds"],
                                           assoc = disc_funct_def["assoc"])
    att.funct = funct

    # pylint: disable=protected-access
    # _alternatives
    if alt_values:
        att._alternatives = _parse_dexi_alternative_values(xml)
    else:
        att._alternatives = _parse_dexi_alternative_names(xml)
    # pylint: enable=protected-access

    return att

def _parse_dexi(xml: ET.Element) -> DexiModel:
    name = xml.findtext("NAME", default = "")
    if name == "":
        name = "DEXi Model"
    description = xml.findtext("DESCRIPTION", default = "")
    linking = _dexi_bool(xml.findtext("./SETTINGS/LINKING", default = ""))
    root = _parse_dexi_attributes(xml, def_name = "root", alt_values = False)
    return DexiModel(name, description, root, linking)

def read_dexi(filename: str) -> DexiModel:
    """Read a `DexiModel` from file.

    Args:
        filename (str): File name.

    Raises:
        ValueError: When the file does not contain a DEXi model.

    Returns:
        DexiModel: A `DexiModel` object.
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    if root.tag != "DEXi":
        raise ValueError(f'File "{filename}" does not contain a DEXi model')
    return _parse_dexi(root)

def read_dexi_from_string(xml: str) -> DexiModel:
    """Read a `DexiModel` from string.

    Args:
        xml (str): A XML-formatted string containing a `DexiModel`.

    Raises:
        ValueError: When `xml` does not contain a DEXi model.

    Returns:
        DexiModel: A DexiModel object.
    """
    root = ET.fromstring(xml)
    if root.tag != "DEXi":
        raise ValueError("XML argument does not contain a DEXi model")
    return _parse_dexi(root)
