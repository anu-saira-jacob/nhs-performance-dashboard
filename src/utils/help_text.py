# utils/help_text.py
from dash import html
import dash_mantine_components as dmc
import dash_iconify

# -------- Common links (centralised so you can change once) ------------------
LINKS = {
    "rtt_monthly": {
        "label": "NHS England — RTT monthly statistics",
        "url": "https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/",
    },
    "imd_2019": {
        "label": "ONS — English Indices of Deprivation 2019",
        "url": "https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019",
    },
    "nhs_icbs": {
        "label": "NHS England — Integrated Care Boards (ICBs)",
        "url": "https://www.england.nhs.uk/integratedcare/integrated-care-boards/",
    },
    "nhs_regions": {
        "label": "NHS England — Regions",
        "url": "https://www.england.nhs.uk/about/regional-area-teams/",
    },
    "nhs_sicbs": {
        "label": "NHS England — Sub-ICBs",
        "url": "https://www.nhsbsa.nhs.uk/sicbls-icbs-and-other-providers/organisation-and-prescriber-changes/sub-icb-locations",
    },
    "nhs_geographies": {
        "label": "Current NHS Geographies",
        "url": "https://www.ons.gov.uk/methodology/geography/ukgeographies/healthgeography",
    },
    "nhs_geography_changes_2022": {
        "label": "NHS Geography Changes in 2022",
        "url": "https://digital.nhs.uk/services/organisation-data-service/upcoming-code-changes/reconfiguration-toolkit/ccgs-sub-icb-locations-impacted-by-boundary-changes",
    },
    "nhs_geography_changes_2021": {
        "label": "NHS Geography Changes in 2021",
        "url": "https://www.hsj.co.uk/integrated-care/revealed-the-ccg-map-after-new-wave-of-mergers/7026848.article",
    },
    "nhs_geography_changes_2020": {
        "label": "NHS Geography Changes in 2020",
        "url": "https://thiis.co.uk/eight-ccgs-to-merge-into-one-with-plans-to-use-its-substantial-buying-power-to-increase-value/",
    },
    "population_estimate_health_boundaries": {
        "label": "Health Geography Population Estimates",
        "url": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/clinicalcommissioninggroupmidyearpopulationestimates",
    },
    "waiting_times_explained": {
        "label": "NHS England — Waiting Times and their Calculations Explained",
        "url": "https://blog.stopwaiting.co.uk/current-nhs-waiting-times-calculation/",
    },
    "nhs_statistical_press_notice": {
        "label": "NHS Statistical Press Notice- RTT Waiting Times",
        "url": "https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2023/10/RTT-Press-Notice-October-2023.pdf",
    },
    "waiting_list_metrics_explained": {
        "label": "Waiting List Tracker- Data Explained",
        "url": "https://waitinglist.health.lcp.com/data-and-method",
    },
    "incomplete_commissioner_example": {
        "label": "Example of Incomplete Pathway Data",
        "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.england.nhs.uk%2Fstatistics%2Fwp-content%2Fuploads%2Fsites%2F2%2F2025%2F07%2FIncomplete-Commissioner-Mar25-XLSX-4M-revised.xlsx&wdOrigin=BROWSELINK",
    },
    "admitted_commissioner_example": {
        "label": "Example of Admitted Pathway Data",
        "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.england.nhs.uk%2Fstatistics%2Fwp-content%2Fuploads%2Fsites%2F2%2F2025%2F07%2FAdmitted-Commissioner-Mar25-XLSX-2M-revised.xlsx&wdOrigin=BROWSELINK",
    },
    "non_admitted_commissioner_example": {
        "label": "Example of Non-Admitted Pathway Data",
        "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.england.nhs.uk%2Fstatistics%2Fwp-content%2Fuploads%2Fsites%2F2%2F2025%2F07%2FNonAdmitted-Commissioner-Mar25-XLSX-2M-revised.xlsx&wdOrigin=BROWSELINK",
    },
    "new_referral_commissioner_example": {
        "label": "Example of New Referrals Pathway Data",
        "url": "https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.england.nhs.uk%2Fstatistics%2Fwp-content%2Fuploads%2Fsites%2F2%2F2025%2F07%2FNew-Periods-Commissioner-Mar25-XLSX-157K-revised.xlsx&wdOrigin=BROWSELINK",
    },
    "nhs_treatment_functions": {
        "label": "NHS Treatment Functions",
        "url": "https://archive.datadictionary.nhs.uk/DD%20Release%20March%202025/supporting_information/main_specialty_and_treatment_function_codes_table.html",
    }


}

