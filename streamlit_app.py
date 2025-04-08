import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import io

# Embedded layout labels from Layout.xlsx (flattened order)
layout_flat = [
    'Venous High Quality low end hemoglobin conc',
    'Venous High Quality high end hemoglobin conc',
    'Venous Medium Quality low end hemoglobin conc',
    'Venous Medium Quality high end hemoglobin conc',
    'Venous low Quality low end hemoglobin conc',
    'Venous Low Quality high end hemoglobin conc',
    'Arterial High quality low end oxygen sat',
    'Arterial High quality high end oxygen sat',
    'Arterial Medium quality low end oxygen sat',
    'Arterial Medium quality high end oxygen sat',
    'Arterial low quality low end oxygen sat',
    'Arterial Low quality high end oxygen sat',
    'Venous High Quality low end oxygen sat',
    'Venous High Quality high end oxygen sat',
    'Venous Medium Quality low end oxygen sat',
    'Venous Medium Quality high end oxygen sat',
    'Venous low Quality low end oxygen sat',
    'Venous Low Quality high end oxygen sat',
    'Arterial High quality  low end partial pressure',
    'Arterial High quality  high end partial pressure',
    'Arterial Medium quality  low end partial pressure',
    'Arterial Medium quality  high end partial pressure',
    'Arterial low quality  low end partial pressure',
    'Arterial Low quality  high end partial pressure',
    'Venous High Quality low end partial pressure',
    'Venous High Quality high end partial pressure',
    'Venous Medium Quality low end partial pressure',
    'Venous Medium Quality high end partial pressure',
    'Venous low Quality low end partial pressure',
    'Venous Low Quality high end partial pressure',
    'High quality low end flow rate',
    'High quality high end flow rate',
    'medium quality low end flow rate',
    'medium quality high end flow rate',
    'low quality low end flow rate',
    'low quality high end flow rate'
]

# --- Page Setup ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#212529;'>PreservaLife</h1>", unsafe_allow_html=True)

# Upload UI
st.sidebar.markdown("### Upload data.xlsx")
uploaded_file = st.sidebar.file_uploader("Upload data.xlsx", type=["xlsx"])

