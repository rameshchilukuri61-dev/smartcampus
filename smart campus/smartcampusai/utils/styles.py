"""
SmartCampusAI — Premium Design System v2
==========================================
Official glassmorphism dark theme with professional typography,
hero sections, image support, animated components, and a polished
corporate academic aesthetic.
"""

import streamlit as st
import os

# ── Asset path helper ─────────────────────────────────────────
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def asset(filename: str) -> str:
    """Returns the absolute path to an asset file."""
    return os.path.join(ASSETS_DIR, filename)


def apply_custom_css():
    """
    Injects the full SmartCampusAI v2 global design system.
    Professional dark theme with glassmorphism, animations,
    official header/footer, and responsive components.
    """
    st.markdown(
        """
        <style>
        /* ════════════════════════════════════════════════════════
           TYPOGRAPHY & BASE
        ════════════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stApp"] {
            font-family: 'Inter', sans-serif !important;
            background:
                radial-gradient(ellipse at 20% 20%, rgba(67, 56, 202, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(124, 58, 237, 0.07) 0%, transparent 50%),
                linear-gradient(160deg, #04050c 0%, #080b18 35%, #0c0f24 65%, #110a20 100%)
                !important;
            background-attachment: fixed !important;
            color: #e2e8f0 !important;
            min-height: 100vh;
        }

        /* ── Hide Streamlit default chrome ───────────────────── */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stToolbar"] { display: none; }

        /* ════════════════════════════════════════════════════════
           OFFICIAL TOP HEADER BAR
        ════════════════════════════════════════════════════════ */
        .official-header {
            background: linear-gradient(90deg,
                rgba(6, 8, 20, 0.98) 0%,
                rgba(15, 12, 35, 0.98) 50%,
                rgba(6, 8, 20, 0.98) 100%);
            border-bottom: 1px solid rgba(99, 102, 241, 0.25);
            padding: 14px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            backdrop-filter: blur(20px);
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 4px 30px rgba(0,0,0,0.4);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .header-logo-text {
            font-size: 1.35rem;
            font-weight: 800;
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 60%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.3px;
        }

        .header-tagline {
            font-size: 0.72rem;
            color: #4b5563;
            font-weight: 400;
            letter-spacing: 0.5px;
        }

        .header-nav {
            display: flex;
            gap: 6px;
        }

        .nav-chip {
            padding: 6px 16px;
            border-radius: 99px;
            font-size: 0.82rem;
            font-weight: 500;
            color: #94a3b8;
            border: 1px solid rgba(255,255,255,0.07);
            background: rgba(255,255,255,0.04);
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
            letter-spacing: 0.2px;
        }

        .nav-chip:hover {
            color: #c4b5fd;
            border-color: rgba(129, 140, 248, 0.4);
            background: rgba(99, 102, 241, 0.1);
        }

        .nav-chip.active {
            color: #fff;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            border-color: transparent;
        }

        /* ════════════════════════════════════════════════════════
           HERO SECTION
        ════════════════════════════════════════════════════════ */
        .hero-section {
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 36px;
            box-shadow:
                0 25px 60px rgba(0,0,0,0.6),
                0 0 0 1px rgba(255,255,255,0.04);
        }

        .hero-image-container {
            width: 100%;
            height: 340px;
            object-fit: cover;
            display: block;
            filter: brightness(0.7) saturate(1.2);
        }

        .hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                135deg,
                rgba(4, 5, 12, 0.85) 0%,
                rgba(15, 12, 40, 0.60) 50%,
                rgba(99, 38, 130, 0.30) 100%
            );
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 48px 56px;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(129, 140, 248, 0.4);
            border-radius: 99px;
            padding: 6px 16px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #a5b4fc;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 16px;
            width: fit-content;
        }

        .hero-title {
            font-family: 'Playfair Display', serif !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            line-height: 1.15 !important;
            margin-bottom: 14px !important;
            text-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
        }

        .hero-title span {
            background: linear-gradient(135deg, #a5b4fc 0%, #e0a7ff 50%, #f9a8d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            color: #cbd5e1;
            max-width: 520px;
            line-height: 1.7;
            font-weight: 400;
        }

        .hero-cta-row {
            display: flex;
            gap: 14px;
            margin-top: 28px;
            flex-wrap: wrap;
        }

        .cta-primary {
            padding: 13px 32px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 700;
            color: #fff;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            border: none;
            cursor: pointer;
            letter-spacing: 0.3px;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .cta-secondary {
            padding: 13px 32px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #c4b5fd;
            background: rgba(99, 102, 241, 0.12);
            border: 1px solid rgba(129, 140, 248, 0.35);
            cursor: pointer;
            letter-spacing: 0.3px;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        /* ════════════════════════════════════════════════════════
           GLASSMORPHISM CARDS
        ════════════════════════════════════════════════════════ */
        .glass-card {
            background: rgba(10, 13, 28, 0.60);
            border-radius: 20px;
            padding: 28px 30px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            margin-bottom: 20px;
            box-shadow:
                0 8px 40px rgba(0,0,0,0.5),
                inset 0 1px 0 rgba(255,255,255,0.06);
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(129,140,248,0.4), transparent);
        }

        .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(129, 140, 248, 0.22);
            box-shadow:
                0 24px 60px rgba(0,0,0,0.55),
                0 0 0 1px rgba(129,140,248,0.12),
                inset 0 1px 0 rgba(255,255,255,0.09);
        }

        /* Feature card with image area */
        .feature-card {
            background: rgba(10, 13, 28, 0.60);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(20px);
            overflow: hidden;
            margin-bottom: 20px;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 40px rgba(0,0,0,0.5);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(129, 140, 248, 0.25);
        }

        .feature-card-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            display: block;
            filter: brightness(0.75) saturate(1.3);
        }

        .feature-card-body {
            padding: 22px 24px;
        }

        /* ════════════════════════════════════════════════════════
           STAT CARDS & BADGES
        ════════════════════════════════════════════════════════ */
        .stat-card {
            background: rgba(7, 10, 22, 0.75);
            border-radius: 14px;
            padding: 16px 20px;
            border-left: 3px solid #6366f1;
            margin-bottom: 12px;
            transition: border-color 0.2s ease;
        }

        .stat-card.green  { border-left-color: #10b981; }
        .stat-card.purple { border-left-color: #a855f7; }
        .stat-card.pink   { border-left-color: #ec4899; }
        .stat-card.amber  { border-left-color: #f59e0b; }
        .stat-card.red    { border-left-color: #ef4444; }
        .stat-card.blue   { border-left-color: #818cf8; }

        .metric-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 99px;
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }

        .badge-green  { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
        .badge-amber  { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
        .badge-red    { background: rgba(239,68,68,0.12);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
        .badge-purple { background: rgba(168,85,247,0.12); color: #c084fc; border: 1px solid rgba(168,85,247,0.3); }
        .badge-blue   { background: rgba(129,140,248,0.12);color: #818cf8; border: 1px solid rgba(129,140,248,0.3); }

        /* ════════════════════════════════════════════════════════
           GRADIENT TEXT
        ════════════════════════════════════════════════════════ */
        .gradient-text {
            background: linear-gradient(135deg, #818cf8 0%, #c084fc 45%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        /* ════════════════════════════════════════════════════════
           OFFICIAL SECTION HEADINGS
        ════════════════════════════════════════════════════════ */
        .section-heading {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .section-heading-bar {
            width: 4px;
            height: 28px;
            border-radius: 4px;
            background: linear-gradient(180deg, #6366f1, #a855f7);
            flex-shrink: 0;
        }

        .section-heading-text {
            font-size: 1.15rem;
            font-weight: 700;
            color: #e2e8f0;
            letter-spacing: -0.2px;
        }

        /* ════════════════════════════════════════════════════════
           METRIC PANELS (Top KPI Strip)
        ════════════════════════════════════════════════════════ */
        .kpi-card {
            background: rgba(10, 13, 28, 0.70);
            border-radius: 18px;
            padding: 22px 24px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }

        .kpi-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            border-radius: 2px 2px 0 0;
        }

        .kpi-card.indigo::after  { background: linear-gradient(90deg, #6366f1, #818cf8); }
        .kpi-card.purple::after  { background: linear-gradient(90deg, #7c3aed, #a855f7); }
        .kpi-card.pink::after    { background: linear-gradient(90deg, #be185d, #ec4899); }
        .kpi-card.emerald::after { background: linear-gradient(90deg, #059669, #10b981); }

        .kpi-value {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
            margin: 8px 0 4px;
        }

        .kpi-label {
            font-size: 0.78rem;
            color: #64748b;
            font-weight: 500;
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }

        .kpi-icon {
            font-size: 1.6rem;
            margin-bottom: 4px;
        }

        /* ════════════════════════════════════════════════════════
           ANNOUNCEMENT CARDS
        ════════════════════════════════════════════════════════ */
        .ann-card {
            background: rgba(7, 10, 22, 0.70);
            border-radius: 14px;
            padding: 16px 18px;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-left: 3px solid #64748b;
            transition: all 0.2s ease;
        }

        .ann-card:hover { background: rgba(15, 20, 40, 0.80); }
        .ann-card.high   { border-left-color: #ef4444; }
        .ann-card.medium { border-left-color: #f59e0b; }
        .ann-card.low    { border-left-color: #10b981; }

        /* ════════════════════════════════════════════════════════
           SIDEBAR
        ════════════════════════════════════════════════════════ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg,
                rgba(4, 5, 12, 0.98) 0%,
                rgba(8, 10, 20, 0.98) 100%) !important;
            border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
        }

        [data-testid="stSidebar"] * {
            font-family: 'Inter', sans-serif !important;
        }

        .sidebar-logo {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            border-radius: 14px;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            margin: 0 auto 12px;
            box-shadow: 0 8px 20px rgba(99,102,241,0.4);
        }

        .avatar-circle {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 800;
            color: #fff;
            margin: 0 auto 12px;
            border: 2px solid rgba(129,140,248,0.35);
            box-shadow: 0 4px 20px rgba(99,102,241,0.3);
        }

        /* ════════════════════════════════════════════════════════
           INPUTS & FORMS
        ════════════════════════════════════════════════════════ */
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            background-color: rgba(7, 10, 22, 0.90) !important;
            color: #f1f5f9 !important;
            font-family: 'Inter', sans-serif !important;
        }

        div[data-baseweb="input"],
        div[data-baseweb="textarea"] {
            background-color: rgba(7, 10, 22, 0.90) !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease;
        }

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="textarea"]:focus-within {
            border-color: rgba(99,102,241,0.6) !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        }

        /* ── Label styling ─────────────────────────────────── */
        .stTextInput label, .stSelectbox label, .stTextArea label {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
        }

        /* ════════════════════════════════════════════════════════
           BUTTONS
        ════════════════════════════════════════════════════════ */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #6d28d9 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 28px !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 20px rgba(79,70,229,0.4) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100%;
            font-family: 'Inter', sans-serif !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 35px rgba(109,40,217,0.55) !important;
            background: linear-gradient(135deg, #5a52ff 0%, #7c3aed 100%) !important;
        }

        .stButton > button:active { transform: translateY(1px) !important; }

        /* ════════════════════════════════════════════════════════
           CHAT BUBBLES
        ════════════════════════════════════════════════════════ */
        .chat-user {
            background: linear-gradient(135deg, rgba(79,70,229,0.18), rgba(109,40,217,0.12));
            border-radius: 18px 18px 4px 18px;
            padding: 14px 18px;
            margin-bottom: 12px;
            border: 1px solid rgba(79,70,229,0.28);
            color: #c7d2fe;
            font-size: 0.9rem;
        }

        .chat-assistant {
            background: rgba(10, 14, 30, 0.75);
            border-radius: 18px 18px 18px 4px;
            padding: 14px 18px;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.07);
            color: #e2e8f0;
            font-size: 0.9rem;
        }

        /* ════════════════════════════════════════════════════════
           OFFICIAL FOOTER
        ════════════════════════════════════════════════════════ */
        .official-footer {
            margin-top: 64px;
            border-top: 1px solid rgba(255,255,255,0.06);
            padding: 32px 0 24px;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 32px;
        }

        .footer-brand-name {
            font-size: 1.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .footer-desc {
            font-size: 0.83rem;
            color: #475569;
            line-height: 1.7;
            max-width: 300px;
        }

        .footer-col-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: #64748b;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }

        .footer-link {
            display: block;
            font-size: 0.83rem;
            color: #475569;
            margin-bottom: 8px;
            text-decoration: none;
            transition: color 0.2s;
        }

        .footer-link:hover { color: #818cf8; }

        .footer-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.04);
            font-size: 0.78rem;
            color: #334155;
        }

        /* Simple fallback footer for non-hero pages */
        .custom-footer {
            text-align: center;
            font-size: 0.8rem;
            color: #334155;
            margin-top: 60px;
            padding: 24px 0 16px;
            border-top: 1px solid rgba(255,255,255,0.05);
            letter-spacing: 0.3px;
        }

        /* ════════════════════════════════════════════════════════
           DIVIDERS & MISC
        ════════════════════════════════════════════════════════ */
        hr {
            border: none !important;
            border-top: 1px solid rgba(255,255,255,0.06) !important;
            margin: 28px 0 !important;
        }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.15); }
        ::-webkit-scrollbar-thumb {
            background: rgba(99,102,241,0.35);
            border-radius: 99px;
        }

        /* ── Image overrides ───────────────────────────────── */
        .stImage img {
            border-radius: 16px !important;
            box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
        }

        /* ── Progress bars ─────────────────────────────────── */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #6366f1, #a855f7) !important;
            border-radius: 99px !important;
        }

        /* ── Info/Warning/Error messages ───────────────────── */
        .stAlert {
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.07) !important;
        }

        /* ── Page link styling ─────────────────────────────── */
        [data-testid="stPageLink"] a {
            color: #818cf8 !important;
            font-weight: 500 !important;
            text-decoration: none;
            transition: color 0.2s;
        }

        [data-testid="stPageLink"] a:hover { color: #c084fc !important; }

        /* ── Spinner ───────────────────────────────────────── */
        .stSpinner > div {
            border-top-color: #6366f1 !important;
        }

        /* Login/Register form card */
        .auth-card {
            background: rgba(8, 11, 24, 0.80);
            border-radius: 24px;
            padding: 36px 38px;
            border: 1px solid rgba(255,255,255,0.07);
            box-shadow:
                0 20px 60px rgba(0,0,0,0.6),
                inset 0 1px 0 rgba(255,255,255,0.06);
            backdrop-filter: blur(24px);
            position: relative;
            overflow: hidden;
        }

        .auth-card::before {
            content: '';
            position: absolute;
            top: 0; left: 10%; right: 10%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), transparent);
        }

        /* Divider with label */
        .divider-label {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 20px 0;
            color: #374151;
            font-size: 0.78rem;
            font-weight: 500;
        }

        .divider-label::before, .divider-label::after {
            content: '';
            flex: 1;
            height: 1px;
            background: rgba(255,255,255,0.06);
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_official_header(active_page: str = "home", user=None):
    """Renders the sticky top navigation header."""
    pages = {
        "home":      ("🏠 Home",      "app"),
        "login":     ("🔒 Login",     "pages/1_Login"),
        "register":  ("📝 Register",  "pages/2_Register"),
        "dashboard": ("📊 Dashboard", "pages/3_Dashboard"),
    }

    nav_items = ""
    for key, (label, _) in pages.items():
        cls = "nav-chip active" if key == active_page else "nav-chip"
        nav_items += f'<span class="{cls}">{label}</span>'

    user_info = ""
    if user:
        initial = user["username"][0].upper()
        user_info = f"""
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#4f46e5,#7c3aed);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.85rem;color:#fff;">{initial}</div>
            <span style="font-size:0.85rem;color:#94a3b8;font-weight:500;">{user['username']}</span>
        </div>
        """

    st.markdown(
        f"""
        <div class="official-header">
            <div class="header-brand">
                <div style="width:40px;height:40px;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;">🏫</div>
                <div>
                    <div class="header-logo-text">SmartCampusAI</div>
                    <div class="header-tagline">INTELLIGENT ACADEMIC PORTAL</div>
                </div>
            </div>
            <div class="header-nav">{nav_items}</div>
            {user_info}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_official_footer():
    """Renders the multi-column official footer."""
    st.markdown(
        """
        <div class="official-footer">
            <div class="footer-grid">
                <div>
                    <div class="footer-brand-name">🏫 SmartCampusAI</div>
                    <p class="footer-desc">
                        An intelligent academic management platform built to empower students and faculty
                        with AI-driven insights, real-time campus intelligence, and seamless scheduling tools.
                    </p>
                </div>
                <div>
                    <div class="footer-col-title">Platform</div>
                    <span class="footer-link">📊 Dashboard</span>
                    <span class="footer-link">🤖 AI Assistant</span>
                    <span class="footer-link">📅 Schedule</span>
                    <span class="footer-link">📈 Analytics</span>
                </div>
                <div>
                    <div class="footer-col-title">Support</div>
                    <span class="footer-link">📖 Documentation</span>
                    <span class="footer-link">🔒 Privacy Policy</span>
                    <span class="footer-link">⚖️ Terms of Use</span>
                    <span class="footer-link">📞 Contact IT</span>
                </div>
            </div>
            <div class="footer-bottom">
                <span>© 2026 SmartCampusAI — All Rights Reserved</span>
                <span>Version 2.0.0 · Powered by Streamlit &amp; AI</span>
                <span>🔒 ISO 27001 Compliant</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_heading(icon: str, title: str):
    """Renders an official section heading with left accent bar."""
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="section-heading-bar"></div>
            <span class="section-heading-text">{icon} {title}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
