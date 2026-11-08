import streamlit as st
import time

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto Luxury Home | Official",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. BRAND CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Main Container & Background */
    .stApp {
        background-color: #050E1E;
        color: #F7F5F0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Luxury Header Typography */
    h1, h2, h3, .luxury-heading {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 2px;
        color: #F7F5F0;
    }

    /* Custom Logo Styling */
    .logo-container {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .brand-per { color: #E53935; font-size: 3.2rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-f   { color: #FFFFFF; font-size: 3.2rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-ecto { color: #2E7D32; font-size: 3.2rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 6px;
        font-size: 0.85rem;
        color: #D4AF37;
        margin-top: -10px;
    }

    /* Italian Architectural Motif Overlay Card */
    .landmark-banner {
        background: linear-gradient(180deg, rgba(5,14,30,0.4) 0%, rgba(5,14,30,0.95) 100%),
                    url('https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 60px 40px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* Glassmorphism Specs Badge Cards */
    .gold-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .gold-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }
    .card-title {
        font-family: 'Cinzel', serif;
        color: #D4AF37;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .card-subtitle {
        color: #C5A059;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Verification Box */
    .verify-box {
        background: rgba(8, 22, 45, 0.8);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 16px;
        padding: 35px;
        margin-top: 30px;
    }

    /* Mystery Teaser Section */
    .teaser-container {
        background: radial-gradient(circle at center, #0F2342 0%, #050E1E 100%);
        border: 1px dashed rgba(212, 175, 55, 0.5);
        border-radius: 16px;
        padding: 50px 30px;
        text-align: center;
        position: relative;
    }
    .lock-badge {
        font-family: 'Cinzel', serif;
        color: #E53935;
        letter-spacing: 4px;
        font-weight: 700;
        font-size: 0.9rem;
    }

    /* Streamlit Widget Overrides */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #050E1E !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 2rem !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.6) !important;
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #F7F5F0 !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HEADER & BRANDING
# ---------------------------------------------------------
st.markdown("""
<div class="logo-container">
    <div>
        <span class="brand-per">per</span><span class="brand-f">F</span><span class="brand-ecto</span>
    </div>
    <div class="brand-sub">LUXURY HOME</div>
</div>
""", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HERO SECTION (Italian Line-Art Motif Banner)
# ---------------------------------------------------------
st.markdown("""
<div class="landmark-banner">
    <h1 style="font-size: 2.8rem; margin-bottom: 10px;">PERFECTING THE ART OF DINING</h1>
    <p style="color: #D4AF37; font-size: 1.1rem; letter-spacing: 2px; font-weight: 300;">
        MASTERPIECE CUTLERY ROOTED IN ITALIAN HERITAGE
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PRODUCT SHOWCASE & SPECIFICATIONS
# ---------------------------------------------------------
prod_col1, prod_col2 = st.columns([1, 1], gap="large")

with prod_col1:
    st.markdown("### 30-Piece Signature Cutlery Set")
    st.write("""
    Forged with uncompromising Italian craftsmanship, each piece balances timeless line-art elegancy with professional-grade durability. Designed for 6-person full service fine dining.
    """)
    st.write("<br>", unsafe_allow_html=True)
    
    # Custom Spec Grid
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
        <div class="gold-card">
            <div class="card-title">18/10</div>
            <div class="card-subtitle">Stainless Steel</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="gold-card">
            <div class="card-title">3.0 mm</div>
            <div class="card-subtitle">Balanced Thickness</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s2:
        st.markdown("""
        <div class="gold-card">
            <div class="card-title">30 PCS</div>
            <div class="card-subtitle">6 Person Service</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="gold-card">
            <div class="card-title">25 YEARS</div>
            <div class="card-subtitle">Guarantee Warranty</div>
        </div>
        """, unsafe_allow_html=True)

with prod_col2:
    # Set display image
    st.image(
        "188 STAINLESS STEEL CUTLERY DINNER SPOON 6 PCS DINNER FORK 6 PCS DINNER KNIFE TEA SPOON 6 PCS 6 PCS DESSERT FORK 6 PCS SOUP LADLE 1 PC RICE SERVER 1 PC (2800 x 2750 بيكسل).pdf (1).jpg",
        caption="perFecto 18/10 Stainless Steel Cutlery Collection with Stand Holder",
        use_container_width=True
    )

st.write("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. PRODUCT AUTHENTICITY VERIFIER
# ---------------------------------------------------------
st.markdown("## Authenticity Verification")
st.write("Confirm your perFecto item's originality and activate your 25-year manufacturer guarantee.")

st.markdown('<div class="verify-box">', unsafe_allow_html=True)
v_col1, v_col2 = st.columns([3, 1])

with v_col1:
    serial_code = st.text_input(
        "Product Hologram Code",
        placeholder="Enter serial code (e.g. PER-8810-ITA)",
        label_visibility="collapsed"
    )

with v_col2:
    verify_clicked = st.button("VERIFY NOW")

if verify_clicked:
    if serial_code.strip():
        with st.spinner("Connecting to perFecto Registry..."):
            time.sleep(1)
        st.success(f"✓ **AUTHENTIC PRODUCT CONFIRMED** — Code: `{serial_code.upper()}`")
        st.info("Warranty Status: **Active (25-Year Full Coverage Registered)**")
    else:
        st.warning("Please enter your product serial code located on your luxury box stamp.")
st.markdown('</div>', unsafe_allow_html=True)

st.write("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. COMING SOON MYSTERY REVEAL
# ---------------------------------------------------------
st.markdown("## Exclusively Unveiling Soon")

t_col1, t_col2 = st.columns([1, 1], gap="large")

with t_col1:
    st.markdown("### The *Venezia* Crystal Line")
    st.write("""
    An upcoming revelation in table architecture. Hand-blown Italian crystal designed to complement our flagship cutlery set.
    """)
    st.write("<br>", unsafe_allow_html=True)
    
    email_sub = st.text_input("Request VIP Private Access", placeholder="Enter your email for early invitation")
    if st.button("JOIN THE VIP LIST"):
        if email_sub:
            st.success("You are registered on the private perFecto launch list.")
        else:
            st.error("Please provide a valid email address.")

with t_col2:
    st.markdown("""
    <div class="teaser-container">
        <div class="lock-badge">🔒 CONFIDENTIAL PREVIEW</div>
        <h2 style="font-size: 1.8rem; margin: 15px 0; color: #D4AF37;">VENEZIA CRYSTAL</h2>
        <p style="color: #CCCCCC; font-weight: 300;">Crafted in Italy — Launching Spring 2025</p>
    </div>
    """, unsafe_allow_html=True)