# Proceed only if file is uploaded
if uploaded_file:
    data_df = pd.read_excel(uploaded_file)
    data_flat = data_df.stack().reset_index(drop=True)

    # Mapping: label → variable
    label_to_var = {
        "Arterial High quality high end hemoglobin conc": "Hb_a",
        "Arterial High quality high end oxygen sat": "SO2_a",
        "Arterial High quality  high end partial pressure": "pO2_a",
        "Venous High Quality high end hemoglobin conc": "Hb_v",
        "Venous High Quality high end oxygen sat": "SO2_v",
        "Venous High Quality high end partial pressure": "pO2_v"
    }

    var_index_map = {}
    for label, var in label_to_var.items():
        for i, layout_label in enumerate(layout_flat):
            if layout_label.strip().lower() == label.strip().lower():
                var_index_map[var] = i
                break

    Hb_a = data_flat[var_index_map["Hb_a"]]
    SO2_a = data_flat[var_index_map["SO2_a"]]
    pO2_a = data_flat[var_index_map["pO2_a"]]
    Hb_v = data_flat[var_index_map["Hb_v"]]
    SO2_v = data_flat[var_index_map["SO2_v"]]
    pO2_v = data_flat[var_index_map["pO2_v"]]
    RBF = 800
    Hct = 36

    arterial_oxygen = (1.34 * Hb_a * SO2_a) + (0.003 * pO2_a)
    venous_oxygen = (1.34 * Hb_v * SO2_v) + (0.003 * pO2_v)
    oxygen_consumption = RBF * (arterial_oxygen - venous_oxygen)

    # Session state setup
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

    current_time = datetime.now().strftime('%H:%M:%S')
    st.session_state.vo2ren_history.append(oxygen_consumption)
    st.session_state.oc_history.append((arterial_oxygen + venous_oxygen) / 2)
    st.session_state.time_history.append(current_time)

    st.session_state.vo2ren_history = st.session_state.vo2ren_history[-20:]
    st.session_state.oc_history = st.session_state.oc_history[-20:]
    st.session_state.time_history = st.session_state.time_history[-20:]

    # Styling
    st.markdown("""
        <style>
        body { background-color: #f8f9fa; }
        .stApp { background-color: #f8f9fa; }
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

    # --- UI ---
    left, center, right = st.columns([1, 2, 1])
    with left:
        st.markdown(f"<div class='circle' style='background-color:#39CCCC;'>RBF<br>{RBF} mL/min</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='circle' style='background-color:#FF69B4;'>SO₂<br>{SO2_a}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='circle' style='background-color:#FF851B;'>PO₂<br>{pO2_a} mmHg</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='circle' style='background-color:#2ECC40;'>Hct<br>{Hct}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='circle' style='background-color:#B10DC9;'>Hb<br>{Hb_a} g/dL</div>", unsafe_allow_html=True)

    with center:
        st.markdown(f"<div class='device-screen'>VO₂ren: {oxygen_consumption:.2f} mL/min</div>", unsafe_allow_html=True)
        avg_o2 = (arterial_oxygen + venous_oxygen) / 2
        st.markdown(f"<div class='device-screen'>Oxygen Content: {avg_o2:.2f} mL O₂/dL</div>", unsafe_allow_html=True)

        st.markdown("#### Temperature (°C)")
        col_tm, col_tp = st.columns([1, 1])
        with col_tm:
            if st.button("➖", key="temp_minus"):
                st.session_state.temperature_setting = max(30, st.session_state.temperature_setting - 1)
        with col_tp:
            if st.button("➕", key="temp_plus"):
                st.session_state.temperature_setting = min(45, st.session_state.temperature_setting + 1)

        temp = st.session_state.temperature_setting
        temp_color = "#66B2FF" if 35 <= temp <= 38 else "#D4AF37" if temp < 35 else "#FF6B6B"
        st.markdown(f"<div class='device-screen' style='background-color:{temp_color};'>Temperature: {temp} °C</div>", unsafe_allow_html=True)

        st.markdown("#### Pressure (mmHg)")
        col_pm, col_pp = st.columns([1, 1])
        with col_pm:
            if st.button("➖", key="pressure_minus"):
                st.session_state.pressure_setting = max(50, st.session_state.pressure_setting - 1)
        with col_pp:
            if st.button("➕", key="pressure_plus"):
                st.session_state.pressure_setting = min(200, st.session_state.pressure_setting + 1)

        press = st.session_state.pressure_setting
        press_color = "#66B2FF" if 70 <= press <= 100 else "#D4AF37" if 60 <= press < 70 else "#FF6B6B"
        st.markdown(f"<div class='device-screen' style='background-color:{press_color};'>Pressure: {press} mmHg</div>", unsafe_allow_html=True)

        st.markdown("### 📈 VO₂ren & Oxygen Content Trends")
        df1 = pd.DataFrame({'Time': st.session_state.time_history, 'VO₂ren (mL/min)': st.session_state.vo2ren_history})
        st.altair_chart(alt.Chart(df1).mark_line(point=True).encode(x='Time', y='VO₂ren (mL/min)', tooltip=['Time', 'VO₂ren (mL/min)']), use_container_width=True)
        df2 = pd.DataFrame({'Time': st.session_state.time_history, 'Oxygen Content (mL O₂/dL)': st.session_state.oc_history})
        st.altair_chart(alt.Chart(df2).mark_line(point=True).encode(x='Time', y='Oxygen Content (mL O₂/dL)', tooltip=['Time', 'Oxygen Content (mL O₂/dL)']), use_container_width=True)

    with right:
        st.markdown(f"<div class='device-screen'>AOC: {arterial_oxygen:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='device-screen'>RVOC: {venous_oxygen:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='device-screen'>Battery Life: 85%</div>", unsafe_allow_html=True)
        if st.button("⚠️ Emergency Stop"):
            st.error("⚠️ Emergency Stop Activated!")

    # --- Export Section ---
    st.divider()
    col_exp, col_legend1, col_legend2, col_legend3 = st.columns([2, 1, 1, 1])
    with col_exp:
        export_df = pd.DataFrame({
            'Time': st.session_state.time_history,
            'VO₂ren (mL/min)': st.session_state.vo2ren_history,
            'Oxygen Content (mL O₂/dL)': st.session_state.oc_history
        })
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, index=False, sheet_name="Oxygen Metrics")
        buffer.seek(0)
        st.download_button("📤 Export to Excel", buffer, file_name="oxygen_metrics.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col_legend1:
        st.markdown("<div class='device-screen' style='background-color:#FF6B6B;'>Red: Critical</div>", unsafe_allow_html=True)
    with col_legend2:
        st.markdown("<div class='device-screen' style='background-color:#D4AF37;'>Yellow: Warning</div>", unsafe_allow_html=True)
    with col_legend3:
        st.markdown("<div class='device-screen' style='background-color:#66B2FF;'>Blue: Normal</div>", unsafe_allow_html=True)

else:
    st.info("📥 Upload a `data.xlsx` file (structured like Layout) to begin.")
