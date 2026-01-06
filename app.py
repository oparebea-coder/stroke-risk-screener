import streamlit as st
import numpy as np
import pandas as pd
import joblib
import base64
from pathlib import Path
from gtts import gTTS

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Assessment Tool",
    layout="wide"
)

# -------------------------------------------------
# LOAD MODEL & SCALER (CACHED)
# -------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    scaler = joblib.load("stroke_scaler.joblib")
    return model, scaler

model, scaler = load_artifacts()

# -------------------------------------------------
# IMAGE LOADER
# -------------------------------------------------
BASE_DIR = Path(__file__).parent

def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

hero1 = load_image_base64(BASE_DIR / "images/strokeprediction.png")
hero2 = load_image_base64(BASE_DIR / "images/image2.png")
hero3 = load_image_base64(BASE_DIR / "images/image3.png")

# -------------------------------------------------
# STYLING (UNCHANGED LOOK)
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #0e0e0e; color: white; }
h1,h2,h3,h4 { color: #ff69b4; }
.card {
    background: #111;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
button {
    background-color: #ff69b4 !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="card" style="text-align:center;">
<h1>🧠 Stroke Risk Assessment Tool</h1>
<p>Empowering you to take control of your brain health</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO SLIDESHOW
# -------------------------------------------------
st.markdown(f"""
<div style="display:flex; gap:10px;">
<img src="data:image/png;base64,{hero1}" width="33%">
<img src="data:image/png;base64,{hero2}" width="33%">
<img src="data:image/png;base64,{hero3}" width="33%">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# RISK ASSESSMENT FORM
# -------------------------------------------------
st.markdown("## 📝 Stroke Risk Assessment")

with st.form("risk_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 120)
        hypertension = st.selectbox("Hypertension", [0, 1])
        heart_disease = st.selectbox("Heart Disease", [0, 1])
        avg_glucose = st.number_input("Average Glucose Level", 50.0, 300.0)

    with col2:
        bmi = st.number_input("BMI", 10.0, 60.0)
        smoking = st.selectbox("Smoking Status", [0, 1])

    submit = st.form_submit_button("Predict Stroke Risk")

# -------------------------------------------------
# PREDICTION + RESULT (IMMEDIATE)
# -------------------------------------------------
if submit:
    # EXACT FEATURE ORDER USED DURING TRAINING
    X = np.array([[age, avg_glucose, bmi, hypertension, heart_disease, smoking]])

    # SCALE FIRST
    X_scaled = scaler.transform(X)

    # PREDICT
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]

    st.markdown("## 📊 Your Result")

    if prediction == 1:
        st.error(f"⚠️ High Stroke Risk\n\nProbability: {probability:.2%}")
    else:
        st.success(f"✅ Low Stroke Risk\n\nProbability: {probability:.2%}")

# -------------------------------------------------
# AUDIO NARRATION
# -------------------------------------------------
def narrate(text):
    tts = gTTS(text)
    tts.save("audio.mp3")
    audio = open("audio.mp3", "rb").read()
    st.audio(audio)

st.markdown("## 🔊 Listen")
narrate("This application predicts stroke risk using a trained machine learning model.")

# -------------------------------------------------
# FOOTER (FIXED)
# -------------------------------------------------
st.markdown("""
<div class="card" style="text-align:center;">
<p>© 2026 Stroke Risk Assessment Tool</p>
<p>Developed by <strong>Precious Oparebea Obinna</strong></p>
</div>
""", unsafe_allow_html=True)

