import base64
import os
import re
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from html import escape

import pandas as pd
import streamlit as st
import gspread
from google.oauth2 import service_account

# ---------------------------------------------------------
# 1. PAGE CONFIG & CONNECTIONS
# ---------------------------------------------------------
st.set_page_config(
    page_title="perFecto | Italian Luxury Tableware",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

class DirectGSheetsConnection:
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Load directly from the uploaded service_account.json file in your repository
        if os.path.exists("service_account.json"):
            creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=scope)
            with open("service_account.json", "r") as f:
                import json
                file_info = json.load(f)
                self.spreadsheet_url = file_info.get("spreadsheet") or st.secrets["connections"]["gsheets"]["spreadsheet"]
        else:
            # Fallback if secrets.toml is used
            sec = dict(st.secrets["connections"]["gsheets"])
            creds = service_account.Credentials.from_service_account_info(sec, scopes=scope)
            self.spreadsheet_url = sec.get("spreadsheet")
            
        self.client = gspread.authorize(creds)
        self.sh = self.client.open_by_url(self.spreadsheet_url)

    def read(self, worksheet: str, ttl=0):
        try:
            ws = self.sh.worksheet(worksheet)
            data = ws.get_all_records()
            return pd.DataFrame(data)
        except Exception:
            return pd.DataFrame()

    def update(self, worksheet: str, data: pd.DataFrame):
        try:
            ws = self.sh.worksheet(worksheet)
        except Exception:
            ws = self.sh.add_worksheet(title=worksheet, rows=100, cols=20)
        ws.clear()
        df_clean = data.fillna("")
        ws.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())

# Initialize robust direct connection
try:
    conn = DirectGSheetsConnection()
except Exception as e:
    st.error(f"Google Sheets connection error: {e}")
    conn = None

SERIAL_RE = re.compile(r"PER-\d{4}-\d{4}", re.IGNORECASE)
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


