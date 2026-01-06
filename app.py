import streamlit as st
from gtts import gTTS
import base64
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Stroke Risk Screener",
    layout="wide"
)

# ---------------- THEME (PINK / BLACK / OFF-WHITE) ----------------
st.markdown("""
<style>
body {
    background-color: #0b0b0b;
    color: #f5f5f5;
}
h1, h2, h3 {
    color: #ff4f9a;
}
.section {
    background-color: #111;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 25px;
}
.stButton > button {
    background-color: #ff4f9a;
    color: white;
    border-radius: 10px;
    padding: 10px 22px;
    border: none;
}
.stButton > button:hover {
    background-color: #ff2f87;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE NAV ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- HEADER ----------------
st.markdown("""
<div class="section" style="text-align:center;">
    <h1>🧠 Stroke Risk Assessment Tool</h1>
    <p>Empowering you to take control of your brain health</p>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO IMAGE ----------------
st.image("images/hero.png", use_container_width=True)

# ---------------- NAV BUTTONS ----------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.page = "home"
with col2:
    if st.button("Risk Assessment"):
        st.session_state.page = "assessment"
with col3:
    if st.button("Results"):
        st.session_state.page = "results"

st.divider()

# ================= HOME =================
if st.session_state.page == "home":
    st.markdown("""
    <div class="section">
        <h2>Learn About Stroke</h2>
        <p>
        A stroke occurs when blood flow to part of the brain is interrupted,
        preventing oxygen delivery. Early detection saves lives.
        </p>
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        st.image("images/brain.png", caption="Brain & Stroke Risk")
    with colB:
        st.image("images/warning.png", caption="Warning Signs")

# ================= ASSESSMENT =================
elif st.session_state.page == "assessment":
    st.markdown("<div class='section'><h2>Risk Assessment (Demo)</h2></div>", unsafe_allow_html=True)

    age = st.slider("Age", 18, 100, 40)
    bp = st.selectbox("High Blood Pressure?", ["No", "Yes"])
    smoke = st.selectbox("Do you smoke?", ["No", "Yes"])

    if st.button("Calculate Risk"):
        risk = "HIGH" if (age > 55 or bp == "Yes" or smoke == "Yes") else "LOW"
        st.session_state.result = risk
        st.session_state.page = "results"

# ================= RESULTS =================
elif st.session_state.page == "results":
    st.markdown("<div class='section'><h2>Your Result</h2></div>", unsafe_allow_html=True)

    result = st.session_state.get("result", "Not calculated")

    if result == "HIGH":
        st.error("⚠️ High Stroke Risk Detected")
    else:
        st.success("✅ Low Stroke Risk Detected")

# ---------------- AUDIO NARRATION ----------------
def speak(text):
    tts = gTTS(text)
    tts.save("audio.mp3")
    audio = open("audio.mp3", "rb").read()
    b64 = base64.b64encode(audio).decode()
    st.markdown(
        f"<audio controls><source src='data:audio/mp3;base64,{b64}'></audio>",
        unsafe_allow_html=True
    )

with st.expander("🔊 Listen to this page"):
    speak("This stroke risk screener helps demonstrate early risk awareness.")

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center>
<b>© 2026 Precious Oparebea Obinna</b><br>
Stroke Risk Screener – Educational Demonstration
</center>
""", unsafe_allow_html=True)
