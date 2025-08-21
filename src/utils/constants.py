# utils/constants.py
import dash_mantine_components as dmc
import dash_iconify
import html
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
import dash_mantine_components as dmc
import dash_iconify


METRIC_MODE_LABELS = {
    "Average (median) waiting time (in weeks)": [
        {"label": "Top 5 longest waits", "value": "top"},
        {"label": "Top 5 shortest waits", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
    "% within 18 weeks": [
        {"label": "Top 5 highest compliance rates", "value": "top"},
        {"label": "Top 5 lowest compliance rates", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
    "92nd percentile waiting time (in weeks)": [
        {"label": "Top 5 longest 92nd percentile waits", "value": "top"},
        {"label": "Top 5 shortest 92nd percentile waits", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
    "95th percentile waiting time (in weeks)": [
        {"label": "Top 5 longest 95th percentile waits", "value": "top"},
        {"label": "Top 5 shortest 95th percentile waits", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
    "Total number of incomplete pathways": [
        {"label": "Top 5 highest incomplete patient counts", "value": "top"},
        {"label": "Top 5 lowest incomplete patient counts", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
    "Total 52 plus weeks": [
        {"label": "Top 5 highest 52+ week counts", "value": "top"},
        {"label": "Top 5 lowest 52+ week counts", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],

    # ----- Admitted -----
    "Total number of completed pathways (all)": [
        {"label": "Top 5 highest completed pathway counts", "value": "top"},
        {"label": "Top 5 lowest completed pathway counts", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],

     # ----- New Referrals -----
    "Number of new RTT clock starts during the month": [
        {"label": "Top 5 highest new referral starts", "value": "top"},
        {"label": "Top 5 lowest new referral starts", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],

     "default": [
        {"label": "Top 5 highest values", "value": "top"},
        {"label": "Top 5 lowest values", "value": "bottom"},
        {"label": "Manual selection", "value": "manual"},
    ],
}


def _metric_formatting(metric: str):
    """
    Infer axis title and hover format from the metric label you already use.
    Also returns whether to scale by 100 for percentages (to match your code).
    """
    m = (metric or "").lower()
    if "%" in metric:
        return ("Percentage (%)", "%{y:.1f}%", True)
    if "waiting time" in m:
        return ("Waiting time (weeks)", "%{y:.2f} weeks", False)
    if "total" in m or "number" in m or "count" in m:
        return ("Total Count", "%{y:,.0f}", False)
    return ("Value", "%{y:.2f}", False)

def _fy_shapes_and_annotations(dates: pd.Series):
    """
    Vertical dotted lines at 1 April (FY boundary) + FY labels at ~Oct.
    """
    if dates.empty:
        return [], []

    start = dates.min().to_period("M").start_time
    end   = dates.max().to_period("M").end_time

    shapes, ann = [], []
    min_year, max_year = dates.dt.year.min(), dates.dt.year.max()

    # 1 April dividers
    for yr in range(min_year, max_year + 1):
        boundary = pd.Timestamp(year=yr, month=4, day=1)
        if start < boundary < end:
            shapes.append(
                dict(
                    type="line", xref="x", yref="paper",
                    x0=boundary, x1=boundary, y0=0, y1=1,
                    line=dict(color="#cbd5e1", width=1, dash="dot"),
                    layer="below",
                )
            )

    # FY labels (FY yy/yy+1) around October
    for yr in range(min_year, max_year):
        mid = pd.Timestamp(year=yr, month=10, day=1)
        ann.append(
            dict(
                x=mid, y=1.02, xref="x", yref="paper", xanchor="center",
                text=f"FY {str(yr)[-2:]}/{str(yr+1)[-2:]}",
                showarrow=False, font=dict(size=11, color="#64748b"),
            )
        )
    return shapes, ann

def build_trend_figure(
    df: pd.DataFrame,
    metric: str,
    title: str,
    line_color: str = "#2a9d8f",       # your current teal
    font_family: str = "Segoe UI",
    show_rolling: bool = True,
) -> go.Figure:
    """
    df must contain: ['year','month','value'].
    Returns a styled Plotly Figure with quarterly ticks, FY dividers,
    and an optional 3-month rolling average. Keeps your hover & color.
    """
    if df is None or df.empty:
        return go.Figure().update_layout(
            height=420, title=title, margin=dict(t=40, r=10, b=60, l=60),
            font=dict(family=font_family, size=14),
        )

    df = df.copy()

    # Metric formatting (and percent scaling) exactly like your code
    y_title, hover_fmt, scale_to_pct = _metric_formatting(metric)
    if scale_to_pct:
        df["value"] = df["value"] * 100

    # Build a proper monthly datetime and sort
    df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=1), errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    # 3-month centered rolling mean for trend readability
    if show_rolling and len(df) >= 3:
        df["roll3"] = df["value"].rolling(window=3, center=True, min_periods=1).mean()
    else:
        df["roll3"] = None

    fig = go.Figure()

    # Main monthly series (lines + markers)
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["value"],
            mode="lines+markers",
            name=metric,
            line=dict(width=2, color=line_color),
            marker=dict(size=5),
            hovertemplate=f"<b>%{{x|%b %Y}}</b><br>{hover_fmt}<extra></extra>",
        )
    )

    # Rolling mean (subtle, no hover)
    if show_rolling and df["roll3"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=df["date"],
                y=df["roll3"],
                mode="lines",
                name="3-month avg",
                line=dict(width=3),  # default color pairs well
                hoverinfo="skip",
                opacity=0.9,
            )
        )

    # Quarterly ticks (Apr/Jul/Oct/Jan etc.)
    fig.update_xaxes(
        type="date",
        tickformat="%b %y",
        dtick="M3",
        tickangle=0,
        showgrid=True,
        gridcolor="#e8edf2",
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
    )

    # FY dividers + labels
    shapes, ann = _fy_shapes_and_annotations(df["date"])
    fig.update_layout(shapes=shapes, annotations=ann)

    # Y-axis + layout polish (your font preserved)
    fig.update_yaxes(title_text=f"<b>{y_title}</b>", gridcolor="#e8edf2")
    fig.update_layout(
        title=title,
        height=420,
        hovermode="x unified",
        margin=dict(t=40, r=10, b=60, l=60),
        font=dict(family=font_family, size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def _render_min_help(content: dict) -> dmc.Stack:
    """
    Render the minimal sidebar help (bullets, links, CTA).
    Uses Markdown in bullets so **bold** works.
    """
    # bullets via Markdown (small text)
    # bullets = dmc.List(
    #     [
    #         dmc.ListItem(
    #             dcc.Markdown(b, mathjax=False)  # <-- Markdown parses **bold**
    #         )
    #         for b in content.get("bullets", [])
    #     ],
    #     spacing="xs",
    #     icon=dash_iconify.DashIconify(icon="mdi:circle-small", width=18),
    #     withPadding=False,
    # )
    bullets = dmc.Stack(
    [
        dcc.Markdown(b, mathjax=False)
        for b in content.get("bullets", [])
    ],
    gap="sm",   # space between paragraphs
    )

    links = content.get("links", [])
    links_block = (
        dmc.Stack(
            [
                dmc.Anchor(
                    l["label"], href=l["url"], target="_blank", size="sm", underline=True
                )
                for l in links
            ],
            gap="xs",
        )
        if links
        else None
    )

    cta = content.get("cta")
    cta_btn = (
        dmc.Anchor(                                      # <-- href goes here
            dmc.Button(
                "Open full help page",
                variant="light",
                size="sm",
                leftSection=dash_iconify.DashIconify(icon="mdi:open-in-new", width=16),
            ),
            href=cta.get("href", "/help"),
            target="_blank",                             # <-- open new tab
            # rel="noopener noreferrer",
            underline=False,
        )
        if cta else None
    )

    return dmc.Stack(
        [
            # (Removed duplicate title here)
            bullets,
            dmc.Divider(my="sm"),
            dmc.Text("Sources", fw=600, size="sm"),
            links_block if links_block else dmc.Text("—", size="sm", c="dimmed"),
            dmc.Divider(my="sm"),
            cta_btn if cta_btn else html.Div(),
        ],
        gap="sm",
    )


def _wrap_label(label: str, width: int = 18) -> str:
    if not isinstance(label, str):
        return label
    if ", " in label:
        return label.replace(", ", "<br>", 1)
    if " and " in label:
        return label.replace(" and ", "<br>", 1)
    if len(label) > width:
        mid = len(label) // 2
        left = label.rfind(" ", 0, mid)
        right = label.find(" ", mid)
        cut = left if left != -1 else (right if right != -1 else -1)
        if cut != -1:
            return label[:cut] + "<br>" + label[cut+1:]
    return label
