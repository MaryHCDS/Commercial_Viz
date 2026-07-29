"""Chart functions for healthcare commercial analytics.

Each public function accepts a pandas DataFrame and returns a matplotlib
Figure and Axes as a tuple ``(fig, ax)``. Functions never modify the
caller's DataFrame.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Visual theme constants (consulting style)
# ---------------------------------------------------------------------------

# Consulting-style palette (see PROJECT_PLAN.md). Deep navy dominates and
# bright teal is used only to highlight the most important result.
NAVY = "#001F33"       # dominant color for most bars / lines
TEAL = "#0099B8"       # selective emphasis (the key result)
DARK_TEXT = "#0B2239"  # text on light backgrounds

# Shared figure sizing and typography.
FIGURE_SIZE = (8, 5)   # width, height in inches
TITLE_FONTSIZE = 14
LABEL_FONTSIZE = 11


def _format_value(number, value_format):
    """Format a number as a plain number, currency, or percent string."""
    if value_format == "currency":
        return f"${number:,.0f}"
    if value_format == "percent":
        return f"{number:,.1f}%"
    return f"{number:,.0f}"


def _apply_theme(ax):
    """Apply the shared consulting look to an axis.

    Removes the top, right, and left spines, turns off gridlines, hides the
    numeric x-axis (the data labels already carry the numbers), and colors
    the category tick labels in dark navy.
    """
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


# ---------------------------------------------------------------------------
# Public chart functions
# ---------------------------------------------------------------------------

def performance_bar(df, category, value, title=None, value_format="number"):
    """Draw a clean, sorted horizontal bar chart of commercial performance.

    Useful for views such as sales by region or prescriptions by product.
    Values are summed per category and the largest bar is highlighted in
    teal. The caller's DataFrame is never modified.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    category : str
        Column of category labels (e.g. ``"region"``).
    value : str
        Numeric column to total per category (e.g. ``"sales"``).
    title : str, optional
        Chart title.
    value_format : str, default "number"
        How to format the data labels: ``"number"``, ``"currency"``,
        or ``"percent"``.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    # Validate inputs with clear, specific errors.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("df must not be empty.")
    for column_name in (category, value):
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' is not in the DataFrame.")

    # Total the value per category, then sort smallest to largest so the
    # biggest bar sits at the top of the horizontal chart.
    totals = df.groupby(category)[value].sum().sort_values(ascending=True)
    categories = list(totals.index)
    amounts = list(totals.values)

    # Highlight only the largest category (the last one) in teal.
    bar_colors = [NAVY] * len(amounts)
    bar_colors[-1] = TEAL

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.barh(categories, amounts, color=bar_colors)
    _label_bars(ax, bars, amounts, value_format)

    if title:
        ax.set_title(
            title,
            fontsize=TITLE_FONTSIZE,
            fontweight="bold",
            color=DARK_TEXT,
            loc="left",
        )

    _apply_theme(ax)
    fig.tight_layout()
    return fig, ax


def actual_vs_target(df, category, actual, target, title=None, value_format="number"):
    """Compare actual commercial performance against a target per category.

    Useful for views such as sales versus quota or prescriptions versus
    forecast. Actual values are drawn as navy bars and each target is
    marked with a teal vertical line, so it is easy to see who beat or
    missed plan. The caller's DataFrame is never modified.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    category : str
        Column of category labels (e.g. ``"region"``).
    actual : str
        Column holding actual values (e.g. ``"sales"``).
    target : str
        Column holding target values (e.g. ``"quota"``).
    title : str, optional
        Chart title.
    value_format : str, default "number"
        How to format the actual-value labels: ``"number"``,
        ``"currency"``, or ``"percent"``.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    # Validate inputs with clear, specific errors.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("df must not be empty.")
    for column_name in (category, actual, target):
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' is not in the DataFrame.")

    # Total actual and target per category, then sort by actual so the
    # strongest performer sits at the top of the horizontal chart.
    totals = df.groupby(category)[[actual, target]].sum().sort_values(actual)
    categories = list(totals.index)
    actual_values = list(totals[actual].values)
    target_values = list(totals[target].values)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    bars = ax.barh(categories, actual_values, color=NAVY)

    # Draw each target as a short teal vertical line across its bar.
    for bar, target_value in zip(bars, target_values):
        ax.vlines(
            target_value,
            bar.get_y(),
            bar.get_y() + bar.get_height(),
            color=TEAL,
            linewidth=3,
        )

    _label_bars(ax, bars, actual_values, value_format)

    # A small, frameless legend explains what the teal marker means.
    target_marker = Line2D([0], [0], color=TEAL, linewidth=3, label="Target")
    ax.legend(handles=[target_marker], loc="lower right", frameon=False)

    if title:
        ax.set_title(
            title,
            fontsize=TITLE_FONTSIZE,
            fontweight="bold",
            color=DARK_TEXT,
            loc="left",
        )

    _apply_theme(ax)
    fig.tight_layout()
    return fig, ax


def trend_line(df, date, value, group=None, marker_date=None, title=None):
    """Plot a metric over time, optionally split into groups.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    date : str
        Time column.
    value : str
        Numeric metric column.
    group : str, optional
        Column that draws one line per group (e.g. per brand).
    marker_date : optional
        Draws a vertical reference line (e.g. a launch date).
    title : str, optional
        Chart title.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    raise NotImplementedError


def market_share(df, category, value, title=None):
    """Show each category's share of the total as percentages.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    category : str
        Column of segment labels.
    value : str
        Numeric size column; shares are computed as a percent of the total.
    title : str, optional
        Chart title.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    raise NotImplementedError


def distribution_plot(df, value, bins=20, show_mean=True, title=None):
    """Show the distribution of a single numeric column as a histogram.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    value : str
        Numeric column to plot.
    bins : int, default 20
        Number of histogram bins.
    show_mean : bool, default True
        Draw a vertical reference line at the mean.
    title : str, optional
        Chart title.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    raise NotImplementedError
