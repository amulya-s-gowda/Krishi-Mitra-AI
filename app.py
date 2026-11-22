
import streamlit as st
from datetime import date
from datetime import datetime
from zoneinfo import ZoneInfo
from modules.weather_service import get_district_weather_prediction
from modules.climate_service import get_seasonal_climate
from modules.weather_alerts import get_weather_alert
from modules.weather_advisory import get_farming_advisory
from models.crop_recommendation_no_rainfall import (
    recommend_crop_without_rainfall,
    recommend_crop_with_soil_report
)
from modules.crop_recommendation_without_soil_test import (
    recommend_crops_without_soil_test
)

from modules.crop_information import (
    get_crop_information,
    crop_information,
    crop_information_kn
)
from modules.voice_assistant import (
    capture_voice_question,
    generate_speech_audio
)
@st.cache_data(ttl=3600)
def get_cached_weather(district_name):
    return get_district_weather_prediction(district_name)

# Application configuration
st.set_page_config(
    page_title="Krishi-Mitra AI",
    page_icon="🌱",
    layout="wide"
)




st.markdown("""
<style>
:root {
  --forest: #174d35;
  --leaf: #2f8550;
  --lime: #b7d94b;
  --sun: #f5b942;
  --cream: #fffaf0;
  --ink: #26392e;
}
.stApp {
  background: radial-gradient(ellipse at 8% 2%, rgba(191,222,145,.30), transparent 32%),
              radial-gradient(ellipse at 95% 8%, rgba(255,207,112,.24), transparent 28%),
              linear-gradient(180deg, #f7f8ec 0%, #f3f7ed 48%, #fffaf0 100%);
  color: var(--ink);
}
.block-container {
    max-width: 1320px;
    padding-top: 4.5rem !important;
    padding-bottom: 3rem;
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp small { color: var(--ink); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  color: var(--forest) !important; font-weight: 800 !important; letter-spacing: -.025em;
}
.stApp h2 { margin-top: 1.2rem; }
/* Hero banner */
.km-hero {
  position: relative; overflow: hidden; border-radius: 28px; padding: 30px 34px;
  margin: 8px 0 24px; color: white;
  background: linear-gradient(118deg, #123f2d 0%, #237348 53%, #76a83b 100%);
  box-shadow: 0 16px 38px rgba(28,82,48,.18);
  border: 1px solid rgba(255,255,255,.35);
}
.km-hero:before { content:""; position:absolute; width:300px; height:300px; right:-75px; top:-155px; border-radius:50%; background:rgba(255,255,255,.11); }
.km-hero:after { content:""; position:absolute; width:220px; height:220px; right:115px; bottom:-165px; border-radius:50%; background:rgba(255,211,104,.18); }
.km-hero-inner { position:relative; z-index:1; display:flex; align-items:center; justify-content:space-between; gap:20px; }
.km-kicker { color:#e4f5c8; text-transform:uppercase; letter-spacing:.16em; font-size:12px; font-weight:800; margin-bottom:9px; }
.km-title { color:#fff; font-size:clamp(30px,4vw,46px); font-weight:900; line-height:1.05; letter-spacing:-.04em; margin:0 0 10px; }
.km-subtitle { color:#f0f8e8; font-size:17px; line-height:1.5; max-width:680px; margin:0; }
/* Improve hero banner text visibility */
.km-hero .km-kicker,
.km-hero .km-title,
.km-hero .km-subtitle,
.km-hero .km-pill {
    color: #ffffff !important;
}

.km-hero .km-kicker {
    color: #eaffd8 !important;
}

/* Readable farming season banner */
.km-season-banner {
    background: linear-gradient(110deg, #123f2d, #237348);
    color: #ffffff !important;
    padding: 16px 20px;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 800;
    margin: 12px 0;
}

.km-season-banner * {
    color: #ffffff !important;
}

/* Improve descriptive text readability */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #425b49 !important;
    font-size: 14px !important;
}
.km-hero-art { font-size:76px; line-height:1; filter: drop-shadow(0 8px 8px rgba(0,0,0,.16)); padding:14px; }
.km-pill-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }
.km-pill { display:inline-block; border:1px solid rgba(255,255,255,.28); background:rgba(255,255,255,.13); color:#fff; border-radius:99px; padding:6px 12px; font-size:12px; font-weight:700; }
/* Inputs and controls */
/* Clear and readable language selector and input fields */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input {
    background-color: #ffffff !important;
    color: #173d2b !important;
    border: 2px solid #8eae83 !important;
    border-radius: 10px !important;
}

/* Selected language and dropdown text */
.stSelectbox div[data-baseweb="select"] *,
.stMultiSelect div[data-baseweb="select"] * {
    color: #173d2b !important;
}

/* Widget labels */
.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stDateInput label {
    color: #174d35 !important;
    font-size: 15px !important;
    font-weight: 750 !important;
}

/* Input placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #65796b !important;
    opacity: 1 !important;
}

/* Voice assistant text */
.stApp iframe {
    color-scheme: light;
}
/* Readable information and warning messages */
div[data-testid="stAlert"] {
    background-color: #edf6e9 !important;
    border: 1px solid #a8c99b !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #173d2b !important;
    font-size: 14px !important;
}
div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input, .stDateInput input {
  background:#fff !important; border:1.5px solid #d5e2c9 !important; border-radius:13px !important; min-height:46px;
}
div[data-baseweb="select"] * { color:#244332 !important; }
.stRadio label, .stCheckbox label { font-weight:600; }
.stButton > button, .stFormSubmitButton > button {
  background:linear-gradient(110deg,#247849,#4c9b45) !important; color:#fff !important;
  border:0 !important; border-radius:14px !important; min-height:46px; padding:10px 20px !important;
  font-weight:800 !important; box-shadow:0 6px 15px rgba(37,115,65,.18); transition:transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-2px); box-shadow:0 9px 20px rgba(37,115,65,.25); }
.stButton > button p, .stButton > button span, .stFormSubmitButton > button p { color:#fff !important; }
/* Metric tiles */
div[data-testid="stMetric"] { background:linear-gradient(145deg,#fff 0%,#f0f7e9 100%); border:1px solid #d9e8ce; border-radius:18px; padding:17px 18px; box-shadow:0 6px 18px rgba(43,85,48,.06); }
div[data-testid="stMetricLabel"] { color:#54705b !important; font-weight:700; }
div[data-testid="stMetricValue"] { color:#174d35 !important; font-weight:900; }
/* Expanders, bordered containers and tabs */
details[data-testid="stExpander"] { background:rgba(255,255,255,.88); border:1px solid #dce8d4; border-radius:16px; overflow:hidden; }
details[data-testid="stExpander"] summary { font-weight:750; color:#1c5738; }
div[data-testid="stVerticalBlockBorderWrapper"] { background:rgba(255,255,255,.78); border:1px solid #dce8d4; border-radius:18px; padding:12px; }
button[data-baseweb="tab"] { font-weight:750; }
button[data-baseweb="tab"][aria-selected="true"] { color:#1e7043 !important; }
/* Alerts */
div[data-testid="stAlert"] { border-radius:15px !important; border-width:1px !important; }
div[data-testid="stAlert"] p, div[data-testid="stAlert"] span { font-weight:550; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color:#617565 !important; }
hr { border-color:#dce8d4 !important; margin:1.3rem 0 !important; }
footer { visibility:hidden; }
@media(max-width:700px) {
 .block-container { padding:1rem .85rem 2rem; }
 .km-hero { padding:23px 20px; border-radius:21px; }
 .km-hero-inner { align-items:flex-start; }
 .km-hero-art { font-size:48px; padding:4px; }
 .km-subtitle { font-size:15px; }
 .stApp h1 { font-size:28px !important; }
}

/* FINAL FIX: readable information cards */
div[data-testid="stAlert"],
div[data-testid="stAlert"] > div {
    background: #eaf6e5 !important;
    background-color: #eaf6e5 !important;
    border: 2px solid #a8c99b !important;
    border-radius: 15px !important;
}

div[data-testid="stAlert"] * {
    color: #174d35 !important;
    background-color: transparent !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #174d35 !important;
    font-weight: 650 !important;
}
/* Language selector */
.language-heading {
    color: #174d35 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 10px;
    padding: 10px 14px;
    background: #e8f3df;
    border-left: 5px solid #2f8550;
    border-radius: 8px;
}

div[data-testid="stSelectbox"] {
    margin-bottom: 18px;
}
/* Fix the black Streamlit top header */
header[data-testid="stHeader"] {
    background: #f7f8ec !important;
}

header[data-testid="stHeader"] button {
    color: #174d35 !important;
}

div[data-testid="stToolbar"] {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)




# English and Kannada translations
translations = {
    "English": {
        "title": "Krishi-Mitra AI 🌱",
        "welcome": "Welcome, Farmer!",
        "description": "Your smart farming assistant",
        "district": "Select your district",
        "weather": "Weather Prediction",
        "crop": "Crop Recommendation",
        "soil": "Select your soil type",
        "start": "Get Started"
    },

    "ಕನ್ನಡ": {
        "title": "Krishi-Mitra AI 🌱",
        "welcome": "ನಮಸ್ಕಾರ ರೈತರೇ!",
        "description": "ನಿಮ್ಮ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",
        "district": "ನಿಮ್ಮ ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "weather": "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
        "crop": "ಬೆಳೆ ಶಿಫಾರಸು",
        "soil": "ನಿಮ್ಮ ಮಣ್ಣಿನ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "start": "ಪ್ರಾರಂಭಿಸಿ"
    }
}

# ONBOARDING FLOW
if "onboarding_step" not in st.session_state:
    st.session_state["onboarding_step"] = "welcome"

if st.session_state["onboarding_step"] == "welcome":
    # Language selection
    st.markdown(
        '<div class="language-heading">🌐 Choose Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ</div>',
        unsafe_allow_html=True
    )

    language = st.selectbox(
        "Language",
        ["English", "ಕನ್ನಡ"],
        label_visibility="collapsed",
        key="language_selector"
    )

    # Select translations
    t = translations[language]

    # Farmer-friendly welcome banner
    hero_art = "🌾🌱🚜"
    if language == "English":
        hero_kicker = "KARNATAKA • SMART FARMING • AI"
        hero_subtitle = "Weather insights, crop guidance and a friendly voice assistant in one place."
        hero_pills = ["🌦️ Weather insights", "🌱 Crop guidance", "🎙️ Voice support", "ಕನ್ನಡ • English"]
    else:
        hero_kicker = "ಕರ್ನಾಟಕ • ಸ್ಮಾರ್ಟ್ ಕೃಷಿ • ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ"
        hero_subtitle = "ಹವಾಮಾನ ಮಾಹಿತಿ, ಬೆಳೆ ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಧ್ವನಿ ಸಹಾಯಕ — ಎಲ್ಲವೂ ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ."
        hero_pills = ["🌦️ ಹವಾಮಾನ ಮಾಹಿತಿ", "🌱 ಬೆಳೆ ಮಾರ್ಗದರ್ಶನ", "🎙️ ಧ್ವನಿ ಸಹಾಯ", "ಕನ್ನಡ • English"]
    hero_pills_html = "".join(f'<span class="km-pill">{pill}</span>' for pill in hero_pills)
    st.markdown(
        f'''
        <section class="km-hero">
          <div class="km-hero-inner">
            <div>
              <div class="km-kicker">{hero_kicker}</div>
              <div class="km-title">{t["title"]}</div>
              <p class="km-subtitle">{t["welcome"]} {t["description"]}. {hero_subtitle}</p>
              <div class="km-pill-row">{hero_pills_html}</div>
            </div>
            <div class="km-hero-art" aria-hidden="true">{hero_art}</div>
          </div>
        </section>
        ''',
        unsafe_allow_html=True
    )

    st.divider()




    if st.button(
        "Continue to Farmer Details \u2192"
        if language == "English"
        else "\u0cae\u0cc1\u0c82\u0ca6\u0cc1\u0cb5\u0cb0\u0cbf\u0caf\u0cbf\u0cb0\u0cbf \u2192",
        use_container_width=True
    ):
        st.session_state["onboarding_step"] = "farmer"
        st.rerun()

    st.stop()

else:
    language = st.session_state.get("language_selector", "English")
    t = translations[language]

# Farm location and soil setup
st.subheader("🧭 Tell us about your farm" if language == "English" else "🧭 ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳನ್ನು ತಿಳಿಸಿ")
st.caption("Choose your district and soil type to get more relevant guidance." if language == "English" else "ಸೂಕ್ತ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ನಿಮ್ಮ ಜಿಲ್ಲೆ ಮತ್ತು ಮಣ್ಣಿನ ಪ್ರಕಾರವನ್ನು ಆಯ್ಕೆಮಾಡಿ.")

districts = [
    "Bagalkote",
    "Ballari",
    "Belagavi",
    "Bengaluru Rural",
    "Bengaluru South",
    "Bengaluru Urban",
    "Bidar",
    "Chamarajanagar",
    "Chikkaballapura",
    "Chikkamagaluru",
    "Chitradurga",
    "Dakshina Kannada",
    "Davanagere",
    "Dharwad",
    "Gadag",
    "Hassan",
    "Haveri",
    "Kalaburagi",
    "Kodagu",
    "Kolar",
    "Koppal",
    "Mandya",
    "Mysuru",
    "Raichur",
    "Shivamogga",
    "Tumakuru",
    "Udupi",
    "Uttara Kannada",
    "Vijayanagara",
    "Vijayapura",
    "Yadgiri"
]
district_names_kn = {
    "Bagalkote": "ಬಾಗಲಕೋಟೆ",
    "Ballari": "ಬಳ್ಳಾರಿ",
    "Belagavi": "ಬೆಳಗಾವಿ",
    "Bengaluru Rural": "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ",
    "Bengaluru South": "ಬೆಂಗಳೂರು ದಕ್ಷಿಣ",
    "Bengaluru Urban": "ಬೆಂಗಳೂರು ನಗರ",
    "Bidar": "ಬೀದರ್",
    "Chamarajanagar": "ಚಾಮರಾಜನಗರ",
    "Chikkaballapura": "ಚಿಕ್ಕಬಳ್ಳಾಪುರ",
    "Chikkamagaluru": "ಚಿಕ್ಕಮಗಳೂರು",
    "Chitradurga": "ಚಿತ್ರದುರ್ಗ",
    "Dakshina Kannada": "ದಕ್ಷಿಣ ಕನ್ನಡ",
    "Davanagere": "ದಾವಣಗೆರೆ",
    "Dharwad": "ಧಾರವಾಡ",
    "Gadag": "ಗದಗ",
    "Hassan": "ಹಾಸನ",
    "Haveri": "ಹಾವೇರಿ",
    "Kalaburagi": "ಕಲಬುರಗಿ",
    "Kodagu": "ಕೊಡಗು",
    "Kolar": "ಕೋಲಾರ",
    "Koppal": "ಕೊಪ್ಪಳ",
    "Mandya": "ಮಂಡ್ಯ",
    "Mysuru": "ಮೈಸೂರು",
    "Raichur": "ರಾಯಚೂರು",
    "Shivamogga": "ಶಿವಮೊಗ್ಗ",
    "Tumakuru": "ತುಮಕೂರು",
    "Udupi": "ಉಡುಪಿ",
    "Uttara Kannada": "ಉತ್ತರ ಕನ್ನಡ",
    "Vijayanagara": "ವಿಜಯನಗರ",
    "Vijayapura": "ವಿಜಯಪುರ",
    "Yadgiri": "ಯಾದಗಿರಿ"
}

district = st.selectbox(
    t["district"],
    districts,
    format_func=lambda x: district_names_kn[x] if language == "ಕನ್ನಡ" else x,
    key="farmer_district"
)

# Soil selection
soil_types = [
    "Red Soil",
    "Black Soil",
    "Alluvial Soil",
    "Laterite Soil",
    "Clay Soil"
]


season_names_kn = {
    "Kharif": "ಮುಂಗಾರು",
    "Rabi": "ಹಿಂಗಾರು",
    "Summer": "ಬೇಸಿಗೆ"
}
soil_names_kn = {
    "Red Soil": "ಕೆಂಪು ಮಣ್ಣು",
    "Black Soil": "ಕಪ್ಪು ಮಣ್ಣು",
    "Alluvial Soil": "ಮೆಕ್ಕಲು ಮಣ್ಣು",
    "Laterite Soil": "ಜಂಬಿಟ್ಟಿಗೆ ಮಣ್ಣು",
    "Clay Soil": "ಜೇಡಿ ಮಣ್ಣು"
}


soil = st.selectbox(
    t["soil"],
    soil_types,
    format_func=lambda x: soil_names_kn[x] if language == "ಕನ್ನಡ" else x,
    key="farmer_soil"
)


# Automatically detect farming season
today = datetime.now(ZoneInfo("Asia/Kolkata"))
current_month = today.month

if current_month in [6, 7, 8, 9, 10]:
    season = "Kharif"

elif current_month in [11, 12, 1, 2]:
    season = "Rabi"

else:
    season = "Summer"

season_names_kn = {
    "Kharif": "ಮುಂಗಾರು",
    "Rabi": "ಹಿಂಗಾರು",
    "Summer": "ಬೇಸಿಗೆ"
}
# ---------------------------------
# SEASONAL CLIMATE INFORMATION
# ---------------------------------

st.subheader("Seasonal Climate Information" if language == "English" else "\u0c8b\u0ca4\u0cc1\u0cae\u0cbe\u0ca8\u0ca6 \u0cb9\u0cb5\u0cbe\u0cae\u0cbe\u0ca8 \u0cae\u0cbe\u0cb9\u0cbf\u0ca4\u0cbf")

district_mapping = {
    "Chamarajanagar": "Chamarajanagara",
    "Yadgiri": "Yadgir"
}

climate_district = district_mapping.get(district, district)

try:
    climate = get_seasonal_climate(
        climate_district,
        season
    )

    st.caption(
        "Historical seasonal averages based on 2023\u20132025 data" if language == "English" else "\u0cb9\u0cbf\u0c82\u0ca6\u0cbf\u0ca8 \u0cb9\u0cb5\u0cbe\u0cae\u0cbe\u0ca8\u0ca6 \u0cb8\u0cb0\u0cbe\u0cb8\u0cb0\u0cbf \u0cae\u0cc2\u0cb2\u0ccd\u0caf\u0c97\u0cb3\u0cc1"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Rainfall" if language == "English" else "\u0cb8\u0cb0\u0cbe\u0cb8\u0cb0\u0cbf \u0cae\u0cb3\u0cc6",
            f'{climate["rainfall"]:.2f} mm/day'
        )

    with col2:
        st.metric(
            "Average Temperature" if language == "English" else "\u0cb8\u0cb0\u0cbe\u0cb8\u0cb0\u0cbf \u0ca4\u0cbe\u0caa\u0cae\u0cbe\u0ca8",
            f'{climate["temperature"]:.2f} °C'
        )

    with col3:
        st.metric(
            "Average Humidity" if language == "English" else "\u0cb8\u0cb0\u0cbe\u0cb8\u0cb0\u0cbf \u0c86\u0cb0\u0ccd\u0ca6\u0ccd\u0cb0\u0ca4\u0cc6",
            f'{climate["humidity"]:.2f} %'
        )

except Exception as error:
    st.warning(f"Climate information unavailable: {error}")
# Display detected season
st.subheader(
    "Current Farming Season" if language == "English"
    else "ಪ್ರಸ್ತುತ ಕೃಷಿ ಹಂಗಾಮು"
)

st.markdown(
    f"""
    <div class="km-season-banner">
        🌾 {"Current Season: " + str(season) if language == "English" else "ಪ್ರಸ್ತುತ ಹಂಗಾಮು: " + str(season_names_kn[season])}
    </div>
    """,
    unsafe_allow_html=True
)



land_area = st.number_input(
    "Enter Land Area (in acres)" if language == "English" else "\u0c9c\u0cae\u0cc0\u0ca8\u0cbf\u0ca8 \u0cb5\u0cbf\u0cb8\u0ccd\u0ca4\u0cc0\u0cb0\u0ccd\u0ca3 (\u0c8e\u0c95\u0cb0\u0cc6\u0c97\u0cb3\u0cb2\u0ccd\u0cb2\u0cbf)",
    min_value=0.1,
    max_value=1000.0,
    value=1.0,
    step=0.5
,
    key="farmer_land_area"
)




# ONBOARDING: FARMER DETAILS
if not st.session_state.get("onboarding_completed", False):

    st.divider()
    back_col, continue_col = st.columns(2)

    with back_col:
        if st.button(
            "\u2190 Back" if language == "English" else "\u2190 \u0cb9\u0cbf\u0c82\u0ca6\u0cc6",
            use_container_width=True
        ):
            st.session_state["onboarding_step"] = "welcome"
            st.rerun()

    with continue_col:
        if st.button(
            "Continue \u2192" if language == "English" else "\u0cae\u0cc1\u0cc2\u0ca6\u0cc1\u0cb5\u0cb0\u0cbf\u0caf\u0cbf\u0cb0\u0cbf \u2192",
            type="primary",
            use_container_width=True
        ):
            st.session_state["onboarding_completed"] = True
            st.rerun()

    st.stop()

# ---------------------------------

st.divider()

st.header("🌾 Farmer Dashboard" if language == "English" else "🌾 ರೈತರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್")

# Display farmer selections
st.subheader("Your Farm Details" if language == "English" else "ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳು")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"📍 District: {district_names_kn[district] if language == 'ಕನ್ನಡ' else district}"
    )

with col2:
    st.info(
        f"🌱 Soil: {soil_names_kn[soil] if language == 'ಕನ್ನಡ' else soil}"
    )

st.info(
    f"🌦️ Season: {season_names_kn[season] if language == 'ಕನ್ನಡ' else season}"
)

st.info(f"🌾 Land Area: {land_area} acres")

st.divider()

# Weather section
st.subheader(
    "🌦️ Weather Prediction" if language == "English"
    else "🌦️ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ"
)

st.write(
    "Get weather information for your selected district."
    if language == "English"
    else "ನಿಮ್ಮ ಆಯ್ಕೆ ಮಾಡಿದ ಜಿಲ್ಲೆಯ ಹವಾಮಾನ ಮಾಹಿತಿಯನ್ನು ಪಡೆಯಿರಿ."
)




try:
    # Match the app's district names with the weather module
    district_mapping = {
        "Chamarajanagar": "Chamarajanagara",
        "Yadgiri": "Yadgir"
    }

    weather_district = district_mapping.get(district, district)

    # Get weather information for the selected district
    result = get_cached_weather(weather_district)

    weather = result["weather_inputs"]

    # Display weather data date
    st.write(
        ("Weather data date: " if language == "English"
         else "ಹವಾಮಾನ ದತ್ತಾಂಶದ ದಿನಾಂಕ: "),
        result["weather_date"].strftime("%d-%m-%Y")
    )

    # Display weather information
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Temperature (°C)" if language == "English" else "ತಾಪಮಾನ (°C)",
            round(weather["temperature"], 2)
        )

        st.metric(
            "Maximum Temperature (°C)" if language == "English" else "ಗರಿಷ್ಠ ತಾಪಮಾನ (°C)",
            round(weather["max_temperature"], 2)
        )

        st.metric(
            "Minimum Temperature (°C)" if language == "English" else "ಕನಿಷ್ಠ ತಾಪಮಾನ (°C)",
            round(weather["min_temperature"], 2)
        )

    with col2:
        st.metric(
            "Humidity (%)" if language == "English" else "ಆರ್ದ್ರತೆ (%)",
            round(weather["humidity"], 2)
        )

        st.metric(
            "Recent Rainfall (mm)" if language == "English" else "ಇತ್ತೀಚಿನ ಮಳೆ (ಮಿಮೀ)",
            round(weather["rainfall"], 2)
        )

        st.metric(
            "Data Age (days)" if language == "English" else "ದತ್ತಾಂಶದ ವಯಸ್ಸು (ದಿನಗಳು)",
            result["data_age_days"]
        )

    # Show prediction only when data is sufficiently recent
    if result["is_recent"]:

        st.success(
            "Weather data is recent." if language == "English"
            else "ಹವಾಮಾನ ದತ್ತಾಂಶವು ಇತ್ತೀಚಿನದ್ದಾಗಿದೆ."
        )

        st.write(
            ("Prediction date: " if language == "English"
             else "ಮುನ್ಸೂಚನೆಯ ದಿನಾಂಕ: "),
            result["prediction_date"].strftime("%d-%m-%Y")
        )

        st.metric(
            "Predicted Next-Day Rainfall (mm)" if language == "English"
            else "ಮುಂದಿನ ದಿನದ ನಿರೀಕ್ಷಿತ ಮಳೆ (ಮಿಮೀ)",
            round(result["predicted_rainfall"], 2)
        )

    else:

        st.warning(
            result["status_message"] if language == "English"
            else "ಹವಾಮಾನ ದತ್ತಾಂಶ ತಡವಾಗಿ ಲಭ್ಯವಾಗಿದೆ. ಇದನ್ನು ಪ್ರಸ್ತುತ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಎಂದು ಪರಿಗಣಿಸಬೇಡಿ."
        )

        st.write(
            ("Historical model estimate: " if language == "English"
             else "ಹಿಂದಿನ ದತ್ತಾಂಶದ ಆಧಾರದ ಅಂದಾಜು: "),
            round(result["predicted_rainfall"], 2),
            "mm"
        )

    # ---------------------------------
    # WEATHER ALERTS AND FARMER ADVISORY
    # ---------------------------------

    st.divider()

    st.subheader(
        "⚠️ Weather Alerts and Farmer Advisory"
        if language == "English"
        else "⚠️ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ ಮತ್ತು ರೈತರ ಸಲಹೆ"
    )

    if result["is_recent"]:

        alert = get_weather_alert(
            result["predicted_rainfall"],
            language
        )

        st.metric(
            "Predicted Rainfall"
            if language == "English"
            else "ನಿರೀಕ್ಷಿತ ಮಳೆ",
            f'{alert["rainfall"]:.2f} mm'
        )

        st.write(
            "**Rainfall Category:**"
            if language == "English"
            else "**ಮಳೆಯ ವರ್ಗ:**",
            alert["category"]
        )

        if alert["rainfall"] >= 64.5:
            st.warning(alert["advice"])
        else:
            st.info(alert["advice"])
                    # Additional weather-based farming suggestions
        farming_advisories = get_farming_advisory(
            rainfall=result["predicted_rainfall"],
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            language=language
        )

        st.markdown(
            "### 🌱 Farming Suggestions"
            if language == "English"
            else "### 🌱 ಕೃಷಿ ಸಲಹೆಗಳು"
        )

        for advice in farming_advisories:
            st.info("• " + advice)

        st.caption(
            "Advisory based on the model estimate, not an official IMD warning."
            if language == "English"
            else "ಈ ಸಲಹೆಯು ಮಾದರಿಯ ಅಂದಾಜಿನ ಆಧಾರದ ಮೇಲೆ ನೀಡಲಾಗಿದೆ. ಇದು ಅಧಿಕೃತ IMD ಎಚ್ಚರಿಕೆಯಲ್ಲ."
        )

    else:

        st.warning(
            "Weather alerts are unavailable because the latest weather data is delayed. "
            "Please check official weather updates."
            if language == "English"
            else "ಇತ್ತೀಚಿನ ಹವಾಮಾನ ದತ್ತಾಂಶ ತಡವಾಗಿ ಲಭ್ಯವಾಗಿರುವುದರಿಂದ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ. "
                 "ದಯವಿಟ್ಟು ಅಧಿಕೃತ ಹವಾಮಾನ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."
        )


except Exception as error:

    st.error(
        ("Unable to retrieve weather data: " if language == "English"
         else "ಹವಾಮಾನ ದತ್ತಾಂಶವನ್ನು ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ: ")
        + str(error)
    )


st.divider()

# Crop section

st.subheader(
    "🌱 Crop Recommendation" if language == "English"
    else "🌱 ಬೆಳೆ ಶಿಫಾರಸು"
)

st.write(
    "Find suitable crops based on soil, season and weather."
    if language == "English"
    else "ಮಣ್ಣು, ಹಂಗಾಮು ಮತ್ತು ಹವಾಮಾನದ ಆಧಾರದ ಮೇಲೆ ಸೂಕ್ತ ಬೆಳೆಗಳನ್ನು ತಿಳಿಯಿರಿ."
)

# Ask whether the farmer has a soil test report
soil_report_option = st.radio(
    "Do you have a soil test report?"
    if language == "English"
    else "ನಿಮ್ಮ ಬಳಿ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಇದೆಯೇ?",

    [
        "Yes, I have a report",
        "No, I don't have a report"
    ] if language == "English" else [
        "ಹೌದು, ವರದಿ ಇದೆ",
        "ಇಲ್ಲ, ವರದಿ ಇಲ್ಲ"
    ],

    index=None,
    key="soil_report_option"
)

has_soil_report = (
    soil_report_option == "Yes, I have a report"
    if language == "English"
    else soil_report_option == "ಹೌದು, ವರದಿ ಇದೆ"
)
if soil_report_option is None:
    has_soil_report = None

soil_inputs = {}

if soil_report_option is None:

    st.info(
        "Please select whether you have a soil test report."
        if language == "English"
        else "ದಯವಿಟ್ಟು ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಇದೆಯೇ ಎಂದು ಆಯ್ಕೆಮಾಡಿ."
    )

elif has_soil_report:

    st.info(
        "Enter the values exactly as shown in your soil test report."
        if language == "English"
        else "ನಿಮ್ಮ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿಯಲ್ಲಿರುವ ಮೌಲ್ಯಗಳನ್ನು ನಮೂದಿಸಿ."
    )

    col1, col2 = st.columns(2)

    with col1:
        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=None,
            step=1.0,
            format="%.2f",
            key="soil_nitrogen_input"
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=None,
            step=1.0,
            format="%.2f",
            key="soil_phosphorus_input"
        )

    with col2:
        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=None,
            step=1.0,
            format="%.2f",
            key="soil_potassium_input"
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=None,
            step=0.1,
            format="%.2f",
            key="soil_ph_input"
        )

    soil_inputs = {
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "ph": ph
    }

    st.caption(
        "These values will be used for crop suitability analysis."
        if language == "English"
        else "ಈ ಮೌಲ್ಯಗಳನ್ನು ಬೆಳೆ ಸೂಕ್ತತೆ ವಿಶ್ಲೇಷಣೆಗೆ ಬಳಸಲಾಗುತ್ತದೆ."
    )

else:

    st.warning(
        "A soil test is recommended for reliable NPK and pH values. "
        "Please visit a soil testing laboratory. "
        "We will not invent soil values."
        if language == "English"
        else "NPK ಮತ್ತು pH ಮೌಲ್ಯಗಳನ್ನು ನಿಖರವಾಗಿ ತಿಳಿಯಲು ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ ಮಾಡಿಸುವುದು ಉತ್ತಮ. "
             "ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ಪ್ರಯೋಗಾಲಯವನ್ನು ಸಂಪರ್ಕಿಸಿ. "
             "ತಪ್ಪಾದ ಮೌಲ್ಯಗಳನ್ನು ನಾವು ಊಹಿಸುವುದಿಲ್ಲ."
    )

# ML crop recommendation
st.divider()

st.subheader(
    "🌱 District-Aware Crop Recommendations"
    if language == "English"
    else "🌱 ಜಿಲ್ಲೆಯ ಆಧಾರಿತ ಬೆಳೆ ಶಿಫಾರಸುಗಳು"
)

# Case 1: Farmer has not selected Yes or No
if soil_report_option is None:

    st.info(
        "Please select whether you have a soil test report above."
        if language == "English"
        else "ದಯವಿಟ್ಟು ಮೇಲಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿ ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ."
    )

# Case 2: Farmer has a soil test report
elif has_soil_report:

    if st.button(
        "Get Crop Recommendation"
        if language == "English"
        else "ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ",
        use_container_width=True,
        key="ml_crop_recommendation"
    ):

                # Validate soil values
        valid_values = (
            nitrogen is not None
            and phosphorus is not None
            and potassium is not None
            and ph is not None
            and 0 <= nitrogen <= 140
            and 5 <= phosphorus <= 145
            and 5 <= potassium <= 205
            and 3.5 <= ph <= 9.94
        )

        if any(value is None for value in (
            nitrogen, phosphorus, potassium, ph
        )):
            st.error(
                "Please enter all four values from your soil test report."
                if language == "English"
                else "ದಯವಿಟ್ಟು ಮಣ್ಣಿನ ಪರೀಕ್ಷಾ ವರದಿಯಲ್ಲಿರುವ ಎಲ್ಲಾ ನಾಲ್ಕು ಮೌಲ್ಯಗಳನ್ನು ನಮೂದಿಸಿ."
            )

        elif not valid_values:
            st.error(
                "One or more soil values are outside the model's training data ranges. "
                "Please check your soil report."
                if language == "English"
                else "ಕೆಲವು ಮಣ್ಣಿನ ಮೌಲ್ಯಗಳು ಮಾದರಿಯ ತರಬೇತಿ ದತ್ತಾಂಶದ ವ್ಯಾಪ್ತಿಯಲ್ಲಿಲ್ಲ. "
                     "ದಯವಿಟ್ಟು ನಿಮ್ಮ ವರದಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."
            )

        else:

            try:

                # Match district names with the climate dataset
                district_mapping = {
                    "Chamarajanagar": "Chamarajanagara",
                    "Yadgiri": "Yadgir"
                }

                climate_district = district_mapping.get(
                    district, district
                )

                # Get historical seasonal temperature and humidity
                climate = get_seasonal_climate(
                    climate_district,
                    season
                )

                temperature = climate["temperature"]
                humidity = climate["humidity"]

                # Call the six-feature ML model
                # Get district-aware ML crop recommendations
                result = recommend_crop_with_soil_report(
    n=nitrogen,
    p=phosphorus,
    k=potassium,
    temperature=temperature,
    humidity=humidity,
    ph=ph,
    district=district,
    soil=soil,
    season=season
)
                st.session_state["voice_recommendations"] = result
                st.session_state["voice_recommendation_type"] = "ml"
                st.session_state["voice_recommendation_context"] = (district, soil, season)

                # Display top 3 crop recommendations
                st.success(
                    "Top 3 Recommended Crops"
                    if language == "English"
                    else "ಅತ್ಯುತ್ತಮ 3 ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆಗಳು"
                )

                for i, crop in enumerate(result, start=1):

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.write(
                            f"**{i}. {crop['crop'].upper()}**"
                        )

                    with col2:

                        if crop["confidence"] > 0:

                            st.metric(
                                "ML Prediction Score"
                                if language == "English"
                                else "ML Prediction Score",
                                f"{crop['confidence']}%"
                            )

                        else:

                            st.metric(
                                "ML Score (No Model Support)"
                                if language == "English"
                                else "ML Score (No Model Support)",
                                "0.0%"
                            )
                    if crop["confidence"] > 0:

                        st.success(
                            "ML-supported prediction"
                            if language == "English"
                            else "ML-supported prediction"
                        )

                    else:

                        st.info(
                            "Soil and season-based alternative; "
                            "the ML model assigned a 0% score."
                            if language == "English"
                            else "Soil and season-based alternative; "
                                 "the ML model assigned a 0% score."
                        )
                    # Get crop information in selected language
                    info = get_crop_information(
                        crop["crop"],
                        language
                    )

                    if info:

                        with st.expander(
                            f"🌱 Farming Guide - {info['name']}"
                            if language == "English"
                            else f"🌱 ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ - {info['name']}"
                        ):

                            st.write(
                                "**Season:**"
                                if language == "English"
                                else "**ಹಂಗಾಮು:**",
                                info["season"]
                            )

                            st.write(
                                "**Suitable Soil:**"
                                if language == "English"
                                else "**ಸೂಕ್ತ ಮಣ್ಣು:**",
                                info["soil"]
                            )

                            st.write(
                                "**Water Requirements:**"
                                if language == "English"
                                else "**ನೀರಿನ ಅವಶ್ಯಕತೆ:**",
                                info["water"]
                            )
                            crop_field_labels = {
                                "sowing": (
                                    "Sowing Time:"
                                    if language == "English"
                                    else "ಬಿತ್ತನೆ ಸಮಯ:"
                                ),
                                "seed_rate": (
                                    "Seed Rate:"
                                    if language == "English"
                                    else "ಬೀಜದ ಪ್ರಮಾಣ:"
                                ),
                                "duration": (
                                    "Crop Duration:"
                                    if language == "English"
                                    else "ಬೆಳೆಯ ಅವಧಿ:"
                                ),
                                "irrigation": (
                                    "Irrigation:"
                                    if language == "English"
                                    else "ನೀರಾವರಿ:"
                                ),
                                "harvesting": (
                                    "Harvesting:"
                                    if language == "English"
                                    else "ಕೊಯ್ಲು:"
                                )
                            }

                            for field, label in crop_field_labels.items():
                                if info.get(field):
                                    st.write(
                                        f"**{label}**",
                                        info[field]
                                    )


                            st.write(
                                "**Farming Guidance:**"
                                if language == "English"
                                else "**ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ:**"
                            )

                            for point in info["guidance"]:
                                st.write("•", point)

                            st.info(info["karnataka_note"])

                # Display climate information
                st.metric(
                    "Temperature"
                    if language == "English"
                    else "ತಾಪಮಾನ",
                    f"{temperature:.2f} °C"
                )

                st.caption(
                    f"Seasonal humidity used: {humidity:.2f}%"
                    if language == "English"
                    else f"ಬಳಸಿದ ಹಂಗಾಮಿನ ತೇವಾಂಶ: {humidity:.2f}%"
                )

                st.info(
                    "This is a preliminary ML-based suggestion. "
                    "Temperature and humidity are historical seasonal averages "
                    "from 2023–2025, not live forecasts. The model uses a general "
                    "crop dataset and has not been validated through Karnataka field trials. "
                    "Please consult local agricultural experts before planting."
                    if language == "English"
                    else "ಇದು ಪ್ರಾಥಮಿಕ ML ಆಧಾರಿತ ಸಲಹೆಯಾಗಿದೆ. "
                         "ತಾಪಮಾನ ಮತ್ತು ತೇವಾಂಶವು 2023–2025ರ ಐತಿಹಾಸಿಕ ಹಂಗಾಮಿನ ಸರಾಸರಿಗಳಾಗಿವೆ. "
                         "ಇವು ಪ್ರಸ್ತುತ ಮುನ್ಸೂಚನೆಗಳಲ್ಲ. ಬೆಳೆ ಬಿತ್ತುವ ಮೊದಲು ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
                )

            except Exception as error:

                st.error(
                    f"Unable to generate crop recommendation: {error}"
                    if language == "English"
                    else f"ಬೆಳೆ ಶಿಫಾರಸು ನೀಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ: {error}"
                )

# Case 3: Farmer does not have a soil test report
else:

    if st.button(
        "Get Crop Recommendation"
        if language == "English"
        else "ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ",
        use_container_width=True,
        key="no_soil_recommendation"
    ):

        try:

            # Get recommendations using soil type, season and district

            result = recommend_crops_without_soil_test(
                soil=soil,
                season=season,
                district=district
            )
            st.session_state["voice_recommendations"] = result
            st.session_state["voice_recommendation_type"] = "rules"
            st.session_state["voice_recommendation_context"] = (district, soil, season)

            st.success(
                "Top 3 Suitable Crop Suggestions"
                if language == "English"
                else "ಅತ್ಯುತ್ತಮ 3 ಸೂಕ್ತ ಬೆಳೆ ಸಲಹೆಗಳು"
            )

            for i, crop in enumerate(result, start=1):

                info = get_crop_information(crop["crop"], language)

                display_name = (
                    info["name"]
                    if info
                    else crop["crop"].replace("_", " ").title()
                )

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**{i}. {display_name}**")

                with col2:
                    st.metric(
                        "Rule Match Score"
                        if language == "English"
                        else "ನಿಯಮ ಹೊಂದಾಣಿಕೆ ಅಂಕ",
                        f"{crop['score']}/4"
                    )

                    st.caption(
    f"{crop['score']} out of 4 soil-and-season rule points matched."
    if language == "English"
    else f"ಮಣ್ಣು ಮತ್ತು ಹಂಗಾಮಿನ ನಿಯಮಗಳಲ್ಲಿ {crop['score']} / 4 ಅಂಶಗಳು ಹೊಂದಿಕೆಯಾಗಿವೆ."
)

                st.write(
                    "**Rule Match Details:**"
                    if language == "English"
                    else "**ನಿಯಮ ಹೊಂದಾಣಿಕೆಯ ವಿವರಗಳು:**"
                )

                if crop["soil_match"]:
                    st.write(
                        "✓ Matches selected soil type"
                        if language == "English"
                        else "✓ ಆಯ್ಕೆ ಮಾಡಿದ ಮಣ್ಣಿನ ವಿಧಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆ"
                    )

                if crop["season_match"]:
                    st.write(
                        "✓ Matches selected farming season"
                        if language == "English"
                        else "✓ ಆಯ್ಕೆ ಮಾಡಿದ ಹಂಗಾಮಿಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆ"
                    )

                if crop.get("district_match") is True:
                    st.write(
                        "✓ Included in the selected district's crop profile"
                        if language == "English"
                        else "✓ ಆಯ್ಕೆ ಮಾಡಿದ ಜಿಲ್ಲೆಯ ಬೆಳೆ ಪ್ರೊಫೈಲ್‌ನಲ್ಲಿ ಸೇರಿಸಲಾಗಿದೆ"
                    )

                elif crop.get("district_match") is None:
                    st.info(
                        "District-specific crop data is not yet available."
                        if language == "English"
                        else "ಈ ಜಿಲ್ಲೆಗೆ ಸಂಬಂಧಿಸಿದ ಪ್ರತ್ಯೇಕ ಬೆಳೆ ಮಾಹಿತಿ ಇನ್ನೂ ಲಭ್ಯವಿಲ್ಲ."
                    )



                if info:
                    with st.expander(
                        f"🌱 Farming Guide - {info['name']}"
                        if language == "English"
                        else f"🌱 ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ - {info['name']}"
                    ):
                        st.write(
                            "**Season:**" if language == "English" else "**ಹಂಗಾಮು:**",
                            info["season"]
                        )
                        st.write(
                            "**Suitable Soil:**" if language == "English" else "**ಸೂಕ್ತ ಮಣ್ಣು:**",
                            info["soil"]
                        )
                        st.write(
                            "**Water Requirements:**" if language == "English" else "**ನೀರಿನ ಅವಶ್ಯಕತೆ:**",
                            info["water"]
                        )
                        crop_field_labels = {
                            "sowing": (
                                "Sowing Time:"
                                if language == "English"
                                else "ಬಿತ್ತನೆ ಸಮಯ:"
                            ),
                            "seed_rate": (
                                "Seed Rate:"
                                if language == "English"
                                else "ಬೀಜದ ಪ್ರಮಾಣ:"
                            ),
                            "duration": (
                                "Crop Duration:"
                                if language == "English"
                                else "ಬೆಳೆಯ ಅವಧಿ:"
                            ),
                            "irrigation": (
                                "Irrigation:"
                                if language == "English"
                                else "ನೀರಾವರಿ:"
                            ),
                            "harvesting": (
                                "Harvesting:"
                                if language == "English"
                                else "ಕೊಯ್ಲು:"
                            )
                        }

                        for field, label in crop_field_labels.items():
                            if info.get(field):
                                st.write(
                                    f"**{label}**",
                                    info[field]
                                )

                        st.write(
                            "**Farming Guidance:**"
                            if language == "English"
                            else "**ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ:**"
                        )

                        for point in info["guidance"]:
                            st.write("•", point)

                        st.info(info["karnataka_note"])

            st.warning(
                "These are preliminary rule-based suggestions using soil type, "
                "farming season and available district crop profiles. They are "
                "not guaranteed yield predictions. Check local rainfall, water "
                "availability and agricultural advice before planting."
                if language == "English"
                else "ಇವು ಮಣ್ಣಿನ ವಿಧ, ಕೃಷಿ ಹಂಗಾಮು ಮತ್ತು ಲಭ್ಯವಿರುವ ಜಿಲ್ಲೆಯ ಬೆಳೆ ಮಾಹಿತಿಯ "
                     "ಆಧಾರದ ಪ್ರಾಥಮಿಕ ನಿಯಮಾಧಾರಿತ ಸಲಹೆಗಳಾಗಿವೆ. ಇವು ಖಚಿತ ಇಳುವರಿ ಮುನ್ಸೂಚನೆಗಳಲ್ಲ. "
                     "ಬಿತ್ತನೆಗೂ ಮೊದಲು ಸ್ಥಳೀಯ ಮಳೆ, ನೀರಿನ ಲಭ್ಯತೆ ಮತ್ತು ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪರಿಶೀಲಿಸಿ."
            )

        except Exception as error:
            st.error(
                f"Unable to generate crop suggestions: {error}"
                if language == "English"
                else f"ಬೆಳೆ ಸಲಹೆಗಳನ್ನು ನೀಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ: {error}"
            )


# KRISHIMITRA VOICE ASSISTANT
# ---------------------------------


st.divider()

with st.container(border=True):

    st.subheader(
        "🎙️ Krishi-Mitra AI Voice Assistant"
        if language == "English"
        else "🎙️ ಕೃಷಿಮಿತ್ರ ಧ್ವನಿ ಸಹಾಯಕ"
    )

    st.write(
        "Ask your farming questions using your voice or type them below."
        if language == "English"
        else "ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಧ್ವನಿಯ ಮೂಲಕ ಕೇಳಿ ಅಥವಾ ಕೆಳಗೆ ಟೈಪ್ ಮಾಡಿ."
    )

    st.info(
        "Click Start speaking, ask your question, and then click Stop recording."
        if language == "English"
        else "ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ ಆಯ್ಕೆಮಾಡಿ, ಪ್ರಶ್ನೆ ಕೇಳಿ ಮತ್ತು ನಂತರ ರೆಕಾರ್ಡಿಂಗ್ ನಿಲ್ಲಿಸಿ."
    )

    voice_question = None

    if "saved_voice_question" not in st.session_state:
        st.session_state.saved_voice_question = ""

    try:
        voice_question = capture_voice_question(language)

        if voice_question:
            st.session_state.saved_voice_question = voice_question

            st.success(
                "Voice question recognized!"
                if language == "English"
                else "ಧ್ವನಿ ಪ್ರಶ್ನೆಯನ್ನು ಗುರುತಿಸಲಾಗಿದೆ!"
            )

            st.write("**" + (
                "Your question:"
                if language == "English"
                else "ನಿಮ್ಮ ಪ್ರಶ್ನೆ:"
            ) + "**")

            st.write(voice_question)

    except Exception:
        st.warning(
            "Voice recognition is temporarily unavailable."
            if language == "English"
            else "ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆ ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ."
        )

    st.divider()

    text_question = st.text_input(
        "Or type your farming question"
        if language == "English"
        else "ಅಥವಾ ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ",
        key="voice_text_question"
    )

farmer_question = (
    voice_question
    or text_question
    or st.session_state.get("saved_voice_question", "")
)




if st.button(
    "Get Answer" if language == "English" else "ಉತ್ತರ ಪಡೆಯಿರಿ",
    key="voice_get_answer"
):
    if not farmer_question or not farmer_question.strip():
        st.warning(
            "Please ask a question first."
            if language == "English"
            else "ದಯವಿಟ್ಟು ಮೊದಲು ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ."
        )

    else:

        question = farmer_question.lower()

        crop_keywords = [
            "crop", "crops", "suitable", "recommend",
            "soil", "water", "irrigation", "precaution",
            "guidance", "tips", "season", "sow",
            "why", "reason", "care",
            "ಬೆಳೆ", "ಬೆಳೆಗಳು", "ಸೂಕ್ತ", "ಮಣ್ಣು",
            "ಉದ್ದು", "ಬ್ಲ್ಯಾಕ್‌ಗ್ರಾಮ್"
        ]
                        # Identify weather-related questions in English and Kannada
        weather_keywords = [
            "weather", "rain", "rainfall", "forecast",
            "temperature", "humidity", "hot", "cold",
            "weather alert", "precaution",
            "ಹವಾಮಾನ", "ಮಳೆ", "ಮಳೆಯ", "ತಾಪಮಾನ",
            "ಆರ್ದ್ರತೆ", "ಮುನ್ಸೂಚನೆ", "ಬಿಸಿಲು", "ಚಳಿ"
        ]

        answer_text = None
        show_recommendations = False

        if any(word in question for word in weather_keywords):

            try:
                district_mapping = {
                    "Chamarajanagar": "Chamarajanagara",
                    "Yadgiri": "Yadgir"
                }

                weather_district = district_mapping.get(
                    district, district
                )

                result = get_cached_weather(weather_district)
                weather = result["weather_inputs"]

                if language == "English":

                    answer_text = (
                        f"Weather information for {district}. "
                        f"The latest available weather data is from "
                        f"{result['weather_date'].strftime('%d-%m-%Y')}. "
                        f"Temperature: {weather['temperature']:.1f} "
                        f"degrees Celsius. "
                        f"Maximum temperature: "
                        f"{weather['max_temperature']:.1f} degrees. "
                        f"Minimum temperature: "
                        f"{weather['min_temperature']:.1f} degrees. "
                        f"Humidity: {weather['humidity']:.1f} percent. "
                        f"Latest recorded rainfall: "
                        f"{weather['rainfall']:.1f} millimetres. "
                    )

                else:

                    answer_text = (
                        f"{district} ಜಿಲ್ಲೆಯ ಹವಾಮಾನ ಮಾಹಿತಿ. "
                        f"ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಹವಾಮಾನ ದತ್ತಾಂಶದ ದಿನಾಂಕ "
                        f"{result['weather_date'].strftime('%d-%m-%Y')}. "
                        f"ತಾಪಮಾನ {weather['temperature']:.1f} "
                        f"ಡಿಗ್ರಿ ಸೆಲ್ಸಿಯಸ್. "
                        f"ಗರಿಷ್ಠ ತಾಪಮಾನ "
                        f"{weather['max_temperature']:.1f} ಡಿಗ್ರಿ. "
                        f"ಕನಿಷ್ಠ ತಾಪಮಾನ "
                        f"{weather['min_temperature']:.1f} ಡಿಗ್ರಿ. "
                        f"ಆರ್ದ್ರತೆ {weather['humidity']:.1f} ಶೇಕಡಾ. "
                        f"ಇತ್ತೀಚಿನ ದಾಖಲಾದ ಮಳೆ "
                        f"{weather['rainfall']:.1f} ಮಿಲಿಮೀಟರ್. "
                    )

                if result["is_recent"]:

                    predicted_rainfall = result["predicted_rainfall"]

                    alert = get_weather_alert(
                        predicted_rainfall,
                        language
                    )

                    farming_advisories = get_farming_advisory(
    rainfall=predicted_rainfall,
    temperature=weather["temperature"],
    humidity=weather["humidity"],
    language=language,
    data_is_recent=result["is_recent"]
)

                    if language == "English":

                        answer_text += (
                            f"Next-day rainfall estimate for "
                            f"{result['prediction_date'].strftime('%d-%m-%Y')} "
                            f"is {predicted_rainfall:.1f} millimetres. "
                            f"Rainfall category: {alert['category']}. "
                            f"{alert['advice']} "
                            f"Farming suggestions: "
                            + " ".join(farming_advisories)
                        )

                    else:

                        answer_text += (
                            f"ಮುಂದಿನ ದಿನದ ಮಳೆಯ ಅಂದಾಜು "
                            f"{result['prediction_date'].strftime('%d-%m-%Y')} "
                            f"ರಂದು {predicted_rainfall:.1f} ಮಿಲಿಮೀಟರ್. "
                            f"ಮಳೆಯ ವರ್ಗ: {alert['category']}. "
                            f"{alert['advice']} "
                            f"ಕೃಷಿ ಸಲಹೆಗಳು: "
                            + " ".join(farming_advisories)
                        )

                else:

                    if language == "English":

                        answer_text += (
                            "Weather data is delayed. "
                            "The following is only a historical model estimate, "
                            f"not a current forecast: "
                            f"{result['predicted_rainfall']:.1f} millimetres. "
                            "Please check official IMD weather updates."
                        )

                    else:

                        answer_text += (
                            "ಹವಾಮಾನ ದತ್ತಾಂಶ ತಡವಾಗಿ ಲಭ್ಯವಾಗಿದೆ. "
                            "ಮುಂದಿನ ಮಳೆಯ ಅಂದಾಜು ಹಿಂದಿನ ದತ್ತಾಂಶದ ಆಧಾರದ ಮೇಲೆ "
                            f"{result['predicted_rainfall']:.1f} ಮಿಲಿಮೀಟರ್. "
                            "ಇದನ್ನು ಪ್ರಸ್ತುತ ಮುನ್ಸೂಚನೆ ಎಂದು ಪರಿಗಣಿಸಬೇಡಿ. "
                            "ಅಧಿಕೃತ IMD ಹವಾಮಾನ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."
                        )

            except Exception:
                answer_text = (
                    "Weather information is temporarily unavailable. "
                    "Please try again later."
                    if language == "English"
                    else "ಹವಾಮಾನ ಮಾಹಿತಿ ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ. "
                         "ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಪ್ರಯತ್ನಿಸಿ."
                )

        elif any(word in question for word in crop_keywords):

            recommendations = st.session_state.get(
                "voice_recommendations"
            )

            recommendation_type = st.session_state.get(
                "voice_recommendation_type"
            )

            # Identify crops using both English and Kannada names
            crop_name = None

            for key, info in crop_information.items():
                english_name = info.get("name", "").lower()

                kannada_name = crop_information_kn.get(
                    key, {}
                ).get("name", "").lower()

                if (
                    key.lower() in question
                    or english_name in question
                    or (kannada_name and kannada_name in question)
                ):
                    crop_name = key
                    break

            # Additional Kannada aliases for Blackgram
            if crop_name is None and any(
    alias in question
    for alias in [
        "black gram",
        "ಬ್ಲ್ಯಾಕ್‌ಗ್ರಾಮ್",
        "ಬ್ಲಾಕ್‌ಗ್ರಾಮ್",
        "ಉದ್ದು"
    ]
):
             crop_name = "blackgram"

            # Identify the question category
            question_type = None

            if any(word in question for word in [
                "why", "reason", "recommended",
                "ಏಕೆ", "ಯಾಕೆ", "ಕಾರಣ"
            ]):
                question_type = "why"

            elif any(word in question for word in [
                "soil", "type of soil", "ಮಣ್ಣು", "ಮಣ್ಣಿನ"
            ]):
                question_type = "soil"

            elif any(word in question for word in [
                "water", "irrigation", "watering",
                "ನೀರು", "ನೀರಾವರಿ"
            ]):
                question_type = "water"

            elif any(word in question for word in [
                "precaution", "care", "guidance", "tips",
                "ಮುನ್ನೆಚ್ಚರಿಕೆ", "ಆರೈಕೆ", "ಮಾರ್ಗದರ್ಶನ", "ಸಲಹೆ"
            ]):
                question_type = "guidance"

            elif any(word in question for word in [
                "season", "when to grow", "when to sow",
                "ಹಂಗಾಮು", "ಯಾವಾಗ", "ಬಿತ್ತನೆ"
            ]):
                question_type = "season"

            show_recommendations = False
            answer_text = None

            # Ordinary crop information does not require recommendations
            if crop_name and question_type:

                info = get_crop_information(
                    crop_name,
                    language
                )

                if info:

                    if question_type == "why":

                        saved_context = st.session_state.get(
                            "voice_recommendation_context"
                        )

                        current_context = (district, soil, season)

                        if saved_context != current_context:
                            st.warning(
                                "Please generate the crop recommendation "
                                "below first, or regenerate it after changing "
                                "your district, soil or season."
                                if language == "English"
                                else "ಮೊದಲು ಬೆಳೆ ಶಿಫಾರಸನ್ನು ರಚಿಸಿ ಅಥವಾ "
                                "ಜಿಲ್ಲೆ, ಮಣ್ಣು ಅಥವಾ ಹಂಗಾಮು ಬದಲಿಸಿದ ನಂತರ "
                                "ಮತ್ತೆ ಶಿಫಾರಸನ್ನು ರಚಿಸಿ."
                            )

                        elif not recommendations:
                            st.warning(
                                "No crop recommendations are available yet."
                                if language == "English"
                                else "ಇನ್ನೂ ಯಾವುದೇ ಬೆಳೆ ಶಿಫಾರಸುಗಳು ಲಭ್ಯವಿಲ್ಲ."
                            )

                        elif not any(
                            item["crop"].lower().replace("_", " ").strip()
                            == crop_name
                            for item in recommendations
                        ):
                            st.info(
                                "This crop is not in your current "
                                "recommendations."
                                if language == "English"
                                else "ಈ ಬೆಳೆ ಪ್ರಸ್ತುತ ಶಿಫಾರಸುಗಳಲ್ಲಿ ಇಲ್ಲ."
                            )

                        else:
                            answer_text = (
                                f"{info['name']} is included in your "
                                "current crop recommendations. "
                                f"Suitable season: {info['season']}. "
                                f"Soil requirement: {info['soil']}. "
                                f"Karnataka guidance: "
                                f"{info['karnataka_note']}"
                            )

                    elif question_type == "soil":

                        if language == "ಕನ್ನಡ":
                            answer_text = (
                                f"{info['name']} ಬೆಳೆಗೆ "
                                f"{info['soil']} ಸೂಕ್ತ."
                            )
                        else:
                            answer_text = (
                                f"{info['name']} requires "
                                f"{info['soil']}."
                            )

                    elif question_type == "water":
                        answer_text = (
                            f"{info['name']}: {info['water']}."
                        )

                    elif question_type == "season":

                        if language == "ಕನ್ನಡ":
                            answer_text = (
                                f"{info['name']} ಬೆಳೆಯುವ ಸೂಕ್ತ ಹಂಗಾಮು: "
                                f"{info['season']}."
                            )
                        else:
                            answer_text = (
                                f"{info['name']} is grown during "
                                f"{info['season']}."
                            )

                    else:

                        answer_text = (
                            f"Guidance for {info['name']}: "
                            + " ".join(info["guidance"])
                        )

                else:
                    answer_text = (
                        "Crop information is currently unavailable."
                    )

            # Questions asking for a list of recommended crops
            elif any(word in question for word in [
                "recommend", "recommendation", "suggest", "suitable", "what crops", "which crops",
                "ಶಿಫಾರಸು", "ಶಿಫಾರಸುಗಳು"
            ]):

                saved_context = st.session_state.get(
                    "voice_recommendation_context"
                )

                current_context = (district, soil, season)

                # Automatically prepare rule-based suggestions when
                # the farmer has no soil test report.
                if has_soil_report is False and (
                    saved_context != current_context or not recommendations
                ):
                    recommendations = recommend_crops_without_soil_test(
                        soil=soil,
                        season=season,
                        district=district
                    )
                    recommendation_type = "rules"
                    st.session_state["voice_recommendations"] = recommendations
                    st.session_state["voice_recommendation_type"] = "rules"
                    st.session_state["voice_recommendation_context"] = current_context
                    saved_context = current_context

                if saved_context != current_context:
                    st.warning(
                        "Please generate the crop recommendation below "
                        "first, or regenerate it after changing your "
                        "district, soil or season."
                        if language == "English"
                        else "ಮೊದಲು ಬೆಳೆ ಶಿಫಾರಸನ್ನು ರಚಿಸಿ ಅಥವಾ "
                        "ಜಿಲ್ಲೆ, ಮಣ್ಣು ಅಥವಾ ಹಂಗಾಮು ಬದಲಿಸಿದ ನಂತರ "
                        "ಮತ್ತೆ ಶಿಫಾರಸನ್ನು ರಚಿಸಿ."
                    )

                elif not recommendations:
                    st.warning(
                        "No crop recommendations are available yet."
                        if language == "English"
                        else "ಇನ್ನೂ ಯಾವುದೇ ಬೆಳೆ ಶಿಫಾರಸುಗಳು ಲಭ್ಯವಿಲ್ಲ."
                    )

                else:
                    show_recommendations = True

                    if recommendation_type == "ml":

                        if language == "English":
                            answer_text = (
                                f"Based on your soil report and the selected "
                                f"farm details, the recommended crops for "
                                f"{district} are: "
                            )

                            for item in recommendations:
                                answer_text += (
                                    f"{item['crop'].title()}, "
                                    f"ML model score "
                                    f"{item['confidence']} percent. "
                                )

                            answer_text += (
                                "These model scores are not guarantees of "
                                "crop yield or success. Please consider local "
                                "rainfall, water availability and "
                                "agricultural advice."
                            )

                        else:
                            answer_text = (
                                f"ನಿಮ್ಮ {district} ಜಿಲ್ಲೆಯ {soil} ಮಣ್ಣಿನಲ್ಲಿ "
                                f"{season} ಹಂಗಾಮಿಗೆ ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆಗಳು: "
                            )

                            for item in recommendations:
                                answer_text += (
                                    f"{item['crop']}, "
                                    f"ML ಮಾದರಿಯ ಅಂಕ "
                                    f"{item['confidence']} ಶೇಕಡಾ. "
                                )

                            answer_text += (
                                "ಈ ಮಾದರಿಯ ಅಂಕಗಳು ಇಳುವರಿಯ ಖಾತರಿಯಲ್ಲ. "
                                "ಮಳೆ, ನೀರಿನ ಲಭ್ಯತೆ ಮತ್ತು ಕೃಷಿ ತಜ್ಞರ "
                                "ಸಲಹೆಯನ್ನು ಪರಿಗಣಿಸಿ."
                            )

                    else:

                        if language == "English":
                            answer_text = (
                                f"For {soil} in {district} during {season}, "
                                "these crops match the current "
                                "district-aware rules: "
                            )

                            for item in recommendations:
                                answer_text += (
                                    f"{item['crop'].title()}, "
                                    f"rule match score "
                                    f"{item['score']} out of 4. "
                                )

                            answer_text += (
                                "These are preliminary rule-based suggestions, "
                                "not a guarantee of crop yield. Please consider "
                                "local rainfall, water availability and "
                                "agricultural advice."
                            )

                        else:
                            answer_text = (
                                f"ನಿಮ್ಮ {district} ಜಿಲ್ಲೆಯ {soil} ಮಣ್ಣಿನಲ್ಲಿ "
                                f"{season} ಹಂಗಾಮಿಗೆ ಸೂಕ್ತವಾದ ಬೆಳೆಗಳು: "
                            )

                            for item in recommendations:
                                answer_text += (
                                    f"{item['crop']}, "
                                    f"ನಿಯಮ ಹೊಂದಾಣಿಕೆ ಅಂಕ "
                                    f"{item['score']} ರಲ್ಲಿ 4. "
                                )

                            answer_text += (
                                "ಇವು ಪ್ರಾಥಮಿಕ ಸಲಹೆಗಳು ಮಾತ್ರ. "
                                "ಇಳುವರಿ ಖಚಿತವಲ್ಲ. ಮಳೆ, ನೀರಿನ ಲಭ್ಯತೆ "
                                "ಮತ್ತು ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆಯನ್ನು ಪರಿಗಣಿಸಿ."
                            )


            else:
                st.info(
                    "Please ask about crop or weather information."
                    if language == "English"
                    else "ಬೆಳೆ ಅಥವಾ ಹವಾಮಾನ ಮಾಹಿತಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನಿಸಿ."
                )

        # Display crop suggestions only for recommendation questions
        if show_recommendations:
            st.success(
                "🌱 Crop Suggestions"
                if language == "English"
                else "🌱 ಬೆಳೆ ಸಲಹೆಗಳು"
            )

            for item in recommendations:
                if recommendation_type == "ml":
                    st.write(
                        f"🌱 **{item['crop'].title()}** — "
                        f"ML score: {item['confidence']}%"
                    )
                else:
                    st.write(
                        f"🌱 **{item['crop'].title()}** — "
                        f"{item['score']}/4"
                    )

        # Display answers for both weather and crop questions
        if answer_text:
            st.info(answer_text)

            try:
                answer_audio = generate_speech_audio(
                    answer_text,
                    language
                )
                st.audio(answer_audio, format="audio/mp3")

            except Exception:
                st.warning(
                    "Speech output is temporarily unavailable. "
                    "Please read the answer above."
                )

        else:
            st.info(
                "Currently, I can answer questions about crop suitability "
                "and district weather."
                if language == "English"
                else "ಪ್ರಸ್ತುತ ಬೆಳೆ ಸೂಕ್ತತೆ ಮತ್ತು ಜಿಲ್ಲೆಯ "
                "ಹವಾಮಾನದ ಬಗ್ಗೆ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಬಹುದು."
            )
