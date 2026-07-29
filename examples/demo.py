"""Demo script for commercial_viz.

Renders one example of each chart as it is implemented. Run with::

    python examples/demo.py

Currently shows: performance_bar.
"""

import matplotlib.pyplot as plt
import pandas as pd

from commercial_viz import performance_bar


def main():
    """Render the performance_bar example."""
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


if __name__ == "__main__":
    main()
