"""
InsightOS - Reusable UI Components
Generates clean HTML metric cards, executive badge tags, callout banners, and data displays.
"""

from typing import Optional
import streamlit as st


def render_executive_header(title: str, subtitle: str, badge_text: Optional[str] = "InsightOS Enterprise"):
    """Render top page header banner with crisp styling."""
    badge_html = f'<span class="badge-tag badge-slate" style="float: right;">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div class="executive-header">
        {badge_html}
        <h1 class="executive-title">{title}</h1>
        <p class="executive-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_type: str = "positive",
    subtext: Optional[str] = None
):
    """Render an individual executive KPI card."""
    delta_html = ""
    if delta:
        css_class = {
            "positive": "kpi-delta-positive",
            "negative": "kpi-delta-negative",
            "neutral": "kpi-delta-neutral"
        }.get(delta_type, "kpi-delta-neutral")
        icon = "↑ " if delta_type == "positive" else ("↓ " if delta_type == "negative" else "• ")
        delta_html = f'<div class="{css_class}">{icon}{delta}</div>'

    subtext_html = f'<div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">{subtext}</div>' if subtext else ""

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
        {subtext_html}
    </div>
    """, unsafe_allow_html=True)


def render_callout(text: str, title: str = "Executive Insight", tone: str = "info"):
    """Render custom executive callout box."""
    border_color = "#2563EB" if tone == "info" else ("#059669" if tone == "success" else "#BE123C")
    st.markdown(f"""
    <div class="executive-callout" style="border-left-color: {border_color};">
        <div style="font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; color: #334155; margin-bottom: 4px;">
            {title}
        </div>
        <div style="font-size: 14px; color: #1E293B; line-height: 1.5;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)
