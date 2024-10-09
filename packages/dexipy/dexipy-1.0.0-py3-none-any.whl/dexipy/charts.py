"""
Module `dexipy.charts` is aimed at drawing various charts of alternatives.
"""

import math
from typing import Optional, Iterable
import matplotlib.pyplot as plt
from matplotlib.text import Text, TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.projections.polar import PolarAxes
from matplotlib.transforms import Bbox
from matplotlib.typing import ColorType
from dexipy.types import DexiValue, DexiOrder, DexiAltData
from dexipy.dexi import DexiDiscreteScale, DexiModel, DexiAttribute
from dexipy.dexi import alt_name
from dexipy.eval import get_alt_value, get_alternatives
import dexipy.utils as utl
import dexipy.eval as evl

def _get_text_size(text: str, font_size: float = 12, font_name: str = 'DejaVu Sans') -> Bbox:
    """Get `text` dimensions without actually drawing on a canvas.

    Args:
        text (str): _description_
        font_size (float, optional): Font size. Defaults to 12.
        font_name (str, optional): Font name. Defaults to 'DejaVu Sans'.

    Returns:
        Bbox: Text dimensions.
    """

    # Create a FontProperties object with the desired font and size
    font_prop = FontProperties(family = font_name, size = font_size)

    # Create a TextPath object which calculates text size
    text_path = TextPath((0, 0), text, prop=font_prop)

    # Get the bounding box of the TextPath and extract the width
    return text_path.get_extents()

def _get_plot_size(fig: Figure) -> tuple[float, float]:
    """Given plot as `fig`, determine its width and height in pixels.

    Args:
        fig (Figure): Matplotlib Figure object.

    Returns:
        tuple[float, float]: Plot width and height in pixels.
    """
    # Get the figure DPI (dots per inch)
    dpi = fig.get_dpi()

    # Get the figure size in inches (width, height)
    size = fig.get_size_inches()
    return (size[0] * dpi, size[1] * dpi)

def _get_font_info(text_obj: Text) -> tuple[str, float]:
    """Get font info of `text_obj`.

    Args:
        text_obj (Text): Matplotlib Text object.

    Returns:
        tuple[str, float]: Font name and size.
    """
    font_properties = text_obj.get_fontproperties()
    font_name = font_properties.get_name()    # Get font name
    font_size = font_properties.get_size()    # Get font size
    return font_name, font_size

def _expand_value_to_points(value: DexiValue, attribute: DexiAttribute,
                            colors: tuple[ColorType, ColorType, ColorType] = ('r', 'k', 'g')
                            ) -> Optional[tuple[list[float], list[float], list[ColorType]]]:
    """Expand a DEXi `value` to a sequence of individual elements (points).
       Helper for chart-drawing functions that display DEXi values
       with dots of different sizes and colors.

    Args:
        value (DexiValue): A Dexi value.
        attribute (DexiAttribute): A DexiAttribute object. Required.
        colors (tuple, optional):
            A tuple of three colors for displaying "bad", "neutral" and "good" values,
            respectively. Defaults to ('r', 'k', 'g').

    Raises:
        ValueError: When `value` or `attribute` are None.

    Returns:
        Optional[tuple[list[float], list[float], list[ColorType]]]:
            Three lists of equal lengths: data points (ordinal numbers or floats),
            sizes of those points, and colors of those points.
    """
    if value is None:
        return None
    if attribute is None:
        return None
    scl = attribute.scale
    if isinstance(value, (int, float)):
        points = [value]
        sizes = [1.0]
    elif isinstance(value, (set, tuple)):
        points = list(value)
        sizes = len(value) * [1.0]
    elif isinstance(value, list):
        points = list(utl.distr_to_set(value))
        sizes = [value[int(p)] for p in points]
    else:
        raise ValueError(f"Cannot expand value to points: {value}")
    point_colors: list[ColorType] = []
    for p in points:
        if scl is None:
            c = colors[1]
        else:
            q = scl.value_quality(p)
            c = colors[1] if q is None else colors[q.value + 1]
        point_colors.append(c)
    return (points, sizes, point_colors)

