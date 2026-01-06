import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Assessment Tool",
    layout="wide"
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
# SIDEBAR NAVIGATION (WORKING)
# --------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Risk Assessment", "Results", "Recommendations"]
)

# --------------------------------------------------
# IMAGE PATHS (MATCH YOUR GITHUB EXACTLY)
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
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
# HOME PAGE
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
# RISK ASSESSMENT
# --------------------------------------------------
elif page == "Risk Assessment":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Stroke Risk Input")

    age = st.slider("Age", 18, 100, 45)
    glucose = st.slider("Average Glucose Level", 50, 300, 120)
    hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])

    if st.button("Estimate Risk"):
        risk = age * 0.03 + glucose * 0.02
        if hypertension == "Yes":
            risk += 10
        if heart_disease == "Yes":
            risk += 10
        if smoking == "Current":
            risk += 5

        st.session_state["risk"] = min(risk, 100)
        st.success("Assessment complete. View Results.")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
elif page == "Results":

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Your Results")

    risk = st.session_state.get("risk")

    if risk is None:
        st.warning("Please complete the Risk Assessment first.")
    else:
        st.metric("Estimated Stroke Risk (%)", f"{risk:.1f}%")
        if risk < 30:
            st.success("Low Risk")
        elif risk < 60:
            st.warning("Moderate Risk")
        else:
            st.error("High Risk – consult a healthcare professional")

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
        <li>Seek medical advice</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER (CORRECT NAME & YEAR)
# --------------------------------------------------
st.markdown("""
<hr>
<p style="text-align:center;color:#ff4f9a;">
© 2026 Stroke Risk Assessment Tool<br>
Developed by <strong>Precious Oparebea Obinna</strong>
</p>
""", unsafe_allow_html=True)
