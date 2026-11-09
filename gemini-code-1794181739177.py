import streamlit as st
import time
import os

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto | Luxury Tableware",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. EXACT DESIGN CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Montserrat:wght@300;400;500;600;700&display=swap');

    /* Global Page Styling */
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 30px;
        padding: 10px 20px 20px 20px;
        border-bottom: 1px solid #E9ECEF;
        margin-bottom: 30px;
    }
    .nav-item {
        text-align: center;
        color: #495057;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
    }
    .nav-icon {
        font-size: 1.2rem;
        display: block;
        margin-bottom: 2px;
    }

    /* Left Navy Hero Banner */
    .navy-hero {
        background: linear-gradient(180deg, #0A1B3A 0%, #061126 100%);
        border-radius: 4px;
        padding: 45px 35px;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        min-height: 680px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Brand Logo Text */
    .brand-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0;
        line-height: 1;
    }
    .brand-per { color: #FF3333; }
    .brand-f   { color: #FFFFFF; }
    .brand-ecto { color: #00A859; }
    .brand-sub {
        letter-spacing: 5px;
        font-size: 0.75rem;
        color: #CCCCCC;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Hero Headline */
    .hero-heading {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.25;
        letter-spacing: 1px;
        margin-top: 40px;
        margin-bottom: 15px;
        color: #FFFFFF;
    }
    .hero-sub {
        font-size: 1rem;
        color: #D1D5DB;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* CTA Button inside Hero */
    .hero-cta {
        display: inline-block;
        background-color: #FFFFFF;
        color: #0A1B3A;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        padding: 12px 24px;
        border-radius: 4px;
        text-transform: uppercase;
        border: none;
        text-align: center;
    }

    /* Italian Architectural Motif Styling */
    .landmark-watermark {
        margin-top: 40px;
        opacity: 0.35;
        border-top: 1px solid rgba(255,255,255,0.15);
        padding-top: 20px;
        text-align: center;
    }

    /* Product Specification Callouts */
    .spec-callout {
        background: #FFFFFF;
        border-left: 4px solid #0A1B3A;
        padding: 15px 20px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .spec-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0A1B3A;
        margin-bottom: 2px;
    }
    .spec-desc {
        font-size: 0.85rem;
        color: #6C757D;
    }

    /* Interactive Sections (Authenticity & Teaser) */
    .section-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 25px;
        border: 1px solid #E9ECEF;
    }

    /* Streamlit Overrides */
    .stButton>button {
        background-color: #0A1B3A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.5rem !important;
        width: 100%;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. TOP NAVIGATION BAR
# ---------------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="nav-item"><span class="nav-icon">🏠</span>Home</div>
    <div class="nav-item"><span class="nav-icon">㗊</span>Range</div>
    <div class="nav-item"><span class="nav-icon">ℹ️</span>About</div>
    <div class="nav-item"><span class="nav-icon">🛒</span>Cart</div>
    <div class="nav-item"><span class="nav-icon">👤</span>Profile</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. MAIN TWO-COLUMN LAYOUT
# ---------------------------------------------------------
left_col, right_col = st.columns([1.1, 1.4], gap="large")

# --- LEFT COLUMN: NAVY HERO BANNER ---
with left_col:
    st.markdown("""
    <div class="navy-hero">
        <div>
            <!-- BRAND LOGO -->
            <div class="brand-title">
                <span class="brand-per">per</span><span class="brand-f">F</span><span class="brand-ecto</span>
            </div>
            <div class="brand-sub">LUXURY HOME</div>
            
            <!-- HEADLINE & SUBTITLE -->
            <div class="hero-heading">
                PERFECTING<br>THE ART OF<br>DINING.
            </div>
            <div class="hero-sub">
                Luxury Tableware for the Discerning Home.
            </div>
            
            <div class="hero-cta">
                EXPLORE THE COLLECTION
            </div>
        </div>
        
        <!-- ITALIAN LANDMARK MOTIF -->
        <div class="landmark-watermark">
            <svg width="100%" height="80" viewBox="0 0 300 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 70 V20 H50 V70 M35 20 V70 M100 70 C100 40 140 40 140 70 M140 70 C140 40 180 40 180 70 M180 70 C180 40 220 40 220 70" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="3 3"/>
            </svg>
            <div style="font-size: 0.65rem; letter-spacing: 3px; color: #A0ABBA; margin-top: 5px;">ITALIAN HERITAGE & DESIGN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- RIGHT COLUMN: PRODUCT SHOWCASE & INTERACTIVE FEATURES ---
with right_col:
    # 1. Product Image Display
    image_filename = "product_image.jpg"
    
    if os.path.exists(image_filename):
        st.image(image_filename, use_container_width=True)
    else:
        # High quality fallback matching your cutlery photo
        st.image(
            "https://images.unsplash.com/photo-1615865417286-dae52c658fdf?q=80&w=1000&auto=format&fit=crop",
            caption="perFecto 18/10 Stainless Steel 30-Piece Cutlery Set with Rack",
            use_container_width=True
        )

    # 2. Product Specifications (Matching Callouts)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="spec-callout">
            <div class="spec-title">30-piece set | 6-person service</div>
            <div class="spec-desc">Complete dinner, dessert & serving cutlery</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="spec-callout">
            <div class="spec-title">Premium 18/10 Stainless Steel</div>
            <div class="spec-desc">3.0 mm ergonomic thickness & weight balance</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Product Authenticity Verification Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🛡️ Product Authenticity Check")
    st.write("Verify that your **perFecto** set is 100% original and register your 25-Year Guarantee.")
    
    v_col1, v_col2 = st.columns([2.5, 1])
    with v_col1:
        serial_input = st.text_input("Product Hologram Serial Number", placeholder="e.g., PER-1810-7792", label_visibility="collapsed")
    with v_col2:
        verify_btn = st.button("VERIFY NOW")

    if verify_btn:
        if serial_input.strip():
            with st.spinner("Verifying with perFecto Registry..."):
                time.sleep(0.6)
            st.success(f"✅ **AUTHENTIC PRODUCT**: Code `{serial_input.upper()}` is verified.")
            st.info("Warranty Status: **25-Year Coverage Active**")
        else:
            st.warning("Please enter the code from your product box.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Mystery / Coming Soon Product Section
    st.markdown('<div class="section-card" style="border-left: 4px solid #FF3333;">', unsafe_allow_html=True)
    st.subheader("✨ Coming Soon: The *Venezia* Crystal Collection")
    st.write("Our new line of hand-blown Italian glassware will be available soon.")
    
    e_col1, e_col2 = st.columns([2.5, 1])
    with e_col1:
        email_input = st.text_input("VIP Early Access Email", placeholder="Enter your email address", label_visibility="collapsed")
    with e_col2:
        notify_btn = st.button("GET VIP ACCESS")

    if notify_btn:
        if email_input.strip():
            st.success("Thank you! You are registered for private launch access.")
        else:
            st.error("Please enter a valid email.")
    st.markdown('</div>', unsafe_allow_html=True)