def plotalt1(model: DexiModel,
             attribute: Optional[DexiAttribute | str | int] = None,
             alternatives: Optional[DexiAltData] = None,
             colors: tuple[ColorType, ColorType, ColorType] = ('r', 'k', 'g'),
             marker: str = 'o',
             markersize: float = 1.0,
             left_adjust: Optional[float] = None,
             plot: bool = True
             ) -> Optional[tuple[Figure, Axes]]:
    """Plot `alternatives` with respect to a single `attribute`.

    Args:
        model (DexiModel): A `DexiModel` object. Required.
        attribute (Optional[DexiAttribute | str | int], optional):
            A `DexiAttribute` object, attribute ID or attribute index.
            Defaults to None, which selects `model.first()`.
        alternatives (Optional[DexiAltData], optional):
            A single `DexiAlternative` or a list
            of alternatives (`DexiAlternatives`).
            Defaults to None, which selects `model.alternatives`.
        colors (tuple[ColorType, ColorType, ColorType], optional):
            A tuple of three colors for displaying "bad", "neutral" and "good" values, respectively.
            Defaults to ('r', 'k', 'g').
        marker (str, optional): Matplotlib marker to draw plot points. Defaults to 'o'.
        markersize (float, optional):
            Relative marker size with respect to default plot size. Defaults to 1.0.
        left_adjust (Optional[float], optional):
            A number between 0 and 0.5 that reserves the left
            proportion of the plot for `y`-axis label and names of alternatives.
            Defaults to None, which approximates this proportion considering alternatives' names.
        plot (bool, optional):
            Whether to draw (True) or return (False) the plot.

    Returns:
        Optional[tuple[Figure, Axes]]:
            Draws the plot (if `plot` = True) or
            returns Matplotlib figure and axes (False).

    Raises:
        ValueError:
            When `model` is None, when `attribute` cannot be determined
            from the second argument, or when `attribute.scale` is None.
    """

    # Check & prepare arguments
    if model is None:
        raise ValueError("Undefined model")
    att = None
    if attribute is None:
        att = model.first()
    if isinstance(attribute, DexiAttribute):
        att = attribute
    if isinstance(attribute, (str, int)):
        att = model.attrib(attribute)
    if att is None:
        raise ValueError("Undefined attribute")
    if att.scale is None:
        raise ValueError("Undefined attribute scale")
    alts = get_alternatives(alternatives, model)

    # Create points to draw
    altnames: list[str] = []
    x: list[float] = []
    y: list[float] = []
    sizes: list[float] = []
    point_colors: list[ColorType] = []
    for idx, alt in enumerate(alts):
        altnames.append(alt_name(alt, "Alt" + str(idx + 1)))
        value = get_alt_value(alt, att.id)
        expand = _expand_value_to_points(value, att, colors = colors)
        if expand is None:
            continue
        p, s, c = expand
        y.extend(len(p) * [idx])
        x.extend(p)
        sizes.extend(s)
        point_colors.extend(c)

    # Draw
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    alt_title = "Alternatives"
    plt.scatter(x, y, s = [markersize * 72 * s for s in sizes],
                c = point_colors, marker = marker)
    plt.ylim(len(alts) - 0.5, -0.5)
    plt.yticks(list(range(len(alts))), labels = altnames)
    plt.xlabel(att.id)
    if att.is_discrete():
        assert isinstance(att.scale, DexiDiscreteScale)
        plt.xlim(-0.5, att.scale.count() - 0.5)
        plt.xticks(list(range(att.scale.count())), labels = att.scale.values)
    plt.ylabel(alt_title)
    plt.grid(axis = 'y', which = 'major')

    if left_adjust is None:
        pw , _ = _get_plot_size(fig)
        font_name, font_size = _get_font_info(ax.yaxis.label)
        aw = max(_get_text_size(an, font_size, font_name).width for an in altnames)
        left_adjust = \
            (aw + 8 * _get_text_size(alt_title, font_size, font_name).height) / (0.95 * pw)

    plt.subplots_adjust(left = min(left_adjust, 0.5), right = 0.95)

    if plot:
        plt.show()
        return None
    return (fig, ax)

