import streamlit as st

def gradient_header(title: str, subtitle: str = None):
    """Render a futuristic gradient header with optional subtitle."""
    sub_html = f"<p style='color: #94A3B8; margin-top: -10px; font-size: 1.05rem; margin-bottom: 1.8rem;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div>
        <h1 class='gradient-text' style='font-size: 2.8rem; margin-bottom: 0.2rem; font-family: "Outfit", sans-serif; line-height: 1.2;'>{title}</h1>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def card(title: str, value: str, description: str = None, icon: str = None, border_color: str = "#6C63FF"):
    """
    Render a clean glassmorphic dashboard card with a colored left-border,
    icon indicator, and optional helper text.
    """
    icon_html = f"<div style='font-size: 1.8rem; margin-right: 16px; min-width: 36px; text-align: center;'>{icon}</div>" if icon else ""
    desc_html = f"<div style='color: #94A3B8; font-size: 0.8rem; margin-top: 4px;'>{description}</div>" if description else ""
    
    st.markdown(f"""
    <div style='
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 4px solid {border_color};
        border-radius: 10px;
        padding: 16px 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
    '>
        {icon_html}
        <div style='flex-grow: 1;'>
            <div style='color: #94A3B8; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;'>{title}</div>
            <div style='color: #FFFFFF; font-size: 1.6rem; font-weight: 700; font-family: "Outfit", sans-serif; line-height: 1.25; margin-top: 2px;'>{value}</div>
            {desc_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_glass_box(html_content: str):
    """Wrap content string inside a glassmorphic container layout."""
    st.markdown(f"""
    <div class="glass-card">
        {html_content}
    </div>
    """, unsafe_allow_html=True)

def render_stat_tile(title: str, value: str, is_accent: bool = False):
    """
    Inline HTML segment for simple dashboard tiles.
    Returns a HTML string rather than writing directly to Streamlit,
    which is useful for side-by-side flex layouts.
    """
    accent_class = "stat-accent" if is_accent else ""
    return f"""
    <div class="stat-card">
        <div class="stat-title">{title}</div>
        <div class="stat-value {accent_class}">{value}</div>
    </div>
    """
