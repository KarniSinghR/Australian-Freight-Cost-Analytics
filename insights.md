# Australian Freight Cost Intelligence — Key Insights & Recommendations

## Executive Summary

Australian road freight costs have risen ~115% since 1997 (index 64 → 137),
with the sharpest acceleration during 2021–2023. Analysis of fuel prices,
wages, and general inflation shows that **fuel and wage costs are the
significant drivers of freight cost movements, and both affect freight with a
one-quarter lag**. A 12-month forecast projects continued moderate growth of
roughly 5%.

> **Industry context (2026):** This analysis is especially timely given the 2026
> Australian diesel price spike, which prompted the Fair Work Commission's
> Road Transport Contractual Chain Order mandating fuel cost recovery in freight
> contracts — underscoring that fuel pass-through to freight rates is a live,
> material issue for the sector.

---

## Insight 1 — Freight costs have more than doubled, with a recent surge

The road freight cost index rose from 64 (1997) to 137 (2026). Growth was
steady until 2020, then surged sharply through 2021–2023 — coinciding with
post-COVID supply-chain disruption and the 2022 global fuel price spike — before
stabilising at a higher plateau.

**Business implication:** the post-2020 cost base is structurally higher and has
not reverted. Budgets built on pre-2020 freight rates are materially understated.

---

## Insight 2 — Fuel is the strongest driver, but its effect is delayed

Quarter-to-quarter, fuel price changes show little *immediate* relationship with
freight costs (correlation 0.14). However, when fuel changes are lagged one
quarter, the relationship more than triples (correlation 0.50) — the strongest
single relationship in the analysis. Regression confirms fuel as the most
statistically robust driver (p < 0.001).

**Why:** Australian freight fuel surcharges typically reset on monthly
(increasingly fortnightly) review cycles benchmarked to the AIP weekly terminal
gate diesel price. This contractual reset cadence is the real-world mechanism
behind the one-quarter statistical lag — a diesel price shock takes roughly
three months to fully pass through to freight rates.

**Business implication:** fuel price movements are a leading indicator. A diesel
spike this quarter signals a freight cost rise next quarter — giving roughly one
quarter of lead time to act.

---

## Insight 3 — Wages drive the long-run trend; CPI adds no independent signal

Wage growth is a significant secondary driver (p = 0.001), also at a one-quarter
lag. General inflation (CPI) appeared correlated with freight but had **no
independent predictive effect** once fuel was accounted for — fuel and CPI
overlap heavily (they share fuel as a component), so CPI added nothing the model
didn't already capture, and was excluded.

**Business implication:** monitoring fuel and wages is sufficient; tracking
headline CPI separately as a freight predictor is redundant.

---

## Insight 4 — Costs are projected to keep rising ~5% over the next year

A Prophet time-series forecast projects the freight index rising from 137 to
~144 over the next four quarters (~5%), continuing the long-run trend without
extrapolating the 2021–2023 shock. The 80% confidence band spans roughly
±2.5 index points.

**Business implication:** plan for mid-single-digit freight cost inflation in the
coming year as the baseline scenario.

---

## Recommendations

1. **Treat diesel prices as an early-warning indicator.** Build a simple monthly
   fuel-price watch referenced to the AIP weekly terminal gate diesel price; a
   sustained diesel rise this quarter implies freight cost pressure next quarter,
   allowing pre-emptive budget and contract action.

2. **Tighten fuel surcharge review cycles.** Standard Australian practice
   nominates a base freight rate plus a fuel levy that adjusts as a referenced
   diesel index moves. In volatile periods, shortening the review cycle from
   monthly to fortnightly — and ensuring it adjusts symmetrically up and down —
   reduces the cost-absorption window for carriers and improves rate
   predictability for shippers.

3. **Lock longer-term contracts ahead of forecast rises.** With ~5% projected
   growth, securing rates now hedges against the expected increase.

4. **Budget for a structurally higher cost base.** Post-2020 costs have not
   reverted; forecasting off pre-2020 baselines will understate spend.

---

## Methodology & Limitations

- **Data:** ABS Producer Price Index (road freight), ABS Automotive Fuel CPI
  (diesel proxy), ABS Wage Price Index, ABS All-Groups CPI. Quarterly,
  1997–2026 (115 observations).
- **Methods:** correlation and lag analysis, OLS regression on differenced
  (quarter-on-quarter) data to remove spurious shared-trend correlation, and
  Prophet for forecasting.
- **Limitations:** The model explains ~33% of quarter-to-quarter freight
  variation — meaningful but partial; much short-run movement comes from factors
  not modelled (contract timing, competition, one-off shocks). The fuel measure
  is the ABS Automotive Fuel index (petrol-weighted; diesel ~10% of the class),
  used as a proxy for clean quarterly alignment. The forecast is built on the
  long-run historical trend and does not fully capture the 2026 diesel price
  spike, which falls largely outside the modelled window; forecasts assume
  historical patterns persist and cannot anticipate future shocks.
