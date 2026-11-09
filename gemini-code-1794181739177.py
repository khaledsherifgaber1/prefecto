import streamlit as st
import time
import os

# 1. Page Configuration
st.set_page_config(
    page_title="perFecto | Luxury Home",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Clean Styling (Only CSS rules, no HTML elements inside markdown)
st.markdown("""
<style>
    /* Global Page Styling */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Input & Button Styling */
    .stButton>button {
        background-color: #0A1B3A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 4px !important;
        width: 100%;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #00A859 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Top Navigation Bar
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([6, 1, 1, 1, 1])
with nav_col2:
    st.write("🏠 Home")
with nav_col3:
    st.write("㗊 Range")
with nav_col4:
    st.write("🛒 Cart")
with nav_col5:
    st.write("👤 Profile")

st.divider()

# 4. Main Two-Column Layout
left_hero, right_content = st.columns([1, 1.2], gap="large")

# --- LEFT SIDEBAR / HERO CONTAINER ---
with left_hero:
    with st.container(border=True):
        # Logo Display
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            # Fallback text logo if logo.png is not found yet
            st.title(":red[per]:white[F]:green[ecto]")
            st.caption("LUXURY HOME")

        st.markdown("---")
        
        # Hero Headline
        st.subheader("PERFECTING THE ART OF DINING.")
        st.write("Luxury Tableware for the Discerning Home.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.button("EXPLORE THE COLLECTION", key="hero_cta")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("🏛️ ITALIAN HERITAGE & DESIGN")

# --- RIGHT SIDE: PRODUCT & FEATURES ---
with right_content:
    # 1. Product Image Display
    if os.path.exists("product.jpg"):
        st.image("product.jpg", use_container_width=True, caption="perFecto 18/10 Cutlery Set")
    else:
        st.info("💡 Place your product photo named 'product.jpg' in the project folder to view your image here.")

    # 2. Product Callouts / Specs
    spec_col1, spec_col2 = st.columns(2)
    with spec_col1:
        with st.container(border=True):
            st.markdown("**30-piece set | 6-person service**")
            st.caption("Complete dinner, dessert & serving cutlery")
            
    with spec_col2:
        with st.container(border=True):
            st.markdown("**Premium 18/10 Stainless Steel**")
            st.caption("3.0 mm ergonomic thickness & balance")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Product Authenticity Verification
    with st.container(border=True):
        st.subheader("🛡️ Product Authenticity Check")
        st.write("Verify that your **perFecto** set is 100% original and register your 25-Year Guarantee.")
        
        serial_code = st.text_input("Product Hologram Code", placeholder="e.g. PER-1810-7792", label_visibility="collapsed")
        
        if st.button("VERIFY NOW"):
            if serial_code.strip():
                with st.spinner("Checking perFecto Authenticity Registry..."):
                    time.sleep(0.5)
                st.success(f"✅ Code `{serial_code.upper()}` is Verified Original perFecto Product!")
                st.info("Warranty Status: 25-Year Manufacturer Guarantee Active")
            else:
                st.warning("Please enter your serial code.")

    # 4. Mystery / Coming Soon Section
    with st.container(border=True):
        st.subheader("✨ Coming Soon: Venezia Crystal Collection")
        st.write("Our upcoming hand-blown Italian crystal glassware line.")
        
        vip_email = st.text_input("VIP Access Email", placeholder="Enter your email address", label_visibility="collapsed")
        
        if st.button("GET VIP EARLY ACCESS"):
            if vip_email.strip():
                st.success("Thank you! You are registered on the VIP early access list.")
            else:
                st.error("Please enter a valid email address.")
