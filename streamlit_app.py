import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import io
import random

# --- Hardcoded labels from Layout.xlsx (42 entries) ---
layout_flat = [
    "Arterial High quality low end hemoglobin conc", "Arterial High quality high end hemoglobin conc",
    "Arterial Medium quality low end hemoglobin conc", "Arterial Medium quality high end hemoglobin conc",
    "Arterial Low quality low end hemoglobin conc", "Arterial Low quality high end hemoglobin conc",
    "Venous High Quality low end hemoglobin conc", "Venous High Quality high end hemoglobin conc",
    "Venous Medium Quality low end hemoglobin conc", "Venous Medium Quality high end hemoglobin conc",
    "Venous Low Quality low end hemoglobin conc", "Venous Low Quality high end hemoglobin conc",
    "Arterial High quality low end oxygen sat", "Arterial High quality high end oxygen sat",
    "Arterial Medium quality low end oxygen sat", "Arterial Medium quality high end oxygen sat",
    "Arterial Low quality low end oxygen sat", "Arterial Low quality high end oxygen sat",
    "Venous High Quality low end oxygen sat", "Venous High Quality high end oxygen sat",
    "Venous Medium Quality low end oxygen sat", "Venous Medium Quality high end oxygen sat",
    "Venous Low Quality low end oxygen sat", "Venous Low Quality high end oxygen sat",
    "Arterial High quality low end partial pressure", "Arterial High quality high end partial pressure",
    "Arterial Medium quality low end partial pressure", "Arterial Medium quality high end partial pressure",
    "Arterial Low quality low end partial pressure", "Arterial Low quality high end partial pressure",
    "Venous High Quality low end partial pressure", "Venous High Quality high end partial pressure",
    "Venous Medium Quality low end partial pressure", "Venous Medium Quality high end partial pressure",
    "Venous Low Quality low end partial pressure", "Venous Low Quality high end partial pressure",
    "High quality low end flow rate", "High quality high end flow rate",
    "medium quality low end flow rate", "medium quality high end flow rate",
    "low quality low end flow rate", "low quality high end flow rate"
]

# --- Page Setup ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#212529;'>PreservaLife</h1>", unsafe_allow_html=True)

