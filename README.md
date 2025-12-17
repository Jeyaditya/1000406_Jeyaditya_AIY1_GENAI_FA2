# 1000406_Jeyaditya_AIY1_GENAI_FA2

## Agribot — Friendly Farm Assistant

Agribot is a Streamlit-based Smart Farming Assistant designed to help farmers make better day-to-day agricultural decisions. It combines simple data inputs with AI-powered insights (Google Gemini 1.5) to provide guidance on crops, pests, soil care, watering, and basic market trends.

This project was built as part of a Formative Assessment with a focus on practical, sustainable, and farmer-friendly technology.

## Problem Statement

  Farmers often face challenges such as:

  Unpredictable rainfall and climate changes

  Pest and disease outbreaks

  Declining soil fertility

  Lack of timely and localized farming advice

  Unclear market trends for selling crops

  Agribot addresses these problems by offering interactive, region-aware, and easy-to-use agricultural support through a single web app.

## Objectives

  Provide crop planning suggestions based on season and rainfall

  Assist in identifying common leaf and pest issues

  Offer soil and watering guidance for sustainable farming

  Give a simple visual overview of crop market trends

  Maintain farmer notes and snapshots for future reference

## Key Features

* Farmer Profile

  Store name, location, soil type, and soil pH

  Acts as context for all recommendations

* Ask Agribot (AI Chat)

  Farmers can ask natural-language questions

  Uses Google Gemini 1.5 when API key is provided

  Falls back to friendly demo responses if AI is disabled

* Plant Planner

  Suggests crops based on:

  Season (Kharif / Rabi / Summer)

  Expected rainfall

  Soil conditions

* Leaf Doctor

  Upload a leaf image

  Get likely causes and treatment suggestions

  Designed for early pest and disease detection

* Soil Care

  Provides soil improvement tips

  Considers soil type and pH value

* Watering Advisor

  Uses rain probability and soil moisture

  Gives simple irrigation decisions

* Market View

  Displays simulated crop price trends

  Helps farmers understand basic price movement patterns

* Save & Notes

  Save farming snapshots as CSV

  Maintain historical records of decisions and observations

## Tech Stack

Python

Streamlit (Web UI)

Google Gemini 1.5 API (Generative AI)

Pandas & NumPy (Data handling)

Pillow (PIL) (Image handling)

Matplotlib / Streamlit Charts (Visualization)

## Installation & Setup
1. Clone the Repository
git clone https://github.com/your-username/agribot.git
cd agribot
2. Install Dependencies
pip install streamlit pandas numpy pillow google-generativeai
3. Add Gemini API Key

Inside app.py, replace:

GEMINI_API_KEY = "PUT_YOUR_GEMINI_API_KEY_HERE"

With your actual API key:

GEMINI_API_KEY = "YOUR_API_KEY"

If no valid key is provided, Agribot runs safely in demo mode.

## 4. Run the App
streamlit run app.py
Project Structure
|-- app.py
|-- agribot_notes.csv
|-- README.md

## Sustainability Focus

Agribot promotes:

Organic pest control suggestions

Water conservation

Soil health improvement

Climate-aware decision making

This project aligns with:

UN SDG 2: Zero Hunger

UN SDG 13: Climate Action

## Target Users

Small and medium-scale farmers

Agricultural students and educators

Smart farming and AgriTech enthusiasts

## Future Enhancements

Real-time weather API integration

Live mandi market price feeds

Multilingual support (Tamil, Hindi, etc.)

Mobile-first UI optimization

Advanced image-based disease detection

## License

This project is developed for educational purposes.

## Author

Jeyadita
Smart Farming Assistant — Formative Assessment Project