def plotalt2(model: DexiModel,
             attribute1: DexiAttribute | str | int,
             attribute2: DexiAttribute | str | int,
             alternatives: Optional[DexiAltData] = None,
             colors: list[ColorType] = [],
             marker: str = 'o',
             markersize: float = 1.0,
             left_adjust: Optional[float] = None,
             label_adjust: float = 0.1,
             plot: bool = True
             ) -> Optional[tuple[Figure, Axes]]:
    """Draw a scatterpolot of `alternatives` with `attribute1` and `attribute2` on the
    :math:`x` and :math:`y` axis, respectively.

    Args:
        model (DexiModel):
            A `DexiModel` object. Required.
        attribute1 (DexiAttribute | str | int):
            First attribute (`x`-axis). A `DexiAttribute` object, attribute ID or index.
        attribute2 (DexiAttribute | str | int):
            Second attribute (`y`-axis). A `DexiAttribute` object, attribute ID or index.
        alternatives (Optional[DexiAltData], optional):
            A single `DexiAlternative` or a list of alternatives (`DexiAlternatives`).
            Defaults to None, which selects `model.alternatives`.
        colors (list[ColorType], optional):
            A list of colors to be used for drawing consecutive alternatives
            (circulated if necessary).
            Defaults to [], which selects the `matplotlib` default color palette.
        marker (str, optional):
            Matplotlib marker to draw plot points. Defaults to 'o'.
        markersize (float, optional):
            Relative marker size with respect to default plot size. Defaults to 1.0.
        left_adjust (Optional[float], optional):
            A number between 0 and 0.5 that reserves the left
            proportion of the plot for y-axis label and names of alternatives.
            Defaults to None, which approximates this proportion
            considering `y`-axis attribute values.
        label_adjust (float, optional):
            A number (in plot coordinates) indicating the displacement of alternative names,
            which are displayed with individual points, to the right. Defaults to 0.1.
        plot (bool, optional):
            Whether to draw (True) or return (False) the plot.

    Returns:
        Optional[tuple[Figure, Axes]]:
            Draws the plot (if `plot` = True) or
            returns Matplotlib figure and axes (False).

    Raises:
        ValueError:
            When `model` is None,
            when `attribute1` or `attribute2` cannot be determined from
            the respective arguments, or
            when attributes' scales are not discrete.
    """
    # Check & prepare arguments
    if model is None:
        raise ValueError("Undefined model")
    if attribute1 is None or attribute2 is None:
        raise ValueError("Undefined attribute(s)")
    att1: Optional[DexiAttribute]  = \
        model.attrib(attribute1) if isinstance(attribute1, (int, str)) \
        else attribute1 if isinstance(attribute1, DexiAttribute) \
        else None
    att2: Optional[DexiAttribute]  = \
        model.attrib(attribute2) if isinstance(attribute2, (int, str)) \
        else attribute2 if isinstance(attribute2, DexiAttribute) \
        else None
    if att1 is None or att2 is None:
        raise ValueError("Attribute(s) not found")
    if not (att1.is_discrete() and att2.is_discrete()):
        raise ValueError("Only discrete attributes are supported")
    assert att1.scale is not None and isinstance(att1.scale, DexiDiscreteScale)
    assert att2.scale is not None and isinstance(att2.scale, DexiDiscreteScale)
    alts = get_alternatives(alternatives, model)

    if colors is None or len(colors) == 0:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    nval1 = att1.scale.count()
    nval2 = att2.scale.count()
    altnames: list[str] = []
    altvalues1: list[DexiValue] = []
    altvalues2: list[DexiValue] = []
    for idx, alt in enumerate(alts):
        altnames.append(alt_name(alt, "Alt" + str(idx + 1)))
        altvalues1.append(get_alt_value(alt, att1.id))
        altvalues2.append(get_alt_value(alt, att2.id))

    # Construct points to be displayed
    x: list[int] = []
    y: list[int] = []
    c: list[ColorType] = []
    s: list[float] = []
    l: dict[tuple[int, int], str] = {}

    for idx, alt in enumerate(alts):
        value1, value2 = altvalues1[idx], altvalues2[idx]
        expand1 = _expand_value_to_points(value1, att1)
        expand2 = _expand_value_to_points(value2, att2)
        if expand1 is None or expand2 is None:
            continue
        pts1, siz1, _ = expand1
        pts2, siz2, _ = expand2
        for i1, p1 in enumerate(pts1):
            for i2, p2 in enumerate(pts2):
                x.append(int(p1))
                y.append(int(p2))
                s.append(math.sqrt(siz1[i1] * siz2[i2]))
                c.append(colors[idx % len(colors)])
                key = (int(p1), int(p2))
                l[key] = l[key] + "\n" + altnames[idx] if key in l else altnames[idx]
    # Draw
    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    plt.scatter(x, y, s = [markersize * 72 * z for z in s], c = c, marker = marker)
    plt.xlim(-0.5, nval1 - 0.2)
    plt.xticks(list(range(nval1)), labels = att1.scale.values)
    plt.xlabel(att1.id)
    plt.ylim(-0.5, nval2 - 0.5)
    plt.ylabel(att2.id)
    plt.yticks(list(range(nval2)), labels = att2.scale.values)
    plt.grid(axis = 'both', which = 'major')
    for i1 in range(nval1):
        for i2 in range(nval2):
            key = (i1, i2)
            if key in l:
                plt.text(
                    i1 + label_adjust,
                    i2,
                    l[key],
                    horizontalalignment = "left",
                    verticalalignment = "top"
                    )

    if left_adjust is None:
        pw ,_ = _get_plot_size(fig)
        font_name, font_size = _get_font_info(ax.yaxis.label)
        aw = max(_get_text_size(an, font_size, font_name).width for an in att2.scale.values)
        left_adjust = \
            (aw + 8 * _get_text_size(att2.id, font_size, font_name).height) / (0.95 * pw)
    plt.subplots_adjust(left = min(left_adjust, 0.5), right = 0.95)

    if plot:
        plt.show()
        return None
    return (fig, ax)

