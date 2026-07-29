# CLAUDE.md

## Project

`commercial_viz` is a **beginner-friendly Python library** for healthcare
commercial analytics visualizations. It provides a small set of clean,
consulting-style chart functions built on pandas and matplotlib.

## Dependencies

- **Use only** pandas and matplotlib.
- **Do not use** seaborn, plotly, numpy directly, dashboards, notebooks,
  classes, machine learning, or AI-generated analysis.

## Code Rules

- Keep the core source code close to **200 lines**.
- Use **simple functions** and **descriptive variable names** — code a
  Python student can read and explain.
- Every public function must **accept a pandas DataFrame** and **return a
  matplotlib `Figure` and `Axes`** (`(fig, ax)`).
- **Do not modify the caller's DataFrame** — copy before transforming.
- **Validate required columns** and raise **clear, specific errors** when
  they are missing.
- Use a **consistent consulting-style visual theme** across all charts.
- Add **concise docstrings** to every public function.

## Workflow

- Work in **small steps**.
- **Run tests after changes.**
- **Do not commit** generated build folders or datasets.
