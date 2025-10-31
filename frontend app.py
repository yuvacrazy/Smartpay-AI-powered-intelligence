import streamlit as st
import requests
import plotly.graph_objects as go
import time

# ------------------------------
# Config
# ------------------------------
API_URL = "https://smartpay-ai-powered-intelligence.onrender.com"  # your backend URL
API_KEY = None  # Leave None if backend auth is disabled

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["x-api-key"] = API_KEY

st.set_page_config(page_title="SmartPay | Salary Prediction", page_icon="💼", layout="wide")

st.markdown("<h1 style='text-align:center;color:#00c6ff;'>SmartPay – AI Salary Intelligence</h1>", unsafe_allow_html=True)
st.write("")

# ------------------------------
# Inputs
# ------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", 17, 100, 28)
    education = st.selectbox("Education", ["High School", "Bachelor’s", "Master’s", "PhD"])
with col2:
    job_title = st.text_input("Job Title", "Software Engineer")
    hours_per_week = st.slider("Hours per Week", 20, 100, 40)
with col3:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])

# ------------------------------
# Prediction Button
# ------------------------------
if st.button("🔍 Predict Salary"):
    BACKEND_URL = "https://ai-powered-salary-prediction-system.onrender.com/predict"

    with st.spinner("Generating Prediction..."):
        time.sleep(1.2)
        try:
            data = {
                "age": age,
                "education": education,
                "job_title": job_title,
                "hours_per_week": hours_per_week,
                "gender": gender,
                "marital_status": marital_status
            }
            response = requests.post(BACKEND_URL, json=data)
            if response.status_code == 200:
                result = response.json()
                salary = float(result.get("predicted_salary_usd", 0))
                st.success(f"💰 Predicted Salary: ${salary:,.2f}")
            else:
                st.error(f"⚠️ API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Unable to connect to backend: {e}")