def plotalt_parallel(model: DexiModel,
            attributes: Optional[Iterable[DexiAttribute | str | int]] = None,
            alternatives: Optional[DexiAltData] = None,
            aggregate: Optional[str] = "minmax",
            name: str = "name",
            interpret: str = "distribution",
            scale_values: bool = True,
            omin: float = 0,
            omax: float = 1,
            defined_ranges: dict[str, tuple[float, float]] = {},
            reverse_descending: bool = True,
            shift: float = 0,
            colors: str | list[ColorType] = [],
            marker: str = 'o',
            markersize: float = 5.0,
            linestyle: str = '-',
            linewidth: float = 2.0,
            figsize: tuple[float, float] = (10, 5),
            rect: tuple[float, float, float, float] = (0.1, 0.1, 0.7, 0.8),
            plot: bool = True
           ) -> Optional[tuple[Figure, list[Axes]]]:
    """Plots DEXi `alternatives` on parallel axes, corresponding to `attributes`.

    Args:
        model (DexiModel):
            A `DexiModel` object.
        attributes (Optional[Iterable[DexiAttribute | str | in]]], optional):
            A sequence of `DexiAttributes`, attribute IDs or indices.
            Defaults to None, which selects `model.non_root`.
        alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.
        aggregate (Optional[str], optional):
            One of  "min", "max", "mean" or "minmax".
            Determines aggregation operation for sets and distributions.
            "minmax" selects both "min" and "max", so that each alternative is plotted twice.
            Defaults to "minmax".
        name (str):
            Name of `DexiAlternative` element that contains alternatives' name.
            Defaults to "name".
        interpret (str, optional):
            One of "set" or "distribution".
            Determines whether to interpret value distributions as sets or distributions.
            Defaults to "distribution".
        scale_values (bool, optional):
            Whether or not to scale values to the [`omin`, `omax`] interval. Defaults to True.
        omin (float, optional):
            Lower output bound for value scaling. Defaults to 0.
        omax (float, optional):
            Upper output bound for value scaling. Defaults to 1.
        defined_ranges (dict[str, tuple[float, float]], optional):
            A dictionary of pre-determined value ranges.
            Applicable to continuous attributes.
            Continuous attribute ranges, which are not specified in `defined_ranges`,
            are determined from `alternatives` data.
            Discrete attribute ranges are always determibned from their scales.
            Defaults to {}.
        reverse_descending (bool, optional):
            Whether or not to reverse values of descending attributes.
            Defaults to True.
        shift (float, optional):
            Used to "shift" numerical values by a small amount to avoid
            overlapping lines in charts. Defaults to 0.
        colors (list[ColorType], optional):
            A list of colors to be used for drawing consecutive alternatives
            (circulated if necessary).
            Defaults to [], which selects the `matplotlib` default color palette.
        marker (str, optional):
            Matplotlib marker to draw plot points. Defaults to 'o'.
        markersize (float, optional):
            Marker size. Defaults to 5.0.
        linestyle (str, optional):
            Matplotlib style to draw lines. Defaults to '-'.
        linewidth (float, optional):
            Line width. Defaults to 2.0.
        figsize (tuple[float, float], optional):
            Figure size in inches. Defaults to (10, 5).
        rect (tuple[float, float, float, float], optional):
            (left, bottom, width, height), defines the position of the figure on the canvas.
            Elements are numbers between 0 and 1. Defaults to (0.1, 0.1, 0.7, 0.8).
        plot (bool, optional):
            Whether to draw (True) or return (False) the plot.

    Returns:
        Optional[tuple[Figure, list[Axes]]]:
            Draws the plot (if `plot` = True) or
            returns Matplotlib figure and axes (False).
    """

    # Check & prepare arguments
    assert model is not None, "Undefined model"
    assert aggregate in ["min", "max", "mean", "minmax"], \
        'Parameter `aggregate` must be one of: "min", "max", "mean" or "minmax"'
    assert interpret in ["set", "distribution"], \
        'Parameter `interpret` must be one of: "set" or "distribution"'
    alts = get_alternatives(alternatives, model)
    altnames = [alt["name"] for alt in alts]

    # Determine attributes
    if attributes is None:
        attributes = model.non_root
    atts = model.attribute_list(attributes)
    natt = len(atts)
    assert natt > 0, "No attributes are suitable for plotting"
    assert natt > 1, "At least two attributes are required"

    # Define colors
    if colors is None or len(colors) == 0:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if isinstance(colors, str):
        cmap = plt.cm.get_cmap(colors)
        color_values = [(i / (natt - 1)) for i in range(natt)]
        colors = [cmap(val) for val in color_values]
    if colors is None or len(colors) == 0:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Prepare alternatives for drawing
    if aggregate == "minmax":
        calts = evl.convert_alternatives(model, alts, atts, aggregate = "max",
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)
        calts2 = evl.convert_alternatives(model, alts, atts, aggregate = "min",
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)
    else:
        calts = evl.convert_alternatives(model, alts, atts, aggregate = aggregate,
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)

