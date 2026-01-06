import streamlit as st
from pathlib import Path
from gtts import gTTS
import time
import os

# --------------------------------------------------
# PAGE CONFIG (NOT WIDE)
# --------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Assessment Tool",
    layout="centered"
)

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
# IMAGE PATHS (MUST MATCH GITHUB)
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"

HERO_IMAGE = IMAGE_DIR / "strokeprediction.png"
IMAGE_2 = IMAGE_DIR / "image2.png"
IMAGE_3 = IMAGE_DIR / "image3.png"

# --------------------------------------------------
# VOICE FUNCTION (SAFE)
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
# NAVIGATION
# --------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Risk Assessment", "Results", "Recommendations"]
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div style="background:#ff4f9a;padding:25px;border-radius:18px;text-align:center;">
<h1 style="color:white;">🧠 Stroke Risk Assessment Tool</h1>
<p style="color:white;font-size:18px;">
Early screening tool for stroke risk awareness
</p>
</div>
""", unsafe_allow_html=True)

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
    <h2>About Stroke</h2>
    <p>
    A stroke occurs when blood flow to part of the brain is interrupted,
    preventing oxygen and nutrients from reaching brain tissue.
    Early detection can save lives.
    </p>

    <h3>FAST Warning Signs</h3>
    <ul>
        <li><strong>F</strong> – Face drooping</li>
        <li><strong>A</strong> – Arm weakness</li>
        <li><strong>S</strong> – Speech difficulty</li>
        <li><strong>T</strong> – Time to call emergency services</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# RISK ASSESSMENT (SAFE RULE-BASED)
# --------------------------------------------------
elif page == "Risk Assessment":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Stroke Risk Input")

    age = st.slider("Age", 18, 100, 45)
    glucose = st.slider("Average Glucose Level (mg/dL)", 50, 300, 120)
    bmi = st.slider("Body Mass Index (BMI)", 10.0, 50.0, 25.0)

    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])

    if st.button("Estimate Risk"):
        risk_score = 0

        if age > 55:
            risk_score += 15
        if glucose > 140:
            risk_score += 20
        if bmi > 30:
            risk_score += 10
        if hypertension == "Yes":
            risk_score += 20
        if heart_disease == "Yes":
            risk_score += 20
        if smoking == "Current":
            risk_score += 15

        risk_score = min(risk_score, 100)
        st.session_state["risk"] = risk_score

        message = f"Your estimated stroke risk is {risk_score} percent."

        if risk_score < 30:
            message += " This indicates a low risk."
            st.success(message)
        elif risk_score < 60:
            message += " This indicates a moderate risk."
            st.warning(message)
        else:
            message += " This indicates a high risk. Please seek medical advice."
            st.error(message)

        speak(message)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
elif page == "Results":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Results")

    risk = st.session_state.get("risk")

    if risk is None:
        st.warning("Please complete the risk assessment first.")
    else:
        st.metric("Estimated Stroke Risk (%)", f"{risk}%")

        if risk < 30:
            st.success("Low Risk")
        elif risk < 60:
            st.warning("Moderate Risk")
        else:
            st.error("High Risk – seek medical advice")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------
elif page == "Recommendations":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Health Recommendations")

    st.markdown("""
    <ul>
        <li>Maintain healthy blood pressure and glucose levels</li>
        <li>Exercise regularly</li>
        <li>Eat a balanced diet</li>
        <li>Avoid smoking</li>
        <li>Seek routine medical check-ups</li>
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
