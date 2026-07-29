"""Tests for commercial_viz chart functions."""

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")  # non-interactive backend for testing

import commercial_viz
from commercial_viz.charts import actual_vs_target, performance_bar


def sample_df():
    """A small commercial dataset: sales by region (with a repeat region)."""
    return pd.DataFrame(
        {
            "region": ["West", "East", "South", "West"],
            "sales": [100, 250, 175, 50],
        }
    )


def test_public_functions_are_importable():
    """The two public chart functions should be importable from the package."""
    for name in ["performance_bar", "actual_vs_target"]:
        assert hasattr(commercial_viz, name)


def test_returns_fig_and_ax():
    """performance_bar returns a matplotlib Figure and Axes."""
    fig, ax = performance_bar(sample_df(), "region", "sales")
    assert fig.__class__.__name__ == "Figure"
    assert ax.__class__.__name__ in ("Axes", "AxesSubplot")


def test_aggregates_and_sorts_ascending():
    """Values are summed per category and sorted smallest to largest."""
    fig, ax = performance_bar(sample_df(), "region", "sales")
    # West is summed to 150; order bottom-to-top should be smallest first.
    labels = [tick.get_text() for tick in ax.get_yticklabels()]
    assert labels == ["West", "South", "East"]
    widths = [bar.get_width() for bar in ax.patches]
    assert widths == [150.0, 175.0, 250.0]


def test_largest_bar_is_teal():
    """The largest category is highlighted in teal; others are navy."""
    from commercial_viz.charts import NAVY, TEAL

    fig, ax = performance_bar(sample_df(), "region", "sales")
    colors = [bar.get_facecolor() for bar in ax.patches]
    top_bar_color = matplotlib.colors.to_hex(colors[-1])
    other_color = matplotlib.colors.to_hex(colors[0])
    assert top_bar_color.upper() == TEAL
    assert other_color.upper() == NAVY


def test_does_not_modify_caller_dataframe():
    """The original DataFrame must be untouched."""
    df = sample_df()
    before = df.copy()
    performance_bar(df, "region", "sales")
    pd.testing.assert_frame_equal(df, before)


def test_rejects_non_dataframe():
    with pytest.raises(TypeError):
        performance_bar([1, 2, 3], "region", "sales")


def test_rejects_empty_dataframe():
    with pytest.raises(ValueError):
        performance_bar(pd.DataFrame({"region": [], "sales": []}), "region", "sales")


def test_rejects_missing_columns():
    with pytest.raises(ValueError):
        performance_bar(sample_df(), "region", "missing_column")


# ---------------------------------------------------------------------------
# actual_vs_target
# ---------------------------------------------------------------------------

def target_df():
    """Sales versus quota by region (with a repeat region to aggregate)."""
    return pd.DataFrame(
        {
            "region": ["West", "East", "South", "West"],
            "sales": [100, 250, 175, 50],
            "quota": [120, 200, 180, 30],
        }
    )


def test_avt_returns_fig_and_ax_and_marks_targets():
    """actual_vs_target returns (fig, ax), navy bars, and teal target lines."""
    from commercial_viz.charts import NAVY, TEAL

    fig, ax = actual_vs_target(target_df(), "region", "sales", "quota")
    assert fig.__class__.__name__ == "Figure"
    assert ax.__class__.__name__ in ("Axes", "AxesSubplot")

    # Actual bars are navy; sorted by actual (West=150), so West on top.
    bar_colors = {matplotlib.colors.to_hex(b.get_facecolor()).upper() for b in ax.patches}
    assert bar_colors == {NAVY}
    widths = [bar.get_width() for bar in ax.patches]
    assert widths == [150.0, 175.0, 250.0]

    # Each target is drawn as a teal LineCollection (one per category).
    teal_lines = [
        c for c in ax.collections
        if matplotlib.colors.to_hex(c.get_color()[0]).upper() == TEAL
    ]
    assert len(teal_lines) == 3


def test_avt_rejects_missing_columns():
    with pytest.raises(ValueError):
        actual_vs_target(target_df(), "region", "sales", "missing_target")


def test_avt_rejects_empty_dataframe():
    empty = pd.DataFrame({"region": [], "sales": [], "quota": []})
    with pytest.raises(ValueError):
        actual_vs_target(empty, "region", "sales", "quota")


def test_avt_does_not_modify_caller_dataframe():
    df = target_df()
    before = df.copy()
    actual_vs_target(df, "region", "sales", "quota")
    pd.testing.assert_frame_equal(df, before)