#    left, bottom, width, height = rect
    fig = plt.figure(figsize = figsize)
    ax0 = fig.add_axes(rect)
    axes = [ax0] + [ax0.twinx() for i in range(natt - 1)]

    ax0.xaxis.tick_top()
    ax0.xaxis.set_ticks_position("none")
    ax0.set_xlim((0, natt - 1))
    ax0.set_xticks(range(natt))
    ax0.set_xticklabels([att.id for att in atts])

    # Format y-axis
    for i, ax in enumerate(axes):
        ax.spines["left"].set_position(("axes", 1 / (natt - 1) * i))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        ax.yaxis.set_ticks_position("left")
        if atts[i].is_discrete():
            att = atts[i]
            assert isinstance(att.scale, DexiDiscreteScale)
            if att.scale.order == DexiOrder.DESCENDING:
                ax.set_ylim(ymin = 1, ymax = 0)
            else:
                ax.set_ylim(ymin = 0, ymax = 1)
            ax.set_yticks([v / (att.scale.count() - 1) for v in range(att.scale.count())])
            ax.set_yticklabels(att.scale.values)

    for altidx, alt in enumerate(calts):
        col = colors[altidx % len(colors)]
        x = list(range(natt))
        y = [alt[att.id] for att in atts]
        ax0.plot(x, y, color = col, clip_on = False,            # type: ignore
                 linestyle = linestyle, linewidth = linewidth,
                 marker = marker, markersize = markersize,
                 label = altnames[altidx])
        if aggregate == "minmax":
            y2 = [calts2[altidx][att.id] for att in atts]
            ax0.plot(x, y2, color = col, clip_on = False,       # type: ignore
                 linestyle = linestyle, linewidth = linewidth,
                 marker = marker, markersize = markersize,
                 label = "_ignore")

    ax0.legend(
        loc = "upper left",
        bbox_to_anchor = (1, 1),
        title = f"Alternatives ({aggregate})", ncols = 1
        )

    if plot:
        plt.show()
        return None
    return (fig, axes)