# --- Upload UI ---
st.sidebar.markdown("### Upload data.xlsx")
uploaded_file = st.sidebar.file_uploader("Upload data.xlsx", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    if df.shape != (7, 6):
        st.error(f"❌ File must be exactly 7 rows × 6 columns (A1:F7). Found: {df.shape}")
        st.stop()

    data_flat = df.values.flatten()
    mapped_values = {label: value for label, value in zip(layout_flat, data_flat)}

    RBF = 800
    Hct = 36

    for key, default in {
        'pressure_setting': 100,
        'temperature_setting': 37,
        'vo2ren_history': [],
        'oc_history': [],
        'time_history': [],
        'metrics': None
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    metrics = st.session_state.metrics
    if metrics:
        Hb_a = metrics["Hb_a"]
        SO2_a = metrics["SO2_a"]
        pO2_a = metrics["pO2_a"]
        Hb_v = metrics["Hb_v"]
        SO2_v = metrics["SO2_v"]
        pO2_v = metrics["pO2_v"]
        arterial_oxygen = metrics["arterial_oxygen"]
        venous_oxygen = metrics["venous_oxygen"]
        oxygen_consumption = metrics["oxygen_consumption"]
        flow_rate = metrics["flow_rate"]

    # --- UI Styling ---
    st.markdown("""<style>
        html, body, [data-testid="stAppViewContainer"] {background-color: #ffffff !important; color: #212529 !important;}
        .block-container {background-color: #ffffff !important;}
        .device-screen {
            background-color: #ffffff; color: #212529; font-family: monospace; padding: 14px;
            border-radius: 10px; text-align: center; font-size: 18px; font-weight: bold;
            margin-bottom: 12px; box-shadow: 0 0 8px rgba(0,0,0,0.05);
        }
        .circle {
            width: 120px; height: 120px; border-radius: 50%; display: flex; flex-direction: column;
            align-items: center; justify-content: center; font-weight: bold; background-color: #ffffff;
            color: #212529; margin: 20px auto; padding: 10px; font-size: 15px; line-height: 1.3;
            box-shadow: 0 0 6px rgba(0,0,0,0.08);
        }
        h1, h2, h3, h4, h5, h6, p, label { color: #212529 !important; }
        [data-testid="stSidebar"] { background-color: #f8f9fa !important; }
        button, .stDownloadButton button {
            background-color: #ffffff !important; color: #212529 !important;
            border: 1px solid #ccc !important; font-weight: bold;
        }
    </style>""", unsafe_allow_html=True)

    # --- Layout ---
    left, center, right = st.columns([1, 2, 1])

    with left:
        if metrics:
            st.markdown(f"<div class='circle' style='background-color:#39CCCC;'>RBF<br>{RBF} mL/min</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='circle' style='background-color:#0074D9;'>Flow Rate<br>{round(flow_rate, 1)} mL/min</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='circle' style='background-color:#FF69B4;'>SO₂<br>{round(SO2_a, 1)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='circle' style='background-color:#FF851B;'>PO₂<br>{round(pO2_a, 1)} mmHg</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='circle' style='background-color:#2ECC40;'>Hct<br>{Hct}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='circle' style='background-color:#B10DC9;'>Hb<br>{round(Hb_a, 1)} g/dL</div>", unsafe_allow_html=True)

    with center:
        if metrics:
            st.markdown(f"<div class='device-screen'>VO₂ren: {oxygen_consumption:.2f} mL/min</div>", unsafe_allow_html=True)
            avg_o2 = (arterial_oxygen + venous_oxygen) / 2
            st.markdown(f"<div class='device-screen'>Oxygen Content: {avg_o2:.2f} mL O₂/dL</div>", unsafe_allow_html=True)

        if st.button("🔁 Generate Metrics"):
            Hb_a = random.uniform(mapped_values["Arterial Low quality low end hemoglobin conc"],
                                  mapped_values["Arterial Low quality high end hemoglobin conc"])
            SO2_a = random.uniform(mapped_values["Arterial Medium quality low end oxygen sat"],
                                   mapped_values["Arterial Medium quality high end oxygen sat"])
            pO2_a = random.uniform(mapped_values["Arterial Medium quality low end partial pressure"],
                                   mapped_values["Arterial Medium quality high end partial pressure"])

            Hb_v = random.uniform(mapped_values["Venous High Quality low end hemoglobin conc"],
                                  mapped_values["Venous High Quality high end hemoglobin conc"])
            SO2_v = random.uniform(mapped_values["Venous Low Quality low end oxygen sat"],
                                   mapped_values["Venous Low Quality high end oxygen sat"])
            pO2_v = random.uniform(mapped_values["Venous Medium Quality low end partial pressure"],
                                   mapped_values["Venous Medium Quality high end partial pressure"])

            flow_rate = random.uniform(mapped_values["High quality low end flow rate"],
                                       mapped_values["High quality high end flow rate"])

            arterial_oxygen = (1.34 * Hb_a * SO2_a) + (0.003 * pO2_a)
            venous_oxygen = (1.34 * Hb_v * SO2_v) + (0.003 * pO2_v)
            oxygen_consumption = RBF * (arterial_oxygen - venous_oxygen)

            st.session_state.metrics = {
                "Hb_a": Hb_a, "SO2_a": SO2_a, "pO2_a": pO2_a,
                "Hb_v": Hb_v, "SO2_v": SO2_v, "pO2_v": pO2_v,
                "arterial_oxygen": arterial_oxygen,
                "venous_oxygen": venous_oxygen,
                "oxygen_consumption": oxygen_consumption,
                "flow_rate": flow_rate
            }

            now = datetime.now().strftime('%H:%M:%S')
            st.session_state.vo2ren_history.append(oxygen_consumption)
            st.session_state.oc_history.append((arterial_oxygen + venous_oxygen) / 2)
            st.session_state.time_history.append(now)

            for key in ['vo2ren_history', 'oc_history', 'time_history']:
                st.session_state[key] = st.session_state[key][-20:]

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
        df_vo2 = pd.DataFrame({'Time': st.session_state.time_history, 'VO₂ren (mL/min)': st.session_state.vo2ren_history})
        st.altair_chart(alt.Chart(df_vo2).mark_line(point=True).encode(x='Time', y='VO₂ren (mL/min)'), use_container_width=True)

        df_oc = pd.DataFrame({'Time': st.session_state.time_history, 'Oxygen Content (mL O₂/dL)': st.session_state.oc_history})
        st.altair_chart(alt.Chart(df_oc).mark_line(point=True).encode(x='Time', y='Oxygen Content (mL O₂/dL)'), use_container_width=True)

    with right:
        if metrics:
            st.markdown(f"<div class='device-screen'>AOC: {arterial_oxygen:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='device-screen'>RVOC: {venous_oxygen:.2f} mL O₂/dL</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='device-screen'>Battery Life: 85%</div>", unsafe_allow_html=True)
        if st.button("⚠️ Emergency Stop"):
            st.error("⚠️ Emergency Stop Activated!")

    st.markdown("### 🧭 Status Color Legend")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='device-screen' style='background-color:#FF6B6B;'>Red: Critical</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='device-screen' style='background-color:#D4AF37;'>Yellow: Warning</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='device-screen' style='background-color:#0074D9;'>Blue: Normal</div>", unsafe_allow_html=True)

    st.divider()
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

else:
    st.info("📥 Upload a data.xlsx file (structured as 7x6, A1:F7) to begin.")
