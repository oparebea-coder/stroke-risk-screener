import streamlit as st

# --------------------------------------------------
# PAGE CONFIG (NOT WIDE)
# --------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Assessment Tool",
    layout="centered"
)

# --------------------------------------------------
# STYLING (Original Theme)
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
    st.markdown("""
    <div class="section">
    <h2>About Stroke</h2>
    <p>
    This tool provides an educational stroke risk screening based on
    established clinical risk factors. It is not a diagnostic device.
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
# RISK ASSESSMENT
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

        st.success("Assessment completed. View results.")

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
        <li>Adopt a balanced diet</li>
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
