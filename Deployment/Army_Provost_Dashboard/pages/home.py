
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

from database import get_supabase_client

from ui_styles import (
    render_page_header,
    render_prototype_banner
)


# ======================================================================
# PAGE HEADER
# ======================================================================

render_page_header(
    eyebrow="CONTROL ROOM / SITUATIONAL OVERVIEW",
    title="Base Operational Overview",
    subtitle=(
        "Simulated installation monitoring, zone awareness "
        "and incident-status visualization."
    )
)


# ======================================================================
# SIMULATION BANNER
# ======================================================================

render_prototype_banner(
    """
    <b>SIMULATED ENVIRONMENT</b> — All installation zones, incident
    information, layout positions and operational statuses displayed
    on this page are fictional and intended solely for academic
    prototype demonstration.
    """
)



# ======================================================================
# LIVE INCIDENT STATISTICS
# ======================================================================

def load_live_zone_statistics():
    """
    Load incident statistics for the fictional operational zones
    from Supabase.

    Only incidents recorded during the last 7 days and containing
    a valid simulated incident_zone are included.
    """

    zone_stats = {
        zone: {
            "recent_incidents": 0,
            "high_priority_incidents": 0,
            "most_common_incident": "No recent incidents",
            "last_incident": "No recent incidents",
            "status": "NORMAL"
        }
        for zone in "ABCDEFGH"
    }

    try:

        client = get_supabase_client()

        cutoff = (
            datetime.now()
            - timedelta(days=7)
        ).isoformat()

        response = (
            client
            .table("dss_incident_audit")
            .select(
                "decision_timestamp,"
                "primary_type,"
                "provost_incident_category,"
                "priority,"
                "incident_zone"
            )
            .gte(
                "decision_timestamp",
                cutoff
            )
            .not_.is_(
                "incident_zone",
                "null"
            )
            .order(
                "decision_timestamp",
                desc=True
            )
            .execute()
        )

        records = response.data or []

        for zone_letter in "ABCDEFGH":

            zone_name = f"Zone {zone_letter}"

            zone_records = [
                record
                for record in records
                if record.get("incident_zone") == zone_name
            ]

            if not zone_records:
                continue

            priorities = [
                str(record.get("priority") or "")
                for record in zone_records
            ]

            critical_count = sum(
                priority == "Critical"
                for priority in priorities
            )

            high_count = sum(
                priority == "High"
                for priority in priorities
            )

            categories = [
                record.get("provost_incident_category")
                for record in zone_records
                if record.get("provost_incident_category")
            ]

            if categories:
                most_common = max(
                    set(categories),
                    key=categories.count
                )
            else:
                most_common = "Unclassified"

            latest = zone_records[0]

            latest_incident = (
                latest.get("primary_type")
                or latest.get("provost_incident_category")
                or "Unclassified incident"
            )

            if critical_count > 0:
                status = "ELEVATED"

            elif high_count > 0:
                status = "MONITOR"

            else:
                status = "NORMAL"

            zone_stats[zone_letter] = {
                "recent_incidents":
                    len(zone_records),

                "high_priority_incidents":
                    critical_count + high_count,

                "most_common_incident":
                    most_common,

                "last_incident":
                    latest_incident,

                "status":
                    status
            }

        return zone_stats

    except Exception as exc:

        st.warning(
            "Live zone statistics could not be loaded. "
            "The schematic will display zero live incidents."
        )

        return zone_stats


LIVE_ZONE_STATS = load_live_zone_statistics()

# ======================================================================
# SIMULATED BASE ZONE DATA
# ======================================================================

