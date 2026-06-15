# 🚚 Australian Freight Cost Intelligence & Forecasting Platform

An end-to-end analytics platform that ingests Australian economic data, analyses
what drives road freight costs, forecasts future trends, and provides an
interactive scenario-planning tool — built with Python, PostgreSQL, and Streamlit.

**[🔗 Live Dashboard](ADD_YOUR_URL_HERE)** · **[📊 Insights & Recommendations](insights.md)**

---

## What this project does

Freight costs are a major, volatile expense for any logistics operation. This
platform answers four business questions:

1. **Why are freight costs rising?** — driver analysis (fuel, wages, inflation)
2. **Which factors matter most?** — correlation + regression modelling
3. **Where are costs heading?** — 12-month time-series forecast
4. **What if input costs change?** — interactive scenario simulator

## Key findings

- Road freight costs rose **~115% since 1997**, with a sharp surge in 2021–2023.
- **Fuel is the strongest driver, but with a one-quarter lag** — diesel shocks
  pass through to freight rates ~3 months later (matching Australian fuel
  surcharge review cycles).
- **Wages** are a significant secondary driver; **CPI** had no independent effect
  once fuel was accounted for (multicollinearity).
- Costs are forecast to rise **~5% over the next 12 months**.

## Tech stack

| Layer | Tools |
|---|---|
| Data ingestion (ETL) | Python, pandas |
| Database | PostgreSQL, SQLAlchemy |
| Analysis | pandas, statsmodels, scikit-learn |
| Forecasting | Prophet |
| Dashboard | Streamlit, matplotlib |
| Version control | Git / GitHub |

## Architecture
ABS / AIP data (xlsx)
│  extract.py  — pull series by ABS Series ID
▼
transform.py  — clean, align to quarterly, merge
│  load.py
▼
PostgreSQL  (staging tables → fact_freight_analysis)
│
├── EDA & driver analysis (notebooks, statsmodels)
├── Prophet forecast → forecast_results table
└── Streamlit dashboard (5 pages, live from DB)

## Data sources

All from the Australian Bureau of Statistics (ABS), quarterly 1997–2026:
- Road Freight Producer Price Index (target)
- Automotive Fuel CPI (diesel proxy)
- Wage Price Index
- All-Groups CPI

## Running it locally

```bash
# 1. Create environment
conda create -n freight python=3.11 -y
conda activate freight
pip install -r requirements.txt

# 2. Set up PostgreSQL, then build the database
psql -d freight_analytics -f sql/create_tables.sql

# 3. Run the ETL pipeline
python src/transform.py   # extract + transform
python src/load.py        # load into PostgreSQL

# 4. Launch the dashboard
streamlit run dashboard/app.py
```

## Repository structure
├── README.md
├── insights.md              # business findings & recommendations
├── requirements.txt
├── data/                    # raw (gitignored) + processed
├── sql/create_tables.sql    # database schema
├── src/
│   ├── db.py                # database connection
│   ├── extract.py           # pull series from ABS files
│   ├── transform.py         # clean + merge
│   ├── load.py              # load into PostgreSQL
│   └── simulator.py         # scenario engine (regression-based)
├── notebooks/               # EDA, driver analysis, forecasting
└── dashboard/app.py         # Streamlit dashboard

## Methodology notes

Driver analysis uses **first-differenced** data to avoid spurious correlation
from shared trends, and tests **lag structure** (fuel/wages affect freight one
quarter later). The forecast uses a trend-only Prophet model — yearly
seasonality was tested but rejected as overfitting on quarterly data. The model
explains ~33% of quarter-to-quarter variation; see [insights.md](insights.md)
for full limitations.