# -------- Optional tiny token helper (for later dynamic insertion) -----------
def fill_tokens(text: str, tokens: dict | None = None) -> str:
    """Replace {token} in text with values from tokens dict. Safe if missing."""
    if not tokens:
        return text
    out = text
    for k, v in tokens.items():
        out = out.replace("{" + k + "}", str(v))
    return out


# =============================================================================
#  Minimal sidebar content per page (shown in the right-hand Drawer)
#  Keep this short: 3–5 bullets max + 'Learn more' link to /help#<anchor>
# =============================================================================

PAGE_HELP_MIN = {
    "home": {
        "title": "Help — Home",
        "bullets": [
            "This interactive tool is used to explore NHS England's RTT waiting times. Before analysing the data, if you're unfamiliar with the NHS terminology, the system hierarchy, or what the RTT pathways represent, please read the help page linked at the bottom before proceeding.",
            "Select a **Granularity** (National or Regional) and a **Pathway** (Incomplete, Admitted, Non-Admitted, New Referrals).",
            "For **Regional** dashboards, select a region by clicking the map outline or using the dropdown.",
            "Click **Go** to open the relevant dashboard.",
        ],
        "links": [
            LINKS["rtt_monthly"], LINKS["nhs_regions"]
        ],
        "cta": {
            "label": "Learn more about the NHS and RTT pathways",
            "href": "/help#home",
        },
    },

    "incomplete_national": {
        "title": "Help — Incomplete pathway National",
        "bullets": [
                    "This page shows the national overview of Incomplete RTT pathways (Apr 2022 – Mar 2025), helping track the overall backlog of patients still waiting to start treatment.",
                    "The **Trend line chart** displays how the selected metric has changed over the past 3 years. Both the monthly values and a 3-month rolling average are shown to smooth short-term fluctuations. This chart shows the overall NHS picture (all treatment types combined).",
                    "The **Monthly comparison bar chart** breaks the chosen metric down by treatment function for a selected month. You can view the 5 best performing services, the 5 worst performing services, or manually select services to compare.",
                    "The **ICB deprivation vs RTT metric scatter plot** compares deprivation with the selected metric across ICBs. Each bubble is an ICB (colour = region, size = deprivation group). Larger bubbles represent more deprived populations (based on aggregated IMD 2019 scores). The green line marks the national average, making it easy to spot ICBs performing better or worse than average. The population of each ICB is shown on the x-axis, while the selected RTT metric is shown on the y-axis.",
                    "For more background on definitions, pathways, and metrics, please see the full **Help** page."
                ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["incomplete_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
        ],
        "cta": {
            "label": "Learn more about the Incomplete page",
            "href": "/help#incomplete",
        },
    },
    "incomplete_regional": {
        "title": "Help — Incomplete pathway Regional",
        "bullets": [
                    "This page shows the regional overview of Incomplete RTT pathways (Apr 2022 – Mar 2025), allowing you to explore variation within each NHS England region.",
                    "The **Trend line chart** tracks the selected metric over the last 3 years for the chosen region, with both monthly values and a 3-month rolling average shown. This provides an overall regional picture across all treatment types.",
                    "The **Monthly comparison bar chart** breaks the chosen metric down by treatment function for a selected month. You can view the 5 best performing treatment functions, the 5 worst performing treatment functions, or manually select services to compare.",
                    "The **Regional deprivation map and ICB bar chart** show how deprivation (IMD) relates to RTT waits within the region. The map displays CCG-level IMD scores (2019) shaded by deprivation quantile, with ICB boundaries overlaid. The linked bar chart shows the RTT metric for each ICB. Clicking on an ICB in the map highlights the matching bar, and vice versa. This approach avoids smoothing deprivation to ICB level, so you can still see variation in deprivation within an ICB.",
                    "For more background on definitions, pathways, and metrics, please see the full **Help** page."
                ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["incomplete_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
        ],
        "cta": {
            "label": "Learn more about the Incomplete page",
            "href": "/help#incomplete",
        },
    },

    "admitted_national": {
        "title": "Help — Admitted pathway",
        "bullets": [
                "This page shows the national overview of Admitted RTT pathways, i.e. patients treated with hospital admission, Apr 2022 – Mar 2025.",
                "The **Trend line chart** displays admitted pathway waits over time for your selected metric (median wait, 95th percentile, completed totals, 52+ weeks), with a 3-month rolling average.",
                "The **Monthly comparison bar chart** shows variation by treatment function for a chosen month, with options for Top 5, Bottom 5, or manual comparisons.",
                "The **Deprivation vs RTT metric scatter plot** shows ICBs by population size, deprivation quantile (bubble size), and region colour, with the national average line for context. The population of each ICB is shown on the x-axis, while the selected RTT metric is shown on the y-axis.",
                "Definitions and more detail are available in the **Help** page."
            ],
        "links": [
                    LINKS["rtt_monthly"],
                    LINKS["admitted_commissioner_example"],
                    LINKS["imd_2019"],
                    LINKS["nhs_geographies"],
                    LINKS["nhs_regions"],
                    LINKS["nhs_icbs"],
                    LINKS["population_estimate_health_boundaries"],
                    LINKS["nhs_treatment_functions"],
                  ],
        "cta": {"label": "Learn more about the Admitted page", "href": "/help#admitted"},
    },
     "admitted_regional": {
        "title": "Help — Admitted pathway",
        "bullets": [
            "This page shows the regional overview of Admitted RTT pathways, Apr 2022 – Mar 2025.",
            "The **Trend line chart** shows admitted waits for the selected metric over the last 3 years within the chosen region, including a rolling average.",
            "The **Monthly comparison bar chart** highlights admitted pathway variation across treatment functions in a given month, with Top 5, Bottom 5, or manual options.",
            "The **Regional deprivation map (CCG) + ICB bar chart** shows deprivation patterns alongside RTT waits. The map shades CCGs by IMD quantile, with ICB boundaries overlaid, and the linked bar chart shows admitted waits by ICB. Click either chart to highlight the other.",
            "Full pathway/metric definitions are available in the **Help** page."
        ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["admitted_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
        ],
        "cta": {"label": "Learn more about the Admitted page", "href": "/help#admitted"},
    },

    "non_admitted_national": {
        "title": "Help — Non‑Admitted pathway",
        "bullets": [
                "This page shows the national overview of Non-Admitted RTT pathways, i.e. patients treated without hospital admission, Apr 2022 – Mar 2025.",
                "The **Trend line chart** displays non-admitted waits over time for your selected metric (median wait, 95th percentile, completed totals, 52+ weeks), with a rolling average.",
                "The **Monthly comparison bar chart** compares treatment functions in a selected month, showing Top 5, Bottom 5, or manual service comparisons.",
                "The **Deprivation vs RTT metric scatter plot chart** plots ICBs nationally by population, deprivation quantile (bubble size), and region colour. The national average line is also shown for context. The population size of each ICB is on the x-axis, while the selected RTT metric is on the y-axis.",
                "Further detail is available on the **Help** page."
        ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["non_admitted_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
                  ],
        "cta": {"label": "Learn more about the Non‑Admitted page", "href": "/help#non-admitted"},
    },
    "non_admitted_regional": {
        "title": "Help — Non‑Admitted pathway",
        "bullets": [
            "This page shows the regional overview of Non-Admitted RTT pathways, Apr 2022 – Mar 2025.",
            "The **Trend line chart** tracks non-admitted waits for the chosen metric within the region, with monthly and 3-month rolling average values.",
            "The **Monthly comparison bar chart** highlights treatment function variation in the selected month, with Top 5, Bottom 5, or manual selection.",
            "The **Regional deprivation map (CCG) and ICB bar chart** provide context by linking IMD deprivation to RTT waits. CCGs are shaded by IMD quantile with ICB outlines shown; linked bars display RTT results at ICB level. Clicking map or bars highlights the other.",
            "For metric definitions and background, see the full **Help** page."
        ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["non_admitted_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
                  ],
        "cta": {"label": "Learn more about the Non‑Admitted page", "href": "/help#non-admitted"},
    },

    "new_national": {
        "title": "Help — New Referrals",
        "bullets": [
                "This page shows the national overview of New RTT Referrals (‘clock starts’) from Apr 2022 – Mar 2025.",
                "The **Trend line chart** tracks how many new referral pathways begin each month, with a 3-month rolling average to smooth monthly variation.",
                "The **Monthly comparison bar chart** shows which treatment functions had the highest or lowest numbers of new referrals in a chosen month. You can select Top 5, Bottom 5, or manually choose services.",
                "The **Deprivation vs Referrals scatter plot** compares ICBs nationally. Each bubble represents an ICB, sized by deprivation quantile (larger = more deprived), coloured by region, with the national average line shown. The population of each ICB is shown on the x-axis, while the selected RTT metric is shown on the y-axis.",
                "For more detail on pathways and referral definitions, see the full **Help** page."
            ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["new_referral_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
        ],
        "cta": {"label": "Learn more about the New Referrals page", "href": "/help#new"},
    },
    "new_regional": {
        "title": "Help — New Referrals",
        "bullets": [
            "This page shows the regional overview of New RTT Referrals (‘clock starts’) from Apr 2022 – Mar 2025.",
            "The **Trend line chart** shows the number of new referrals over time for the selected region, with a 3-month rolling average.",
            "The **Monthly comparison bar chart** breaks referrals down by treatment function in that region, with options for Top 5, Bottom 5, or manual selection.",
            "The **Deprivation map (CCG) with ICB bars** lets you explore how new referral volumes compare with local deprivation. The CCG-level IMD map is overlaid with ICB boundaries, and the linked bar chart shows referral counts by ICB. Clicking the map highlights the bar and vice-versa.",
            "See the full **Help** page for pathway and metric definitions."
        ],
        "links": [
            LINKS["rtt_monthly"],
            LINKS["new_referral_commissioner_example"],
            LINKS["imd_2019"],
            LINKS["nhs_geographies"],
            LINKS["nhs_regions"],
            LINKS["nhs_icbs"],
            LINKS["population_estimate_health_boundaries"],
            LINKS["nhs_treatment_functions"],
        ],
        "cta": {"label": "Learn more about the New Referrals page", "href": "/help#new"},
    },
}


# =============================================================================
#  Full help-page content (render on /help). Use anchors: #home, #incomplete...
#  Keep sections compact but complete; link out for detail.
# =============================================================================

HELP_PAGE_CONTENT = {
    "home": {
            "anchor": "home",
            "title": "NHS Referral to Treatment (RTT) Dashboard",
            # "overview": (
            #     "We use the Consultant-led Referral to Treatment (RTT) Wait Time data published by NHS England on a monthly basis as outlined below. The data is reported at national, regional, integrated care board, and sub-integrated care board (sub-ICB) level. "
            # ),
            "sections": [
                {
                    "heading": "Referral to Treatment (RTT) Wait Times",
                    "body": (
                        "Referral to Treatment (RTT) measures the time from when a patient is first "
                        "referred (usually by a GP) until they begin their first definitive treatment. "
                        "The official data source is NHS England’s [Consultant-led RTT statistics]"
                        "(https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/), "
                        "which are published monthly.\n\n"
                        "The RTT datasets record **pathways**, not individual patients. Each pathway "
                        "represents one entry on the waiting list. If a person is waiting for two "
                        "different procedures, this will count as two separate pathways.\n\n"
                        "In this dashboard we use the monthly consultant-led RTT data, reported at "
                        "national, regional, and Integrated Care Board (ICB) level. Pathways are grouped "
                        "into four categories:\n\n"
                        "- **Incomplete**: pathways still waiting to start treatment.\n"
                        "- **Admitted**: pathways completed with admission to hospital.\n"
                        "- **Non-Admitted**: pathways completed without admission (for example: outpatient procedures).\n"
                        "- **New Referrals**: new RTT ‘clock starts’ when a patient first enters the pathway.\n\n"
                        "This section provides a high-level overview. More detailed explanations of each "
                        "pathway, the associated metrics, and what those metrics mean are provided in "
                        "their respective sections of the help page."
                    ),
                },
                {
                    "heading": "NHS System Hierarchy",
                    "body": 
                        dmc.Paper(
                            dmc.Image(
                                src="/assets/nhs_system_hierarchy.png",
                                alt="NHS system hierarchy pyramid",
                                w="100%",     # fill the paper width
                                maw=750,      # allow it to be large
                                mah=600,      # cap height if needed
                                fit="contain",
                                radius="md",
                            ),
                            withBorder=True,
                            shadow="sm",
                            p="sm",
                            radius="md",
                            style={"display": "inline-block", "maxWidth": "980px"},  # overall cap
                        )
                    
                },
                {
                    "heading": "NHS Geography Changes (2019–2022)",
                    "body": (
                        "Between 2019 and 2022 the NHS went through several major organisational "
                        "changes. Small Clinical Commissioning Groups (CCGs) were gradually merged, "
                        "and in July 2022 all CCGs were replaced by Sub-Integrated Care Board (Sub-ICB) "
                        "locations, with Integrated Care Boards (ICBs) becoming the new statutory bodies.\n\n"
                        "These changes present a challenge for analysis and dashboards. It is not only "
                        "the **metrics** that are affected (because data is now published against new "
                        "organisations), but also the **boundaries** used for maps and geographic visualisations. "
                        "Unfortunately, there is no single authoritative mapping or lookup document that "
                        "captures *all* of these reorganisations in one place. Instead, information has to "
                        "be pieced together from multiple NHS releases (e.g. CCG merger announcements in 2020 "
                        "and 2021, the Sub-ICB transition in 2022, and separate notes on boundary adjustments "
                        "such as Bassetlaw or Glossop).\n\n"
                        "Because of this, care should be taken when comparing historical and current figures "
                        "or when interpreting geographic patterns. Boundaries, names, and codes may not align "
                        "perfectly across different periods."
                    ),
                },
                {
                    "heading": "Data sources",
                    "body": (
                        "This dashboard ingests monthly **RTT Excel workbooks** published by NHS England from 2022-2025. "
                        "Geographies reflect the NHS reorganisation (ICBs live from mid-2022)."
                    ),
                },
            ],
            "links": [LINKS["rtt_monthly"], LINKS["nhs_geography_changes_2020"], LINKS["nhs_geography_changes_2021"],LINKS["nhs_geography_changes_2022"]],
        },
    "deprivation": {
        "anchor": "deprivation",
        "title": "IMD Score",
        # "overview": (
        #     "Explore waiting-time performance for **incomplete pathways** at National or Regional level. "
        #     "The page shows a time trend, a monthly comparison by treatment function, and a deprivation view "
        #     "(bubble plot in National; IMD map with ICB overlays in Regional)."
        # ),
        "sections": [
            {
                "heading": "What is IMD?",
                "body": (
                    "The Index of Multiple Deprivation (IMD) score is a measure of the deprivation of an area, accounting for a range of factors including: income, crime, education, health, employment, living environment and barriers to housing and services. It is often used in healthcare to understand how deprivation affects health outcomes and access to services.  "
                    "The most recent IMD data is from 2019, and it is used to provide context for the RTT data, particularly in understanding how deprivation may impact waiting times and access to care."
                ),
            },
            {
                "heading": "Index of Multiple Deprivation (IMD) and RTT",
                "body": (
                    "The Index of Multiple Deprivation (IMD) is a national measure of relative deprivation, "
                    "last updated in 2019. The next release is expected in October 2025. Because our RTT data "
                    "covers the period 2022–2025, this creates challenges: IMD boundaries are aligned to "
                    "Clinical Commissioning Groups (CCGs, pre-2022), whereas RTT metrics are now published "
                    "for Integrated Care Boards (ICBs)."
                ),
            },
            {
                "heading": "Mapping IMD to ICBs",
                "body": (
                    "To align IMD scores with RTT metrics, we mapped CCG-level IMD data to their respective "
                    "ICBs. We then aggregated the deprivation scores using a **population-weighted average** "
                    "to produce an ICB-level IMD score. This makes it possible to compare deprivation and RTT "
                    "at national or ICB scale, but aggregation inevitably smooths out variation and reduces "
                    "local detail."
                ),
            },
            {
                "heading": "Preserving Granularity in Regional Analysis",
                "body": (
                    "For regional views, we take a different approach. Instead of collapsing to ICB averages, "
                    "we display a **choropleth map of CCGs shaded by IMD scores**, with ICB boundaries overlaid. "
                    "This allows users to see how diverse an ICB can be internally: some areas may be highly "
                    "deprived while others are much less so. Even though RTT metrics are only published at ICB "
                    "level, this mapping lets users understand the deprivation context within those boundaries."
                ),
            }
        ],
        "links": [LINKS["imd_2019"], LINKS["population_estimate_health_boundaries"],  LINKS["nhs_geographies"]],
    },

    "incomplete": {
        "anchor": "incomplete",
        "title": "Incomplete pathway",
        # "overview": (
        #     "Explore waiting-time performance for **incomplete pathways** at National or Regional level. "
        #     "The page shows a time trend, a monthly comparison by treatment function, and a deprivation view "
        #     "(bubble plot in National; IMD map with ICB overlays in Regional)."
        # ),
        "sections": [
            {
                "heading": "What does Incomplete pathway mean?",
                "body": ( 
                    "Incomplete pathways are the waiting times for cases where patients are waiting to start treatment at the end of the reporting period. In these cases, patients will be at various stages of their pathway, for example, waiting for diagnostics, an appointment with a consultant, or for admission for a procedure. These are sometimes referred to as waiting list waiting times and the volume of incomplete RTT pathways as the size of the RTT waiting list.",
                ),
            },
            {
                "heading": "Metrics for Incomplete Pathways",
                "body": (
                    "Several measures are used to describe how long people are waiting on incomplete "
                    "RTT pathways (i.e. those still waiting to start treatment). All of these are "
                    "calculated as a **snapshot at the end of each reporting month**:\n\n"
                    "- **Average (Median) Waiting Time**: All incomplete pathways are ordered by how "
                    "long they have been waiting, and the middle value is taken. Half of pathways "
                    "have shorter waits than this, and half have longer. The median is used instead "
                    "of a simple average because it is less affected by a small number of extremely "
                    "long waits.\n\n"
                    "- **92nd Percentile Waiting Time**: Shows the point below which 92% of all waits "
                    "fall. For example, if this is 17 weeks, then 92% of people have been waiting less "
                    "than 17 weeks and the longest-waiting 8% have been waiting longer. This metric "
                    "links to the NHS standard that at least 92% of patients should start treatment "
                    "within 18 weeks.\n\n"
                    "- **% Within 18 Weeks**: The proportion of incomplete pathways that are still within "
                    "18 weeks of referral. This reflects the NHS maximum standard for non-urgent, "
                    "consultant-led treatment.\n\n"
                    "- **Total Incomplete Pathways**: The total number of pathways still waiting to start "
                    "treatment at the end of the month. Note that pathways are not the same as patients: "
                    "if one person is waiting for two separate procedures, this counts as two pathways.\n\n"
                    "- **Total Waiting Over 52 Weeks**: The number of incomplete pathways where the wait "
                    "has reached a year or more since referral."
                ),
            },
        ],
        "links": [LINKS["rtt_monthly"], LINKS["nhs_statistical_press_notice"], LINKS["waiting_times_explained"], LINKS["waiting_list_metrics_explained"], LINKS["incomplete_commissioner_example"], LINKS["admitted_commissioner_example"], LINKS["non_admitted_commissioner_example"], LINKS["new_referral_commissioner_example"]],
    },

    "admitted": {
        "anchor": "admitted",
        "title": "Admitted pathway",
        # "overview": (
        #     "Investigate admitted RTT performance over time and across treatment functions, at National or Regional level."
        # ),
        "sections": [
            {
                "heading": "What does Admitted Pathway mean?",
                "body": "Admitted pathways are the waiting times for cases where patients started treatment during the reporting period and the treatment involved admission to hospital. These are sometimes referred to as inpatient waiting times. They include the complete time waited from referral until start of inpatient treatment. ",
            },
            {
                "heading": "Metrics for Admitted Pathways",
                "body": (
                    "The following measures are reported at the end of each month:\n\n"
                    "- **Average (Median) Waiting Time**: All admitted pathways are ordered by how long the patient "
                    "waited from referral until admission. The middle value is taken, meaning half of pathways were "
                    "shorter than this and half were longer. Median is used as it better reflects a typical experience "
                    "than a simple average.\n\n"
                    "- **95th Percentile Waiting Time**: Shows how long 95% of admitted pathways took from referral "
                    "to treatment. For example, if this is 24 weeks, then 95% of patients started treatment within "
                    "24 weeks and the longest-waiting 5% took longer.\n\n"
                    "- **Total Completed Pathways**: The total number of RTT pathways completed with an admission "
                    "during the month.\n\n"
                    "- **Total Waiting Over 52 Weeks**: The number of admitted pathways where the patient waited "
                    "a year or more before admission.\n\n"
                    "_Note: For admitted pathways the **95th percentile** is used, rather than the 92nd percentile "
                    "used for incomplete waits. This is because the RTT operational standard (92% within 18 weeks) "
                    "applies to incomplete pathways, whereas admitted and non-admitted waits are reported using "
                    "a conventional 95th percentile measure to capture the longest waits._"
                ),
            },
        ],
        "links": [LINKS["rtt_monthly"], LINKS["nhs_statistical_press_notice"], LINKS["waiting_times_explained"], LINKS["admitted_commissioner_example"]],
    },

    "non_admitted": {
        "anchor": "non-admitted",
        "title": "Non‑Admitted pathway",
        # "overview": (
        #     "Explore non‑admitted RTT performance over time and by treatment function, at National or Regional level."
        # ),
        "sections": [
            {
                "heading": "What does Non-Admitted Pathway mean?",
                "body": "Non-admitted pathways are the waiting times for cases where patients completed their pathway during the reporting period for reasons other than an inpatient or day case admission to hospital for treatment. These are sometimes referred to as outpatient waiting times. They include the time waited for cases where a patient’s RTT waiting time clock either stopped for treatment or other reasons, such as a patient declining treatment. ",
            },
            {
                "heading": "Metrics for Non-Admitted Pathways",
                "body": (
                    "Since Non-admitted pathways are those that were completed without the patient being admitted to "
                    "hospital (for example, treatment in an outpatient setting). The same measures are used as in admitted pathways:\n\n"
                    "- **Average (Median) Waiting Time**: All non-admitted pathways are ordered by how long the "
                    "patient waited from referral until treatment, and the middle value is reported.\n\n"
                    "- **95th Percentile Waiting Time**: Indicates the point below which 95% of non-admitted pathways "
                    "were completed. This highlights the longest waits without being skewed by extreme cases.\n\n"
                    "- **Total Completed Pathways**: The total number of RTT pathways completed without admission "
                    "during the month.\n\n"
                    "- **Total Waiting Over 52 Weeks**: The number of non-admitted pathways where the wait was a year "
                    "or more from referral to treatment.\n\n"
                    "_Note: As with admitted pathways, the **95th percentile** is used here. The RTT 92% standard "
                    "relates specifically to incomplete waits, so completed pathways (admitted and non-admitted) "
                    "are reported using the 95th percentile instead._"
                ),
            }
        ],
        "links": [LINKS["rtt_monthly"], LINKS["nhs_statistical_press_notice"], LINKS["waiting_times_explained"], LINKS["non_admitted_commissioner_example"]],  
    },

    "new": {
        "anchor": "new",
        "title": "New Referrals",
        # "overview": (
        #     "Inspect **new RTT clock starts** over time and, where applicable, by treatment function."
        # ),
        "sections": [
            {
                "heading": "What are New Referrals?",
                "body": "New RTT periods or New Referrals are the number of new RTT pathways where the clock start date is within the reporting month.",
            },
            {
                "heading": "Metrics for New Referrals",
                "body": (
                    "New referrals are cases where a new RTT ‘clock’ starts — in other words, the point at which "
                    "a patient is newly referred into consultant-led care. Only one main measure is reported:\n\n"
                    "- **Number of New RTT Clock Starts**: The total number of new pathways that began in the "
                    "reporting month. Each new referral represents a new entry onto the waiting list, and if a "
                    "person is referred for more than one procedure, each referral counts as a separate pathway.\n\n"
                    "This metric provides insight into the demand for services, as it shows how many new patients "
                    "are entering the RTT system each month."
                ),
            }
        ],
        "links": [LINKS["rtt_monthly"], LINKS["new_referral_commissioner_example"]],
    },
}


METRIC_HELP_TEXT = {
    "incomplete": {
        "median_wait_weeks": "The median wait time at month end is the middle value when all pathways are ordered by length of wait, in other words, the midpoint of the RTT waiting times distribution.",
        "p92_weeks": "92nd percentile waiting time shows the point below which 92% of all waits fall. This metric links to the NHS standard that at least 92% of patients should start treatment within 18 weeks.",
        "pct_within_18w": "The proportion of incomplete pathways that are still within 18 weeks of referral. This reflects the NHS maximum standard for non-urgent, consultant-led treatment.",
        "incomplete_total": "The total number of pathways still waiting to start treatment at the end of each month. ",
        "over52_total": "The number of incomplete pathways where the wait has reached a year or more since referral.",
    },
    "admitted": {
        "median_wait_weeks": "Median time from referral to admission for pathways completed at end of each month.",
        "p95_weeks": "Shows how long 95% of admitted pathways took from referral to treatment. This highlights the longest waits without being skewed by extreme cases.",
        "completed_total": "Total number of RTT pathways completed with an admission at the end of each month.",
        "over52_total": "Number of admitted pathways where the wait reached 52+ weeks before treatment.",
    },
    "non_admitted": {
        "median_wait_weeks": "Median time from referral to treatment for pathways completed without admission at end of each month",
        "p95_weeks": "Shows how long 95% of non-admitted pathways took from referral to treatment. This highlights the longest waits without being skewed by extreme cases.",
        "completed_total": "Total number of RTT pathways completed without admission at the end of each month.",
        "over52_total": "Number of non-admitted pathways where the wait reached 52+ weeks before treatment.",
    },
    "new_referrals": {
        "new_clock_starts": "Count of new RTT ‘clock starts’ at the end of each month (each referral is a separate pathway).",
    },
}

INCOMPLETE_DROPDOWN_MAP = {
    "Average (median) waiting time (in weeks)": "median_wait_weeks",
    "92nd percentile waiting time (in weeks)": "p92_weeks",
    "% within 18 weeks": "pct_within_18w",
    "Total number of incomplete pathways": "incomplete_total",
    "Total 52 plus weeks": "over52_total",
}

COMPLETED_DROPDOWN_MAP = {
    "Average (median) waiting time (in weeks)": "median_wait_weeks",
    "95th percentile waiting time (in weeks)": "p95_weeks",
    "Total number of completed pathways (all)": "completed_total",
    "Total 52 plus weeks": "over52_total",
}


NEW_REFERRAL_DROPDOWN_MAP = {
    "Number of new RTT clock starts during the month": "new_clock_starts",
}




def build_help_icon(text: str):
    return dmc.Tooltip(
        label=text,
        multiline=True,
        w=280,
        children=dash_iconify.DashIconify(
            icon="mdi:help-circle-outline",
            width=16,
            style={"marginLeft": "6px", "cursor": "pointer", "color": "#555"},
        ),
    )