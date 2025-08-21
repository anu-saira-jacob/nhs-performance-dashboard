# queries.py
from db import fetch_df



# ---------INCOMPLETE PATHWAY QUERIES----------------------------------

def get_incomplete_trend(metric="Average (median) waiting time (in weeks)", geo_level="National", nhs_code = None):
    query = """
        SELECT year, month, value
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = %(geo_level)s
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
    """

    params = {"metric": metric, "geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY year, month;"

    return fetch_df(query, params)


def get_all_treatment_functions(geo_level="National", nhs_code=None):
    query = """
        SELECT DISTINCT treatment_function_code, treatment_function
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = %(geo_level)s
    """
    params = {"geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY treatment_function;"
    return fetch_df(query, params=params) 


def get_monthly_treatment_comparison(year, month, treatment_codes, geo_level="National", nhs_code=None, metric="Average (median) waiting time (in weeks)"):
    placeholders = ", ".join(["%s"] * len(treatment_codes))
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = %s
          AND metric = %s
          AND year = %s AND month = %s
          AND treatment_function_code IN ({placeholders})
    """
    params = [geo_level, metric, year, month] + treatment_codes

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += " ORDER BY treatment_function;"
    return fetch_df(query, tuple(params))


def get_top_or_bottom_treatments(year, month, order="desc",  geo_level="National", nhs_code=None, limit=5, metric="Average (median) waiting time (in weeks)"):
    direction = "DESC" if order == "desc" else "ASC"
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = %s
          AND metric = %s
          AND treatment_function_code != 'C_999'
          AND year = %s AND month = %s
    """
    params = [geo_level, metric, year, month]

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += f" ORDER BY value {direction} LIMIT {limit};"
    return fetch_df(query, tuple(params))


# ------------------------------- ADMIITTED PATHWAY QUERIES -------------------------------

def get_admitted_trend(metric="Average (median) waiting time (in weeks)", geo_level="National", nhs_code=None):
    query = """
        SELECT year, month, value
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = %(geo_level)s
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
    """
    params = {"metric": metric, "geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY year, month;"

    return fetch_df(query, params)



def get_all_treatment_functions_admitted(geo_level="National", nhs_code=None):
    query = """
        SELECT DISTINCT treatment_function_code, treatment_function
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = %(geo_level)s
    """
    params = {"geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY treatment_function;"
    return fetch_df(query, params=params)



def get_monthly_treatment_comparison_admitted(year, month, treatment_codes, geo_level="National", nhs_code=None, metric="Average (median) waiting time (in weeks)"):
    placeholders = ", ".join(["%s"] * len(treatment_codes))
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = %s
          AND metric = %s
          AND year = %s AND month = %s
          AND treatment_function_code IN ({placeholders})
    """
    params = [geo_level, metric, year, month] + treatment_codes

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += " ORDER BY treatment_function;"
    return fetch_df(query, tuple(params))


def get_top_or_bottom_treatments_admitted(year, month, order="desc",  geo_level="National", nhs_code=None, limit=5, metric="Average (median) waiting time (in weeks)"):
    direction = "DESC" if order == "desc" else "ASC"
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = %s
          AND metric = %s
          AND treatment_function_code != 'C_999'
          AND year = %s AND month = %s
    """
    params = [geo_level, metric, year, month]

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += f" ORDER BY value {direction} LIMIT {limit};"
    return fetch_df(query, tuple(params))



# -------------------------------NON-ADMIITTED PATHWAY QUERIES -------------------------------

def get_non_admitted_trend(metric="Average (median) waiting time (in weeks)", geo_level="National", nhs_code = None):
    query = """
        SELECT year, month, value
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = %(geo_level)s
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
    """
    params = {"metric": metric, "geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY year, month;"

    return fetch_df(query, params)


def get_all_treatment_functions_non_admitted(geo_level="National", nhs_code=None):
    query = """
        SELECT DISTINCT treatment_function_code, treatment_function
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = %(geo_level)s
    """
    params = {"geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY treatment_function;"
    return fetch_df(query, params=params) 


def get_monthly_treatment_comparison_non_admitted(year, month, treatment_codes, geo_level="National", nhs_code=None, metric="Average (median) waiting time (in weeks)"):
    placeholders = ", ".join(["%s"] * len(treatment_codes))
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = %s
          AND metric = %s
          AND year = %s AND month = %s
          AND treatment_function_code IN ({placeholders})
    """

    params = [geo_level, metric, year, month] + treatment_codes

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += " ORDER BY treatment_function;"
    return fetch_df(query, tuple(params))
    

def get_top_or_bottom_treatments_non_admitted(year, month, order="desc",  geo_level="National", nhs_code=None, limit=5, metric="Average (median) waiting time (in weeks)"):
    direction = "DESC" if order == "desc" else "ASC"
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = %s
          AND metric = %s
          AND treatment_function_code != 'C_999'
          AND year = %s AND month = %s
    """
    params = [geo_level, metric, year, month]

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += f" ORDER BY value {direction} LIMIT {limit};"
    return fetch_df(query, tuple(params))


# -------------------------------NEW REFERRALS PATHWAY QUERIES -------------------------------

def get_new_referrals_trend(metric="Number of new RTT clock starts during the month", geo_level="National", nhs_code = None):
    query = """
        SELECT year, month, value
        FROM rtt_data
        WHERE pathway_type = 'New'
          AND geo_level = %(geo_level)s
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
    """
    params = {"metric": metric, "geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY year, month;"

    return fetch_df(query, params)

def get_all_treatment_functions_new(geo_level="National", nhs_code=None):
    query = """
        SELECT DISTINCT treatment_function_code, treatment_function
        FROM rtt_data
        WHERE pathway_type = 'New'
        AND geo_level = %(geo_level)s
    """
    params = {"geo_level": geo_level}

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %(nhs_code)s"
        params["nhs_code"] = nhs_code

    query += " ORDER BY treatment_function;"
    return fetch_df(query, params=params)


def get_monthly_treatment_comparison_new(year, month, treatment_codes, geo_level="National", nhs_code=None, metric='Number of new RTT clock starts during the month'):
    placeholders = ", ".join(["%s"] * len(treatment_codes))
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'New'
          AND geo_level = %s
          AND metric = %s
          AND year = %s AND month = %s
          AND treatment_function_code IN ({placeholders})
    """
    params = [geo_level, metric, year, month] + treatment_codes

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += " ORDER BY treatment_function;"
    return fetch_df(query, tuple(params))



def get_top_or_bottom_treatments_new(year, month, order="desc",  geo_level="National", nhs_code=None, limit=5, metric="Number of new RTT clock starts during the month"):
    direction = "DESC" if order == "desc" else "ASC"
    query = f"""
        SELECT treatment_function, value
        FROM rtt_data
        WHERE pathway_type = 'New'
          AND geo_level = %s
          AND metric = %s
          AND treatment_function_code != 'C_999'
          AND year = %s AND month = %s
    """
    params = [geo_level, metric, year, month]

    if geo_level == "Region" and nhs_code:
        query += " AND org_code = %s"
        params.append(nhs_code)

    query += f" ORDER BY value {direction} LIMIT {limit};"
    return fetch_df(query, tuple(params))


#-------------------- INTERACTIVE MAP QUERIES----------

def get_all_regions():
    query = """
        SELECT DISTINCT nhs_code AS value, name AS label
        FROM geo_boundaries
        WHERE geo_level = 'Region'
        ORDER BY name;
    """
    return fetch_df(query)


def get_geo_boundaries():
    query = """
        SELECT nhs_code, name, ST_AsGeoJSON(geometry)::json AS geojson
        FROM geo_boundaries
        WHERE geo_level = 'Region';
    """
    return fetch_df(query)


from functools import lru_cache
import geopandas as gpd
import json
from db import engine


@lru_cache(maxsize=1)
def get_all_regions_geojson():
    gdf = gpd.read_postgis(
        "SELECT name, nhs_code, geometry FROM geo_boundaries WHERE geo_level = 'Region';",
        con=engine,
        geom_col="geometry"
    )

    # Compute centroid for each geometry
    gdf["centroid"] = gdf.geometry.centroid

    features = [
        {
            "type": "Feature",
            "geometry": json.loads(gpd.GeoSeries([row["geometry"]]).to_json())["features"][0]["geometry"],
            "properties": {
                "name": row["name"],
                "nhs_code": row["nhs_code"],
                "tooltip": row["name"],
                "center_lat": row["centroid"].y,
                "center_lon": row["centroid"].x
            }
        }
        for _, row in gdf.iterrows()
    ]

    return {"type": "FeatureCollection", "features": features}


# ----QUERIES FOR DEPRIVATION AND ICB LINK INCOMPLETE ---------------


def get_icb_rtt_for_region_incomplete(year, month, metric, region_code):
    """
    Returns ICB-level RTT values for the selected month/metric/region
    for the Incomplete pathway (Total treatment_function_code = C_999).
    Columns returned: org_code, org_name, value (sorted desc).
    """
    query = """
        SELECT org_code, org_name, value
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = 'ICB'
          AND treatment_function_code = 'C_999'
          AND region_code = %(region_code)s
          AND year = %(year)s AND month = %(month)s
          AND metric = %(metric)s
        ORDER BY value DESC, org_name ASC;
    """
    params = {
        "region_code": region_code,
        "year": year,
        "month": month,
        "metric": metric,
    }
    return fetch_df(query, params)

# ----QUERIES FOR DEPRIVATION AND ICB LINK ADMITTED ---------------


def get_icb_rtt_for_region_admitted(year, month, metric, region_code):
    """
    Returns ICB-level RTT values for the selected month/metric/region
    for the Incomplete pathway (Total treatment_function_code = C_999).
    Columns returned: org_code, org_name, value (sorted desc).
    """
    query = """
        SELECT org_code, org_name, value
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = 'ICB'
          AND treatment_function_code = 'C_999'
          AND region_code = %(region_code)s
          AND year = %(year)s AND month = %(month)s
          AND metric = %(metric)s
        ORDER BY value DESC, org_name ASC;
    """
    params = {
        "region_code": region_code,
        "year": year,
        "month": month,
        "metric": metric,
    }
    return fetch_df(query, params)

# ----QUERIES FOR DEPRIVATION AND ICB LINK NON ADMITTED ---------------


def get_icb_rtt_for_region_non_admitted(year, month, metric, region_code):
    """
    Returns ICB-level RTT values for the selected month/metric/region
    for the Incomplete pathway (Total treatment_function_code = C_999).
    Columns returned: org_code, org_name, value (sorted desc).
    """
    query = """
        SELECT org_code, org_name, value
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = 'ICB'
          AND treatment_function_code = 'C_999'
          AND region_code = %(region_code)s
          AND year = %(year)s AND month = %(month)s
          AND metric = %(metric)s
        ORDER BY value DESC, org_name ASC;
    """
    params = {
        "region_code": region_code,
        "year": year,
        "month": month,
        "metric": metric,
    }
    return fetch_df(query, params)

# ----QUERIES FOR DEPRIVATION AND ICB LINK NEW ---------------


def get_icb_rtt_for_region_new(year, month, metric, region_code):
    """
    Returns ICB-level RTT values for the selected month/metric/region
    for the Incomplete pathway (Total treatment_function_code = C_999).
    Columns returned: org_code, org_name, value (sorted desc).
    """
    query = """
        SELECT org_code, org_name, value
        FROM rtt_data
        WHERE pathway_type = 'New'
          AND geo_level = 'ICB'
          AND treatment_function_code = 'C_999'
          AND region_code = %(region_code)s
          AND year = %(year)s AND month = %(month)s
          AND metric = %(metric)s
        ORDER BY value DESC, org_name ASC;
    """
    params = {
        "region_code": region_code,
        "year": year,
        "month": month,
        "metric": metric,
    }
    return fetch_df(query, params)



# REGION MAP QUERIES --- COMMON ------
@lru_cache(maxsize=64)
def get_ccg_imd_geojson(region_code: str):
    """
    CCG polygons for a region with IMD attributes (geom_100m).
    imd_quintile_ccg from DB is 1=least deprived, 5=most → invert to 1=most deprived, 5=least.
    Properties: ccg_code, ccg_name, icb_code, icb_name, imd_quintile (inverted), imd_avg_score
    """
    sql = """
        SELECT
            ccg19cd,
            ccg19nm,
            icb_code,
            icb_name,
            imd_quintile_ccg,
            imd_avg_score,
            geom_100m AS geometry
        FROM ccg_imd_2019
        WHERE nhser19cdh = %(region_code)s
          AND geom_100m IS NOT NULL
    """
    gdf = gpd.read_postgis(sql, con=engine, geom_col="geometry", params={"region_code": region_code})

    features = []
    for _, row in gdf.iterrows():
        inverted_val = None
        if row["imd_quintile_ccg"] is not None:
            inverted_val = 6 - int(row["imd_quintile_ccg"])  # 1 ↔ 5, 2 ↔ 4, etc.

        geom_json = json.loads(gpd.GeoSeries([row["geometry"]]).to_json())["features"][0]["geometry"]
        features.append({
            "type": "Feature",
            "geometry": geom_json,
            "properties": {
                "ccg_code": row["ccg19cd"],
                "ccg_name": row["ccg19nm"],
                "icb_code": row["icb_code"],
                "icb_name": row["icb_name"],
                "imd_quintile": inverted_val,
                "imd_avg_score": float(row["imd_avg_score"]) if row["imd_avg_score"] is not None else None,
            }
        })

    return {"type": "FeatureCollection", "features": features}


@lru_cache(maxsize=128)
def get_region_bounds(region_code: str):
    """
    Returns Leaflet bounds [[south, west], [north, east]] for a Region
    from geo_boundaries (EPSG:4326). Returns None if not found.
    """
    sql = """
        SELECT geometry
        FROM geo_boundaries
        WHERE geo_level = 'Region'
          AND nhs_code = %(region_code)s
        LIMIT 1
    """
    gdf = gpd.read_postgis(sql, con=engine, geom_col="geometry", params={"region_code": region_code})
    if gdf.empty:
        return None

    minx, miny, maxx, maxy = gdf.total_bounds  # lon/lat order
    return [[float(miny), float(minx)], [float(maxy), float(maxx)]]

@lru_cache(maxsize=64)
def get_icb_boundaries_geojson(region_code: str):
    """
    Returns ICB boundary GeoJSON for ICBs present in the given region.
    Properties include: icb_code, icb_name, icb_label (compact), center [lat, lon], bounds [[S,W],[N,E]].
    """
    #  1) Find distinct ICB codes present in the region
    icb_sql = """
        SELECT DISTINCT org_code AS icb_code
            FROM rtt_data
            WHERE geo_level = 'ICB'
            AND region_code = %(region_code)s
            AND org_code IS NOT NULL
            ORDER BY org_code;
    """
    
    icb_df = fetch_df(icb_sql, {"region_code": region_code})
    if icb_df is None or icb_df.empty:
        return {"type": "FeatureCollection", "features": []}

    icb_codes = icb_df["icb_code"].dropna().unique().tolist()
    if not icb_codes:
        return {"type": "FeatureCollection", "features": []}

    # 2) Pull their geometries from geo_boundaries
    geom_sql = """
        SELECT nhs_code AS icb_code, name AS icb_name, geometry
        FROM geo_boundaries
        WHERE geo_level = 'ICB'
          AND nhs_code = ANY(%(codes)s)
    """
    gdf = gpd.read_postgis(geom_sql, con=engine, geom_col="geometry", params={"codes": icb_codes})
    if gdf.empty:
        return {"type": "FeatureCollection", "features": []}

    # Compute centers/bounds per feature
    gdf["centroid"] = gdf.geometry.centroid   # CRS is EPSG:4326; acceptable for display centroids
    bounds_df = gdf.bounds  # xmin, ymin, xmax, ymax

    features = []
    for idx, row in gdf.iterrows():
        geom_json = json.loads(gpd.GeoSeries([row["geometry"]]).to_json())["features"][0]["geometry"]
        b = bounds_df.loc[idx]
        bounds = [[float(b["miny"]), float(b["minx"])], [float(b["maxy"]), float(b["maxx"])]]
        center = [float(row["centroid"].y), float(row["centroid"].x)]

        # Compact label: strip to → "South East London ICB"
        full = row["icb_name"] or ""
        label = full
        if label.startswith("NHS "):
            label = label[4:]
        if label.endswith(" Integrated Care Board"):
            label = label[: -len(" Integrated Care Board")]
        icb_label = f"{label} ICB"

        features.append({
            "type": "Feature",
            "geometry": geom_json,
            "properties": {
                "icb_code": row["icb_code"],
                "icb_name": row["icb_name"],
                "icb_label": icb_label,
                "center": center,
                "bounds": bounds,
                "tooltip": icb_label,  # keep a generic 'tooltip' key for convenience
            }
        })

    return {"type": "FeatureCollection", "features": features}

# # ----QUERIES FOR DEPRIVATION AND ICB LINK INCOMPLETE ---------------

def get_icb_imd_scatter_data_incomplete(year, month, metric):
    """
    Returns one row per ICB for national deprivation scatter:
    icb_code, icb_name, region_code, region_name, icb_pop_2019,
    icb_imd_weighted, imd_quintile (as stored: 5=most), rtt_value.
    """
    query = """
        SELECT
            s.icb_code,
            s.icb_name,
            s.region_code,
            s.region_name,
            s.icb_pop_2019,
            s.icb_imd_weighted,
            s.imd_quintile,           -- NOTE: 5 = most deprived in source
            r.value AS rtt_value
        FROM icb_imd_2019_summary s
        LEFT JOIN rtt_data r
          ON r.pathway_type = 'Incomplete'
         AND r.geo_level = 'ICB'
         AND r.treatment_function_code = 'C_999'
         AND r.metric = %(metric)s
         AND r.year = %(year)s
         AND r.month = %(month)s
         AND r.org_code = s.icb_code
        ORDER BY s.region_name, s.icb_name;
    """
    return fetch_df(query, {"metric": metric, "year": year, "month": month})


def get_national_metric_value_incomplete(year, month, metric):
    """
    Returns a single-row DataFrame with the national value for the given month/metric
    (Incomplete pathway, C_999, geo_level='National').
    """
    sql = """
        SELECT value
        FROM rtt_data
        WHERE pathway_type = 'Incomplete'
          AND geo_level = 'National'
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
          AND year = %(year)s
          AND month = %(month)s
        LIMIT 1;
    """
    return fetch_df(sql, {"metric": metric, "year": year, "month": month})


# # ----QUERIES FOR DEPRIVATION AND ICB LINK ADMITTED ---------------

def get_icb_imd_scatter_data_admitted(year, month, metric):
    """
    Returns one row per ICB for national deprivation scatter:
    icb_code, icb_name, region_code, region_name, icb_pop_2019,
    icb_imd_weighted, imd_quintile (as stored: 5=most), rtt_value.
    """
    query = """
        SELECT
            s.icb_code,
            s.icb_name,
            s.region_code,
            s.region_name,
            s.icb_pop_2019,
            s.icb_imd_weighted,
            s.imd_quintile,           -- NOTE: 5 = most deprived in source
            r.value AS rtt_value
        FROM icb_imd_2019_summary s
        LEFT JOIN rtt_data r
          ON r.pathway_type = 'Admitted'
         AND r.geo_level = 'ICB'
         AND r.treatment_function_code = 'C_999'
         AND r.metric = %(metric)s
         AND r.year = %(year)s
         AND r.month = %(month)s
         AND r.org_code = s.icb_code
        ORDER BY s.region_name, s.icb_name;
    """
    return fetch_df(query, {"metric": metric, "year": year, "month": month})


def get_national_metric_value_admitted(year, month, metric):
    """
    Returns a single-row DataFrame with the national value for the given month/metric
    (Incomplete pathway, C_999, geo_level='National').
    """
    sql = """
        SELECT value
        FROM rtt_data
        WHERE pathway_type = 'Admitted'
          AND geo_level = 'National'
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
          AND year = %(year)s
          AND month = %(month)s
        LIMIT 1;
    """
    return fetch_df(sql, {"metric": metric, "year": year, "month": month})



# # ----QUERIES FOR DEPRIVATION AND ICB LINK NON-ADMITTED ---------------

def get_icb_imd_scatter_data_non_admitted(year, month, metric):
    """
    Returns one row per ICB for national deprivation scatter:
    icb_code, icb_name, region_code, region_name, icb_pop_2019,
    icb_imd_weighted, imd_quintile (as stored: 5=most), rtt_value.
    """
    query = """
        SELECT
            s.icb_code,
            s.icb_name,
            s.region_code,
            s.region_name,
            s.icb_pop_2019,
            s.icb_imd_weighted,
            s.imd_quintile,           -- NOTE: 5 = most deprived in source
            r.value AS rtt_value
        FROM icb_imd_2019_summary s
        LEFT JOIN rtt_data r
          ON r.pathway_type = 'Non-Admitted'
         AND r.geo_level = 'ICB'
         AND r.treatment_function_code = 'C_999'
         AND r.metric = %(metric)s
         AND r.year = %(year)s
         AND r.month = %(month)s
         AND r.org_code = s.icb_code
        ORDER BY s.region_name, s.icb_name;
    """
    return fetch_df(query, {"metric": metric, "year": year, "month": month})


def get_national_metric_value_non_admitted(year, month, metric):
    """
    Returns a single-row DataFrame with the national value for the given month/metric
    (Incomplete pathway, C_999, geo_level='National').
    """
    sql = """
        SELECT value
        FROM rtt_data
        WHERE pathway_type = 'Non-Admitted'
          AND geo_level = 'National'
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
          AND year = %(year)s
          AND month = %(month)s
        LIMIT 1;
    """
    return fetch_df(sql, {"metric": metric, "year": year, "month": month})


# # ----QUERIES FOR DEPRIVATION AND ICB LINK NEW ---------------

def get_icb_imd_scatter_data_new(year, month, metric):
    """
    Returns one row per ICB for national deprivation scatter:
    icb_code, icb_name, region_code, region_name, icb_pop_2019,
    icb_imd_weighted, imd_quintile (as stored: 5=most), rtt_value.
    """
    query = """
        SELECT
            s.icb_code,
            s.icb_name,
            s.region_code,
            s.region_name,
            s.icb_pop_2019,
            s.icb_imd_weighted,
            s.imd_quintile,           -- NOTE: 5 = most deprived in source
            r.value AS rtt_value
        FROM icb_imd_2019_summary s
        LEFT JOIN rtt_data r
          ON r.pathway_type = 'New'
         AND r.geo_level = 'ICB'
         AND r.treatment_function_code = 'C_999'
         AND r.metric = %(metric)s
         AND r.year = %(year)s
         AND r.month = %(month)s
         AND r.org_code = s.icb_code
        ORDER BY s.region_name, s.icb_name;
    """
    return fetch_df(query, {"metric": metric, "year": year, "month": month})


def get_national_metric_value_new(year, month, metric):
    """
    Returns a single-row DataFrame with the national value for the given month/metric
    (Incomplete pathway, C_999, geo_level='National').
    """
    sql = """
        SELECT value
        FROM rtt_data
        WHERE pathway_type = 'New'
          AND geo_level = 'National'
          AND treatment_function_code = 'C_999'
          AND metric = %(metric)s
          AND year = %(year)s
          AND month = %(month)s
        LIMIT 1;
    """
    return fetch_df(sql, {"metric": metric, "year": year, "month": month})


def count_regions_national() -> int:
    q = """
      SELECT COUNT(DISTINCT region_code) AS n
      FROM org_info
      WHERE region_code IS NOT NULL
    """
    df = fetch_df(q)
    return int(df.iloc[0]["n"]) if df is not None and not df.empty else 7  # fallback

def count_icbs_national() -> int:
    q = """
      SELECT COUNT(DISTINCT health_geography_code) AS n
      FROM org_info
      WHERE health_geography_code IS NOT NULL
    """
    df = fetch_df(q)
    return int(df.iloc[0]["n"]) if df is not None and not df.empty else 42  # fallback

def count_icbs_by_region(region_code: str) -> int:
    q = """
      SELECT COUNT(DISTINCT health_geography_code) AS n
      FROM org_info
      WHERE region_code = %(r)s
        AND health_geography_code IS NOT NULL
    """
    df = fetch_df(q, {"r": region_code})
    return int(df.iloc[0]["n"]) if df is not None and not df.empty else 0

def count_providers_national() -> int:
    q = """
      SELECT COUNT(*) AS n
      FROM org_info
      WHERE org_type = 'Provider'
        AND latitude IS NOT NULL AND longitude IS NOT NULL
    """
    df = fetch_df(q)
    return int(df.iloc[0]["n"]) if df is not None and not df.empty else 0

def count_providers_by_region(region_code: str) -> int:
    q = """
      SELECT COUNT(*) AS n
      FROM org_info
      WHERE org_type = 'Provider'
        AND region_code = %(r)s
        AND latitude IS NOT NULL AND longitude IS NOT NULL
    """
    df = fetch_df(q, {"r": region_code})
    return int(df.iloc[0]["n"]) if df is not None and not df.empty else 0


def get_population_national() -> int:
    q = """
      SELECT SUM(icb_pop_2019)::bigint AS pop
      FROM icb_imd_2019_summary
    """
    df = fetch_df(q)
    return int(df.iloc[0]["pop"]) if df is not None and not df.empty else 0


def get_population_by_region(region_code: str) -> int:
    q = """
      SELECT SUM(icb_pop_2019)::bigint AS pop
      FROM icb_imd_2019_summary
      WHERE region_code = %(r)s
    """
    df = fetch_df(q, {"r": region_code})
    return int(df.iloc[0]["pop"]) if df is not None and not df.empty else 0
