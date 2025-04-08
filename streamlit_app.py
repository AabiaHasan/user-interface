import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import io

# --- Fixed Simulated Values ---
RBF = 400  # mL/min
SO2_a = 98
SO2_v = 75
pO2_a = 90
pO2_v = 45
Hb = 12  # g/dL
Hct = 36  # %

# OC Calculation Function
def calc_OC(Hb, SO2, pO2):
    return (1.34 * Hb * SO2 / 100) + (0.003 * pO2)

# Oxygen Content Calculations
AOC = calc_OC(Hb, SO2_a, pO2_a)
RVOC = calc_OC(Hb, SO2_v, pO2_v)
VO2ren = RBF * (AOC - RVOC)
oxygen_content_avg = (AOC + RVOC) / 2

# --- Session State Initialization ---
if 'pressure_setting' not in st.session_state:
    st.session_state.pressure_setting = 100
if 'temperature_setting' not in st.session_state:
    st.session_state.temperature_setting = 37
if 'vo2ren_history' not in st.session_state:
    st.session_state.vo2ren_history = []
if 'oc_history' not in st.session_state:
    st.session_state.oc_history = []
if 'time_history' not in st.session_state:
    st.session_state.time_history = []

# --- Update Historical Values ---
current_time = datetime.now().strftime('%H:%M:%S')
st.session_state.vo2ren_history.append(VO2ren)
st.session_state.oc_history.append(oxygen_content_avg)
st.session_state.time_history.append(current_time)

# --- Limit to Last 20 Entries ---
max_points = 20
st.session_state.vo2ren_history = st.session_state.vo2ren_history[-max_points:]
st.session_state.oc_history = st.session_state.oc_history[-max_points:]
st.session_state.time_history = st.session_state.time_history[-max_points:]

# --- Page Config & Styling ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#212529;'>PreservaLife</h1>", unsafe_allow_html=True)

