# test_spatial_queries.py
from queries import (
    get_ccg_imd_geojson,
    get_region_bounds,
    get_icb_boundaries_geojson,
)

REGION = "Y56"

print("→ Testing region bounds…")
bounds = get_region_bounds(REGION)
print("Bounds:", bounds)

print("\n→ Testing CCG IMD GeoJSON…")
ccg_fc = get_ccg_imd_geojson(REGION)
print("CCG features:", len(ccg_fc["features"]))
print("First CCG props (sample):", ccg_fc["features"][0]["properties"] if ccg_fc["features"] else "None")

print("\n→ Testing ICB boundaries GeoJSON…")
icb_fc = get_icb_boundaries_geojson(REGION)
print("ICB features:", len(icb_fc["features"]))
print("First ICB props (sample):", icb_fc["features"][0]["properties"] if icb_fc["features"] else "None")
