"""Chart functions for healthcare commercial analytics.

Each public function accepts a pandas DataFrame and returns a matplotlib
Figure and Axes as a tuple ``(fig, ax)``. Functions never modify the
caller's DataFrame.

NOTE: These are placeholder signatures only. The chart logic is not
implemented yet.
"""

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Visual theme constants (consulting style)
# ---------------------------------------------------------------------------

# Consulting-style palette (see PROJECT_PLAN.md). Deep navy dominates and
# bright teal is used only to highlight the most important result.
NAVY = "#001F33"       # dominant color for most bars / lines
TEAL = "#0099B8"       # selective emphasis (the key result)
WHITE = "#FFFFFF"
OFF_WHITE = "#F7F7F3"  # soft light background
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


# ---------------------------------------------------------------------------
# Placeholder function signatures
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

    # Add a formatted data label just past the end of each bar.
    for bar, amount in zip(bars, amounts):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            "  " + _format_value(amount, value_format),
            va="center",
            ha="left",
            color=DARK_TEXT,
            fontsize=LABEL_FONTSIZE,
        )

    if title:
        ax.set_title(
            title,
            fontsize=TITLE_FONTSIZE,
            fontweight="bold",
            color=DARK_TEXT,
            loc="left",
        )

    # Remove clutter: drop spines, gridlines, and the numeric x-axis
    # (the data labels already carry the numbers).
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(left=False)
    for label in ax.get_yticklabels():
        label.set_color(DARK_TEXT)

    fig.tight_layout()
    return fig, ax


def actual_vs_target(df, category, actual, target, title=None):
    """Compare actual values against target values per category.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.
    category : str
        Column of category labels (e.g. ``"region"``).
    actual : str
        Column holding actual values.
    target : str
        Column holding target values.
    title : str, optional
        Chart title.

    Returns
    -------
    (matplotlib.figure.Figure, matplotlib.axes.Axes)
    """
    raise NotImplementedError


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
