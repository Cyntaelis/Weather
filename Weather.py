import streamlit as st
from src import aqi
from src import forecast
from src import gazetteer
from src import alerts
 
st.set_page_config(
    page_title="Weather",
    page_icon="tornado",
    layout="wide",
)

@st.cache_data
def get_gazetteer():
    return gazetteer.get_zip_dict()

st.title("Weather and stuff")
#st.checkbox("Disable text input widget", key="disabled")
st.radio(
    "Data Type",
    key="query",
    options=["Forecast", "AQI", "Alerts"],
)
# st.text_input(
#     "Zip code",
#     "",
#     key="zip_code",
# )

with st.form(key="my_form"):
    stuff = st.text_input(
    "Zip code",
    "",
    key="zip_code")
    st.form_submit_button("Refresh")

if st.session_state.zip_code != "":
    if st.session_state.query == "AQI":
        thingy = aqi.get_aqi(st.session_state.zip_code)
    if st.session_state.query == "Forecast":
        if st.session_state.zip_code in get_gazetteer():
            zip_coords = get_gazetteer()[st.session_state.zip_code]
            zone = forecast.coords_to_zone(zip_coords)
            thingy = forecast.weather(zone)
        else:
            thingy = "invalid zip",st.session_state.zip_code,get_gazetteer().keys()
    if st.session_state.query == "Alerts":
        if st.session_state.zip_code in get_gazetteer():
            zip_coords = get_gazetteer()[st.session_state.zip_code]
            thingy = alerts.get_alerts(zip_coords)
        else:
            thingy = "invalid zip",st.session_state.zip_code,get_gazetteer().keys()
else:
    thingy = ""

txt = st.text_area(st.session_state.query, thingy, height=800)
                   
