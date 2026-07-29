# Commercial_Viz

`commercial-viz` is a beginner-friendly Python library of clean,
consulting-style visualizations for **healthcare & pharmaceutical
commercial analytics**, built on pandas and matplotlib.

## Charts

- `performance_bar` — rank categories by a metric
- `actual_vs_target` — compare results against goals
- `trend_line` — track a metric over time
- `market_share` — show composition / share of total
- `distribution_plot` — show the spread of a numeric variable

Every function takes a pandas `DataFrame` and returns a matplotlib
`(fig, ax)`.

## Install

```bash
pip install -e .
```

## Usage

```python
from commercial_viz import performance_bar
```

> Chart functions are not implemented yet — this is the initial package
> scaffold.
