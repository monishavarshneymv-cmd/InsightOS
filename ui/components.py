"""
InsightOS - Human-Centered UI Components
Creates friendly, humanized metric cards, actionable takeaway boxes, and clear data guides.
Guarantees 100% text contrast and visibility regardless of OS/browser dark mode settings.
"""

from typing import Optional
import streamlit as st


def render_welcome_banner(title: str, subtitle: str, badge_text: Optional[str] = None):
    """Render friendly top welcoming banner with guaranteed high-contrast text."""
    badge_html = (
        f'<span style="background: #EFF6FF; color: #1D4ED8 !important; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; border: 1px solid #DBEAFE; white-space: nowrap;">'
        f'{badge_text}'
        f'</span>'
    ) if badge_text else ""

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 16px; padding: 22px 26px; margin-bottom: 22px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; gap: 12px;">
            <div style="font-size: 24px; font-weight: 800; color: #0F172A !important; letter-spacing: -0.02em; line-height: 1.2;">
                {title}
            </div>
            <div>{badge_html}</div>
        </div>
        <div style="font-size: 14px; font-weight: 500; color: #475569 !important; line-height: 1.5;">
            {subtitle}
        </div>
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
    """Render an individual friendly KPI card with guaranteed contrast."""
    badge_html = ""
    if badge_text:
        bg = "#ECFDF5" if badge_type == "good" else "#FFF1F2"
        fg = "#059669" if badge_type == "good" else "#E11D48"
        border = "#A7F3D0" if badge_type == "good" else "#FECDD3"
        badge_html = f'<div style="display: inline-flex; align-items: center; gap: 3px; font-size: 12px; font-weight: 700; color: {fg} !important; background: {bg}; padding: 2px 8px; border-radius: 9999px; border: 1px solid {border}; margin-top: 6px;">{badge_text}</div>'

    sub_html = f'<div style="font-size: 12px; color: #64748B !important; margin-top: 6px;">{subtext}</div>' if subtext else ""

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 14px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); transition: all 0.2s ease;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 10px; background: #F1F5F9; font-size: 18px; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 13px; font-weight: 600; color: #64748B !important; margin-bottom: 4px;">{title}</div>
        <div style="font-size: 26px; font-weight: 800; color: #0F172A !important; letter-spacing: -0.03em;">{value}</div>
        {badge_html}
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_insight_takeaway(text: str, title: str = "💡 Key Business Takeaway"):
    """Render clear plain English business takeaway box with solid contrast."""
    st.markdown(f"""
    <div style="background: #F8FAFC; border-left: 4px solid #2563EB; border-radius: 0 12px 12px 0; padding: 14px 18px; margin: 16px 0; border-top: 1.5px solid #E2E8F0; border-right: 1.5px solid #E2E8F0; border-bottom: 1.5px solid #E2E8F0;">
        <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #2563EB !important; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            {title}
        </div>
        <div style="font-size: 13.5px; color: #1E293B !important; line-height: 1.6;">
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)
