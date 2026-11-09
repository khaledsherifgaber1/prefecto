import base64
import csv
import os
import re
import time
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto | Italian Luxury Tableware",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def get_image_base64(file_path: str):
    """Return the image as a base64 string, or None if the file is missing."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


def html(block: str):
    """Render HTML safely: strip indentation and blank lines so Markdown
    never mistakes indented HTML for a code block."""
    cleaned = "\n".join(l.strip() for l in block.strip().splitlines() if l.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def image_tag(b64, alt, filename, css_class="pf-img"):
    if b64:
        return f'<img class="{css_class}" src="data:image/jpeg;base64,{b64}" alt="{alt}"/>'
    return f'<div class="pf-placeholder">Add <b>{filename}</b> to your project folder</div>'


hero_b64 = get_image_base64("hero_banner.jpeg")
product_b64 = get_image_base64("product_cutlery.jpeg")
teaser_b64 = get_image_base64("teaser_unbreakable.jpeg")

# ---------------------------------------------------------
# 2. DESIGN SYSTEM (CSS)
#    Navy  #0A1B3A  – brand, depth
#    Stone #F6F4F0  – page background (soft, warm white)
#    Steel #8A94A6  – secondary text / hairlines
#    Green #00A859  – used only for "verified" moments
# ---------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@300;400;500;600&display=swap');

:root {
    --navy: #0A1B3A;
    --navy-deep: #050E1E;
    --stone: #F6F4F0;
    --paper: #FFFFFF;
    --ink: #14213D;
    --steel: #6B7587;
    --line: #E2DED6;
    --green: #00A859;
}

/* ---- Strip Streamlit chrome ---- */
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden; }

html { scroll-behavior: smooth; }
.stApp { background: var(--stone); color: var(--ink); font-family: 'Jost', sans-serif; }
.block-container { max-width: 1240px; padding: 0 2rem 3rem 2rem !important; }
h1, h2, h3, h4 { font-family: 'Cormorant Garamond', serif !important; color: var(--navy); letter-spacing: -0.01em; }
p, label, span, div { font-family: 'Jost', sans-serif; }

/* ---- Navigation ---- */
.pf-nav {
    position: sticky; top: 0; z-index: 50;
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 4px; margin-bottom: 28px;
    background: rgba(246,244,240,0.92); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--line);
}
.pf-logo { font-family: 'Cormorant Garamond', serif; font-size: 1.9rem; font-weight: 700; color: var(--navy); letter-spacing: 0.01em; }
.pf-logo b { color: var(--green); font-weight: 700; }
.pf-links { display: flex; gap: 38px; align-items: center; }
.pf-links a {
    color: var(--ink) !important; text-decoration: none !important;
    font-size: 0.92rem; font-weight: 400; letter-spacing: 0.02em;
    padding: 4px 0; border-bottom: 1px solid transparent; transition: border-color .2s;
}
.pf-links a:hover { border-bottom-color: var(--navy); }
.pf-links a.pf-cta {
    background: var(--navy); color: #fff !important; padding: 10px 22px; border-radius: 999px; border: none;
}
.pf-links a.pf-cta:hover { background: #12306a; }

/* ---- Hero ---- */
.pf-hero-text { padding: 34px 10px 0 4px; }
.pf-hero-text h1 {
    font-size: clamp(2.8rem, 5.4vw, 5rem); line-height: 1.02; font-weight: 600;
    margin: 0 0 22px 0; color: var(--navy);
}
.pf-hero-text p.lead { font-size: 1.12rem; line-height: 1.7; color: var(--steel); max-width: 470px; font-weight: 300; margin-bottom: 30px; }
.pf-hero-actions { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 38px; }
.pf-btn {
    display: inline-block; padding: 14px 30px; border-radius: 999px; font-weight: 500; font-size: 0.95rem;
    text-decoration: none !important; transition: all .2s;
}
.pf-btn.solid { background: var(--navy); color: #fff !important; }
.pf-btn.solid:hover { background: #12306a; }
.pf-btn.ghost { border: 1px solid var(--navy); color: var(--navy) !important; }
.pf-btn.ghost:hover { background: var(--navy); color: #fff !important; }
.pf-origin { font-size: 0.82rem; color: var(--steel); letter-spacing: 0.04em; border-top: 1px solid var(--line); padding-top: 16px; max-width: 470px; }

.pf-frame { border-radius: 14px; overflow: hidden; background: var(--navy); box-shadow: 0 30px 60px -25px rgba(10,27,58,.45); }
.pf-img { width: 100%; display: block; object-fit: cover; }
.pf-placeholder {
    min-height: 320px; display: flex; align-items: center; justify-content: center; text-align: center;
    color: #9AA3B5; font-size: .9rem; padding: 30px; background: repeating-linear-gradient(135deg,#0d2149,#0d2149 12px,#0A1B3A 12px,#0A1B3A 24px);
}

/* ---- Section headings ---- */
.pf-section { padding-top: 70px; }
.pf-kicker { font-size: .85rem; color: var(--steel); margin-bottom: 8px; }
.pf-h2 { font-family: 'Cormorant Garamond', serif; font-size: clamp(2rem, 3.4vw, 3rem); font-weight: 600; color: var(--navy); line-height: 1.1; margin: 0 0 14px 0; }
.pf-sub { color: var(--steel); font-size: 1.02rem; line-height: 1.7; max-width: 520px; font-weight: 300; }

/* ---- Product ---- */
.pf-product-frame { border-radius: 14px; overflow: hidden; background: var(--paper); border: 1px solid var(--line); }
.pf-specs { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0; margin-top: 26px; border-top: 1px solid var(--line); }
.pf-spec { padding: 22px 6px 22px 0; border-bottom: 1px solid var(--line); }
.pf-spec:nth-child(odd) { border-right: 1px solid var(--line); }
.pf-spec:nth-child(even) { padding-left: 26px; }
.pf-spec .n { font-family: 'Cormorant Garamond', serif; font-size: 2.3rem; font-weight: 600; color: var(--navy); line-height: 1; }
.pf-spec .l { font-size: .85rem; color: var(--steel); margin-top: 6px; }
.pf-note { margin-top: 20px; font-size: .95rem; color: var(--ink); line-height: 1.7; font-weight: 300; }

/* ---- Keyed containers (cards) ---- */
.st-key-verify, .st-key-vip {
    border-radius: 14px; padding: 34px 36px !important;
}
.st-key-verify { background: var(--paper); border: 1px solid var(--line); box-shadow: 0 20px 40px -30px rgba(10,27,58,.35); }
.st-key-vip { background: linear-gradient(160deg, var(--navy) 0%, var(--navy-deep) 100%); border: none; }
.st-key-vip h3, .st-key-vip .pf-h2 { color: #fff !important; }
.st-key-vip .pf-sub { color: #B9C2D4; }

/* ---- Inputs & buttons ---- */
.stTextInput input {
    border-radius: 10px !important; border: 1px solid #CFCAC0 !important; background: #fff !important;
    color: var(--ink) !important; height: 50px; padding: 0 16px !important; font-size: .98rem !important;
}
.stTextInput input:focus { border-color: var(--navy) !important; box-shadow: 0 0 0 3px rgba(10,27,58,.12) !important; }
.stTextInput div[data-baseweb="input"], .stTextInput div[data-baseweb="base-input"] { background: transparent !important; border: none !important; }
.stButton > button {
    background: var(--navy) !important; color: #fff !important; border: none !important; border-radius: 10px !important;
    height: 50px; font-weight: 500 !important; font-size: .95rem !important; width: 100%; transition: background .2s;
}
.stButton > button:hover { background: #12306a !important; color: #fff !important; }
.st-key-vip .stButton > button { background: #fff !important; color: var(--navy) !important; }
.st-key-vip .stButton > button:hover { background: #E9EDF5 !important; }
.stButton > button:focus-visible, .stTextInput input:focus-visible { outline: 2px solid var(--green); outline-offset: 2px; }

/* ---- Verified result ---- */
.pf-ok {
    display: flex; gap: 16px; align-items: center; margin-top: 18px;
    background: #EFFAF4; border: 1px solid #BFE8D2; border-radius: 12px; padding: 18px 20px;
}
.pf-ok .dot { width: 38px; height: 38px; border-radius: 50%; background: var(--green); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; flex: none; }
.pf-ok .t { font-weight: 600; color: #0B5C37; }
.pf-ok .s { font-size: .9rem; color: #3F6F58; margin-top: 2px; }

/* ---- Footer ---- */
.pf-footer { margin-top: 80px; padding-top: 28px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; color: var(--steel); font-size: .85rem; }

/* ---- Mobile ---- */
@media (max-width: 768px) {
    .block-container { padding: 0 1rem 2rem 1rem !important; }
    .pf-links a:not(.pf-cta) { display: none; }
    .pf-section { padding-top: 48px; }
    .st-key-verify, .st-key-vip { padding: 24px 20px !important; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } * { transition: none !important; } }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 3. NAVIGATION
# ---------------------------------------------------------
html("""
<div class="pf-nav">
    <div class="pf-logo">per<b>F</b>ecto</div>
    <div class="pf-links">
        <a href="#top">Home</a>
        <a href="#range">The set</a>
        <a href="#verify">Authenticity</a>
        <a href="#coming-soon">Coming soon</a>
        <a class="pf-cta" href="#verify">Verify my set</a>
    </div>
