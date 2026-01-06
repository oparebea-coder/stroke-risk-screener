import streamlit as st
from pathlib import Path

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
# IMAGE PATHS (ONLY 2 IMAGES)
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"

HERO_IMAGE = IMAGE_DIR / "strokeprediction.png"
IMAGE_2 = IMAGE_DIR / "image2.png"

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
Stroke risk screening based on established clinical factors
</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HOME
# --------------------------------------------------
if page == "Home":

    if HERO_IMAGE.exists():
        st.image(str(HERO_IMAGE), use_column_width=True)

    if IMAGE_2.exists():
        st.image(str(IMAGE_2), use_column_width=True)

    st.markdown("""
    <div class="section">
    <h2>About Stroke</h2>
    <p>
    Stroke occurs when blood supply to the brain is interrupted.
    This tool provides an educational stroke risk screening based on
    clinically recognised risk factors.
    </p>

    <h3>FAST Warning Signs</h3>
    <ul>
        <li><strong>F</strong> – Face drooping</li>
        <li><strong>A</strong> – Arm weakness</li>
        <li><strong>S</strong> – Speech difficulty</li>
        <li><strong>T</strong> – Time to seek emergency care</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# RISK ASSESSMENT (FEATURES MATCH NOTEBOOK)
# --------------------------------------------------
elif page == "Risk Assessment":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Stroke Risk Input")

    age = st.slider("Age (years)", 18, 100, 45)
    avg_glucose_level = st.slider("Average Glucose Level (mg/dL)", 50.0, 300.0, 120.0)
    bmi = st.slider("Body Mass Index (BMI)", 10.0, 50.0, 25.0)

    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"])

    if st.button("Estimate Risk"):

        risk_score = 0

        if age >= 55:
            risk_score += 20
        elif age >= 45:
            risk_score += 10

        if avg_glucose_level >= 140:
            risk_score += 20
        elif avg_glucose_level >= 110:
            risk_score += 10

        if bmi >= 30:
            risk_score += 10

        if hypertension == "Yes":
            risk_score += 20

        if heart_disease == "Yes":
            risk_score += 20

        if smoking_status == "Current":
            risk_score += 15
        elif smoking_status == "Former":
            risk_score += 5

        risk_score = min(risk_score, 100)
        st.session_state["risk"] = risk_score

        if risk_score < 30:
            st.success(f"Estimated Stroke Risk: {risk_score}% (Low Risk)")
        elif risk_score < 60:
            st.warning(f"Estimated Stroke Risk: {risk_score}% (Moderate Risk)")
        else:
            st.error(f"Estimated Stroke Risk: {risk_score}% (High Risk)")

        st.info("➡️ View detailed interpretation in the Results tab.")

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
            st.success("Low risk. Maintain healthy lifestyle habits.")
        elif risk < 60:
            st.warning("Moderate risk. Lifestyle changes are recommended.")
        else:
            st.error("High risk. Please seek medical advice.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------
elif page == "Recommendations":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Health Recommendations")

    st.markdown("""
    <ul>
        <li>Control blood pressure and glucose levels</li>
        <li>Maintain a healthy body weight</li>
        <li>Engage in regular physical activity</li>
        <li>Avoid smoking</li>
        <li>Attend routine medical check-ups</li>
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
