import streamlit as st
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Perfecto Luxury Home",
    page_icon="🍽️",
    layout="wide"
)

# 2. Brand Identity Styling (Royal Navy, Vibrant Red/Green, White Accents)
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0A1B3A;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Header & Branding */
    .brand-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .brand-red { color: #FF3333; }
    .brand-white { color: #FFFFFF; }
    .brand-green { color: #00A859; }
    .brand-sub {
        letter-spacing: 4px;
        font-size: 0.9rem;
        color: #CCCCCC;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Product Cards & Glass Containers */
    .spec-card {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .spec-badge {
        background-color: #002244;
        border: 2px solid #00A859;
        border-radius: 50%;
        width: 90px;
        height: 90px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        font-weight: bold;
    }
    
    /* Input & Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #FF3333 0%, #00A859 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        padding: 0.6rem 2rem;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="brand-title">
        <span class="brand-red">per</span><span class="brand-white">F</span><span class="brand-green">ecto</span>
    </div>
    <div class="brand-sub">LUXURY HOME</div>
""", unsafe_allow_html=True)

st.divider()

# --- HERO & PRODUCT SHOWCASE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Perfecting the Art of Dining")
    st.write("""
    Experience Italian elegance with modern craftsmanship. Our premium 18/10 stainless steel cutlery 
    combines durability, 3.0 mm ergonomic balance, and luxury gold-accented detail tailored for discerning homes.
    """)
    
    # Key Badges Display
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown('<div class="spec-card"><h3>30 Pcs</h3><p>Complete Set</p></div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="spec-card"><h3>18/10</h3><p>Stainless Steel</p></div>', unsafe_allow_html=True)
    with b3:
        st.markdown('<div class="spec-card"><h3>3.0 mm</h3><p>Thickness</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="spec-card"><strong>🛡️ 25 Years Warranty Included</strong></div>', unsafe_allow_html=True)

with col2:
    # Replace with your actual hosted image path/URL
    st.image("188 STAINLESS STEEL CUTLERY DINNER SPOON 6 PCS DINNER FORK 6 PCS DINNER KNIFE TEA SPOON 6 PCS 6 PCS DESSERT FORK 6 PCS SOUP LADLE 1 PC RICE SERVER 1 PC (2800 x 2750 بيكسل).pdf (1).jpg", caption="30-Piece Luxury Cutlery Set with Stand", use_container_width=True)

st.divider()

# --- SECTION 2: PRODUCT AUTHENTICITY VERIFIER ---
st.header("🔍 Verify Product Authenticity")
st.write("Ensure your **perFecto** items are 100% original and register your 25-year warranty.")

auth_col1, auth_col2 = st.columns([2, 1])

with auth_col1:
    serial_input = st.text_input("Enter Product Serial Code / Hologram Number", placeholder="e.g. PER-1810-9942")

with auth_col2:
    st.write(" ")
    st.write(" ")
    verify_btn = st.button("Check Authenticity")

if verify_btn:
    if serial_input.strip() != "":
        st.success(f"✅ Verified Original perFecto Product! Code: **{serial_input.upper()}**")
        st.info("Warranty Status: Active (25 Years Coverage)")
    else:
        st.warning("Please enter a valid serial code found on your packaging badge.")

st.divider()

# --- SECTION 3: COMING SOON (MYSTERY REVEAL) ---
st.header("✨ Mystery Reveal: Coming Soon")

reveal_col1, reveal_col2 = st.columns([1, 1])

with reveal_col1:
    st.markdown("### The *Venezia* Crystal Collection")
    st.write("""
    Something extraordinary is crafted for your table. 
    Our upcoming hand-blown crystal collection combines classic Italian design with unmatched clarity.
    """)
    
    # VIP Access Sign-up
    email = st.text_input("Get Exclusive VIP Launch Invite & Early Access Discount:", placeholder="Enter your email address")
    if st.button("Notify Me Upon Launch"):
        if email:
            st.success("Thank you! You are now on the VIP early access list.")
        else:
            st.error("Please enter a valid email.")

with reveal_col2:
    # Teaser visual card
    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border: 2px dashed #00A859; padding: 40px; border-radius: 12px; text-align: center;">
        <h2 style="color: #FF3333;">🔒 TOP SECRET</h2>
        <p>Unveiling in Spring 2025</p>
        <p style="font-size: 0.8rem; color: #888;">Limited First Edition Production Run</p>
    </div>
    """, unsafe_allow_html=True)