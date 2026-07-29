"""commercial_viz: healthcare commercial analytics visualizations.

Public API re-exports the five chart functions so users can write::

    from commercial_viz import performance_bar
"""

from commercial_viz.charts import (
    actual_vs_target,
    distribution_plot,
    market_share,
    performance_bar,
    trend_line,
)

__version__ = "0.1.0"

__all__ = [
    "performance_bar",
    "actual_vs_target",
    "trend_line",
    "market_share",
    "distribution_plot",
]
