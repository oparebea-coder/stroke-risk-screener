import streamlit as st
import numpy as np
import joblib
from pathlib import Path
from gtts import gTTS
import time
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Assessment Tool",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL + SCALER (ONCE)
# --------------------------------------------------
BASE_DIR = Path(__file__).parent

def load_artifacts():
    model = joblib.load(BASE_DIR / "model.pkl")
    scaler = joblib.load(BASE_DIR / "stroke_scaler.pkl")
    return model, scaler

model, scaler = load_artifacts()

# --------------------------------------------------
# VOICE NARRATION (SAFE)
# --------------------------------------------------
def speak(text):
    try:
        filename = f"voice_{int(time.time())}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(filename)
        with open(filename, "rb") as audio:
            st.audio(audio.read(), format="audio/mp3")
        os.remove(filename)
    except Exception:
        st.info("🔊 Voice narration unavailable.")

# --------------------------------------------------
# GLOBAL STYLING (Pink / Black / Off-white)
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0b0b0b;
    color: #f7f5f2;
}
h1, h2, h3 {
    color: #ff4f9a;
}
.section {
    background-color: #f7f5f2;
    color: #111;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 25px;
}
button {
    background-color: #ff4f9a !important;
    color: white !important;
    border-radius: 10px !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Risk Assessment", "Results", "Recommendations"]
)

# --------------------------------------------------
# IMAGE PATHS (MATCH YOUR GITHUB)
# --------------------------------------------------
IMAGE_DIR = BASE_DIR / "images"
HERO_IMAGE = IMAGE_DIR / "strokeprediction.png"
IMAGE_2 = IMAGE_DIR / "image2.png"
IMAGE_3 = IMAGE_DIR / "image3.png"

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div style="background:#ff4f9a;padding:25px;border-radius:18px;text-align:center;">
<h1 style="color:white;">🧠 Stroke Risk Assessment Tool</h1>
<p style="color:white;font-size:18px;">
Empowering you to take control of your brain health
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# HOME
# --------------------------------------------------
if page == "Home":

    if HERO_IMAGE.exists():
        st.image(str(HERO_IMAGE), use_column_width=True)

    colA, colB = st.columns(2)
    with colA:
        if IMAGE_2.exists():
            st.image(str(IMAGE_2), use_column_width=True)
    with colB:
        if IMAGE_3.exists():
            st.image(str(IMAGE_3), use_column_width=True)

    st.markdown("""
    <div class="section">
    <h2>Learn About Stroke</h2>
    <p>
    A stroke occurs when blood flow to part of the brain is interrupted,
    preventing oxygen and nutrients from reaching brain tissue.
    Early detection can save lives.
    </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section">
        <h3>Types of Stroke</h3>
        <ul>
            <li>Ischemic – artery blockage</li>
            <li>Hemorrhagic – burst blood vessel</li>
            <li>TIA – mini-stroke</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
        <h3>Common Causes</h3>
        <ul>
            <li>High blood pressure</li>
            <li>Heart disease</li>
            <li>Diabetes</li>
            <li>Smoking</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section">
        <h3>Symptoms</h3>
        <ul>
            <li>Face drooping</li>
            <li>Arm weakness</li>
            <li>Speech difficulty</li>
            <li>Dizziness</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section">
        <h3>FAST Test</h3>
        <ul>
            <li>F – Face</li>
            <li>A – Arms</li>
            <li>S – Speech</li>
            <li>T – Time to call emergency</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# RISK ASSESSMENT (REAL MODEL + SCALER)
# --------------------------------------------------
elif page == "Risk Assessment":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Stroke Risk Input")

    age = st.slider("Age", 18, 100, 45)
    avg_glucose = st.slider("Average Glucose Level", 50.0, 300.0, 120.0)
    bmi = st.slider("BMI", 10.0, 50.0, 25.0)

    hypertension = st.selectbox("Hypertension (0 = No, 1 = Yes)", [0, 1])
    heart_disease = st.selectbox("Heart Disease (0 = No, 1 = Yes)", [0, 1])
    smoking = st.selectbox("Smoking Status (0 = No, 1 = Yes)", [0, 1])

    if st.button("Estimate Risk"):
        X = np.array([[age, avg_glucose, bmi, hypertension, heart_disease, smoking]])
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0][1]

        st.session_state["prediction"] = prediction
        st.session_state["probability"] = probability

        if prediction == 1:
            message = (
                f"You are at high risk of stroke. "
                f"The estimated probability is {probability:.0%}. "
                f"Please seek medical advice."
            )
            st.error(message)
        else:
            message = (
                f"You are at low risk of stroke. "
                f"The estimated probability is {probability:.0%}. "
                f"Continue maintaining a healthy lifestyle."
            )
            st.success(message)

        speak(message)
        st.info("➡️ View detailed results in the Results tab.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
elif page == "Results":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Your Results")

    if "prediction" not in st.session_state:
        st.warning("Please complete the Risk Assessment first.")
    else:
        prob = st.session_state["probability"]
        st.metric("Stroke Risk Probability", f"{prob:.2%}")

        if st.session_state["prediction"] == 1:
            st.error("⚠️ High Stroke Risk – consult a healthcare professional")
        else:
            st.success("✅ Low Stroke Risk")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------
elif page == "Recommendations":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Health Recommendations")

    st.markdown("""
    <ul>
        <li>Control blood pressure and blood sugar</li>
        <li>Exercise regularly</li>
        <li>Eat a balanced diet</li>
        <li>Avoid smoking</li>
        <li>Seek professional medical advice</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<hr>
<p style="text-align:center;color:#ff4f9a;">
© 2026 Stroke Risk Assessment Tool<br>
Developed by <strong>Precious Oparebea Obinna</strong>
</p>
""", unsafe_allow_html=True)
