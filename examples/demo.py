"""Demo script for commercial_viz.

Renders one example of each chart as it is implemented. Run with::

    python examples/demo.py

Currently shows: performance_bar, actual_vs_target.
"""

import matplotlib.pyplot as plt
import pandas as pd

from commercial_viz import actual_vs_target, performance_bar


def main():
    """Render the performance_bar and actual_vs_target examples."""
    sales_by_region = pd.DataFrame(
        {
            "region": ["Northeast", "Southeast", "Midwest", "West", "Southwest"],
            "sales": [820_000, 610_000, 540_000, 930_000, 470_000],
        }
    )

    fig, ax = performance_bar(
        sales_by_region,
        category="region",
        value="sales",
        title="West leads U.S. sales this quarter",
        value_format="currency",
    )
    fig.savefig("performance_bar_demo.png", dpi=150, bbox_inches="tight")
    print("Saved performance_bar_demo.png")
    plt.close(fig)

    sales_vs_quota = pd.DataFrame(
        {
            "region": ["Northeast", "Southeast", "Midwest", "West", "Southwest"],
            "sales": [820_000, 610_000, 540_000, 930_000, 470_000],
            "quota": [750_000, 650_000, 500_000, 800_000, 520_000],
        }
    )

    fig, ax = actual_vs_target(
        sales_vs_quota,
        category="region",
        actual="sales",
        target="quota",
        title="West and Northeast beat quota; Southwest fell short",
        value_format="currency",
    )
    fig.savefig("actual_vs_target_demo.png", dpi=150, bbox_inches="tight")
    print("Saved actual_vs_target_demo.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
