"""
app.py — Australian Freight Cost Intelligence Dashboard (Streamlit).
Run with:  streamlit run dashboard/app.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Freight Cost Intelligence", page_icon="🚚", layout="wide")

# --- Data loading (cached so it doesn't re-query on every interaction) ---
@st.cache_data
def load_data():
    engine = create_engine("postgresql://karnisinghrathore@localhost:5432/freight_analytics")
    facts = pd.read_sql("SELECT * FROM fact_freight_analysis ORDER BY quarter_date", engine)
    forecast = pd.read_sql("SELECT * FROM forecast_results ORDER BY quarter_date", engine)
    facts["quarter_date"] = pd.to_datetime(facts["quarter_date"])
    forecast["quarter_date"] = pd.to_datetime(forecast["quarter_date"])
    return facts, forecast

facts, forecast = load_data()

# --- Sidebar navigation ---
st.sidebar.title("🚚 Freight Cost Intelligence")
page = st.sidebar.radio(
    "Navigate",
    ["Executive Summary", "Cost Trends", "Cost Drivers", "Forecasting", "Scenario Simulator"],
)

# ============================================================
if page == "Executive Summary":
    st.title("Executive Summary")
    st.caption("Australian road freight cost intelligence — 1997 to 2026")

    # Compute KPIs
    current_freight = facts["freight_cost"].iloc[-1]
    year_ago_freight = facts["freight_cost"].iloc[-5]   # 4 quarters back
    yoy_change = (current_freight - year_ago_freight) / year_ago_freight * 100

    future = forecast[forecast["is_future"]]
    forecast_end = future["forecast"].iloc[-1]
    forecast_change = (forecast_end - current_freight) / current_freight * 100

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Freight Index", f"{current_freight:.1f}")
    c2.metric("Past 12 Months", f"{yoy_change:+.1f}%")
    c3.metric("Forecast (next 12 mo)", f"{forecast_change:+.1f}%")
    c4.metric("Main Cost Driver", "Fuel", help="Lagged fuel is the strongest driver (p<0.001)")

    st.divider()

    # Hero chart: freight history
    st.subheader("Freight Cost Index Over Time")
    chart_df = facts.set_index("quarter_date")[["freight_cost"]]
    st.line_chart(chart_df, height=350)

# ============================================================
elif page == "Cost Trends":
    st.title("Cost Trends")
    st.caption("How freight cost and its drivers have moved since 1997")

    view = st.radio("View", ["Raw index values", "Normalised (1997 = 100)"],
                    horizontal=True)

    plot_df = facts.set_index("quarter_date")[
        ["freight_cost", "fuel_index", "wage_index", "cpi_index"]
    ].copy()
    plot_df.columns = ["Freight", "Fuel", "Wages", "CPI"]

    if view == "Normalised (1997 = 100)":
        plot_df = plot_df / plot_df.iloc[0] * 100
        st.caption("All series rebased to 100 at their starting point, "
                   "so growth is directly comparable.")

    st.line_chart(plot_df, height=420)

    with st.expander("What this shows"):
        st.write(
            "Freight cost roughly tracks wages and CPI over the long run, "
            "while fuel is far more volatile. The normalised view reveals that "
            "fuel grew the most overall but transmits to freight with a lag "
            "(explored on the Cost Drivers page)."
        )

elif page == "Cost Drivers":
    st.title("Cost Drivers")
    st.caption("What actually moves freight costs — and when")

    # Key finding callout
    st.success(
        "**Key finding:** Freight costs respond to fuel and wage changes with a "
        "**one-quarter lag**. Fuel is the strongest driver (p < 0.001); wages "
        "contribute significantly (p = 0.001). General inflation (CPI) had no "
        "independent effect once fuel was accounted for."
    )

    col1, col2 = st.columns(2)

    # Lag profile: correlation of freight change vs each driver at lags 0-4
    with col1:
        st.subheader("Effect arrives with a 1-quarter lag")
        chg = facts[["freight_cost", "fuel_index", "wage_index", "cpi_index"]].diff()
        lag_data = {}
        for col, label in [("fuel_index", "Fuel"), ("wage_index", "Wages"), ("cpi_index", "CPI")]:
            lag_data[label] = [chg["freight_cost"].corr(chg[col].shift(lag)) for lag in range(5)]
        lag_df = pd.DataFrame(lag_data, index=[f"Lag {i}" for i in range(5)])
        st.bar_chart(lag_df, height=320)
        st.caption("Correlation of freight change vs each driver, shifted 0–4 quarters. "
                   "All peak at lag 1.")

    # Regression results table
    with col2:
        st.subheader("Regression model (final)")
        reg = pd.DataFrame({
            "Driver": ["Fuel (lag 1)", "Wages (lag 1)", "Intercept"],
            "Coefficient": [0.156, 1.358, -0.560],
            "p-value": ["< 0.001", "0.001", "0.099"],
            "Significant?": ["Yes", "Yes", "—"],
        })
        st.dataframe(reg, hide_index=True, use_container_width=True)
        st.metric("Model R²", "0.33", help="Explains ~33% of quarter-to-quarter freight movement")
        st.caption("CPI excluded — redundant with fuel (multicollinearity, r = 0.57).")

elif page == "Forecasting":
    st.title("Forecasting")
    st.caption("12-month freight cost projection (Prophet, trend-only model)")

    current = facts["freight_cost"].iloc[-1]
    fut = forecast[forecast["is_future"]]
    end_val = fut["forecast"].iloc[-1]
    pct = (end_val - current) / current * 100

    k1, k2, k3 = st.columns(3)
    k1.metric("Current Index", f"{current:.1f}")
    k2.metric("Forecast (Mar 2027)", f"{end_val:.1f}")
    k3.metric("Projected Change", f"{pct:+.1f}%")

    st.divider()

    # Build a single chart frame: actuals + forecast + band
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(11, 5))

    last_actual = facts["quarter_date"].max()
    fc_hist = forecast[~forecast["is_future"]]

    ax.plot(facts["quarter_date"], facts["freight_cost"],
            color="#1f4e79", linewidth=1.8, label="Actual")
    ax.plot(fut["quarter_date"], fut["forecast"],
            color="#c0392b", linewidth=2.5, label="Forecast")
    ax.fill_between(fut["quarter_date"], fut["forecast_lower"], fut["forecast_upper"],
                    color="#c0392b", alpha=0.2, label="80% confidence")
    ax.axvline(last_actual, color="gray", linestyle="--", alpha=0.6)
    ax.set_xlabel("Year"); ax.set_ylabel("Freight Cost Index")
    ax.legend(loc="upper left"); ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    with st.expander("About this forecast"):
        st.write(
            "Projected with Facebook Prophet on 115 quarters of history. "
            "Yearly seasonality was tested but rejected — with only 4 data points "
            "per year it overfit, producing spurious within-year swings. The final "
            "trend-only model projects steady growth of about "
            f"{pct:.1f}% over the next 12 months. The shaded band is the 80% "
            "confidence interval, widening with the forecast horizon."
        )

elif page == "Scenario Simulator":
    import simulator

    st.title("Scenario Simulator")
    st.caption("What happens to freight costs if input costs change next quarter?")

    st.write(
        "Adjust the sliders to model cost shocks. Predictions use the regression "
        "model (fuel + wages, one-quarter lag). Fuel can swing widely quarter to "
        "quarter; wages move slowly, so its range is deliberately narrow."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Inputs")
        fuel_change = st.slider("Diesel / fuel change (%)", -20.0, 20.0, 10.0, 0.5)
        wage_change = st.slider("Wage change (%)", -1.0, 3.0, 0.0, 0.1)
        if st.button("Reset to baseline"):
            st.rerun()

    result = simulator.simulate(fuel_change, wage_change)

    with col2:
        st.subheader("Predicted impact (next quarter)")
        st.metric("Freight cost change", f"{result['freight_pct_change']:+.2f}%",
                  delta=f"{result['freight_point_change']:+.2f} index pts")
        st.metric("New freight index", f"{result['new_freight_level']:.1f}",
                  help="Current level is 137.3")

        # Contribution breakdown
        fuel_contrib = simulator.FUEL_COEF * (simulator.CURRENT_FUEL * fuel_change / 100)
        wage_contrib = simulator.WAGE_COEF * (simulator.CURRENT_WAGE * wage_change / 100)
        contrib = pd.DataFrame({
            "Source": ["Fuel", "Wages", "Baseline drift"],
            "Index points": [round(fuel_contrib, 2), round(wage_contrib, 2),
                             simulator.INTERCEPT],
        })
        st.bar_chart(contrib.set_index("Source"), height=240)

    st.caption(
        "⚠️ Model explains ~33% of quarterly freight variation and predicts one "
        "quarter ahead. Treat as directional guidance, not a precise forecast."
    )
