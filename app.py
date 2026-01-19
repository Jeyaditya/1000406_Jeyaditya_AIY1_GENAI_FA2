import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
import matplotlib.pyplot as plt
import google.generativeai as genai

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Agribot",
    page_icon="🌱",
    layout="wide"
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


def ask_gemini(prompt):
    if GEMINI_API_KEY.startswith("PASTE"):
        return "⚠️ Gemini API Key not configured. Please add your API key."
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini Error: {e}"

# ================= STYLING =================
st.markdown("""
<style>
body {
    background-color: #0b3d2e;
}
h1, h2, h3 {
    color: #b7f7d4;
}
p, label {
    color: #e8fff4;
}

/* Tabs styling */
.stTabs [role="tab"] {
    background-color: #0f5132;
    color: #c7f7dd;
    border-radius: 8px;
    padding: 10px 20px;
    margin-right: 6px;
    font-weight: 600;
}
.stTabs [role="tab"][aria-selected="true"] {
    background-color: #1e7f54;
    color: white;
}
.stTabs [role="tablist"] {
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("<h1 style='text-align:center;'>🌱 AGRIBOT</h1>", unsafe_allow_html=True)

# ================= TOP NAVIGATION =================
tabs = st.tabs([
    "Your Profile",
    "Ask Agribot",
    "Plant Planner",
    "Leaf Doctor",
    "Soil Care",
    "Watering",
    "Market View"
])

# ================= 1. YOUR PROFILE =================
with tabs[0]:
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Your name")
    place = col2.text_input("Place")
    soil_type = col3.selectbox(
        "Soil Type",
        ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Clayey", "Loamy"]
    )
    soil_ph = st.slider("Soil pH", 4.0, 10.0, 7.0)
    farm_note = st.text_area("Area to note down your thoughts:")

# ================= 2. ASK AGRIBOT =================
with tabs[1]:
    question = st.text_area("Ask your question related to farming:")
    if st.button("Ask Agribot"):
        with st.spinner("Agribot is thinking..."):
            answer = ask_gemini(question)
        st.success(answer)

# ================= 3. PLANT PLANNER =================
with tabs[2]:
    rainfall = st.slider("Expected Rainfall (mm)", 0, 500, 100)
    season = st.selectbox("Season", ["Kharif", "Rabi", "Summer"])
    if st.button("Get Plant Suggestions"):
        with st.spinner("Planning crops..."):
            prompt = (
                f"Suggest suitable crops for {soil_type} soil, "
                f"pH {soil_ph}, rainfall {rainfall}mm in {season} season."
            )
            response = ask_gemini(prompt)
        st.success(response)
# ================= 4. LEAF DOCTOR =================
with tabs[3]:
    uploaded = st.file_uploader("Upload the damaged / diseased leaf image", type=["jpg", "png"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Leaf", width=350)
        if st.button("Analyze Leaf"):
            st.warning(
                ask_gemini("Identify pest or disease in this leaf and suggest organic treatment")
            )

# ================= 5. SOIL CARE =================
with tabs[4]:
    soil_selected = st.selectbox(
        "Select Soil Type",
        ["Alluvial", "Black", "Red", "Laterite", "Sandy", "Clayey", "Loamy"]
    )
    if st.button("Get Soil Care Advice"):
        with st.spinner("Analyzing soil health..."):
            prompt = f"How to maintain healthy pH and fertility for {soil_selected} soil?"
            response = ask_gemini(prompt)
        st.success(response)

# ================= 6. WATERING =================
with tabs[5]:
    water_depth = st.slider("Water Depth Required (cm)", 1, 300, 50)
    rain_chance = st.slider("Chance of Precipitation (%)", 1, 100, 30)
    soil_moisture = st.slider("Soil Moisture (%)", 1, 100, 40)

    if st.button("Get Watering Advice"):
        with st.spinner("Calculating irrigation needs..."):
            prompt = (
                f"Water depth required {water_depth}cm, "
                f"chance of precipitation {rain_chance}%, "
                f"soil moisture {soil_moisture}%. "
                f"Provide precise irrigation advice."
            )
            response = ask_gemini(prompt)
        st.info(response)

# ================= 7. MARKET VIEW =================
with tabs[6]:
    crop = st.selectbox(
        "Select Crop",
        ["Rice", "Wheat", "Tomato", "Onion", "Maize", "Cotton"]
    )
    days = list(range(1, 31))
    prices = [random.randint(1200, 2600) for _ in days]

    fig, ax = plt.subplots()
    ax.plot(days, prices, color="green")
    ax.set_title(f"{crop} Market Prices (₹)")
    ax.set_xlabel("Days")
    ax.set_ylabel("Price per Quintal (₹)")
    st.pyplot(fig)

    st.caption("⚠️ Market prices are simulated for demonstration purpose only")

# ================= FOOTER =================
st.markdown(
    "<p style='text-align:center;color:#9ff3c9;'>Agribot • Smart Farming Dashboard 🌱</p>",
    unsafe_allow_html=True
)