</div>
<div id="top"></div>
""")

# ---------------------------------------------------------
# 4. HERO
# ---------------------------------------------------------
hero_l, hero_r = st.columns([1, 1.15], gap="large")

with hero_l:
    html("""
    <div class="pf-hero-text">
        <h1>Perfecting the art of dining.</h1>
        <p class="lead">Luxury tableware for the discerning home. Italian design, finished by hand,
        and made to be used every day for decades.</p>
        <div class="pf-hero-actions">
            <a class="pf-btn solid" href="#range">See the 30-piece set</a>
            <a class="pf-btn ghost" href="#verify">Verify your set</a>
        </div>
        <div class="pf-origin">Italian heritage and craftsmanship</div>
    </div>
    """)

with hero_r:
    html(f'<div class="pf-frame">{image_tag(hero_b64, "perFecto brand banner", "hero_banner.jpeg")}</div>')

# ---------------------------------------------------------
# 5. FLAGSHIP PRODUCT
# ---------------------------------------------------------
html('<div id="range" class="pf-section"></div>')
prod_l, prod_r = st.columns([1.15, 1], gap="large")

with prod_l:
    html(f'<div class="pf-product-frame">{image_tag(product_b64, "perFecto cutlery set", "product_cutlery.jpeg")}</div>')

with prod_r:
    html("""
    <div class="pf-kicker">The flagship set</div>
    <div class="pf-h2">Everything for six at the table.</div>
    <p class="pf-sub">A complete dinner and serving cutlery set in premium 18/10 stainless steel,
    weighted for a confident, balanced grip.</p>
    <div class="pf-specs">
        <div class="pf-spec"><div class="n">30</div><div class="l">pieces in the set</div></div>
        <div class="pf-spec"><div class="n">6</div><div class="l">place settings</div></div>
        <div class="pf-spec"><div class="n">18/10</div><div class="l">stainless steel</div></div>
        <div class="pf-spec"><div class="n">3.0 mm</div><div class="l">thickness for weight and balance</div></div>
    </div>
    <p class="pf-note">Every set carries a 25-year guarantee. Register yours below to activate it.</p>
    """)

# ---------------------------------------------------------
# 6. AUTHENTICITY CHECK
# ---------------------------------------------------------
html('<div id="verify" class="pf-section"></div>')
ver_l, ver_r = st.columns([1, 1.15], gap="large")

with ver_l:
    html("""
    <div class="pf-kicker">Authenticity</div>
    <div class="pf-h2">Confirm your set is genuine.</div>
    <p class="pf-sub">Enter the serial code from your set's packaging to confirm it is an original
    perFecto and to activate your 25-year guarantee.</p>
    """)

with ver_r:
    with st.container(key="verify"):
        st.markdown("**Serial code**")
        v1, v2 = st.columns([2.4, 1])
        with v1:
            serial = st.text_input(
                "Serial code", placeholder="e.g. PER-1810-7792", label_visibility="collapsed", key="serial_input"
            )
        with v2:
            verify_clicked = st.button("Verify", key="verify_btn")

        if verify_clicked:
            code = serial.strip().upper()
            if not code:
                st.warning("Enter the serial code from your packaging.")
            elif not re.fullmatch(r"PER-\d{4}-\d{4}", code):
                st.error("That code doesn't match the format PER-0000-0000. Check the packaging and try again.")
            else:
                with st.spinner("Checking the perFecto registry..."):
                    time.sleep(0.6)  # TODO: replace with a real registry lookup
                html(f"""
                <div class="pf-ok">
                    <div class="dot">✓</div>
                    <div>
                        <div class="t">Original perFecto confirmed</div>
                        <div class="s">Code {code} · 25-year guarantee active</div>
                    </div>
                </div>
                """)

# ---------------------------------------------------------
# 7. COMING SOON + VIP LIST
# ---------------------------------------------------------
html('<div id="coming-soon" class="pf-section"></div>')
with st.container(key="vip"):
    t_l, t_r = st.columns([1.1, 1], gap="large")
    with t_l:
        html(f'<div class="pf-frame" style="box-shadow:none;border-radius:10px;">{image_tag(teaser_b64, "Something unbreakable is coming", "teaser_unbreakable.jpeg")}</div>')
    with t_r:
        html("""
        <div style="font-size:.85rem;color:#9FB0D0;margin-bottom:8px;">Private launch list</div>
        <div class="pf-h2">Something unbreakable is coming.</div>
        <p class="pf-sub">A new collection built for endurance. Join the list to see it before anyone else.</p>
        """)
        email = st.text_input(
            "Email address", placeholder="you@example.com", label_visibility="collapsed", key="vip_email"
        )
        if st.button("Get early access", key="vip_btn"):
            if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
                try:
                    with open("vip_list.csv", "a", newline="", encoding="utf-8") as f:
                        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), email.strip()])
                except OSError:
                    pass  # swap for a database or email-service call in production
                st.success("You're on the list. We'll email you before the launch.")
            else:
                st.error("Enter a valid email address, like you@example.com.")

# ---------------------------------------------------------
# 8. FOOTER
# ---------------------------------------------------------
html(f"""
<div class="pf-footer">
    <div>© {datetime.now().year} perFecto. Luxury tableware, Italian heritage.</div>
    <div>25-year guarantee on every set</div>
</div>
""")
