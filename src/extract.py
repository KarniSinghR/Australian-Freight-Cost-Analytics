"""
extract.py — Pull a single time series out of an ABS data-cube file.

All four ABS files share the same layout on their 'Data1' sheet:
  - rows 0-9  = metadata (description, unit, Series ID, etc.)
  - row 10+   = the actual data: dates in col 0, values in the series column
"""

import pandas as pd


def extract_abs_series(filepath, value_col, sheet="Data1", skip_meta=10):
    """Read one ABS series into a tidy ['quarter_date', 'value'] DataFrame."""
    raw = pd.read_excel(filepath, sheet_name=sheet, header=None)
    series_id = raw.iat[9, value_col]   # FIX: read ID from the value column

    data = raw.iloc[skip_meta:, [0, value_col]].copy()
    data.columns = ["quarter_date", "value"]
    data["quarter_date"] = pd.to_datetime(data["quarter_date"])
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["value"]).reset_index(drop=True)

    print(f"  Extracted {series_id}: {len(data)} rows, "
          f"{data['quarter_date'].min().date()} to {data['quarter_date'].max().date()}")
    return data


# Column index for each series, confirmed by Series ID.
SOURCES = {
    "freight": ("data/raw/freight_ppi.xlsx",    1),   # A2314058K
    "fuel":    ("data/raw/fuel_cpi.xlsx",        96),  # A2328636K
    "wage":    ("data/raw/wage_index.xlsx",      6),   # A2713849C
    "cpi":     ("data/raw/cpi_allgroups.xlsx",   9),   # A2325846C
}


def extract_all():
    """Extract all four series, return them in a dict keyed by name."""
    out = {}
    for name, (path, col) in SOURCES.items():
        print(f"Extracting {name}...")
        out[name] = extract_abs_series(path, value_col=col)
    return out


if __name__ == "__main__":
    series = extract_all()
    print("\n--- Preview of each ---")
    for name, df in series.items():
        print(f"\n{name.upper()}  (first 2, last 2):")
        print(df.head(2).to_string(index=False))
        print(df.tail(2).to_string(index=False))
