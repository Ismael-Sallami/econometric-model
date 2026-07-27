# econometric-model

![Python](https://img.shields.io/badge/Python-3.12-3776AB)
![statsmodels](https://img.shields.io/badge/statsmodels-0.14-4c72b0)
[![checks](https://img.shields.io/github/actions/workflow/status/Ismael-Sallami/econometric-model/ci.yml?branch=main&logo=github&label=checks)](https://github.com/Ismael-Sallami/econometric-model/actions/workflows/ci.yml)
![license](https://img.shields.io/badge/license-MIT-4c1)

An OLS model that estimates body weight from habits and personal traits, and the three
diagnostics that decide whether its coefficients can be believed.

## Context

Coursework for **Econometría**, year 3 of the double degree in Computer Science and Business
Administration, University of Granada (2024-25).

## The problem

Given 2.111 records with seventeen variables about diet, activity, transport and family
history, estimate weight and say which factors actually matter.

The estimation is the easy half. A regression always returns coefficients; the work is
showing they mean something, which is where multicollinearity, heteroscedasticity and
autocorrelation come in: each one breaks a different assumption, and each one breaks the
model in a different way.

## The solution

**The model.** Ordinary least squares with `statsmodels`, weight as the dependent variable
and twelve regressors: age, height, family history of overweight, high-calorie food, vegetable
intake, main meals a day, eating between meals, water, physical activity, screen time,
alcohol and means of transport. The categorical ones are label-encoded before entering the
matrix.

**The diagnostics**, each with its own report in `docs/`:

| Check | What it looks for | How |
| --- | --- | --- |
| Multicollinearity | Regressors that carry the same information | Variance inflation factors and the correlation matrix |
| Heteroscedasticity | Residual variance that grows with the fitted value | Residual plots and formal tests |
| Autocorrelation | Residuals that carry information from the previous one | Durbin-Watson |

The preliminary model and the final one are separate documents on purpose: the second one
exists because the first one failed a diagnostic.

## Layout

```
src/model.py       the analysis, exported from Colab
src/model.ipynb    the same notebook, with its output
data/              the obesity dataset, 2.111 rows
docs/              the four reports, the presentation charts and the dataset description
tools/check.py     the check the CI runs
```

## Requirements

- Python 3.12 with `pandas`, `numpy`, `statsmodels`, `scipy` and `matplotlib`.

## Build and run

The script is a Colab export: it mounts Google Drive and reads the dataset from there, so it
does not run unchanged outside Colab. Opening the notebook is the direct way, and the data is
now in the repository:

```bash
jupyter lab src/model.ipynb        # the path to the dataset is data/obesity-dataset.csv
python3 tools/check.py             # what the CI runs
```

## Results

The fitted model, from `docs/econometric-model.pdf`:

| Measure | Value |
| --- | --- |
| R² | 0,576 |
| Adjusted R² | 0,572 |
| F statistic | 177,5 (p < 0,001) |

The model explains 57,6 % of the variation in weight, and the F test says the regressors are
jointly significant. The gap between R² and its adjusted version is small, which means the
twelve variables are pulling their weight rather than padding the fit.

The CI prints, on every push:

```
ok    src/model.py parses
ok    src/model.ipynb: 74 cells, 36 of them code
ok    data/obesity-dataset.csv: 2111 rows, 17 columns, all regressors present
```

## What I learned

- Explaining 57 % of a person's weight from their habits is a decent fit and a bad predictor.
  The interesting output is which coefficients survive the diagnostics, not the R².
- Label-encoding an ordinal variable such as "how often you eat between meals" imposes an
  order and a distance on it. It is a modelling choice made in one line of code and worth a
  paragraph of justification.
- **Limitations:**
  - The script cannot run outside Colab without editing the path it reads the dataset from.
    That path is left as it was handed in, and the notebook plus the data in `data/` are the
    way to reproduce the analysis.
  - The dataset is partly synthetic: it comes with the source, and the reports say so.
  - The reports and the comments are in Spanish.

## Author and licence

Ismael Sallami Moreno. Released under the MIT licence (see `LICENSE`).
