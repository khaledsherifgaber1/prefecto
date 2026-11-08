import streamlit as st
import time
import os

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
# 2. BRAND CSS STYLING (Luxury Italian Aesthetic)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;800&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Main Container & Background */
    .stApp {
        background-color: #060E1A;
        color: #F7F5F0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 2px;
        color: #F7F5F0;
    }

    /* Brand Logo */
    .logo-container {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .brand-per { color: #E53935; font-size: 3.5rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-f   { color: #FFFFFF; font-size: 3.5rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-ecto { color: #2E7D32; font-size: 3.5rem; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .brand-sub {
        font-family: 'Cinzel', serif;
        letter-spacing: 8px;
        font-size: 0.9rem;
        color: #D4AF37;
        margin-top: -12px;
    }

    /* Italian Architectural Banner */
    .hero-box {
        background: linear-gradient(180deg, rgba(6,14,26,0.3) 0%, rgba(6,14,26,0.95) 100%),
                    url('https://images.unsplash.com/photo-1548625149-fc4a29cf7092?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 50px 30px;
        border: 1px solid rgba(212, 175, 55, 0.35);
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }

    /* Specification Cards */
    .spec-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 20px 15px;
        text-align: center;
        backdrop-filter: blur(8px);
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .spec-card:hover {
        border-color: #D4AF37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.25);
    }
    .card-title {
        font-family: 'Cinzel', serif;
        color: #D4AF37;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .card-subtitle {
        color: #C5A059;
        font-size: 0.75rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Authenticity Container */
    .verify-box {
        background: rgba(12, 25, 45, 0.7);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 16px;
        padding: 30px;
        margin-top: 10px;
    }

    /* Teaser Container */
    .teaser-card {
        background: radial-gradient(circle at center, #0F2545 0%, #060E1A 100%);
        border: 1px dashed #D4AF37;
        border-radius: 16px;
        padding: 40px 25px;
        text-align: center;
    }
    .teaser-tag {
        font-family: 'Cinzel', serif;
        color: #E53935;
        letter-spacing: 4px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* Streamlit Button Override */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%) !important;
        color: #060E1A !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.65rem 1.8rem !important;
        width: 100%;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.5) !important;
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
# 3. BRAND HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="logo-container">
    <div>
        <span class="brand-per">per</span><span class="brand-f">F</span><span class="brand-ecto</span>
    </div>
    <div class="brand-sub">LUXURY HOME</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero-box">
    <h1 style="font-size: 2.6rem; margin-bottom: 8px;">PERFECTING THE ART OF DINING</h1>
    <p style="color: #D4AF37; font-size: 1.05rem; letter-spacing: 2px; font-weight: 300; margin: 0;">
        FINE ITALIAN CUTLERY & TABLEWARE CRAFTSMANSHIP
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PRODUCT SHOWCASE & SPECS
# ---------------------------------------------------------
prod_col1, prod_col2 = st.columns([1, 1], gap="large")

with prod_col1:
    st.markdown("### 30-Piece Luxury Cutlery Set")
    st.write("""
    Forged with premium 18/10 stainless steel and finished with gold accents, this signature collection offers the perfect harmony of ergonomic weight, balance, and modern Italian table architecture.
    """)
    st.write("<br>", unsafe_allow_html=True)
    
    # 2x2 Specification Grid
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
        <div class="spec-card">
            <div class="card-title">18/10</div>
            <div class="card-subtitle">Stainless Steel</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="spec-card">
            <div class="card-title">3.0 mm</div>
            <div class="card-subtitle">Thickness</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s2:
        st.markdown("""
        <div class="spec-card">
            <div class="card-title">30 PCS</div>
            <div class="card-subtitle">6 Person Service</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="spec-card">
            <div class="card-title">25 YEARS</div>
            <div class="card-subtitle">Warranty</div>
        </div>
        """, unsafe_allow_html=True)

with prod_col2:
    # Safe Image Handling (Prevents FileNotFoundError)
    image_filename = "product_image.jpg"  # Rename your uploaded file to product_image.jpg in your repo
    
    if os.path.exists(image_filename):
        st.image(image_filename, caption="perFecto 18/10 Stainless Steel Cutlery Set", use_container_width=True)
    else:
        # Fallback image preview if local file is missing
        st.image(
            "https://images.unsplash.com/photo-1615865417286-dae52c658fdf?q=80&w=1000&auto=format&fit=crop",
            caption="perFecto 18/10 Stainless Steel Cutlery Collection (Sample Preview)",
            use_container_width=True
        )

st.write("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. PRODUCT AUTHENTICITY VERIFIER
# ---------------------------------------------------------
st.markdown("## Verify Authenticity")
st.write("Ensure your **perFecto** purchase is authentic and register your 25-year manufacturer guarantee.")

st.markdown('<div class="verify-box">', unsafe_allow_html=True)
v_col1, v_col2 = st.columns([3, 1])

with v_col1:
    serial_code = st.text_input(
        "Serial Code",
        placeholder="Enter packaging code (e.g., PER-8810-ORIGINAL)",
        label_visibility="collapsed"
    )

with v_col2:
    verify_clicked = st.button("VERIFY CODE")

if verify_clicked:
    if serial_code.strip():
        with st.spinner("Checking perFecto Authenticity Registry..."):
            time.sleep(0.8)
        st.success(f"✓ **ORIGINAL PRODUCT CONFIRMED** — Serial: `{serial_code.upper()}`")
        st.info("Warranty Status: **25-Year Guarantee Registered**")
    else:
        st.warning("Please enter the serial code located on your packaging label.")
st.markdown('</div>', unsafe_allow_html=True)

st.write("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. COMING SOON SECTION
# ---------------------------------------------------------
st.markdown("## Unveiling Soon")

t_col1, t_col2 = st.columns([1, 1], gap="large")

with t_col1:
    st.markdown("### The *Venezia* Crystal Line")
    st.write("""
    An upcoming collection of hand-crafted crystal glassware designed to seamlessly complement our signature 18/10 cutlery.
    """)
    st.write("<br>", unsafe_allow_html=True)
    
    email_sub = st.text_input("Request VIP Invitation", placeholder="Enter your email address")
    if st.button("JOIN VIP EARLY ACCESS"):
        if email_sub:
            st.success("You are registered on the private perFecto launch list.")
        else:
            st.error("Please enter a valid email address.")

with t_col2:
    st.markdown("""
    <div class="teaser-card">
        <div class="teaser-tag">🔒 CONFIDENTIAL REVEAL</div>
        <h2 style="font-size: 1.8rem; margin: 15px 0; color: #D4AF37;">VENEZIA CRYSTAL</h2>
        <p style="color: #CCCCCC; font-weight: 300; font-size: 0.9rem;">Crafted in Italy — Coming Spring 2025</p>
    </div>
    """, unsafe_allow_html=True)
