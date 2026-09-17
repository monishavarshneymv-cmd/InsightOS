"""
InsightOS - Styling & Theme Tokens
Bespoke CSS rules crafted for an executive, editorial look and feel.
Explicitly avoids generic neon/glowing AI aesthetics in favor of crisp financial intelligence styling.
"""

CUSTOM_CSS = """
<style>
/* Base typography and background */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #0F172A;
}

/* App container */
.stApp {
    background-color: #F8FAFC;
}

/* Sidebar refinement */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #0F172A;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Clean Header / Banner */
.executive-header {
    background: #FFFFFF;
    padding: 24px 32px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.executive-title {
    font-size: 26px;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.03em;
}

.executive-subtitle {
    font-size: 14px;
    color: #64748B;
    margin-top: 6px;
    margin-bottom: 0;
}

/* KPI Card Component */
.kpi-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.kpi-card:hover {
    box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.06);
    border-color: #CBD5E1;
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin-bottom: 6px;
}

.kpi-delta-positive {
    font-size: 13px;
    font-weight: 600;
    color: #059669; /* Emerald Green */
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-delta-negative {
    font-size: 13px;
    font-weight: 600;
    color: #BE123C; /* Crimson Red */
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-delta-neutral {
    font-size: 13px;
    font-weight: 500;
    color: #64748B;
}

/* Content section box */
.content-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.content-box-title {
    font-size: 17px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Badges */
.badge-tag {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.badge-blue { background-color: #EFF6FF; color: #1D4ED8; border: 1px solid #DBEAFE; }
.badge-green { background-color: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.badge-red { background-color: #FFF1F2; color: #BE123C; border: 1px solid #FECDD3; }
.badge-amber { background-color: #FFFBEB; color: #B45309; border: 1px solid #FDE68A; }
.badge-slate { background-color: #F1F5F9; color: #334155; border: 1px solid #E2E8F0; }

/* Clean Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 600;
    color: #64748B;
    background-color: transparent;
    border: none;
}

.stTabs [aria-selected="true"] {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
}

/* Button override */
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
    border: 1px solid #CBD5E1;
    background-color: #FFFFFF;
    color: #0F172A;
    padding: 6px 16px;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    background-color: #F8FAFC;
    border-color: #94A3B8;
    color: #0F172A;
}

.stButton > button[kind="primary"] {
    background-color: #0F172A;
    color: #FFFFFF;
    border-color: #0F172A;
}

.stButton > button[kind="primary"]:hover {
    background-color: #1E293B;
    border-color: #1E293B;
}

/* Callout Box */
.executive-callout {
    border-left: 4px solid #2563EB;
    background-color: #F8FAFC;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 16px 0;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
}
</style>
"""

# Plotly styling template for editorial feel
PLOTLY_TEMPLATE = {
    "layout": {
        "font": {"family": "Inter, sans-serif", "color": "#1E293B"},
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
        "margin": {"l": 40, "r": 20, "t": 40, "b": 40},
        "colorway": ["#1E293B", "#2563EB", "#059669", "#D97706", "#BE123C", "#8B5CF6", "#0D9488"]
    }
}
