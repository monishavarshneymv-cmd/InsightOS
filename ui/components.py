"""
InsightOS - Human-Centered UI Components
Creates friendly, humanized metric cards, actionable takeaway boxes, and clear data guides.
"""

from typing import Optional
import streamlit as st


def render_welcome_banner(title: str, subtitle: str, badge_text: Optional[str] = None):
    """Render friendly top welcoming banner."""
    badge_html = f'<span style="background: #EFF6FF; color: #1D4ED8; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 9999px; border: 1px solid #DBEAFE; float: right;">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div class="welcome-banner">
        {badge_html}
        <h1 class="welcome-title">{title}</h1>
        <p class="welcome-desc">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_human_kpi(
    icon: str,
    title: str,
    value: str,
    badge_text: Optional[str] = None,
    badge_type: str = "good",
    subtext: Optional[str] = None
):
    """Render an individual friendly KPI card."""
    badge_html = ""
    if badge_text:
        css = "metric-badge-good" if badge_type == "good" else "metric-badge-warning"
        badge_html = f'<div class="{css}">{badge_text}</div>'

    sub_html = f'<div class="metric-subtext">{subtext}</div>' if subtext else ""

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon-wrap">{icon}</div>
        <div class="metric-title">{title}</div>
        <div class="metric-num">{value}</div>
        {badge_html}
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_insight_takeaway(text: str, title: str = "💡 Key Business Takeaway"):
    """Render clear plain English business takeaway box."""
    st.markdown(f"""
    <div class="human-insight-box">
        <div class="human-insight-title">{title}</div>
        <div class="human-insight-body">{text}</div>
    </div>
    """, unsafe_allow_html=True)
