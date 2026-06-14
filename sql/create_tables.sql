-- ============================================================
-- Freight Cost Analytics — Table Schema
-- Staging tables (one per dataset) + master fact table
-- ============================================================

-- Drop existing tables so this script can be re-run cleanly
DROP TABLE IF EXISTS fact_freight_analysis;
DROP TABLE IF EXISTS freight_cost_index;
DROP TABLE IF EXISTS fuel_index;
DROP TABLE IF EXISTS wage_index;
DROP TABLE IF EXISTS cpi_index;

-- ---------- STAGING TABLES ----------

CREATE TABLE freight_cost_index (
    quarter_date  DATE PRIMARY KEY,
    freight_cost  NUMERIC(10,2) NOT NULL
);

CREATE TABLE fuel_index (
    quarter_date  DATE PRIMARY KEY,
    fuel_index    NUMERIC(10,2) NOT NULL
);

CREATE TABLE wage_index (
    quarter_date  DATE PRIMARY KEY,
    wage_index    NUMERIC(10,2) NOT NULL
);

CREATE TABLE cpi_index (
    quarter_date  DATE PRIMARY KEY,
    cpi_index     NUMERIC(10,2) NOT NULL
);

-- ---------- MASTER FACT TABLE ----------

CREATE TABLE fact_freight_analysis (
    quarter_date  DATE PRIMARY KEY,
    freight_cost  NUMERIC(10,2),
    fuel_index    NUMERIC(10,2),
    wage_index    NUMERIC(10,2),
    cpi_index     NUMERIC(10,2)
);
