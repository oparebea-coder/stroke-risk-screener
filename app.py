import streamlit as st
import numpy as np
import joblib
from pathlib import Path

# --------------------------------------------------
# Page config (UNCHANGED)
# --------------------------------------------------
st.set_page_config(
    page_title="Stroke Risk Prediction",
    layout="wide"
)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model.pkl"
SCALER_PATH = BASE_DIR / "stroke_scaler.joblib"
IMAGE_DIR = BASE_DIR / "images"

# --------------------------------------------------
# Load model and scaler (FIXED)
# --------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

model, scaler = load_artifacts()

# --------------------------------------------------
# Feature engineering (MATCHES TRAINING)
# --------------------------------------------------
def engineer_features(age, glucose):
    age_sq = age ** 2
    glucose_sq = glucose ** 2
    age_glucose = age * glucose
    return age_sq, glucose_sq, age_glucose

# --------------------------------------------------
# ====== YOUR EXISTING STYLING (UNCHANGED) ======
# --------------------------------------------------
st.markdown("""
<style>
body { background-color: #0e0e0e; color: #f5f5f5; }
h1, h2, h3 { color: #ff5c8a; }
.stButton>button {
    background-color:#ff5c8a;
    color:white;
    border-radius:8px;
    font-size:16px;
}
.stButton>button:hover { background-color:#e14c77; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header (UNCHANGED)
# --------------------------------------------------
st.markdown("""
<div style="background-color:#1c1c1c;padding:25px;border-radius:12px;">
<h1>🧠 Stroke Risk Assessment Tool</h1>
<p>Empowering you to take control of your brain health</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# Images (UNCHANGED)
# --------------------------------------------------
c1, c2, c3 = st.columns(3)
with c1:
    st.image(IMAGE_DIR / "strokeprediction.png", use_container_width=True)
with c2:
    st.image(IMAGE_DIR / "image2.png", use_container_width=True)
with c3:
    st.image(IMAGE_DIR / "image3.png", use_container_width=True)

st.write("---")

# --------------------------------------------------
# Risk Assessment Form
# --------------------------------------------------
st.markdown("## 📝 Risk Assessment")

with st.form("risk_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 120, 45)
        hypertension = st.selectbox("Hypertension", [0, 1])
        heart_disease = st.selectbox("Heart Disease", [0, 1])
        avg_glucose = st.number_input("Average Glucose Level", value=100.0)

    with col2:
        bmi = st.number_input("BMI", value=25.0)
        smoking_status = st.selectbox(
            "Smoking Status",
            ["never smoked", "formerly smoked", "smokes"]
        )
        gender = st.selectbox("Gender", ["Male", "Female"])

    predict_btn = st.form_submit_button("Predict Stroke Risk")

# --------------------------------------------------
# Prediction + IMMEDIATE RESULTS (FIXED)
# --------------------------------------------------
if predict_btn:
    # Encode categoricals
    gender_encoded = 1 if gender == "Male" else 0
    smoking_map = {
        "never smoked": 0,
        "formerly smoked": 1,
        "smokes": 2
    }
    smoking_encoded = smoking_map[smoking_status]

    # Feature engineering
    age_sq, glucose_sq, age_glucose = engineer_features(age, avg_glucose)

    # Final feature vector (ORDER MATTERS)
    X = np.array([[
        gender_encoded,
        age,
        hypertension,
        heart_disease,
        avg_glucose,
        bmi,
        smoking_encoded,
        age_sq,
        glucose_sq,
        age_glucose
    ]])

    # Apply scaler (LECTURER FIX)
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]

    st.write("---")
    st.markdown("## 📊 Prediction Result")

    if prediction == 1:
        st.error(
            f"⚠️ **High Stroke Risk Detected**  \n"
            f"Estimated Probability: **{probability:.2%}**"
        )
    else:
        st.success(
            f"✅ **Low Stroke Risk Detected**  \n"
            f"Estimated Probability: **{probability:.2%}**"
        )

# --------------------------------------------------
# Footer (CORRECTED)
# --------------------------------------------------
st.markdown("""
<hr>
<p style="text-align:center;font-size:14px;">
© 2026 <strong>Precious Oparebea Obinna</strong><br>
Stroke Risk Assessment Tool
</p>
""", unsafe_allow_html=True)
