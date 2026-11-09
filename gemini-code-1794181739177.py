import streamlit as st
import base64
import time
import os

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto | Luxury Home",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to safely convert images to base64 strings
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return None

# Convert the three images
hero_b64 = get_image_base64("hero_banner.jpeg")
product_b64 = get_image_base64("product_cutlery.jpeg")
teaser_b64 = get_image_base64("teaser_unbreakable.jpeg")

# ---------------------------------------------------------
# 2. BRAND CSS STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Montserrat:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA;
        color: #1A1A1A;
        font-family: 'Montserrat', sans-serif;
    }

    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 30px;
        padding: 5px 20px 20px 20px;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #4B5563;
    }

    /* Hero Banner Image Card */
    .hero-banner-container {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        background-color: #0A1B3A;
    }
    .hero-banner-img {
        width: 100%;
        display: block;
        object-fit: cover;
    }
    .hero-text-content {
        padding: 30px;
        background: linear-gradient(180deg, #0A1B3A 0%, #050E1E 100%);
        color: white;
    }
    .hero-heading {
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.25;
        margin-bottom: 10px;
        color: #FFFFFF;
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
        font-size: 1rem;
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

    /* Teaser Container Styling */
    .teaser-container {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 25px;
        background-color: #050E1E;
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
<div class="top-nav">
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
left_col, right_col = st.columns([1, 1.25], gap="large")

# --- LEFT COLUMN: BRAND HERO BANNER ---
with left_col:
    if hero_b64:
        st.markdown(f"""
        <div class="hero-banner-container">
            <img src="data:image/jpeg;base64,{hero_b64}" class="hero-banner-img" alt="perFecto Banner"/>
            <div class="hero-text-content">
                <div class="hero-heading">PERFECTING THE ART OF DINING.</div>
                <p style="color: #D1D5DB; font-size: 0.95rem; font-weight: 300; margin-bottom: 20px;">
                    Luxury Tableware for the Discerning Home.
                </p>
                <div style="border-top: 1px solid rgba(255,255,255,0.15); padding-top: 15px; text-align: center;">
                    <span style="font-size: 0.7rem; letter-spacing: 3px; color: #9CA3AF;">ITALIAN HERITAGE & CRAFTSMANSHIP</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Place 'hero_banner.jpeg' in your project directory.")

# --- RIGHT COLUMN: PRODUCT & MYSTERY TEASER ---
with right_col:
    # 1. Flagship Product Image
    if product_b64:
        st.markdown(f"""
        <div style="border-radius: 8px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
            <img src="data:image/jpeg;base64,{product_b64}" style="width:100%; display:block;" alt="perFecto Cutlery Set"/>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Place 'product_cutlery.jpeg' in your project directory.")

    # 2. Key Product Callouts
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

    # 3. Product Authenticity Verification Section
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 🛡️ Product Authenticity Check")
    st.write("Verify that your **perFecto** set is 100% original and register your 25-Year Guarantee.")
    
    v1, v2 = st.columns([2.5, 1])
    with v1:
        serial = st.text_input("Serial Code", placeholder="e.g. PER-1810-7792", label_visibility="collapsed")
    with v2:
        if st.button("VERIFY NOW"):
            if serial.strip():
                with st.spinner("Verifying with perFecto Registry..."):
                    time.sleep(0.5)
                st.success(f"✅ Code `{serial.upper()}` Verified Original!")
                st.info("Warranty Status: 25-Year Manufacturer Guarantee Active")
            else:
                st.warning("Please enter your serial code.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Mystery Reveal (Coming Soon Teaser Section)
    if teaser_b64:
        st.markdown(f"""
        <div class="teaser-container">
            <img src="data:image/jpeg;base64,{teaser_b64}" style="width:100%; display:block;" alt="Something Unbreakable is Coming"/>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card" style="border-left: 4px solid #00A859; margin-top: 15px;">', unsafe_allow_html=True)
    st.markdown("### ✨ Exclusive Reveal: Private VIP List")
    st.write("Be the first to discover our mysterious upcoming collection designed for unmatched endurance.")
    
    e1, e2 = st.columns([2.5, 1])
    with e1:
        email = st.text_input("VIP Email", placeholder="Enter your email address", label_visibility="collapsed")
    with e2:
        if st.button("GET EARLY ACCESS"):
            if email.strip():
                st.success("Thank you! You are registered on the private perFecto launch list.")
            else:
                st.error("Please enter a valid email.")
    st.markdown('</div>', unsafe_allow_html=True)