@st.cache_data(show_spinner=False)
def get_image_base64(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


def render(block: str):
    """Render HTML without Markdown mistaking indented lines for code."""
    cleaned = "\n".join(l.strip() for l in block.strip().splitlines() if l.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def image_tag(b64, alt, filename):
    if b64:
        return f'<img class="pf-img" src="data:image/jpeg;base64,{b64}" alt="{alt}"/>'
    return f'<div class="pf-placeholder">Add <b>{filename}</b> to your project folder</div>'


hero_b64 = get_image_base64("hero_banner.jpeg")
product_b64 = get_image_base64("product_cutlery.jpeg")
teaser_b64 = get_image_base64("teaser_unbreakable.jpeg")


@st.cache_data(show_spinner=False)
def get_logo_src():
    """Look for logo.png / .svg / .webp / .jpg next to app.py and return a data URI."""
    mimes = {"png": "image/png", "svg": "image/svg+xml", "webp": "image/webp", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
    for ext, mime in mimes.items():
        b64 = get_image_base64(f"logo.{ext}")
        if b64:
            return f"data:{mime};base64,{b64}"
    return None


logo_src = get_logo_src()

# ---------------------------------------------------------
# 2. HELPERS: QR, REGISTRY (GOOGLE SHEETS), EMAIL
# ---------------------------------------------------------
def decode_qr(uploaded_file):
    """Read a QR code from a camera photo or uploaded image. Returns text or None."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        st.error("QR scanning needs OpenCV. Run: pip install opencv-python-headless numpy")
        return None
    data = np.frombuffer(uploaded_file.getvalue(), np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        return None
    detector = cv2.QRCodeDetector()
    text, _, _ = detector.detectAndDecode(img)
    if not text:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        big = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        text, _, _ = detector.detectAndDecode(big)
    return text or None


def find_registration(serial: str):
    """Check Google Sheets 'registrations' tab for an existing serial."""
    if not conn:
        return None
    try:
        df = conn.read(worksheet="registrations", ttl=0)
        if df is not None and not df.empty and "serial" in df.columns:
            df["serial"] = df["serial"].astype(str)
            matched = df[df["serial"].str.upper() == serial.upper()]
            if not matched.empty:
                return matched.iloc[-1].to_dict()
    except Exception as e:
        st.error(f"Error reading registrations sheet: {e}")
    return None


def save_registration(serial, email, phone, email_sent):
    """Append a new registration row to the 'registrations' tab in Google Sheets."""
    if not conn:
        return
    try:
        df = conn.read(worksheet="registrations", ttl=0)
        new_row = pd.DataFrame([{
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "serial": str(serial),
            "email": str(email),
            "phone": str(phone),
            "email_sent": str(email_sent)
        }])
        
        expected_cols = ["timestamp", "serial", "email", "phone", "email_sent"]
        if df is not None and not df.empty:
            df = df.dropna(how="all", axis=1)
            df = df[[c for c in expected_cols if c in df.columns]]
            updated_df = pd.concat([df, new_row], ignore_index=True)
        else:
            updated_df = new_row
            
        conn.update(worksheet="registrations", data=updated_df)
    except Exception as e:
        st.error(f"Error saving registration to Google Sheets: {e}")


def save_vip_email(email):
    """Append a new VIP email row to the 'vip_list' tab in Google Sheets."""
    if not conn:
        return False
    try:
        df = conn.read(worksheet="vip_list", ttl=0)
        new_row = pd.DataFrame([{
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "email": str(email)
        }])
        
        expected_cols = ["timestamp", "email"]
        if df is not None and not df.empty:
            df = df.dropna(how="all", axis=1)
            df = df[[c for c in expected_cols if c in df.columns]]
            updated_df = pd.concat([df, new_row], ignore_index=True)
        else:
            updated_df = new_row
            
        conn.update(worksheet="vip_list", data=updated_df)
        return True
    except Exception as e:
        st.error(f"Error saving VIP signup: {e}")
        return False


def smtp_settings():
    """Return hardcoded SMTP settings for local testing."""
    return {
        "host": "smtp.gmail.com",
        "port": 465,
        "user": "gaberkhaled780@gmail.com",
        "password": "xbfmrbqfvwvhpywi",
        "sender": "gaberkhaled780@gmail.com"
    }


def send_confirmation_email(to_email: str, serial: str):
    """Returns (sent: bool, reason: str)."""
    cfg = smtp_settings()
    if not cfg:
        return False, "Email sending isn't set up yet."
    date = datetime.now().strftime("%d %B %Y")
    text = (
        f"Thank you for choosing perFecto.\n\n"
        f"Your set (serial {serial}) is confirmed as an original perFecto, and your 25-year "
        f"guarantee is active from {date}.\n\nKeep this email as your proof of registration.\n\nperFecto"
    )
    body = f"""
    <div style="background:#F6F4F0;padding:40px 16px;font-family:Georgia,'Times New Roman',serif;">
      <div style="max-width:560px;margin:auto;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E2DED6;">
        <div style="background:#0A1B3A;padding:34px;text-align:center;">
          <div style="font-size:30px;color:#ffffff;letter-spacing:1px;">per<span style="color:#E7D8B5;">F</span>ecto</div>
          <div style="height:1px;width:70px;background:#B8975A;margin:16px auto 0;"></div>
        </div>
        <div style="padding:36px 38px;color:#14213D;font-size:16px;line-height:1.7;">
          <div style="font-size:24px;color:#0A1B3A;margin-bottom:12px;">Your set is confirmed.</div>
          Thank you for choosing perFecto. Your set is verified as an original, and your
          <b>25-year guarantee</b> is now active.
          <div style="margin:26px 0;padding:18px 20px;background:#F6F4F0;border-left:3px solid #B8975A;">
            <div style="font-size:13px;color:#6B7587;">Serial code</div>
            <div style="font-size:20px;color:#0A1B3A;letter-spacing:1px;">{escape(serial)}</div>
            <div style="font-size:13px;color:#6B7587;margin-top:10px;">Guarantee active from {date}</div>
          </div>
          Please keep this email as your proof of registration.
        </div>
        <div style="padding:20px;text-align:center;font-size:12px;color:#8A94A6;border-top:1px solid #E2DED6;">
          perFecto &middot; Italian heritage and craftsmanship
        </div>
      </div>
    </div>"""
    msg = EmailMessage()
    msg["Subject"] = "Your perFecto set is confirmed"
    msg["From"] = cfg.get("sender") or cfg.get("user")
    msg["To"] = to_email
    msg.set_content(text)
    msg.add_alternative(body, subtype="html")
    try:
        port = int(cfg.get("port") or 587)
        server = smtplib.SMTP_SSL(cfg["host"], port, timeout=15) if port == 465 else smtplib.SMTP(cfg["host"], port, timeout=15)
        with server:
            if port != 465:
                server.starttls()
            if cfg.get("user"):
                server.login(cfg["user"], cfg.get("password") or "")
            server.send_message(msg)
        return True, "sent"
    except Exception as e:
        return False, f"The email server returned an error: {e}"


# ---------------------------------------------------------
# 3. DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@300;400;500;600&display=swap');

:root {
    --navy:#0A1B3A; --navy-deep:#050E1E; --stone:#F6F4F0; --paper:#FFFFFF; --ink:#14213D;
    --steel:#6B7587; --line:#E2DED6; --green:#00A859; --gold:#B8975A; --gold-soft:#E7D8B5;
}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
html { scroll-behavior:smooth; }
.stApp { background:var(--stone); color:var(--ink); font-family:'Jost',sans-serif; }
.block-container { max-width:1240px; padding:0 2rem 3rem 2rem !important; }
h1,h2,h3,h4 { font-family:'Cormorant Garamond',serif !important; color:var(--navy); }
p,label,span,div { font-family:'Jost',sans-serif; }

@keyframes pf-rise { from { opacity:0; transform:translateY(34px); } to { opacity:1; transform:none; } }
@keyframes pf-shimmer { to { background-position:-200% 0; } }
@keyframes pf-sheen { 0% { left:-60%; } 55%,100% { left:140%; } }
@keyframes pf-kb { from { transform:scale(1); } to { transform:scale(1.07); } }
@keyframes pf-float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-10px); } }
@keyframes pf-pulse { 0% { box-shadow:0 0 0 0 rgba(184,151,90,.6); } 100% { box-shadow:0 0 0 12px rgba(184,151,90,0); } }
@keyframes pf-marquee { to { transform:translateX(-50%); } }
@keyframes pf-glow { 0% { background-position:0% 0%, 100% 100%; } 100% { background-position:30% 40%, 70% 60%; } }
@keyframes pf-pop { 0% { transform:scale(.3); opacity:0; } 70% { transform:scale(1.15); } 100% { transform:scale(1); opacity:1; } }

.pf-load { animation:pf-rise 1s cubic-bezier(.2,.7,.2,1) both; animation-delay:var(--d,0s); }
@supports (animation-timeline: view()) {
    .pf-reveal { animation:pf-rise linear both; animation-timeline:view(); animation-range:entry 0% cover 26%; }
}

.pf-nav { position:sticky; top:0; z-index:50; display:flex; align-items:center; justify-content:space-between;
    padding:20px 4px; margin-bottom:26px; background:rgba(246,244,240,.9); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }
.pf-logo { font-family:'Cormorant Garamond',serif; font-size:1.9rem; font-weight:700; color:var(--navy); }
.pf-logo b { color:var(--gold); }
.pf-logo-img { height:46px; width:auto; display:block; }
.pf-links { display:flex; gap:36px; align-items:center; }
.pf-links a { color:var(--ink) !important; text-decoration:none !important; font-size:.92rem; letter-spacing:.03em; padding:4px 0;
    background:linear-gradient(var(--gold),var(--gold)) 0 100%/0 1px no-repeat; transition:background-size .35s; }
.pf-links a:hover { background-size:100% 1px; }
.pf-links a.pf-cta { background:var(--navy); color:#fff !important; padding:10px 22px; border-radius:999px; transition:background .25s; }
.pf-links a.pf-cta:hover { background:#12306a; }

.pf-rule { height:1px; width:96px; margin:0 0 22px 0; background:linear-gradient(90deg,var(--gold),var(--gold-soft),var(--gold),var(--gold-soft)); background-size:200% 100%; animation:pf-shimmer 4s linear infinite; }
.pf-frame { position:relative; border-radius:14px; overflow:hidden; background:var(--navy); box-shadow:0 34px 60px -28px rgba(10,27,58,.5); }
.pf-frame::after { content:''; position:absolute; inset:12px; border:1px solid rgba(231,216,181,.65); border-radius:8px; pointer-events:none; }
.pf-img { width:100%; display:block; object-fit:cover; animation:pf-kb 20s ease-in-out infinite alternate; }
.pf-placeholder { min-height:320px; display:flex; align-items:center; justify-content:center; text-align:center; color:#9AA3B5; font-size:.9rem; padding:30px;
    background:repeating-linear-gradient(135deg,#0d2149,#0d2149 12px,#0A1B3A 12px,#0A1B3A 24px); }

.pf-kicker { font-size:.85rem; color:var(--steel); margin-bottom:8px; }
.pf-h1 { font-family:'Cormorant Garamond',serif; font-size:clamp(2.8rem,5.4vw,5rem); line-height:1.02; font-weight:600; color:var(--navy); margin:0 0 22px; }
.pf-h2 { font-family:'Cormorant Garamond',serif; font-size:clamp(2rem,3.4vw,3rem); font-weight:600; color:var(--navy); line-height:1.1; margin:0 0 14px; }
.pf-sub { color:var(--steel); font-size:1.04rem; line-height:1.75; max-width:500px; font-weight:300; }
.pf-section { padding-top:78px; }

.st-key-vip { position:relative; overflow:hidden; border-radius:18px; padding:46px 48px !important; min-height:500px; justify-content:center; border:1px solid rgba(184,151,90,.35);
    background:
      radial-gradient(circle at 20% 20%, rgba(184,151,90,.22), transparent 42%),
      radial-gradient(circle at 80% 80%, rgba(40,90,190,.30), transparent 46%),
      linear-gradient(160deg,var(--navy) 0%,var(--navy-deep) 100%);
    background-size:140% 140%,140% 140%,100% 100%; animation:pf-glow 14s ease-in-out infinite alternate; }
.st-key-vip > * { position:relative; z-index:1; }
.st-key-vip .pf-h1 { color:#fff; font-size:clamp(2.4rem,4.6vw,4.2rem); }
.st-key-vip .pf-sub { color:#B9C2D4; }
.pf-badge { display:inline-flex; align-items:center; gap:10px; color:var(--gold-soft); font-size:.85rem; letter-spacing:.14em; text-transform:uppercase; margin-bottom:18px; }
.pf-badge i { width:9px; height:9px; border-radius:50%; background:var(--gold); animation:pf-pulse 1.8s infinite; }

.pf-hero-text { padding:30px 10px 0 4px; }
.pf-hero-text p.lead { font-size:1.12rem; line-height:1.75; color:var(--steel); max-width:470px; font-weight:300; margin-bottom:30px; }
.pf-actions { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:34px; }
.pf-btn { position:relative; overflow:hidden; display:inline-block; padding:14px 30px; border-radius:999px; font-weight:500; font-size:.95rem; text-decoration:none !important; transition:all .25s; }
.pf-btn.solid { background:var(--navy); color:#fff !important; }
.pf-btn.solid::after { content:''; position:absolute; top:0; left:-60%; width:40%; height:100%; background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent); transform:skewX(-20deg); animation:pf-sheen 5s ease-in-out infinite; }
.pf-btn.ghost { border:1px solid var(--navy); color:var(--navy) !important; }
.pf-btn.ghost:hover { background:var(--navy); color:#fff !important; }
.pf-origin { font-size:.82rem; color:var(--steel); letter-spacing:.04em; border-top:1px solid var(--line); padding-top:16px; max-width:470px; }

.pf-marquee { margin-top:70px; overflow:hidden; border-top:1px solid var(--line); border-bottom:1px solid var(--line); padding:20px 0; }
.pf-track { display:flex; width:max-content; animation:pf-marquee 34s linear infinite; }
.pf-track span { font-family:'Cormorant Garamond',serif; font-size:1.5rem; color:var(--navy); padding:0 28px; white-space:nowrap; }
.pf-track span.d { color:var(--gold); padding:0; font-size:.9rem; align-self:center; }

.pf-specs { display:grid; grid-template-columns:repeat(2,1fr); margin-top:26px; border-top:1px solid var(--line); }
.pf-spec { padding:22px 6px 22px 0; border-bottom:1px solid var(--line); }
.pf-spec:nth-child(odd) { border-right:1px solid var(--line); }
.pf-spec:nth-child(even) { padding-left:26px; }
.pf-spec .n { font-family:'Cormorant Garamond',serif; font-size:2.4rem; font-weight:600; color:var(--navy); line-height:1; }
.pf-spec .l { font-size:.85rem; color:var(--steel); margin-top:6px; }
.pf-note { margin-top:20px; font-size:.95rem; line-height:1.7; font-weight:300; }

.st-key-verify { background:var(--paper); border:1px solid var(--line); border-top:2px solid var(--gold); border-radius:14px; padding:30px 34px !important; box-shadow:0 24px 44px -32px rgba(10,27,58,.4); }
.pf-step { display:flex; align-items:center; gap:12px; margin:2px 0 14px; font-weight:500; color:var(--navy); }
.pf-step b { width:28px; height:28px; border-radius:50%; border:1px solid var(--gold); color:var(--gold); display:flex; align-items:center; justify-content:center; font-size:.85rem; }
.pf-ok { display:flex; gap:16px; align-items:center; margin:6px 0 18px; background:#EFFAF4; border:1px solid #BFE8D2; border-radius:12px; padding:18px 20px; }
.pf-ok .dot { width:40px; height:40px; border-radius:50%; background:var(--green); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; flex:none; animation:pf-pop .6s cubic-bezier(.2,.9,.3,1.2) both; }
.pf-ok .t { font-weight:600; color:#0B5C37; }
.pf-ok .s { font-size:.9rem; color:#3F6F58; margin-top:2px; }
.pf-small { font-size:.82rem; color:var(--steel); line-height:1.6; }

.stTextInput input { border-radius:10px !important; border:1px solid #CFCAC0 !important; background:#fff !important; color:var(--ink) !important; height:50px; padding:0 16px !important; font-size:.98rem !important; }
.stTextInput input:focus { border-color:var(--gold) !important; box-shadow:0 0 0 3px rgba(184,151,90,.22) !important; }
.stButton > button, .stFormSubmitButton > button { background:var(--navy) !important; color:#fff !important; border:none !important; border-radius:10px !important; height:50px; font-weight:500 !important; width:100%; transition:all .25s; }
.stButton > button:hover, .stFormSubmitButton > button:hover { background:#12306a !important; transform:translateY(-2px); box-shadow:0 12px 20px -12px rgba(10,27,58,.7); color:#fff !important; }
.st-key-vip .stButton > button { background:linear-gradient(100deg,var(--gold),var(--gold-soft),var(--gold)) !important; background-size:200% 100% !important; color:var(--navy) !important; font-weight:600 !important; }
.stTabs [data-baseweb="tab"] { font-family:'Jost',sans-serif; color:var(--steel); }
.stTabs [aria-selected="true"] { color:var(--navy) !important; }
.stTabs [data-baseweb="tab-highlight"] { background:var(--gold) !important; }
[data-testid="stCameraInput"] { border-radius:12px; overflow:hidden; }

.pf-footer { margin-top:80px; padding-top:28px; border-top:1px solid var(--line); display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; color:var(--steel); font-size:.85rem; }

@media (max-width:768px) {
    .block-container { padding:0 1rem 2rem 1rem !important; }
    .pf-links a:not(.pf-cta) { display:none; }
    .pf-section { padding-top:50px; }
    .st-key-vip { padding:28px 22px !important; }
    .st-key-verify { padding:22px 18px !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 4. NAVIGATION
# ---------------------------------------------------------
logo_html = (
    f'<img class="pf-logo-img" src="{logo_src}" alt="perFecto"/>'
    if logo_src
    else '<div class="pf-logo">per<b>F</b>ecto</div>'
)
render(f"""
<div id="top"></div>
<div class="pf-nav">
    {logo_html}
    <div class="pf-links">
        <a href="#top">Home</a>
        <a href="#range">The set</a>
        <a href="#verify">Authenticity</a>
        <a class="pf-cta" href="#verify">Verify my set</a>
    </div>
</div>
""")

# ---------------------------------------------------------
# 5. COMING SOON
# ---------------------------------------------------------
if teaser_b64:
    st.markdown(
        f"""
<style>
.st-key-vip {{ animation:none !important; }}
.st-key-vip::before {{
    content:''; position:absolute; inset:0; z-index:0;
    background:url(data:image/jpeg;base64,{teaser_b64}) center/cover no-repeat;
    animation:pf-kb 22s ease-in-out infinite alternate;
}}
.st-key-vip::after {{
    content:''; position:absolute; inset:0; z-index:0;
    background:linear-gradient(90deg, rgba(5,14,30,.94) 0%, rgba(5,14,30,.72) 42%, rgba(5,14,30,.12) 100%);
}}
</style>
""",
        unsafe_allow_html=True,
    )

with st.container(key="vip"):
    t_l, _ = st.columns([1.15, 1], gap="large")
    with t_l:
        render("""
        <div class="pf-load" style="--d:.1s"><div class="pf-badge"><i></i>Coming soon</div></div>
        <div class="pf-load" style="--d:.25s"><div class="pf-h1">Something unbreakable is coming.</div></div>
        <div class="pf-load" style="--d:.4s"><div class="pf-rule"></div></div>
        """)
        e1, e2 = st.columns([2.2, 1], gap="small")
        with e1:
            email_vip = st.text_input("Email address", placeholder="Your email address", label_visibility="collapsed", key="vip_email")
        with e2:
            vip_clicked = st.button("Get early access", key="vip_btn")
        if vip_clicked:
            if EMAIL_RE.fullmatch(email_vip.strip()):
                if save_vip_email(email_vip.strip()):
                    st.success("You're on the list. We'll email you before the launch.")
            else:
                st.error("Enter a valid email address, like you@example.com.")

# ---------------------------------------------------------
# 6. HERO
# ---------------------------------------------------------
render('<div class="pf-section"></div>')
hero_l, hero_r = st.columns([1, 1.15], gap="large")
with hero_l:
    render("""
    <div class="pf-hero-text pf-reveal">
        <div class="pf-rule"></div>
        <div class="pf-h1">Perfecting the art of dining.</div>
        <p class="lead">Luxury tableware for the discerning home. Italian design, finished by hand, and made to be used every day for decades.</p>
        <div class="pf-actions">
            <a class="pf-btn solid" href="#range">See the 30-piece set</a>
            <a class="pf-btn ghost" href="#verify">Verify your set</a>
        </div>
        <div class="pf-origin">Italian heritage and craftsmanship</div>
    </div>
    """)
with hero_r:
    render(f'<div class="pf-reveal"><div class="pf-frame">{image_tag(hero_b64, "perFecto brand banner", "hero_banner.jpeg")}</div></div>')

# ---------------------------------------------------------
# 7. MARQUEE
# ---------------------------------------------------------
items = ["18/10 stainless steel", "Italian heritage", "30-piece set", "25-year guarantee", "3.0 mm balance"]
strip = "".join(f'<span>{i}</span><span class="d">◆</span>' for i in items)
render(f'<div class="pf-marquee"><div class="pf-track">{strip}{strip}</div></div>')

# ---------------------------------------------------------
# 8. FLAGSHIP PRODUCT
# ---------------------------------------------------------
render('<div id="range" class="pf-section"></div>')
prod_l, prod_r = st.columns([1.15, 1], gap="large")
with prod_l:
    render(f'<div class="pf-reveal"><div class="pf-frame">{image_tag(product_b64, "perFecto cutlery set", "product_cutlery.jpeg")}</div></div>')
with prod_r:
    render("""
    <div class="pf-reveal">
        <div class="pf-kicker">The flagship set</div>
        <div class="pf-h2">Everything for six at the table.</div>
        <div class="pf-rule"></div>
        <p class="pf-sub">A complete dinner and serving cutlery set in premium 18/10 stainless steel, weighted for a confident, balanced grip.</p>
        <div class="pf-specs">
            <div class="pf-spec"><div class="n">30</div><div class="l">pieces in the set</div></div>
            <div class="pf-spec"><div class="n">6</div><div class="l">place settings</div></div>
            <div class="pf-spec"><div class="n">18/10</div><div class="l">stainless steel</div></div>
            <div class="pf-spec"><div class="n">3.0 mm</div><div class="l">thickness for weight and balance</div></div>
        </div>
        <p class="pf-note">Every set carries a 25-year guarantee. Scan the QR code on your packaging below to activate yours.</p>
    </div>
    """)

# ---------------------------------------------------------
# 9. AUTHENTICITY: SCAN QR -> EMAIL + PHONE -> CONFIRMATION EMAIL
# ---------------------------------------------------------
render('<div id="verify" class="pf-section"></div>')
ver_l, ver_r = st.columns([1, 1.2], gap="large")

with ver_l:
    render("""
    <div class="pf-reveal">
        <div class="pf-kicker">Authenticity</div>
        <div class="pf-h2">Scan to confirm your set is genuine.</div>
        <div class="pf-rule"></div>
        <p class="pf-sub">Scan the QR code on your packaging to confirm your set is an original perFecto.
        Then add your email and phone number to activate your 25-year guarantee. We'll send you a confirmation email.</p>
    </div>
    """)

ss = st.session_state
ss.setdefault("serial", None)
ss.setdefault("done", None)

with ver_r:
    with st.container(key="verify"):
        # ---- Final state ----
        if ss.done:
            render(f"""
            <div class="pf-ok"><div class="dot">✓</div><div>
                <div class="t">Your guarantee is active</div>
                <div class="s">Set {escape(ss.serial)} registered to {escape(ss.done['email'])}</div>
            </div></div>
            """)
            if ss.done["sent"]:
                st.success("A confirmation email is on its way. Check your inbox and spam folder.")
            else:
                st.warning(f"Your registration is saved, but the confirmation email wasn't sent. {ss.done['reason']}")
            if st.button("Register another set", key="again"):
                ss.serial, ss.done = None, None
                st.rerun()

        # ---- Step 2: contact details ----
        elif ss.serial:
            render(f"""
            <div class="pf-ok"><div class="dot">✓</div><div>
                <div class="t">Original perFecto confirmed</div>
                <div class="s">Serial {escape(ss.serial)}</div>
            </div></div>
            <div class="pf-step"><b>2</b>Add your contact details</div>
            """)
            existing = find_registration(ss.serial)
            if existing:
                reg_date = str(existing.get('timestamp', ''))[:10]
                st.info(f"This set was already registered on {reg_date}. If that wasn't you, please contact perFecto support.")
            else:
                with st.form("register_form", border=False):
                    email = st.text_input("Email", placeholder="you@example.com")
                    phone = st.text_input("Phone number", placeholder="+39 333 123 4567")
                    submitted = st.form_submit_button("Activate my guarantee")
                render('<div class="pf-small">We use your details only to confirm and support your guarantee.</div>')
                if submitted:
                    clean_phone = re.sub(r"[\s\-().]", "", phone)
                    if not EMAIL_RE.fullmatch(email.strip()):
                        st.error("Enter a valid email address, like you@example.com.")
                    elif not re.fullmatch(r"\+?\d{8,15}", clean_phone):
                        st.error("Enter a valid phone number with country code, like +39 333 123 4567.")
                    else:
                        with st.spinner("Activating your guarantee..."):
                            sent, reason = send_confirmation_email(email.strip(), ss.serial)
                            save_registration(ss.serial, email.strip(), clean_phone, sent)
                        ss.done = {"email": email.strip(), "sent": sent, "reason": reason}
                        st.rerun()
            if not existing and st.button("Scan a different code", key="rescan"):
                ss.serial = None
                st.rerun()
            elif existing and st.button("Check another code", key="rescan2"):
                ss.serial = None
                st.rerun()

        # ---- Step 1: scan ----
        else:
            render('<div class="pf-step"><b>1</b>Scan the QR code on your packaging</div>')
            tab_cam, tab_up, tab_type = st.tabs(["Use camera", "Upload a photo", "Type the code"])
            decoded, typed = None, None
            with tab_cam:
                shot = st.camera_input("Point the camera at the QR code", label_visibility="collapsed")
                if shot:
                    decoded = decode_qr(shot)
                    if not decoded:
                        st.warning("No QR code found. Hold the code flat, fill the frame, and take the photo again.")
            with tab_up:
                up = st.file_uploader("Upload a photo of the QR code", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
                if up:
                    decoded = decode_qr(up)
                    if not decoded:
                        st.warning("No QR code found in that photo. Try a sharper, closer image.")
            with tab_type:
                c1, c2 = st.columns([2.4, 1])
                with c1:
                    typed = st.text_input("Serial code", placeholder="e.g. PER-1810-7792", label_visibility="collapsed", key="serial_typed")
                with c2:
                    go = st.button("Verify", key="verify_btn")
                if go and not typed.strip():
                    st.warning("Enter the serial code from your packaging.")
                elif not go:
                    typed = None

            candidate = decoded or typed
            if candidate:
                match = SERIAL_RE.search(candidate)
                if match:
                    with st.spinner("Checking the perFecto registry..."):
                        time.sleep(0.6)
                    ss.serial = match.group(0).upper()
                    st.rerun()
                else:
                    st.error("That code isn't a perFecto serial (format PER-0000-0000). Check your packaging and try again.")

# ---------------------------------------------------------
# 10. FOOTER
# ---------------------------------------------------------
render(f"""
<div class="pf-footer">
    <div>© {datetime.now().year} perFecto. Luxury tableware, Italian heritage.</div>
    <div>25-year guarantee on every set</div>
</div>
""")