def plotalt_radar(model: DexiModel,
            attributes: Optional[Iterable[DexiAttribute | str | int]] = None,
            alternatives: Optional[DexiAltData] = None,
            aggregate: Optional[str] = "minmax",
            name: str = "name",
            interpret: str = "distribution",
            scale_values: bool = True,
            omin: float = 0,
            omax: float = 1,
            defined_ranges: dict[str, tuple[float, float]] = {},
            reverse_descending: bool = True,
            shift: float = 0,
            colors: str | list[ColorType] = [],
            fill: float | tuple[float, float] = 0,
            marker: str = 'o',
            markersize: float = 5.0,
            linestyle: str = '-',
            linewidth: float = 2.0,
            inner: float = 0.2,
            figsize: tuple[float, float] = (8, 5),
            legend_pos: tuple[float, float] = (1.1, 1),
            legend_loc: str = "upper left",
            plot: bool = True
           ) -> Optional[tuple[Figure, Axes]]:
    """Plots DEXi `alternatives` on parallel axes, corresponding to `attributes`.

    Args:
        model (DexiModel):
            A `DexiModel` object.
        attributes (Optional[Iterable[DexiAttribute | str | int]], optional):
            A sequence of `DexiAttributes`, attribute IDs or indices.
            Defaults to None, which selects `model.attributes`.
        alternatives (Optional[DexiAltData], optional):
            One or more DEXi alternatives.
            Defaults to None, which selects `model.alternatives`.
        aggregate (Optional[str], optional):
            One of  "min", "max", "mean" or "minmax".
            Determines aggregation operation for sets and distributions.
            "minmax" selects both "min" and "max", so that each alternative is plotted twice.
            Defaults to "minmax".
        name (str):
            Name of `DexiAlternative` element that contains alternatives' name.
            Defaults to "name".
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
            Discrete attribute ranges are always determibned from their scales.
            Defaults to {}.
        reverse_descending (bool, optional):
            Whether or not to reverse values of descending attributes.
            Defaults to True.
        shift (float, optional):
            Used to "shift" numerical values by a small amount to avoid overlapping lines in charts. 
            Defaults to 0.
        colors (list[ColorType], optional):
            A list of colors to be used for drawing consecutive alternatives
            (circulated if necessary).
            Defaults to [], which selects the `matplotlib` default color palette.
        fill (float | tuple[float, float]]):
            Alpha-channel value(s) for color-filling the drawn polygon(s).
            Expected are values from the :math:`[0, 1]` interval.
            If `fill` > 0, polygons are filled with the same color as lines and
            with the given alpha.
            The tuple form may be used for to charts with `aggregate` = "minmax",
            where the two tuple values represent alpha settings for the
            "max" and "min" polygon, respectively.
            Defaults to 0.
        marker (str, optional):
            Matplotlib marker to draw plot points. Defaults to 'o'.
        markersize (float, optional):
            Marker size. Defaults to 5.0.
        linestyle (str, optional):
            Matplotlib style to draw lines. Defaults to '-'.
        linewidth (float, optional):
            Line width. Defaults to 2.0.
        inner (float, optional)
            Radius of the inner chart circle where nothing is drawn.
            The value is relative to the :math:`[0, 1]` scale used to draw the data.
            Defaults to 0.2.
        figsize (tuple[float, float], optional):
            Figure size in inches. Defaults to (8, 5).
        legend_pos (tuple[float, float], optional):
            Legend position. Defaults to (1.1, 1).
        legend_loc (str, optional):
            Legend location. See `matplotlib.axes.Axes.legend` for possible values.
            Defaults to "upper left".
 
        plot (bool, optional):
            Whether to draw (True) or return (False) the plot.

    Returns:
        Optional[tuple[Figure, Axes]]:
            Draws the plot (if `plot` = True) or
            returns Matplotlib figure and axes (False).
    """

    # Check & prepare arguments
    assert model is not None, "Undefined model"
    assert aggregate in ["min", "max", "mean", "minmax"], \
        'Parameter `aggregate` must be one of: "min", "max", "mean" or "minmax"'
    assert interpret in ["set", "distribution"], \
        'Parameter `interpret` must be one of: "set" or "distribution"'
    alts = get_alternatives(alternatives, model)
    altnames = [alt["name"] for alt in alts]

    # Determine attributes
    if attributes is None:
        attributes = model.attributes
    atts = [att for att in model.attribute_list(attributes) \
                if att.is_discrete() or att.is_continuous()
           ]
    natt = len(atts)
    attnames = [att.id for att in atts]
    assert natt > 0, "No attributes are suitable for plotting"
    assert natt > 1, "At least two attributes are required"

    # Define colors
    if colors is None or len(colors) == 0:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if isinstance(colors, str):
        cmap = plt.cm.get_cmap(colors)
        color_values = [(i / (natt - 1)) for i in range(natt)]
        colors = [cmap(val) for val in color_values]
    if colors is None or len(colors) == 0:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if isinstance(fill, tuple):
        fill1, fill2 = fill
    else:
        fill1, fill2 = fill, fill

    # Prepare alternatives for drawing
    if aggregate == "minmax":
        calts = evl.convert_alternatives(model, alts, atts, aggregate = "max",
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)
        calts2 = evl.convert_alternatives(model, alts, atts, aggregate = "min",
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)
    else:
        calts = evl.convert_alternatives(model, alts, atts, aggregate = aggregate,
            name = name, interpret = interpret, defined_ranges = defined_ranges,
            scale_values = scale_values, omin = omin, omax = omax,
            reverse_descending = reverse_descending, shift = shift)

    fig = plt.figure(figsize = figsize)
    ax = plt.subplot(polar = True)
    assert isinstance(ax, PolarAxes)

    axenames = attnames
    axenames.append(axenames[0])
    naxes = len(axenames)

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    x = [i * 2 * math.pi / (naxes - 1) for i in range(natt)] + [0]
    xdeg = [180 * rd / math.pi for rd in x]
    ax.set_thetagrids(xdeg, axenames)

    for label, angle in zip(ax.get_xticklabels(), x):
        if angle in (0, math.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < math.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')

    ax.set_rlabel_position(0)
    plt.yticks([0, 0.5, 1])

    for altidx, alt in enumerate(calts):
        col = colors[altidx % len(colors)]
        y = [alt[att.id] for att in atts]
        y.append(y[0])
        ax.plot(x, y, color = col, clip_on = False,             # type: ignore
             linestyle = linestyle, linewidth = linewidth,
             marker = marker, markersize = markersize,
             label = altnames[altidx])
        if fill1 > 0:
            ax.fill(x, y, color = col, alpha = fill1)
        if aggregate == "minmax":
            y2 = [calts2[altidx][att.id] for att in atts]
            y2.append(y2[0])
            ax.plot(x, y2, color = col, clip_on = False,         # type: ignore
                 linestyle = linestyle, linewidth = linewidth,
                 marker = marker, markersize = markersize,
                 label = "_ignore")
            if fill2 > 0:
                ax.fill(x, y2, color = col, alpha = fill2)

    ax.legend(
        loc = legend_loc,
        bbox_to_anchor = legend_pos,
        title = f"Alternatives ({aggregate})", ncols = 1)

    ax.plot([0], [-abs(inner)], linewidth = 0, marker = None)

    if plot:
        plt.show()
        return None
    return (fig, ax)
