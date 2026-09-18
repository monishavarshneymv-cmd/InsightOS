"""
InsightOS - Modern, Human-Centered UI Styling System
Warm, welcoming, clean, and intuitive design inspired by modern SaaS (Linear, Notion, Stripe).
Guarantees 100% text contrast and readability regardless of OS/browser dark mode settings.
"""

CUSTOM_CSS = """
<style>
/* Modern Typography & Reset */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #0F172A !important;
}

/* Force light background on all Streamlit containers to prevent theme mixing */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"] {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Force dark slate text for all headings and markdown text across the entire app */
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {
    color: #0F172A !important;
    font-weight: 700 !important;
}

/* All paragraphs, labels, and text elements (excluding buttons) */
[data-testid="stMarkdownContainer"]:not(button *) p,
[data-testid="stMarkdownContainer"] li {
    color: #334155 !important;
}

/* Form labels and selectbox headers */
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] span {
    color: #0F172A !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
}

/* Inputs and Selectboxes */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
.stTextInput input,
.stSelectbox div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border-color: #CBD5E1 !important;
}

/* Clean, friendly sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    background-color: #FFFFFF !important;
    border-right: 1.5px solid #E2E8F0 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #0F172A !important;
}

/* Hide circular radio buttons to make menu look like modern SaaS tabs */
div[data-testid="stRadio"] div[data-testid="stRadioBtn"] {
    display: none !important;
}
div[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}

/* Sidebar Nav Radio Styling - Modern SaaS Menu */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 6px !important;
}

div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    background-color: #F8FAFC !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 4px !important;
    cursor: pointer !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.15s ease-in-out !important;
}

div[data-testid="stRadio"] label:hover {
    background-color: #F1F5F9 !important;
    border-color: #94A3B8 !important;
}

div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label div {
    font-size: 13.5px !important;
    font-weight: 700 !important;
    color: #1E293B !important;
    margin: 0 !important;
    line-height: 1.4 !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background-color: #EFF6FF !important;
    border-color: #2563EB !important;
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.12) !important;
}

div[data-testid="stRadio"] label:has(input:checked) p,
div[data-testid="stRadio"] label:has(input:checked) span {
    color: #1D4ED8 !important;
    font-weight: 800 !important;
}

/* Brand Header & Logo Styling */
.brand-title {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.03em !important;
    line-height: 1.2 !important;
}

.brand-blue {
    color: #2563EB !important;
}

.brand-subtitle {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    margin-top: 2px !important;
}

/* User Greeting Banner */
.welcome-banner {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 22px 26px !important;
    margin-bottom: 22px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03) !important;
}

.welcome-title {
    font-size: 24px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    margin: 0 !important;
    letter-spacing: -0.02em !important;
}

.welcome-desc {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #475569 !important;
    margin-top: 6px !important;
    margin-bottom: 0 !important;
    line-height: 1.5 !important;
}

/* Friendly KPI Metric Card */
.metric-card {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.2s ease-in-out !important;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px -2px rgba(15, 23, 42, 0.08) !important;
    border-color: #CBD5E1 !important;
}

.metric-icon-wrap {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 36px !important;
    height: 36px !important;
    border-radius: 10px !important;
    background: #F1F5F9 !important;
    font-size: 18px !important;
    margin-bottom: 10px !important;
}

.metric-title {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    margin-bottom: 4px !important;
}

.metric-num {
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.03em !important;
}

.metric-badge-good {
    display: inline-flex !important;
    align-items: center !important;
    gap: 3px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #059669 !important;
    background: #ECFDF5 !important;
    padding: 2px 8px !important;
    border-radius: 9999px !important;
    border: 1px solid #A7F3D0 !important;
    margin-top: 6px !important;
}

.metric-badge-warning {
    display: inline-flex !important;
    align-items: center !important;
    gap: 3px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #E11D48 !important;
    background: #FFF1F2 !important;
    padding: 2px 8px !important;
    border-radius: 9999px !important;
    border: 1px solid #FECDD3 !important;
    margin-top: 6px !important;
}

.metric-subtext {
    font-size: 12px !important;
    color: #64748B !important;
    margin-top: 6px !important;
}

/* Human Insight Box (Explains WHY in plain English) */
.human-insight-box {
    background: #F8FAFC !important;
    border-left: 4px solid #2563EB !important;
    border-radius: 0 12px 12px 0 !important;
    padding: 14px 18px !important;
    margin: 16px 0 !important;
    border-top: 1.5px solid #E2E8F0 !important;
    border-right: 1.5px solid #E2E8F0 !important;
    border-bottom: 1.5px solid #E2E8F0 !important;
}

.human-insight-title {
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #2563EB !important;
    margin-bottom: 4px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}

.human-insight-body {
    font-size: 13.5px !important;
    color: #1E293B !important;
    line-height: 1.6 !important;
}

/* Card Container */
.human-card {
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}

.human-card-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-bottom: 14px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid #F1F5F9 !important;
}

.human-card-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    margin: 0 !important;
}

/* Persona Badge */
.persona-pill {
    display: inline-block !important;
    padding: 4px 12px !important;
    border-radius: 9999px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
.persona-champion { background: #FEF3C7 !important; color: #92400E !important; border: 1px solid #FDE68A !important; }
.persona-loyal { background: #EFF6FF !important; color: #1E40AF !important; border: 1px solid #DBEAFE !important; }
.persona-atrisk { background: #FFF1F2 !important; color: #9F1239 !important; border: 1px solid #FECDD3 !important; }
.persona-hibernating { background: #F1F5F9 !important; color: #475569 !important; border: 1px solid #E2E8F0 !important; }

/* Friendly Navigation Buttons */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px !important;
    background-color: transparent !important;
    border-bottom: 2px solid #E2E8F0 !important;
    padding-bottom: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 18px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    background-color: transparent !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #2563EB !important;
    border-bottom: 2px solid #2563EB !important;
    font-weight: 700 !important;
}

/* Button override - Secondary / Standard Buttons */
.stButton > button,
button[data-testid="baseButton-secondary"],
[data-testid="stDownloadButton"] > button {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    border: 1.5px solid #CBD5E1 !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    padding: 8px 18px !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover,
button[data-testid="baseButton-secondary"]:hover,
[data-testid="stDownloadButton"] > button:hover {
    background-color: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #0F172A !important;
    transform: translateY(-1px) !important;
}

.stButton > button *,
button[data-testid="baseButton-secondary"] *,
[data-testid="stDownloadButton"] > button * {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Primary Button override - High Contrast Royal Blue with 100% White Text */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"],
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background-color: #2563EB !important;
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%) !important;
    border: 1.5px solid #1D4ED8 !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 14.5px !important;
    padding: 10px 22px !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: #1D4ED8 !important;
    background: #1D4ED8 !important;
    border-color: #1E40AF !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
}

/* Force 100% WHITE text on all inner elements of Primary Buttons */
.stButton > button[kind="primary"] *,
.stButton > button[data-testid="baseButton-primary"] *,
button[kind="primary"] *,
button[data-testid="baseButton-primary"] *,
.stButton > button[kind="primary"] p,
.stButton > button[data-testid="baseButton-primary"] p,
button[kind="primary"] p,
button[data-testid="baseButton-primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[data-testid="baseButton-primary"] span,
button[kind="primary"] span,
button[data-testid="baseButton-primary"] span,
.stButton > button[kind="primary"] div,
.stButton > button[data-testid="baseButton-primary"] div,
button[kind="primary"] div,
button[data-testid="baseButton-primary"] div {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Dataframe clean styling */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    border: 1px solid #E2E8F0 !important;
    overflow: hidden !important;
}
</style>
"""

# Plotly styling template with warm, readable, human-crafted colors
PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Plus Jakarta Sans, sans-serif", "color": "#334155"},
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#FFFFFF",
        "xaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"size": 11, "color": "#64748B"},
            "title": {"font": {"size": 12, "color": "#475569"}}
        },
        "yaxis": {
            "gridcolor": "#F1F5F9",
            "zerolinecolor": "#E2E8F0",
            "tickfont": {"size": 11, "color": "#64748B"},
            "title": {"font": {"size": 12, "color": "#475569"}}
        },
        "margin": {"l": 40, "r": 20, "t": 35, "b": 35},
        "colorway": ["#3B82F6", "#10B981", "#6366F1", "#F59E0B", "#F43F5E", "#8B5CF6", "#06B6D4"]
    }
}
