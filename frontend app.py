import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

# ----------------------------
# CONFIG
# ----------------------------
BACKEND_URL = "https://smartpay-ai-powered-intelligence.onrender.com"  # backend root URL
API_KEY = None  # Optional: set if backend has authentication

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
# TABS
# ----------------------------
tab1, tab2, tab3 = st.tabs(["💰 Prediction", "📊 Analysis", "🧠 Model Insights"])

# ===============================================================
# TAB 1: PREDICTION
# ===============================================================
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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

    if st.button("🔍 Predict Salary", use_container_width=True):
        with st.spinner("Generating Prediction..."):
            time.sleep(1)
            data = {
                "age": age,
                "education": education,
                "job_title": job_title,
                "hours_per_week": hours_per_week,
                "gender": gender,
                "marital_status": marital_status
            }
            try:
                response = requests.post(f"{BACKEND_URL}/predict", json=data, headers=HEADERS)
                if response.status_code == 200:
                    result = response.json()
                    salary = float(result.get("predicted_salary_usd", 0))
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
                else:
                    st.error(f"⚠️ API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Unable to connect to backend: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================================================
# TAB 2: ANALYSIS
# ===============================================================
with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Dataset Insights")
    try:
        response = requests.get(f"{BACKEND_URL}/analyze", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()["summary"]
            col1, col2, col3 = st.columns(3)
            col1.metric("📂 Records", f"{data['record_count']:,}")
            col2.metric("💵 Avg Salary", f"${data['average_salary']:,.2f}")
            col3.metric("🏆 Max Salary", f"${data['max_salary']:,.2f}")

            # Visual
            fig = px.bar(
                x=["Min Salary", "Avg Salary", "Max Salary"],
                y=[data["min_salary"], data["average_salary"], data["max_salary"]],
                color=["Min", "Avg", "Max"],
                color_discrete_sequence=["#1f77b4", "#00c6ff", "#2ca02c"],
                title="Salary Distribution Overview"
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to load analysis data.")
    except Exception as e:
        st.error(f"❌ Unable to fetch analysis: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================================================
# TAB 3: MODEL INSIGHTS
# ===============================================================
with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🧠 Top 5 Features Influencing Salary Prediction")
    try:
        response = requests.get(f"{BACKEND_URL}/explain", headers=HEADERS)
        if response.status_code == 200:
            top_features = pd.DataFrame(response.json()["top_features"])
            st.dataframe(top_features, use_container_width=True)
            fig = px.bar(
                top_features,
                x="feature",
                y="importance",
                title="Feature Importance (Model Explainability)",
                color="importance",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to load explainability data.")
    except Exception as e:
        st.error(f"❌ Unable to fetch explainability: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================================================
# FOOTER
# ===============================================================
st.markdown("""
<footer>
<hr style="opacity:0.1;">
Developed by <b>Yuvaraja P</b> | Final Year CSE (IoT), Paavai Engineering College <br>
<span style="color:#0072ff;">Powered by FastAPI · LightGBM · Streamlit</span>
</footer>
""", unsafe_allow_html=True)

