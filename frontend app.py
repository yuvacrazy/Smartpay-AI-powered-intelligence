import streamlit as st
import requests
import plotly.graph_objects as go
import time

# ----------------------------
# CONFIG
# ----------------------------
BACKEND_URL = "https://ai-powered-salary-prediction-system.onrender.com/predict"
API_KEY = None  # optional; if your backend has API key authentication

HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["x-api-key"] = API_KEY

st.set_page_config(
    page_title="SmartPay | AI Salary Intelligence",
    page_icon="💼",
    layout="wide"
)

# ----------------------------
# STYLING (Corporate Glassy Look)
# ----------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at 20% 20%, #0e1117, #1a1d24);
    color: #fff;
    font-family: 'Inter', sans-serif;
}
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-title {
    text-align: center;
    color: #c9d1d9;
    font-size: 18px;
    margin-bottom: 40px;
}
.glass-card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 25px;
    margin: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.stButton>button {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    border: none;
    padding: 10px 25px;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #00c6ff, #0072ff);
}
footer {
    text-align:center;
    color:#8b949e;
    font-size: 14px;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 class='main-title'>SmartPay – AI Salary Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Predict · Analyze · Explain · Export Salary Reports</p>", unsafe_allow_html=True)

# ----------------------------
# INPUT SECTION
# ----------------------------
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

# ----------------------------
# PREDICTION
# ----------------------------
if st.button("🔍 Predict Salary", use_container_width=True):
    with st.spinner("Generating Prediction..."):
        time.sleep(1.2)

        data = {
            "age": age,
            "education": education,
            "job_title": job_title,
            "hours_per_week": hours_per_week,
            "gender": gender,
            "marital_status": marital_status
        }

        try:
            response = requests.post(BACKEND_URL, json=data, headers=HEADERS)
            if response.status_code == 200:
                result = response.json()
                salary = float(result.get("predicted_salary_usd", 0))

                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=salary,
                    title={'text': "Predicted Annual Salary (USD)", 'font': {'size': 20, 'color': "#00c6ff"}},
                    gauge={
                        'axis': {'range': [0, 250000]},
                        'bar': {'color': "#00c6ff"},
                        'steps': [
                            {'range': [0, 50000], 'color': '#1e1e1e'},
                            {'range': [50000, 120000], 'color': '#24292f'},
                            {'range': [120000, 250000], 'color': '#30363d'}
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f"<h3 style='text-align:center; color:#00c6ff;'>💰 Predicted Salary: ${salary:,.2f}</h3>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.error(f"⚠️ API Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"❌ Unable to connect to backend: {e}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
<footer>
<hr style="opacity:0.1;">
Developed by | Final Year CSE (IoT), Paavai Engineering College <br>
<span style="color:#0072ff;">Powered by FastAPI · LightGBM · Streamlit</span>
</footer>
""", unsafe_allow_html=True)
