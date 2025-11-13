# Stroke Risk Screener  Web App 

This project is a **simple, trustworthy stroke-risk screening tool** built for a clinical setting.  
It uses a **machine learning model** trained on the healthcare stroke dataset, wrapped inside an  
easy-to-use **Streamlit frontend**.

**Disclaimer:** This tool is for educational and demonstration purposes only.  
**It is NOT a medical device and must not be used for clinical decisions.**


## 1. Project Overview

The goal of the project is to design a **small web application** that helps a clinic perform  
**preliminary stroke-risk screening** using a lightweight ML classifier.  
The front-end UI was built using **HTML/CSS/JS and Streamlit components**, while the backend consists of:

- A preprocessing + modeling **pipeline**
- A clean prediction interface (manual and CSV-based)
- Clear explanations and visualizations (optional)
- Reproducible training script and model-saving approach

The app takes in common stroke-related patient features such as age, hypertension status, BMI, glucose levels, etc.,  
and returns a **probability score** along with a **simple explanation**.



## Dataset

This project uses a common educational **stroke prediction dataset** containing features such as:

- Age  
- Sex  
- Systolic & Diastolic Blood Pressure  
- BMI  
- Smoking status  
- Fasting glucose  
- Total & HDL cholesterol  
- On blood pressure medication  
- Physical activity level  

Preprocessing steps (cleaning, encoding, scaling) are documented in `notebooks/training.ipynb`.


##  Web App Features

### **1. Data Input**
Users can:
- Type patient details directly  
- Or upload a CSV with required columns  

### **2. Model Training**
The app displays:
- Train/validation split  
- Accuracy, Precision, Recall, F1-score, ROC-AUC  
- Confusion matrix  
- Plain-language interpretation  

### **3. Prediction & Explanation**
For a patient’s input, the app shows:
- Predicted stroke risk  
- Top contributing features (feature importance)  

### **4. Safety Notice**
Displayed clearly:

> **For education only. Not a medical device. Do not use for clinical decisions.**


##  Installation

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/stroke-risk-screener.git
cd stroke-risk-screener


