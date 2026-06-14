"""
load.py — Load the clean master dataset into PostgreSQL.

Loads:
  - the master fact table  (fact_freight_analysis)
  - each staging table     (freight_cost_index, fuel_index, wage_index, cpi_index)

Reuses the shared engine from db.py.
"""

import pandas as pd
from db import engine


def load():
    master = pd.read_csv("data/processed/master_dataset.csv",
                         parse_dates=["quarter_date"])

    # --- Load the master fact table ---
    master.rename(columns={
        "freight": "freight_cost",
        "fuel": "fuel_index",
        "wage": "wage_index",
        "cpi": "cpi_index",
    }).to_sql("fact_freight_analysis", engine,
              if_exists="append", index=False)
    print(f"Loaded {len(master)} rows -> fact_freight_analysis")

    # --- Load each staging table (date + its own value column) ---
    staging = {
        "freight_cost_index": ("freight", "freight_cost"),
        "fuel_index":         ("fuel",    "fuel_index"),
        "wage_index":         ("wage",    "wage_index"),
        "cpi_index":          ("cpi",     "cpi_index"),
    }
    for table, (src_col, dest_col) in staging.items():
        df = master[["quarter_date", src_col]].rename(columns={src_col: dest_col})
        df.to_sql(table, engine, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows -> {table}")


if __name__ == "__main__":
    load()
    print("\nAll tables loaded.")
