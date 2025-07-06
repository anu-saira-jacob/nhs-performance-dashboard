-- ==========================================
-- 🔁 Update Region Codes for ICB Rows in RTT Data
-- ==========================================

-- This script fills in the missing region_code values in rtt_data for ICB-level entries
-- by joining with the org_info table using ICB org_code.

UPDATE rtt_data
SET region_code = org_info.region_code
FROM org_info
WHERE rtt_data.geo_level = 'ICB'
  AND rtt_data.org_code = org_info.org_code
  AND rtt_data.region_code IS NULL;
