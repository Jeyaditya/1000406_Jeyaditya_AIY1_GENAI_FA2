"""
Agribot — Friendly Farm Assistant

Place your API key here:
GEMINI_API_KEY = "PUT_YOUR_GEMINI_API_KEY_HERE"
"""
from __future__ import annotations
import os
import csv
import random
import datetime
import logging

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
GEMINI_API_KEY = "AIzaSyB3ogfmBaQ93g0pI7uNIqXOz_haAD0TupM"

USE_REAL_AI = bool(GEMINI_API_KEY and GEMINI_API_KEY != "AIzaSyB3ogfmBaQ93g0pI7uNIqXOz_haAD0TupM")
st.set_page_config(page_title="Agribot", page_icon="🌾", layout="wide")

st.markdown(
    """
    <style>
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important; }
    .top-banner { background: linear-gradient(90deg,#0b6aa6,#00a7e1); color: #fff; padding:22px; border-radius:12px; margin-bottom:18px;}
    .card { background: #ffffff; padding:14px; border-radius:10px; box-shadow: 0 6px 20px rgba(0,0,0,0.04); margin-bottom:12px; }
    .hint { color:#2b6f98; font-size:13px; }
    footer {visibility: hidden;}
    .cta > button { background: linear-gradient(90deg,#0b6aa6,#00a7e1); color:white; border-radius:8px; padding:8px 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)
logger = logging.getLogger("agribot")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
LOG_FILENAME = "agribot_notes.csv"

def save_record(row: dict):
    header = list(row.keys())
    exists = os.path.exists(LOG_FILENAME)
    try:
        with open(LOG_FILENAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            if not exists:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        logger.exception("Failed to save record: %s", e)

def load_records() -> pd.DataFrame:
    if os.path.exists(LOG_FILENAME):
        return pd.read_csv(LOG_FILENAME)
    return pd.DataFrame()
def friendly_reply(prompt: str) -> str:
    seed = (hash(prompt) + 42) % 10000
    rnd = random.Random(seed)
    samples = [
        "Try planting ragi or bajra — they need less water and are hardy.",
        "White bugs are likely whiteflies. Neem spray and sticky strips help.",
        "Water lightly in the morning and use mulch to keep the soil moist.",
        "For salty soil, add compost and gypsum; grow legumes to help the soil.",
        "Use garlic-chili spray and welcome ladybugs for natural pest control.",
        "Rotate crops and add green manure to keep the soil healthy.",
        "For tomato issues, remove wet leaves and avoid evening watering.",
    ]
    return rnd.choice(samples)

def ask_ai(prompt: str) -> str:
    if not USE_REAL_AI:
        return friendly_reply(prompt)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        return text if text else str(response)
    except Exception as e:
        logger.exception("AI call failed, using friendly reply.")
        return f"(Demo) {friendly_reply(prompt)}"
def make_sample_leaf(text="Sample leaf: white spots"):
    img = Image.new("RGB", (720, 480), color=(235, 255, 240))
    d = ImageDraw.Draw(img)
    d.text((30, 30), text, fill=(22, 65, 32))
    return img
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Your name here",
        "place": "Your place here",
        "soil": "Loamy",
        "ph": 0.0,
        "profile_note": "",
    }

if "helper_note" not in st.session_state:
    st.session_state.helper_note = ""

if "planner" not in st.session_state:
    st.session_state.planner = {
        "season": "Kharif",
        "rain": 80,
        "planner_note": "",
    }

if "leaf" not in st.session_state:
    st.session_state.leaf = {
        "uploaded": None,
        "leaf_note": "",
    }

if "watering" not in st.session_state:
    st.session_state.watering = {
        "rain_chance": 28,
        "moisture": 36,
        "watering_note": "",
    }

if "soil" not in st.session_state:
    st.session_state.soil = {
        "soil_note": "",
    }

if "market" not in st.session_state:
    st.session_state.market = {
        "crop": "Ragi",
        "market_note": "",
    }
st.markdown("<div class='top-banner'><h1 style='margin:0'>Agribot  🌾</h1>"
            "<div style='opacity:0.95;margin-top:6px'>Friendly help for planting, pests, watering, soil, and small market views.</div></div>",
            unsafe_allow_html=True)
tabs = st.tabs(["Your Profile", "Ask Agribot", "Plant Planner", "Leaf Doctor", "Soil Care", "Watering", "Market View", "Your Notes"])
with tabs[0]:
    st.subheader("Your Profile")
    col1, col2 = st.columns([2,1])
    with col1:
        st.text_input("Your name", key="name_input", value=st.session_state.profile["name"])
        st.text_input("Your village / town", key="place_input", value=st.session_state.profile["place"])
        st.selectbox("Soil type", ["Loamy", "Sandy", "Clay", "Alkaline (saline)"], key="soil_input", index=["Loamy","Sandy","Clay","Alkaline (saline)"].index(st.session_state.profile["soil"]))
        st.slider("Soil pH", 4.0, 10.0, key="ph_input", value=float(st.session_state.profile["ph"]), step=0.1)
        st.text_area("Tell us about your farm (short note)", key="profile_note_input", value=st.session_state.profile["profile_note"])
        if st.button("Save profile details"):
            st.session_state.profile.update({
                "name": st.session_state.name_input,
                "place": st.session_state.place_input,
                "soil": st.session_state.soil_input,
                "ph": st.session_state.ph_input,
                "profile_note": st.session_state.profile_note_input,
            })
            st.success("Profile updated")

    with col2:
        st.markdown("### Quick snapshot")
        st.write(f"Name: {st.session_state.profile['name']}")
        st.write(f"Place: {st.session_state.profile['place']}")
        st.write(f"Soil: {st.session_state.profile['soil']} (pH {st.session_state.profile['ph']:.1f})")
        if st.session_state.profile["profile_note"]:
            st.markdown("**Profile note:**")
            st.write(st.session_state.profile["profile_note"])
with tabs[1]:
    st.subheader("Ask Agribot")
    st.text_area("Helper note (optional):", key="helper_note_input", value=st.session_state.helper_note, help="A short note Agribot will keep in mind for this session.")
    if st.button("Save helper note"):
        st.session_state.helper_note = st.session_state.helper_note_input
        st.success("Saved helper note")
    question = st.text_input("Ask anything:", value="What problem are you facing?")
    if st.button("Ask now"):
        with st.spinner("Agribot is thinking..."):
            prompt = f"{st.session_state.helper_note_input}\nQuestion: {question}"
            answer = ask_ai(prompt)
            st.info(answer)
with tabs[2]:
    st.subheader("Plant Planner")
    col1, col2 = st.columns([2,1])
    with col1:
        season = st.selectbox("Season", ["Kharif", "Rabi", "Summer"], key="season_input", index=["Kharif","Rabi","Summer"].index(st.session_state.planner["season"]))
        rain = st.slider("Expected monthly rainfall (mm)", 0, 500, key="rain_input", value=int(st.session_state.planner["rain"]))
        st.text_area("Notes for planning (optional)", key="planner_note_input", value=st.session_state.planner["planner_note"], help="Seeds you have, area, or market preferences.")
        if st.button("Get plant suggestions"):
            with st.spinner("Finding friendly suggestions..."):
                prompt = f"Profile: {st.session_state.profile.get('soil','Loamy')} soil, pH {st.session_state.profile.get('ph',7.2)}. Season {season}, rain {rain}mm. Notes: {st.session_state.planner.get('planner_note','')}"
                reply = ask_ai(prompt)
                st.success(reply)
    with col2:
        st.markdown("Quick planner note:")
        if st.session_state.planner.get("planner_note"):
            st.write(st.session_state.planner["planner_note"])
        else:
            st.write("No planner notes yet.")

# --------- Leaf Doctor Tab ----------
with tabs[3]:
    st.subheader("Leaf Doctor")
    col1, col2 = st.columns([2,1])
    with col1:
        uploaded = st.file_uploader("Upload a clear photo of the leaf", type=["png","jpg","jpeg"], key="leaf_upload_input")
        if st.button("Show sample photo"):
            sample = make_sample_leaf("Sample leaf: white spots")
            st.image(sample, caption="Sample leaf")
        if uploaded:
            try:
                img = Image.open(uploaded).convert("RGB")
                st.image(img, caption="Your uploaded leaf")
            except Exception:
                st.error("Could not open the image. Try another one.")
        st.text_area("Notes about the leaf (optional)", key="leaf_note_input", value=st.session_state.leaf["leaf_note"], help="How long symptoms have been present, location on plant, etc.")
        if st.button("Check leaf"):
            with st.spinner("Agribot is checking the photo..."):
                prompt = f"Leaf details: {st.session_state.leaf.get('leaf_note','')}. If the leaf has white spots, what might be the cause and friendly treatment?"
                diagnosis = ask_ai(prompt)
                st.warning(diagnosis)
    with col2:
        st.markdown("Quick leaf notes")
        if st.session_state.leaf.get("leaf_note"):
            st.write(st.session_state.leaf["leaf_note"])
        else:
            st.write("No leaf notes yet.")

# --------- Soil Care Tab ----------
with tabs[4]:
    st.subheader("Soil Care")
    st.write(f"Current soil type: {st.session_state.profile.get('soil','Loamy')}  •  pH: {st.session_state.profile.get('ph',7.2):.1f}")
    st.text_area("Soil notes (optional)", key="soil_note_input", value=st.session_state.soil["soil_note"], help="Recent amendments, compost, or problems.")
    if st.button("Give simple soil tips"):
        with st.spinner("Agribot is thinking about soil..."):
            prompt = f"Soil type: {st.session_state.profile.get('soil','Loamy')}, pH: {st.session_state.profile.get('ph',7.2)}. Notes: {st.session_state.soil.get('soil_note','')}"
            advice = ask_ai(prompt)
            st.info(advice)

# --------- Watering Tab ----------
with tabs[5]:
    st.subheader("Watering")
    col1, col2 = st.columns([2,1])
    with col1:
        rain_chance = st.slider("Chance of rain tomorrow (%)", 0, 100, key="rain_chance_input", value=int(st.session_state.watering["rain_chance"]))
        moisture = st.slider("Soil moisture (%)", 0, 100, key="moisture_input", value=int(st.session_state.watering["moisture"]))
        st.text_area("Watering notes (optional)", key="watering_note_input", value=st.session_state.watering["watering_note"], help="Irrigation type, timing, or constraints.")
        if st.button("Get watering tip"):
            if rain_chance >= 62 and moisture > 40:
                st.success("Skip irrigation tomorrow — rain likely and soil moist.")
            elif moisture < 30:
                st.warning("Water lightly in the morning and use mulch to save moisture.")
            else:
                st.info("Check plants in the morning and water only if they look thirsty.")
    with col2:
        st.markdown("Quick watering note")
        if st.session_state.watering.get("watering_note"):
            st.write(st.session_state.watering["watering_note"])
        else:
            st.write("No watering notes yet.")

# --------- Market View Tab ----------
with tabs[6]:
    st.subheader("Market View")
    col1, col2 = st.columns([2,1])
    with col1:
        crop = st.selectbox("Pick a crop to view", ["Rice", "Wheat", "Tomato", "Ragi", "Maize", "Bajra"], index=["Rice","Wheat","Tomato","Ragi","Maize","Bajra"].index(st.session_state.market["crop"]))
        st.text_area("Market notes (optional)", key="market_note_input", value=st.session_state.market["market_note"], help="Nearest mandi or buyers.")
        if st.button("Show price view"):
            days = np.arange(0, 30)
            base = random.randint(700, 1300)
            noise = np.random.normal(scale=12, size=days.shape)
            trend = np.linspace(0, random.uniform(-15, 15), days.size)
            prices = np.round(base + trend + noise + (60 * np.sin(days / 7)), 2)
            df = pd.DataFrame({"day": days, "price": prices})
            st.line_chart(df.set_index("day"))
    with col2:
        st.markdown("Quick market note")
        if st.session_state.market.get("market_note"):
            st.write(st.session_state.market["market_note"])
        else:
            st.write("No market notes yet.")

# --------- Save & Notes Tab ----------
with tabs[7]:
    st.subheader("Save & Notes")
    st.markdown("You can save a snapshot of your profile and notes below.")
    final_note = st.text_area("A short note about your field.")
    if st.button("Save snapshot"):
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "name": st.session_state.get("name_input", st.session_state.profile["name"]),
            "place": st.session_state.get("place_input", st.session_state.profile["place"]),
            "soil": st.session_state.get("soil_input", st.session_state.profile["soil"]),
            "ph": st.session_state.get("ph_input", st.session_state.profile["ph"]),
            "profile_note": st.session_state.get("profile_note_input", st.session_state.profile["profile_note"]),
            "helper_note": st.session_state.get("helper_note_input", st.session_state.helper_note),
            "season": st.session_state.get("season_input", st.session_state.planner["season"]),
            "rain_expected": st.session_state.get("rain_input", st.session_state.planner["rain"]),
            "planner_note": st.session_state.get("planner_note_input", st.session_state.planner.get("planner_note","")),
            "leaf_note": st.session_state.get("leaf_note_input", st.session_state.leaf.get("leaf_note","")),
            "watering_note": st.session_state.get("watering_note_input", st.session_state.watering.get("watering_note","")),
            "rain_chance": st.session_state.get("rain_chance_input", st.session_state.watering["rain_chance"]),
            "moisture": st.session_state.get("moisture_input", st.session_state.watering["moisture"]),
            "market_crop": st.session_state.get("crop", st.session_state.market["crop"]),
            "market_note": st.session_state.get("market_note_input", st.session_state.market.get("market_note","")),
            "visit_note": final_note,
        }
        save_record(record)
        st.success("Saved snapshot")

    records_df = load_records()
    if not records_df.empty:
        st.markdown("Recent saved snapshots")
        st.dataframe(records_df.tail(10))
        csv_bytes = records_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download all snapshots", data=csv_bytes, file_name="agribot_snapshots.csv", mime="text/csv")
    else:
        st.info("No saved snapshots yet.")

# ---------------------------- Footer ---------------------------------------
st.markdown("<div style='text-align:center;padding:10px;margin-top:18px;color:#6b7b8a'>Agribot — Friendly Farm Assistant</div>", unsafe_allow_html=True)
