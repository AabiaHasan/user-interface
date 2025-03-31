import streamlit as st

# Initialize session state for pressure and temperature if not set
if 'pressure_setting' not in st.session_state:
    st.session_state.pressure_setting = 100
if 'temperature_setting' not in st.session_state:
    st.session_state.temperature_setting = 37

# Custom Styling to Mimic a Physical Device Interface
st.markdown(
    """
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
    .control-panel {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        padding: 10px;
    }
    .button-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        margin-top: 10px;
    }
    .button {
        background-color: gray;
        color: white;
        padding: 5px 10px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        font-weight: bold;
    }
    .stop-button {
        background-color: red;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.title("PreservaLife Kidney Monitoring Screen")

# Device Container Start
st.markdown('<div class="device-container">', unsafe_allow_html=True)

# Control Panel Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.session_state.pressure_setting = st.number_input("Set Pressure (mmHg)", min_value=50, max_value=200, value=st.session_state.pressure_setting, step=1, key="pressure_input")
    col1a, col1b = st.columns([1, 1])
    with col1a:
        if st.button("➖", key="pressure_minus"):
            st.session_state.pressure_setting = max(50, st.session_state.pressure_setting - 1)
    with col1b:
        if st.button("➕", key="pressure_plus"):
            st.session_state.pressure_setting = min(200, st.session_state.pressure_setting + 1)
    
    # Determine background color based on pressure value
    if st.session_state.pressure_setting < 60:
        pressure_color = "red"
    elif 60 <= st.session_state.pressure_setting < 70:
        pressure_color = "yellow"
    else:
        pressure_color = "blue"
    
    st.markdown(f"<div class='device-screen' style='background-color:{pressure_color};'>Measured Pressure: {st.session_state.pressure_setting} mmHg</div>", unsafe_allow_html=True)

with col2:
    st.session_state.temperature_setting = st.number_input("Set Temperature (°C)", min_value=30, max_value=45, value=st.session_state.temperature_setting, step=1, key="temperature_input")
    col2a, col2b = st.columns([1, 1])
    with col2a:
        if st.button("➖", key="temp_minus"):
            st.session_state.temperature_setting = max(30, st.session_state.temperature_setting - 1)
    with col2b:
        if st.button("➕", key="temp_plus"):
            st.session_state.temperature_setting = min(45, st.session_state.temperature_setting + 1)
    
    # Determine background color based on temperature value
    if st.session_state.temperature_setting < 34 or st.session_state.temperature_setting > 38:
        temperature_color = "red"
    elif 34 <= st.session_state.temperature_setting < 35:
        temperature_color = "yellow"
    else:
        temperature_color = "blue"
    
    st.markdown(f"<div class='device-screen' style='background-color:{temperature_color};'>Measured Temperature: {st.session_state.temperature_setting} °C</div>", unsafe_allow_html=True)

# Oxygen consumption and urine flow rate are only measured
oxygen_consumption = 250  # Simulated fixed measurement will be adjusted 
st.markdown(f'<div class="device-screen">Measured Oxygen Consumption: {oxygen_consumption} mL/min</div>', unsafe_allow_html=True)

urine_flow_rate = 50  # Simulated fixed measurement
st.markdown(f'<div class="device-screen">Measured Urine Flow Rate: {urine_flow_rate} mL/min</div>', unsafe_allow_html=True)

# Safety Stop Button
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🛑 STOP", key="stop_button"):
    st.error("Emergency Stop Activated!")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close device-container div