st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .device-screen {
        background-color: #ffffff;
        color: #212529;
        font-family: monospace;
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 12px;
        box-shadow: 0 0 8px rgba(0,0,0,0.05);
    }
    .circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #212529;
        margin: 20px auto;
        padding: 10px;
        text-align: center;
        font-size: 15px;
        line-height: 1.3;
        box-shadow: 0 0 6px rgba(0,0,0,0.1);
    }
    button[kind="secondary"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Layout Columns ---
left, center, right = st.columns([1, 2, 1])

# --- LEFT COLUMN: BLOOD PARAMETERS ---
with left:
    st.markdown(f"<div class='circle' style='background-color:#39CCCC;'>RBF<br>{RBF} mL/min</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='circle' style='background-color:#FF69B4;'>SO₂<br>{SO2_a}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='circle' style='background-color:#FF851B;'>PO₂<br>{pO2_a} mmHg</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='circle' style='background-color:#2ECC40;'>Hct<br>{Hct}%</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='circle' style='background-color:#B10DC9;'>Hb<br>{Hb} g/dL</div>", unsafe_allow_html=True)

# --- CENTER COLUMN: METRICS + CONTROLS + CHARTS ---
with center:
    st.markdown(f"<div class='device-screen'>VO₂ren: {VO2ren:.2f} mL/min</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='device-screen'>Oxygen Content: {oxygen_content_avg:.2f} mL O₂/dL</div>", unsafe_allow_html=True)

    # --- Temperature Controls ---
    st.markdown("#### <span style='color:#212529'>Temperature (°C)</span>", unsafe_allow_html=True)
    col_tm, col_tp = st.columns([1, 1])
    with col_tm:
        if st.button("➖", key="temp_minus"):
            st.session_state.temperature_setting = max(30, st.session_state.temperature_setting - 1)
    with col_tp:
        if st.button("➕", key="temp_plus"):
            st.session_state.temperature_setting = min(45, st.session_state.temperature_setting + 1)

    temperature = st.session_state.temperature_setting
    temp_color = "#66B2FF" if 35 <= temperature <= 38 else "#D4AF37" if temperature < 35 else "#FF6B6B"
    st.markdown(f"<div class='device-screen' style='background-color:{temp_color};'>Temperature: {temperature} °C</div>", unsafe_allow_html=True)

    # --- Pressure Controls ---
    st.markdown("#### <span style='color:#212529'>Pressure (mmHg)</span>", unsafe_allow_html=True)
    col_pm, col_pp = st.columns([1, 1])
    with col_pm:
        if st.button("➖", key="pressure_minus"):
            st.session_state.pressure_setting = max(50, st.session_state.pressure_setting - 1)
    with col_pp:
        if st.button("➕", key="pressure_plus"):
            st.session_state.pressure_setting = min(200, st.session_state.pressure_setting + 1)

    pressure = st.session_state.pressure_setting
    press_color = "#66B2FF" if 70 <= pressure <= 100 else "#D4AF37" if 60 <= pressure < 70 else "#FF6B6B"
    st.markdown(f"<div class='device-screen' style='background-color:{press_color};'>Pressure: {pressure} mmHg</div>", unsafe_allow_html=True)

    # --- Charts below pressure ---
    st.markdown("### <span style='color:#212529'>📈 VO₂ren & Oxygen Content Trends</span>", unsafe_allow_html=True)

    # VO₂ren Chart
    vo2ren_df = pd.DataFrame({
        'Time': st.session_state.time_history,
        'VO₂ren (mL/min)': st.session_state.vo2ren_history
    })
    vo2ren_chart = alt.Chart(vo2ren_df).mark_line(point=True).encode(
        x='Time',
        y=alt.Y('VO₂ren (mL/min)', title='VO₂ren (mL/min)'),
        tooltip=['Time', 'VO₂ren (mL/min)']
    ).properties(height=300)
    st.altair_chart(vo2ren_chart, use_container_width=True)

    # Oxygen Content Chart
    oc_df = pd.DataFrame({
        'Time': st.session_state.time_history,
        'Oxygen Content (mL O₂/dL)': st.session_state.oc_history
    })
    oc_chart = alt.Chart(oc_df).mark_line(point=True).encode(
        x='Time',
        y=alt.Y('Oxygen Content (mL O₂/dL)', title='Oxygen Content (mL O₂/dL)'),
        tooltip=['Time', 'Oxygen Content (mL O₂/dL)']
    ).properties(height=300)
    st.altair_chart(oc_chart, use_container_width=True)

# --- RIGHT COLUMN: SYSTEM STATUS ---
with right:
    st.markdown(f"<div class='device-screen'>AOC: {AOC:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='device-screen'>RVOC: {RVOC:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='device-screen'>Battery Life: 85%</div>", unsafe_allow_html=True)

    if st.button("⚠️ Emergency Stop"):
        st.error("⚠️ Emergency Stop Activated!")

# --- FOOTER AREA ---
st.divider()
col_exp, col_legend1, col_legend2, col_legend3 = st.columns([2, 1, 1, 1])
with col_exp:
    # Export Button
    export_df = pd.DataFrame({
        'Time': st.session_state.time_history,
        'VO₂ren (mL/min)': st.session_state.vo2ren_history,
        'Oxygen Content (mL O₂/dL)': st.session_state.oc_history
    })

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Oxygen Metrics')
    excel_buffer.seek(0)

    st.download_button(
        label="📤 Export to Excel",
        data=excel_buffer,
        file_name="oxygen_metrics.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Import Button with separate black label
    st.markdown("📥 <span style='color:black;'>Import Excel</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed")
    if uploaded_file:
        try:
            imported_df = pd.read_excel(uploaded_file)
            st.success("✅ Excel file loaded successfully!")
            st.dataframe(imported_df)
        except Exception as e:
            st.error(f"❌ Failed to load Excel file: {e}")

with col_legend1:
    st.markdown("<div class='device-screen' style='background-color:#FF6B6B;'>Red: Critical</div>", unsafe_allow_html=True)
with col_legend2:
    st.markdown("<div class='device-screen' style='background-color:#D4AF37;'>Yellow: Warning</div>", unsafe_allow_html=True)
with col_legend3:
    st.markdown("<div class='device-screen' style='background-color:#66B2FF;'>Blue: Normal</div>", unsafe_allow_html=True)
