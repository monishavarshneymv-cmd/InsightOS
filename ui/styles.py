"""
InsightOS - Modern, Human-Centered UI Styling System
Warm, welcoming, clean, and intuitive design inspired by modern SaaS (Linear, Notion, Stripe).
Free from generic dark neon AI cliches; optimized for readability, warmth, and business clarity.
"""

CUSTOM_CSS = """
<style>
/* Modern Typography & Reset */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1E293B;
}

/* Background canvas */
.stApp {
    background-color: #F8FAFC;
}

/* Clean, friendly sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    padding-top: 1.5rem;
}

/* User Greeting Banner */
.welcome-banner {
    background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
}

.welcome-title {
    font-size: 24px;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.welcome-desc {
    font-size: 14px;
    color: #64748B;
    margin-top: 6px;
    margin-bottom: 0;
    line-height: 1.5;
}

/* Friendly KPI Metric Card */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease-in-out;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px -2px rgba(15, 23, 42, 0.08);
    border-color: #CBD5E1;
}

.metric-icon-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #F1F5F9;
    font-size: 18px;
    margin-bottom: 12px;
}

.metric-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 4px;
}

.metric-num {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
}

.metric-badge-good {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-size: 12px;
    font-weight: 700;
    color: #059669;
    background: #ECFDF5;
    padding: 2px 8px;
    border-radius: 9999px;
    margin-top: 6px;
}

.metric-badge-warning {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-size: 12px;
    font-weight: 700;
    color: #E11D48;
    background: #FFF1F2;
    padding: 2px 8px;
    border-radius: 9999px;
    margin-top: 6px;
}

.metric-subtext {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 6px;
}

/* Human Insight Box (Explains WHY in plain English) */
.human-insight-box {
    background: #F8FAFC;
    border-left: 4px solid #3B82F6;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin: 14px 0;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
}

.human-insight-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #2563EB;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.human-insight-body {
    font-size: 13.5px;
    color: #334155;
    line-height: 1.5;
}

/* Card Container */
.human-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.human-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #F1F5F9;
}

.human-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
}

/* Persona Badge */
.persona-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
}
.persona-champion { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.persona-loyal { background: #EFF6FF; color: #1E40AF; border: 1px solid #DBEAFE; }
.persona-atrisk { background: #FFF1F2; color: #9F1239; border: 1px solid #FECDD3; }
.persona-hibernating { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }

/* Friendly Navigation Buttons */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: transparent;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 2px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    background-color: transparent;
    border: none;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #2563EB !important;
    border-bottom: 2px solid #2563EB !important;
    font-weight: 700 !important;
}

/* Button override */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 13.5px;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
    color: #1E293B;
    padding: 8px 18px;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background-color: #F8FAFC;
    border-color: #94A3B8;
    color: #0F172A;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] {
    background: #0F172A;
    color: #FFFFFF;
    border-color: #0F172A;
}

.stButton > button[kind="primary"]:hover {
    background: #1E293B;
    border-color: #1E293B;
}

/* Dataframe clean styling */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    overflow: hidden;
}

/* Sidebar Nav Radio Styling - Clear Text & High Visibility */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    gap: 8px !important;
}

div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    background-color: #F8FAFC !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 6px !important;
    cursor: pointer !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.15s ease-in-out !important;
}

div[data-testid="stRadio"] label:hover {
    background-color: #F1F5F9 !important;
    border-color: #94A3B8 !important;
}

/* Radio text visibility guarantee */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label div {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    opacity: 1 !important;
    visibility: visible !important;
    line-height: 1.4 !important;
}

/* Selected item styling */
div[data-testid="stRadio"] label:has(input:checked) {
    background-color: #EFF6FF !important;
    border-color: #2563EB !important;
    box-shadow: 0 2px 4px rgba(37, 99, 235, 0.15) !important;
}

div[data-testid="stRadio"] label:has(input:checked) p,
div[data-testid="stRadio"] label:has(input:checked) span {
    color: #1D4ED8 !important;
    font-weight: 800 !important;
}

/* Sidebar universal text contrast */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #0F172A !important;
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
