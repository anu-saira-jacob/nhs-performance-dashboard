-- =========================================================================================================================================================
-- This SQL script defines the relational schema for the NHS RTT data ingestion and visualisation pipeline. It includes three primary tables:

-- - `org_info`: Stores NHS provider metadata, location, and administrative geography.
-- - `geo_boundaries`: Holds spatial geometries for NHS Regions and ICBs with both ONS and NHS codes.
-- - `rtt_data`: Main fact table for monthly RTT performance statistics, normalized for dashboard queries.

-- All tables use `CREATE TABLE IF NOT EXISTS` to support idempotent execution. Indexes are included to enhance filtering, joins, and geospatial operations.
-- =========================================================================================================================================================

-- ===============================
-- 📦 Database Schema for NHS RTT Dashboard
-- ===============================

-- ORG INFO TABLE: Stores provider metadata and geolocation
CREATE TABLE IF NOT EXISTS org_info (
  org_code TEXT PRIMARY KEY,
  org_name TEXT,
  org_type TEXT DEFAULT 'Provider',
  region_code TEXT,
  health_geography_code TEXT, --ICB code
  postcode TEXT,
  latitude NUMERIC,
  longitude NUMERIC,
  open_date DATE,
  close_date DATE,
  geocode_source TEXT
);


-- GEO BOUNDARIES TABLE: Stores geometric boundaries for regions and ICBs
CREATE TABLE IF NOT EXISTS geo_boundaries (
    ons_code TEXT PRIMARY KEY,               -- ONS code
    nhs_code TEXT,                           -- NHS code (added for consistency)
    name TEXT,                               -- Human-readable name
    geo_level TEXT NOT NULL,                 -- 'Region', 'ICB', etc.
    geometry GEOMETRY(Geometry, 4326)        -- Spatial geometry
);

-- Indexes for spatial and categorical queries
CREATE INDEX IF NOT EXISTS idx_geo_geom ON geo_boundaries USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_geo_level ON geo_boundaries (geo_level);

-- RTT DATA TABLE: Main fact table with RTT statistics
CREATE TABLE IF NOT EXISTS rtt_data (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    pathway_type TEXT NOT NULL,              -- 'Admitted', 'Incomplete', etc.
    org_code TEXT NOT NULL, 
    org_name TEXT,
    geo_level TEXT,                          -- 'Provider', 'ICB', 'Region', 'National
    region_code TEXT,
    treatment_function_code TEXT NOT NULL,
    treatment_function TEXT NOT NULL,        -- e.g., 'Trauma & Orthopaedics'
    metric TEXT NOT NULL,                    -- e.g., 'median_wait'
    value NUMERIC                            -- Metric value
);

-- Indexes for performance tuning
CREATE UNIQUE INDEX IF NOT EXISTS ux_rtt_metric
    ON rtt_data (year, month, org_code, treatment_function_code, pathway_type, metric);
CREATE INDEX IF NOT EXISTS idx_rtt_time ON rtt_data (year, month);
CREATE INDEX IF NOT EXISTS idx_rtt_org ON rtt_data (org_code);
CREATE INDEX IF NOT EXISTS idx_rtt_pathway ON rtt_data (pathway_type);
CREATE INDEX IF NOT EXISTS idx_rtt_geo_level ON rtt_data (geo_level);
CREATE INDEX IF NOT EXISTS idx_rtt_treatment_code ON rtt_data (treatment_function_code);

