"""Chart functions for healthcare commercial analytics.

Each public function accepts a pandas DataFrame and returns a matplotlib
``(fig, ax)``. Functions never modify the caller's DataFrame.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

# Consulting-style palette: deep navy dominates, teal marks the key result.
NAVY = "#001F33"
TEAL = "#0099B8"
DARK_TEXT = "#0B2239"

FIGURE_SIZE = (8, 5)
TITLE_FONTSIZE = 14
LABEL_FONTSIZE = 11


def _format_value(number, value_format):
    """Return ``number`` as a plain, currency, or percent string."""
    if value_format == "currency":
        return f"${number:,.0f}"
    if value_format == "percent":
        return f"{number:,.1f}%"
    return f"{number:,.0f}"


def _apply_theme(ax):
    """Strip spines, gridlines, and the numeric x-axis for a clean look."""
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(left=False)
    for label in ax.get_yticklabels():
        label.set_color(DARK_TEXT)


def _label_bars(ax, bars, values, value_format):
    """Write a formatted value label just past the end of each bar."""
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            "  " + _format_value(value, value_format),
            va="center",
            ha="left",
            color=DARK_TEXT,
            fontsize=LABEL_FONTSIZE,
        )


def performance_bar(df, category, value, title=None, value_format="number"):
    """Sorted horizontal bar chart of performance by category.

    Totals ``value`` per ``category`` and highlights the largest bar in
    teal (e.g. sales by region). Does not modify ``df``.

    Parameters
    ----------
    df : pandas.DataFrame
    category, value : str
        Category-label column and numeric column to total.
    title : str, optional
        Insight-led chart title.
    value_format : {"number", "currency", "percent"}, default "number"
        Data-label formatting.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)

    Raises
    ------
    TypeError
        If ``df`` is not a DataFrame.
    ValueError
        If ``df`` is empty or a required column is missing.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("df must not be empty.")
    for column_name in (category, value):
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' is not in the DataFrame.")

    totals = df.groupby(category)[value].sum().sort_values()
    categories = list(totals.index)
    amounts = list(totals.values)

    bar_colors = [NAVY] * len(amounts)
    bar_colors[-1] = TEAL  # largest category (last after sorting)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.barh(categories, amounts, color=bar_colors)
    _label_bars(ax, bars, amounts, value_format)
    if title:
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight="bold",
                     color=DARK_TEXT, loc="left")
    _apply_theme(ax)
    fig.tight_layout()
    return fig, ax


def actual_vs_target(df, category, actual, target, title=None, value_format="number"):
    """Compare actual commercial performance against a target per category.

    Draws actual values as navy bars sorted by actual, with each target as
    a teal vertical line (e.g. sales vs. quota). Does not modify ``df``.

    Parameters
    ----------
    df : pandas.DataFrame
    category : str
        Category-label column.
    actual, target : str
        Columns holding actual and target values.
    title : str, optional
        Insight-led chart title.
    value_format : {"number", "currency", "percent"}, default "number"
        Actual-value label formatting.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)

    Raises
    ------
    TypeError
        If ``df`` is not a DataFrame.
    ValueError
        If ``df`` is empty or a required column is missing.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("df must not be empty.")
    for column_name in (category, actual, target):
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' is not in the DataFrame.")

    totals = df.groupby(category)[[actual, target]].sum().sort_values(actual)
    categories = list(totals.index)
    actual_values = list(totals[actual].values)
    target_values = list(totals[target].values)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.barh(categories, actual_values, color=NAVY)
    for bar, target_value in zip(bars, target_values):
        ax.vlines(target_value, bar.get_y(), bar.get_y() + bar.get_height(),
                  color=TEAL, linewidth=3)
    _label_bars(ax, bars, actual_values, value_format)

    # Frameless legend explains the teal target marker.
    target_marker = Line2D([0], [0], color=TEAL, linewidth=3, label="Target")
    ax.legend(handles=[target_marker], loc="lower right", frameon=False)
    if title:
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight="bold",
                     color=DARK_TEXT, loc="left")
    _apply_theme(ax)
    fig.tight_layout()
    return fig, ax
