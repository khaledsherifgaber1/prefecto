import streamlit as st
import time
import os

# ---------------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto | Luxury Home",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. STYLING (Fixed CSS & Typography)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Montserrat:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA;
        color: #1A1A1A;
        font-family: 'Montserrat', sans-serif;
    }

    /* Top Nav */
    .nav-bar {
        display: flex;
        justify-content: flex-end;
        gap: 25px;
        padding: 5px 10px 20px 10px;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #4B5563;
    }

    /* Navy Sidebar Card */
    .hero-card {
        background: linear-gradient(180deg, #0A1B3A 0%, #050E1E 100%);
        border-radius: 8px;
        padding: 40px 30px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        min-height: 620px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Brand Logo */
    .brand-logo {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0px;
        line-height: 1;
        letter-spacing: -0.5px;
    }
    .brand-per { color: #FF3333; }
    .brand-f   { color: #FFFFFF; }
    .brand-ecto { color: #00A859; }
    .brand-sub {
        letter-spacing: 5px;
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 6px;
        font-weight: 500;
    }

    /* Headings */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.3rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 35px;
        margin-bottom: 15px;
        color: #FFFFFF;
        letter-spacing: 1px;
    }
    .hero-text {
        font-size: 0.95rem;
        color: #D1D5DB;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* Specification Cards */
    .spec-box {
        background: #FFFFFF;
        border-left: 4px solid #0A1B3A;
        padding: 16px 20px;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 15px;
        border-top: 1px solid #F3F4F6;
        border-right: 1px solid #F3F4F6;
        border-bottom: 1px solid #F3F4F6;
    }
    .spec-h {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0A1B3A;
    }
    .spec-p {
        font-size: 0.82rem;
        color: #6B7280;
        margin-top: 2px;
    }

    /* Feature Section Containers */
    .feature-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #E5E7EB;
        margin-top: 20px;
    }

    /* Streamlit Input & Button Styling */
    .stButton>button {
        background-color: #0A1B3A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 4px !important;
        padding: 0.55rem 1.2rem !important;
        width: 100%;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #00A859 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. TOP NAVIGATION BAR
# ---------------------------------------------------------
st.markdown("""
<div class="nav-bar">
    <div>🏠 Home</div>
    <div>㗊 Range</div>
    <div>ℹ️ About</div>
    <div>🛒 Cart</div>
    <div>👤 Profile</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. MAIN LAYOUT
# ---------------------------------------------------------
left_col, right_col = st.columns([1, 1.3], gap="large")

# --- LEFT HERO BANNER ---
with left_col:
    st.markdown("""
    <div class="hero-card">
        <div>
            <div class="brand-logo">
                <span class="brand-per">per</span><span class="brand-f">F</span><span class="brand-ecto</span>
            </div>
            <div class="brand-sub">LUXURY HOME</div>
            
            <div class="hero-title">
                PERFECTING<br>THE ART OF<br>DINING.
            </div>
            <div class="hero-text">
                Luxury Tableware for the Discerning Home.
            </div>
        </div>
        
        <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 15px; text-align: center;">
            <div style="font-size: 0.7rem; letter-spacing: 3px; color: #9CA3AF;">ITALIAN HERITAGE & DESIGN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- RIGHT PRODUCT AREA ---
with right_col:
    # 1. Product Image Display (Checks local directory, otherwise loads clear online preview)
    image_paths = ["188 STAINLESS STEEL CUTLERY DINNER SPOON 6 PCS DINNER FORK 6 PCS DINNER KNIFE TEA SPOON 6 PCS 6 PCS DESSERT FORK 6 PCS SOUP LADLE 1 PC RICE SERVER 1 PC (2800 x 2750 بيكسل).pdf (1).jpg", "product_image.jpg"]
    
    loaded_img = None
    for img_path in image_paths:
        if os.path.exists(img_path):
            loaded_img = img_path
            break
            
    if loaded_img:
        st.image(loaded_img, use_container_width=True)
    else:
        # Fallback preview if file name is different in your repo
        st.image("https://images.unsplash.com/photo-1615865417286-dae52c658fdf?q=80&w=1000&auto=format&fit=crop", caption="perFecto 18/10 Cutlery Set Showcase", use_container_width=True)

    # 2. Key Product Specifications
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="spec-box">
            <div class="spec-h">30-piece set | 6-person service</div>
            <div class="spec-p">Complete dinner & serving cutlery</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="spec-box">
            <div class="spec-h">Premium 18/10 Stainless Steel</div>
            <div class="spec-p">3.0 mm thickness & balance</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Authenticity Verification Section
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🛡️ Product Authenticity Check")
    st.write("Verify your **perFecto** set is 100% original and activate your 25-Year Guarantee.")
    
    v1, v2 = st.columns([2.5, 1])
    with v1:
        serial = st.text_input("Serial Code", placeholder="e.g. PER-1810-7792", label_visibility="collapsed")
    with v2:
        if st.button("VERIFY NOW"):
            if serial.strip():
                with st.spinner("Checking..."):
                    time.sleep(0.5)
                st.success(f"✅ Code `{serial.upper()}` Verified Original!")
                st.info("25-Year Manufacturer Warranty Active")
            else:
                st.warning("Enter a serial number.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Mystery Reveal (Coming Soon)
    st.markdown('<div class="feature-card" style="border-left: 4px solid #FF3333;">', unsafe_allow_html=True)
    st.markdown("### ✨ Coming Soon: Venezia Crystal")
    st.write("Our upcoming hand-blown Italian crystal tableware collection.")
    
    e1, e2 = st.columns([2.5, 1])
    with e1:
        email = st.text_input("VIP Access Email", placeholder="Enter your email address", label_visibility="collapsed")
    with e2:
        if st.button("GET VIP ACCESS"):
            if email.strip():
                st.success("Registered for early access.")
            else:
                st.error("Enter a valid email.")
    st.markdown('</div>', unsafe_allow_html=True)
