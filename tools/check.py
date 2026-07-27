#!/usr/bin/env python3
"""Check the model script, the notebook and the dataset.

The script is a Colab export: it mounts Google Drive and reads the dataset from
there, so it cannot run unchanged outside Colab. What is checked here is that its
code parses, that the notebook is well formed, and that the dataset in `data/` is
the one the model expects, with the columns it uses.

    python3 tools/check.py

@author Ismael Sallami Moreno
"""

import ast
import csv
import json
import pathlib
import sys

SCRIPT = pathlib.Path("src/model.py")
NOTEBOOK = pathlib.Path("src/model.ipynb")
DATASET = pathlib.Path("data/obesity-dataset.csv")

# The dependent variable and the twelve regressors the report works with.
EXPECTED_COLUMNS = [
    "Weight", "Age", "Height", "family_history_with_overweight", "FAVC", "FCVC",
    "NCP", "CAEC", "CH2O", "FAF", "TUE", "CALC", "MTRANS",
]

EXPECTED_ROWS = 2111


def check_script() -> bool:
    try:
        ast.parse(SCRIPT.read_text(encoding="utf-8"))
    except SyntaxError as error:
        print(f"FAIL  {SCRIPT}: line {error.lineno}: {error.msg}")
        return False
    print(f"ok    {SCRIPT} parses")
    return True


def check_notebook() -> bool:
    try:
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"FAIL  {NOTEBOOK}: not valid JSON, {error}")
        return False
    cells = notebook.get("cells", [])
    code = [c for c in cells if c.get("cell_type") == "code"]
    if not code:
        print(f"FAIL  {NOTEBOOK}: no code cells")
        return False
    print(f"ok    {NOTEBOOK}: {len(cells)} cells, {len(code)} of them code")
    return True


def check_dataset() -> bool:
    with DATASET.open(encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = sum(1 for _ in reader)

    missing = [column for column in EXPECTED_COLUMNS if column not in header]
    if missing:
        print(f"FAIL  {DATASET}: missing columns {missing}")
        return False
    if rows != EXPECTED_ROWS:
        print(f"FAIL  {DATASET}: {rows} rows, expected {EXPECTED_ROWS}")
        return False
    print(f"ok    {DATASET}: {rows} rows, {len(header)} columns, all regressors present")
    return True


def main() -> int:
    results = [check_script(), check_notebook(), check_dataset()]
    if all(results):
        print("\nscript, notebook and dataset are consistent")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
