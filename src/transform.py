"""
transform.py — Merge the four extracted series into one clean dataset.

Steps:
  1. Extract all four series (reuses extract.py).
  2. Rename each 'value' column to its proper name.
  3. Merge them on quarter_date with an inner join, so only quarters
     present in ALL four survive -> automatically trims to the common window.
  4. Save to data/processed/master_dataset.csv.
"""

import pandas as pd
from extract import extract_all


def transform():
    series = extract_all()   # dict: {'freight': df, 'fuel': df, ...}

    # Rename each df's 'value' column to the dataset's name, so columns are distinct.
    renamed = {}
    for name, df in series.items():
        renamed[name] = df.rename(columns={"value": name})

    # Start from freight, merge the rest onto it one by one, joining on date.
    master = renamed["freight"]
    for name in ["fuel", "wage", "cpi"]:
        master = master.merge(renamed[name], on="quarter_date", how="inner")

    # Sort by date and reset the row index.
    master = master.sort_values("quarter_date").reset_index(drop=True)

    print(f"\nMaster dataset: {len(master)} rows "
          f"({master['quarter_date'].min().date()} to {master['quarter_date'].max().date()})")
    print(f"Columns: {list(master.columns)}")
    print(f"Any missing values?\n{master.isna().sum()}")

    out_path = "data/processed/master_dataset.csv"
    master.to_csv(out_path, index=False)
    print(f"\nSaved -> {out_path}")
    return master


if __name__ == "__main__":
    master = transform()
    print("\n--- First 3 rows ---")
    print(master.head(3).to_string(index=False))
    print("\n--- Last 3 rows ---")
    print(master.tail(3).to_string(index=False))
