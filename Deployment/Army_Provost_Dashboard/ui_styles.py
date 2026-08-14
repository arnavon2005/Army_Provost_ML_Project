
import streamlit as st


# ======================================================================
# CENTRALIZED APPLICATION CSS
# ======================================================================

APP_CSS = """
<style>

/* ============================================================
   GLOBAL APPLICATION
   ============================================================ */

.stApp {
    background-color: #f4f7fb;
    color: #172033;
}


/* ============================================================
   MAIN CONTENT AREA
   ============================================================ */

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b1628 0%,
            #101f36 100%
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}


[data-testid="stSidebar"] * {
    color: #eef4ff;
}


[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12);
}


[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #aebbd0;
}


/* ============================================================
   SIDEBAR NAVIGATION
   ============================================================ */

[data-testid="stSidebarNav"] {
    padding-top: 0.5rem;
}


[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin-bottom: 4px;
    transition: all 0.18s ease;
}


[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255,255,255,0.08);
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1 {
    color: #15233b;
    font-weight: 700;
    letter-spacing: -0.02em;
}


h2,
h3 {
    color: #20314d;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow:
        0 4px 14px rgba(25, 43, 72, 0.05);
}


[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 600;
}


[data-testid="stMetricValue"] {
    color: #172033;
    font-weight: 700;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    border: none;
    font-weight: 600;
    transition: all 0.18s ease;
}


.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px);
}


/* ============================================================
   INPUTS
   ============================================================ */

[data-baseweb="input"] > div,
[data-baseweb="select"] > div {
    border-radius: 10px;
}


textarea,
input {
    border-radius: 10px !important;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {
    font-weight: 600;
}


/* ============================================================
   DATAFRAMES / TABLES
   ============================================================ */

[data-testid="stDataFrame"] {
    border: 1px solid #e4eaf2;
    border-radius: 12px;
    overflow: hidden;
    background: #ffffff;
}


/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #ffffff;
}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ============================================================
   CUSTOM CONTROL ROOM COMPONENTS
   ============================================================ */

.control-room-header {
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 22px;
    box-shadow:
        0 4px 18px rgba(25, 43, 72, 0.05);
}


.control-room-eyebrow {
    color: #64748b;
    font-size: 0.80rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 6px;
}


.control-room-title {
    color: #172033;
    font-size: 1.85rem;
    font-weight: 750;
    margin: 0;
}


.control-room-subtitle {
    color: #64748b;
    margin-top: 6px;
    margin-bottom: 0;
}


.control-room-card {
    background: #ffffff;
    border: 1px solid #e3e9f2;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow:
        0 4px 14px rgba(25, 43, 72, 0.04);
}


.control-room-section-label {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}


.control-room-section-title {
    color: #1d2c46;
    font-size: 1.20rem;
    font-weight: 700;
    margin-bottom: 12px;
}


.status-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
}


.status-normal {
    background: #e8f6ee;
    color: #217346;
}


.status-monitor {
    background: #fff6df;
    color: #8a6514;
}


.status-elevated {
    background: #fff0e6;
    color: #a14c16;
}


.prototype-banner {
    background: #edf3fb;
    border: 1px solid #d6e2f2;
    border-left: 4px solid #486b99;
    border-radius: 10px;
    padding: 12px 14px;
    color: #324764;
    margin-bottom: 18px;
}


/* ============================================================
   STREAMLIT DEFAULT CHROME
   ============================================================ */

header[data-testid="stHeader"] {
    background: rgba(244,247,251,0.92);
}


/* ============================================================
   SMALL SCREEN SUPPORT
   ============================================================ */

@media (max-width: 900px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .control-room-title {
        font-size: 1.5rem;
    }
}

</style>
"""


# ======================================================================
# APPLY GLOBAL STYLES
# ======================================================================

def apply_app_styles():
    """
    Apply the shared Dashboard V1.1 visual system.
    """

    st.markdown(
        APP_CSS,
        unsafe_allow_html=True
    )


# ======================================================================
# SHARED PAGE HEADER
# ======================================================================

def render_page_header(
    eyebrow,
    title,
    subtitle=""
):
    """
    Render a consistent page header across Dashboard V1.1.
    """

    subtitle_html = (
        f'<p class="control-room-subtitle">{subtitle}</p>'
        if subtitle
        else ""
    )

    header_html = (
        f'<div class="control-room-header">'
        f'<div class="control-room-eyebrow">{eyebrow}</div>'
        f'<div class="control-room-title">{title}</div>'
        f'{subtitle_html}'
        f'</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True
    )


# ======================================================================
# SHARED PROTOTYPE BANNER
# ======================================================================

def render_prototype_banner(message):
    """
    Render a consistent academic-prototype / simulation notice.
    """

    banner_html = (
        f'<div class="prototype-banner">'
        f'{message}'
        f'</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True
    )
