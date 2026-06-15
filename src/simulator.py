"""
simulator.py — Freight cost scenario simulator.

Built on the Stage-5 OLS regression (2-driver, lag-1 model):

    freight_change = INTERCEPT
                   + FUEL_COEF * fuel_change(t-1)
                   + WAGE_COEF * wage_change(t-1)

The regression works in INDEX-POINT changes. Users think in PERCENTAGES
("diesel +10%"), so we convert pct -> points using each series' current
level, run the model, then express the freight impact as both points and %.

Only fuel and wage are inputs: CPI was tested and dropped from the model
(no independent effect once fuel was controlled for — multicollinearity).
"""

# --- Regression coefficients (from Stage 5, model2: fuel + wage, lag 1) ---
INTERCEPT = -0.5599
FUEL_COEF = 0.1562
WAGE_COEF = 1.3579

# --- Current index levels (latest quarter, 2026-03-01) ---
CURRENT_FREIGHT = 137.3
CURRENT_FUEL = 105.79
CURRENT_WAGE = 160.4


def simulate(fuel_pct_change=0.0, wage_pct_change=0.0):
    """
    Predict next-quarter freight cost impact from % changes in the drivers.

    Parameters
    ----------
    fuel_pct_change : e.g. 10 means fuel rises 10%
    wage_pct_change : e.g. 2  means wages rise 2%

    Returns
    -------
    dict with the inputs, the predicted freight change in index points and %,
    and the resulting freight index level.
    """
    # Convert each % change into an index-POINT change (what the model expects)
    fuel_points = CURRENT_FUEL * (fuel_pct_change / 100.0)
    wage_points = CURRENT_WAGE * (wage_pct_change / 100.0)

    # Run the regression equation
    freight_point_change = (
        INTERCEPT
        + FUEL_COEF * fuel_points
        + WAGE_COEF * wage_points
    )

    # Express the result as a percentage of current freight, and a new level
    freight_pct_change = freight_point_change / CURRENT_FREIGHT * 100.0
    new_freight_level = CURRENT_FREIGHT + freight_point_change

    return {
        "fuel_pct_change": fuel_pct_change,
        "wage_pct_change": wage_pct_change,
        "freight_point_change": round(freight_point_change, 2),
        "freight_pct_change": round(freight_pct_change, 2),
        "new_freight_level": round(new_freight_level, 2),
    }


# Self-test: run `python src/simulator.py` to see a few scenarios.
if __name__ == "__main__":
    scenarios = [
        ("Diesel +10%, wages flat", 10, 0),
        ("Diesel +10%, wages +2%", 10, 2),
        ("Diesel -5%, wages +3%", -5, 3),
        ("Everything flat (baseline)", 0, 0),
    ]
    print(f"{'Scenario':30} {'Freight Δ pts':>14} {'Freight Δ %':>12} {'New level':>11}")
    print("-" * 70)
    for name, f, w in scenarios:
        r = simulate(f, w)
        print(f"{name:30} {r['freight_point_change']:>14} "
              f"{r['freight_pct_change']:>11}% {r['new_freight_level']:>11}")