BASE_ZONES = {

    "A": {
        "zone_name": "HQ / Command Zone",
        "short_name": "HQ / COMMAND",
        "description":
            "Simulated administrative and command area used for "
            "prototype control-room visualization.",
        "recent_incidents":
            LIVE_ZONE_STATS["A"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["A"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["A"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["A"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["A"]["status"]
    },

    "B": {
        "zone_name": "Residential Zone",
        "short_name": "RESIDENTIAL",
        "description":
            "Simulated residential and accommodation area for personnel.",
        "recent_incidents":
            LIVE_ZONE_STATS["B"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["B"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["B"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["B"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["B"]["status"]
    },

    "C": {
        "zone_name": "Vehicle & Transport Zone",
        "short_name": "VEHICLE / TRANSPORT",
        "description":
            "Simulated mobility, vehicle holding and transport area.",
        "recent_incidents":
            LIVE_ZONE_STATS["C"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["C"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["C"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["C"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["C"]["status"]
    },

    "D": {
        "zone_name": "Stores / Logistics Zone",
        "short_name": "STORES / LOGISTICS",
        "description":
            "Simulated stores, supply and logistics support area.",
        "recent_incidents":
            LIVE_ZONE_STATS["D"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["D"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["D"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["D"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["D"]["status"]
    },

    "E": {
        "zone_name": "Training Area",
        "short_name": "TRAINING AREA",
        "description":
            "Simulated training and exercise zone.",
        "recent_incidents":
            LIVE_ZONE_STATS["E"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["E"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["E"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["E"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["E"]["status"]
    },

    "F": {
        "zone_name": "Entry / Security Zone",
        "short_name": "ENTRY / SECURITY",
        "description":
            "Simulated main-access and perimeter security area.",
        "recent_incidents":
            LIVE_ZONE_STATS["F"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["F"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["F"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["F"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["F"]["status"]
    },

    "G": {
        "zone_name": "Medical Zone",
        "short_name": "MEDICAL",
        "description":
            "Simulated medical-support and emergency-response area.",
        "recent_incidents":
            LIVE_ZONE_STATS["G"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["G"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["G"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["G"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["G"]["status"]
    },

    "H": {
        "zone_name": "Restricted / Sensitive Zone",
        "short_name": "RESTRICTED",
        "description":
            "Fictional restricted area included only to demonstrate "
            "situational-awareness concepts.",
        "recent_incidents":
            LIVE_ZONE_STATS["H"]["recent_incidents"],
        "high_priority_incidents":
            LIVE_ZONE_STATS["H"]["high_priority_incidents"],
        "most_common_incident":
            LIVE_ZONE_STATS["H"]["most_common_incident"],
        "last_incident":
            LIVE_ZONE_STATS["H"]["last_incident"],
        "status":
            LIVE_ZONE_STATS["H"]["status"]
    }
}


# ======================================================================
# FICTIONAL SCHEMATIC LAYOUT
# ======================================================================

ZONE_LAYOUT = {

    "A": {
        "x0": 3.7, "x1": 6.3,
        "y0": 6.8, "y1": 9.2
    },

    "B": {
        "x0": 0.7, "x1": 3.3,
        "y0": 6.0, "y1": 8.8
    },

    "C": {
        "x0": 6.7, "x1": 9.3,
        "y0": 5.8, "y1": 8.8
    },

    "D": {
        "x0": 0.8, "x1": 3.4,
        "y0": 2.4, "y1": 5.3
    },

    "E": {
        "x0": 6.6, "x1": 9.2,
        "y0": 2.3, "y1": 5.2
    },

    "F": {
        "x0": 3.8, "x1": 6.2,
        "y0": 0.3, "y1": 2.0
    },

    "G": {
        "x0": 3.8, "x1": 6.2,
        "y0": 4.0, "y1": 6.3
    },

    "H": {
        "x0": 7.4, "x1": 9.4,
        "y0": 0.3, "y1": 1.8
    }
}


# ======================================================================
# SESSION STATE
# ======================================================================

if "selected_base_zone" not in st.session_state:
    st.session_state.selected_base_zone = "A"


# ======================================================================
# SUMMARY CALCULATIONS
# ======================================================================

total_recent_incidents = sum(
    zone["recent_incidents"]
    for zone in BASE_ZONES.values()
)

total_high_priority = sum(
    zone["high_priority_incidents"]
    for zone in BASE_ZONES.values()
)

elevated_zones = sum(
    1
    for zone in BASE_ZONES.values()
    if zone["status"] == "ELEVATED"
)

monitor_zones = sum(
    1
    for zone in BASE_ZONES.values()
    if zone["status"] == "MONITOR"
)

normal_zones = (
    len(BASE_ZONES)
    - elevated_zones
    - monitor_zones
)


# ======================================================================
# COMMAND SUMMARY
# ======================================================================

st.markdown(
    """
    <div class="control-room-section-label">
        01 / COMMAND SUMMARY
    </div>

    <div class="control-room-section-title">
        Installation Status
    </div>
    """,
    unsafe_allow_html=True
)


metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric(
        "Operational Zones",
        len(BASE_ZONES)
    )

with metric_2:
    st.metric(
        "Recent Incidents",
        total_recent_incidents
    )

with metric_3:
    st.metric(
        "High-Priority",
        total_high_priority
    )

with metric_4:
    st.metric(
        "Elevated Zones",
        elevated_zones
    )


st.write("")


# ======================================================================
# INSTALLATION OVERVIEW HEADER
# ======================================================================

st.markdown(
    """
    <div class="control-room-section-label">
        02 / INSTALLATION OVERVIEW
    </div>

    <div class="control-room-section-title">
        Fictional Operational Layout
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Click directly on a zone to inspect it, or use the Zone Inspector "
    "dropdown as an alternate control."
)


# ======================================================================
# BUILD FIGURE
# ======================================================================

fig = go.Figure()


# ----------------------------------------------------------------------
# PERIMETER
# ----------------------------------------------------------------------

fig.add_shape(
    type="rect",
    x0=0,
    y0=0,
    x1=10,
    y1=10,
    line=dict(
        color="#61718a",
        width=3
    ),
    fillcolor="#f8fafc",
    layer="below"
)


# ----------------------------------------------------------------------
# INTERNAL ROUTES
# ----------------------------------------------------------------------

fig.add_shape(
    type="line",
    x0=5,
    y0=2,
    x1=5,
    y1=6.8,
    line=dict(
        color="#d5dce6",
        width=10
    ),
    layer="below"
)

fig.add_shape(
    type="line",
    x0=3.3,
    y0=5.6,
    x1=6.7,
    y1=5.6,
    line=dict(
        color="#d5dce6",
        width=10
    ),
    layer="below"
)


# ======================================================================
# DRAW ZONES
# ======================================================================

for zone_code, layout in ZONE_LAYOUT.items():

    zone = BASE_ZONES[zone_code]

    selected = (
        zone_code
        == st.session_state.selected_base_zone
    )


    # --------------------------------------------------------
    # STATUS VISUALS
    # --------------------------------------------------------

    if zone["status"] == "ELEVATED":

        fill = "rgba(224, 144, 64, 0.24)"
        border = "#b46f27"

    elif zone["status"] == "MONITOR":

        fill = "rgba(210, 177, 77, 0.18)"
        border = "#9c8238"

    else:

        fill = "rgba(75, 139, 103, 0.16)"
        border = "#527a63"


    if selected:

        line_width = 5
        border = "#294d7a"

    else:

        line_width = 2


    # --------------------------------------------------------
    # RECTANGLE
    # --------------------------------------------------------

    fig.add_shape(
        type="rect",
        x0=layout["x0"],
        x1=layout["x1"],
        y0=layout["y0"],
        y1=layout["y1"],
        line=dict(
            color=border,
            width=line_width
        ),
        fillcolor=fill,
        layer="below"
    )


    center_x = (
        layout["x0"]
        + layout["x1"]
    ) / 2

    center_y = (
        layout["y0"]
        + layout["y1"]
    ) / 2


    # --------------------------------------------------------
    # LABEL
    # --------------------------------------------------------

    fig.add_annotation(
        x=center_x,
        y=center_y,
        text=(
            f"<b>ZONE {zone_code}</b><br>"
            f"{zone['short_name']}<br>"
            f"<span style='font-size:10px'>"
            f"{zone['status']}"
            f"</span>"
        ),
        showarrow=False,
        align="center",
        font=dict(
            color="#22344f",
            size=12
        )
    )


    # --------------------------------------------------------
    # CLICK GRID
    # --------------------------------------------------------

    width = (
        layout["x1"]
        - layout["x0"]
    )

    height = (
        layout["y1"]
        - layout["y0"]
    )

    click_x = [
        layout["x0"] + width * 0.25,
        layout["x0"] + width * 0.50,
        layout["x0"] + width * 0.75,

        layout["x0"] + width * 0.25,
        layout["x0"] + width * 0.50,
        layout["x0"] + width * 0.75,

        layout["x0"] + width * 0.25,
        layout["x0"] + width * 0.50,
        layout["x0"] + width * 0.75
    ]

    click_y = [
        layout["y0"] + height * 0.25,
        layout["y0"] + height * 0.25,
        layout["y0"] + height * 0.25,

        layout["y0"] + height * 0.50,
        layout["y0"] + height * 0.50,
        layout["y0"] + height * 0.50,

        layout["y0"] + height * 0.75,
        layout["y0"] + height * 0.75,
        layout["y0"] + height * 0.75
    ]

    custom_data = [
        [
            zone_code,
            zone["zone_name"],
            zone["status"],
            zone["recent_incidents"],
            zone["high_priority_incidents"]
        ]
        for _ in range(
            len(click_x)
        )
    ]


    fig.add_trace(
        go.Scatter(
            x=click_x,
            y=click_y,
            mode="markers",

            marker=dict(
                size=48,
                opacity=0.01
            ),

            customdata=custom_data,

            hovertemplate=(
                "<b>%{customdata[1]}</b><br>"
                "Status: %{customdata[2]}<br>"
                "Recent Incidents: %{customdata[3]}<br>"
                "High Priority: %{customdata[4]}<br>"
                "<br>"
                "<b>Click to inspect</b>"
                "<extra></extra>"
            ),

            showlegend=False
        )
    )


# ======================================================================
# ACCESS MARKER
# ======================================================================

fig.add_annotation(
    x=5,
    y=0.05,
    text="<b>SIMULATED MAIN ACCESS</b>",
    showarrow=False,
    yshift=-18,
    font=dict(
        color="#64748b",
        size=11
    )
)


# ======================================================================
# FIGURE CONFIGURATION
# ======================================================================

fig.update_xaxes(
    visible=False,
    range=[
        -0.3,
        10.3
    ],
    fixedrange=True
)

fig.update_yaxes(
    visible=False,
    range=[
        -0.4,
        10.4
    ],
    fixedrange=True,
    scaleanchor="x",
    scaleratio=1
)

fig.update_layout(
    height=610,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    margin=dict(
        l=5,
        r=5,
        t=15,
        b=35
    ),

    hovermode="closest",
    clickmode="event+select",
    showlegend=False
)


# ======================================================================
# LAYOUT + ZONE INSPECTOR
# ======================================================================

layout_column, detail_column = st.columns(
    [
        1.85,
        1
    ],
    gap="large"
)


# ======================================================================
# SCHEMATIC
# ======================================================================

with layout_column:

    plot_event = st.plotly_chart(
        fig,
        use_container_width=True,
        key="fictional_base_layout",
        on_select="rerun",
        selection_mode="points",
        config={
            "displayModeBar": False,
            "scrollZoom": False
        }
    )


# ======================================================================
# PROCESS ZONE CLICK
# ======================================================================

try:

    selected_points = (
        plot_event.selection.points
    )

except Exception:

    selected_points = []


if selected_points:

    clicked_point = (
        selected_points[0]
    )

    clicked_customdata = (
        clicked_point.get(
            "customdata"
        )
    )

    if clicked_customdata:

        clicked_zone = (
            clicked_customdata[0]
        )

        if (
            clicked_zone in BASE_ZONES
            and clicked_zone
            != st.session_state.selected_base_zone
        ):

            st.session_state.selected_base_zone = (
                clicked_zone
            )

            st.rerun()


# ======================================================================
# ZONE INSPECTOR
# ======================================================================

with detail_column:

    st.markdown(
        """
        <div class="control-room-card">

        <div class="control-room-section-label">
            ZONE INSPECTOR
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # DROPDOWN
    # --------------------------------------------------------

    selected_zone = st.selectbox(
        "Operational Zone",

        options=list(
            BASE_ZONES.keys()
        ),

        index=list(
            BASE_ZONES.keys()
        ).index(
            st.session_state.selected_base_zone
        ),

        format_func=lambda code:
            f"Zone {code} — "
            f"{BASE_ZONES[code]['zone_name']}"
    )


    if (
        selected_zone
        != st.session_state.selected_base_zone
    ):

        st.session_state.selected_base_zone = (
            selected_zone
        )

        st.rerun()


    zone_code = (
        st.session_state.selected_base_zone
    )

    zone = (
        BASE_ZONES[zone_code]
    )


    # --------------------------------------------------------
    # ZONE TITLE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div style="
            margin-top:12px;
            font-size:0.82rem;
            color:#64748b;
            font-weight:700;
            letter-spacing:0.08em;
        ">
            ZONE {zone_code}
        </div>

        <div style="
            font-size:1.35rem;
            font-weight:700;
            color:#1d2c46;
            margin-top:2px;
            margin-bottom:12px;
        ">
            {zone['zone_name']}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STATUS BADGE
    # --------------------------------------------------------

    status_class = {

        "NORMAL":
            "status-normal",

        "MONITOR":
            "status-monitor",

        "ELEVATED":
            "status-elevated"

    }[
        zone["status"]
    ]


    st.markdown(
        f"""
        <span class="
            status-badge
            {status_class}
        ">
            {zone['status']}
        </span>
        """,
        unsafe_allow_html=True
    )


    st.write("")

    st.write(
        zone["description"]
    )

    st.divider()


    # --------------------------------------------------------
    # ZONE METRICS
    # --------------------------------------------------------

    zone_metric_1, zone_metric_2 = st.columns(
        2
    )

    with zone_metric_1:

        st.metric(
            "Recent Incidents",
            zone["recent_incidents"]
        )

    with zone_metric_2:

        st.metric(
            "High Priority",
            zone["high_priority_incidents"]
        )


    # --------------------------------------------------------
    # INCIDENT SUMMARY
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="control-room-section-label"
             style="margin-top:16px;">
            INCIDENT PROFILE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "**Most Common Incident**"
    )

    st.write(
        zone["most_common_incident"]
    )

    st.markdown(
        "**Last Recorded Incident**"
    )

    st.write(
        zone["last_incident"]
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ======================================================================
# OPERATIONAL STATUS SUMMARY
# ======================================================================

st.write("")

st.markdown(
    """
    <div class="control-room-section-label">
        03 / OPERATIONAL STATUS
    </div>

    <div class="control-room-section-title">
        Zone Readiness Summary
    </div>
    """,
    unsafe_allow_html=True
)


status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:

    st.success(
        f"NORMAL — {normal_zones} zones"
    )

with status_col2:

    st.info(
        f"MONITOR — {monitor_zones} zones"
    )

with status_col3:

    st.warning(
        f"ELEVATED — {elevated_zones} zones"
    )


# ======================================================================
# FOOTER / HUMAN OVERSIGHT
# ======================================================================

st.divider()

footer_left, footer_right = st.columns(
    [
        3,
        1
    ]
)

with footer_left:

    st.caption(
        "Decision-support information is advisory. "
        "Final operational authority remains with the authorized "
        "human operator."
    )

with footer_right:

    st.caption(
        "SIMULATED DATA"
    )


st.caption(
    f"Last interface refresh: "
    f"{datetime.now().strftime('%d %b %Y  •  %H:%M:%S')}"
)
