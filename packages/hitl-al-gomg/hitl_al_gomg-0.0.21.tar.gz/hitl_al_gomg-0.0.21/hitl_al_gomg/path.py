from pathlib import Path
import pandas as pd


def table():
    files = [
        [key, value, value.exists()]
        for key, value in globals().items()
        if isinstance(value, Path)
    ]
    return pd.DataFrame(files, columns=["variable", "path", "exists"])

# Path to chembl sample data:
chemspace = "hitl_al_gomg/scoring/chemspace"

# Path to trained Reinvent priors:
priors = "hitl_al_gomg/models/priors"

if __name__ == "__main__":
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(table())
