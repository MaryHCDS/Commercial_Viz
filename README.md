# Commercial_Viz

`commercial_viz` is a lightweight Python library for healthcare and
pharmaceutical commercial analytics built with pandas and matplotlib.

## Features

- `performance_bar()` – compare and rank business performance across categories
- `actual_vs_target()` – compare actual performance against goals

Every function accepts a pandas DataFrame and returns `(fig, ax)`.

## Installation

```bash
pip install -e .
```

## Example

```python
import pandas as pd
from commercial_viz import performance_bar

sales = pd.DataFrame({
    "region": ["West", "East", "South"],
    "revenue": [1250000, 980000, 740000]
})

fig, ax = performance_bar(
    sales,
    category="region",
    value="revenue",
    title="Regional Revenue",
    value_format="currency"
)
```
