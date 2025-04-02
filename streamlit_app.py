import streamlit as st

# Initialize session state
if 'pressure_setting' not in st.session_state:
    st.session_state.pressure_setting = 100
if 'temperature_setting' not in st.session_state:
    st.session_state.temperature_setting = 37

# Custom CSS for styling
st.markdown("""
    <style>
    .device-screen {
        color: grey;
        font-family: 'Courier New', monospace;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        margin: 5px 0;
    }
    .button-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
        justify-content: center;
    }
    .stop-button {
        background-color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("PreservaLife")

# --- Pressure Adjustment ---
st.markdown("###Pressure (mmHg)")
col1_minus, col1_plus = st.columns([1, 1])
with col1_minus:
    if st.button("➖", key="pressure_minus"):
        st.session_state.pressure_setting = max(50, st.session_state.pressure_setting - 1)
with col1_plus:
    if st.button("➕", key="pressure_plus"):
        st.session_state.pressure_setting = min(200, st.session_state.pressure_setting + 1)

# Pressure Display
pressure_color = (
    "red" if st.session_state.pressure_setting < 60 else
    "yellow" if st.session_state.pressure_setting < 70 else
    "blue"
)
st.markdown(f"<div class='device-screen' style='background-color:{pressure_color};'>"
            f"Measured Pressure: {st.session_state.pressure_setting} mmHg</div>", unsafe_allow_html=True)

# --- Temperature Adjustment ---
st.markdown("### Temperature (°C)")
col2_minus, col2_plus = st.columns([1, 1])
with col2_minus:
    if st.button("➖", key="temp_minus"):
        st.session_state.temperature_setting = max(30, st.session_state.temperature_setting - 1)
with col2_plus:
    if st.button("➕", key="temp_plus"):
        st.session_state.temperature_setting = min(45, st.session_state.temperature_setting + 1)

# Temperature Display
temperature_color = (
    "red" if st.session_state.temperature_setting < 34 or st.session_state.temperature_setting > 38 else
    "yellow" if st.session_state.temperature_setting < 35 else
    "blue"
)
st.markdown(f"<div class='device-screen' style='background-color:{temperature_color};'>"
            f"Measured Temperature: {st.session_state.temperature_setting} °C</div>", unsafe_allow_html=True)

# --- Simulated Measurements ---
oxygen_consumption = 250
st.markdown(f'<div class="device-screen">Measured Oxygen Consumption: {oxygen_consumption} mL/min</div>', unsafe_allow_html=True)

urine_flow_rate = 50
st.markdown(f'<div class="device-screen">Measured Urine Flow Rate: {urine_flow_rate} mL/min</div>', unsafe_allow_html=True)

# --- Emergency Stop ---
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🛑 STOP", key="stop_button"):
    st.error("Emergency Stop Activated!")
st.markdown('</div>', unsafe_allow_html=True)
