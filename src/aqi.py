import requests
import time
import streamlit as st

AIRNOW_API_KEY = st.secrets["AIRNOW_API_KEY"]

def get_aqi(zip_code):

    def get_current(zip_code):
        r = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?",
            params={
                "format":"application/json",
                "zipCode":zip_code,
                "API_KEY":AIRNOW_API_KEY})
        current = {}
        for entry in r.json():
            if entry["ParameterName"] == "O3":
                entry["ParameterName"] = "Ozone"
            current[entry["ParameterName"]] = [entry["AQI"], entry["Category"]["Name"], entry["Category"]["Number"]]
        return current

    def fmt_current(gc):
        return f'{zip_code}\nOzone: {gc["Ozone"][:2]}\nPM2.5: {gc["PM2.5"][:2]}\nPM10:  {gc["PM10"][:2]}'
        
    try:
        gc = get_current(zip_code)
        fmt_gc = fmt_current(gc)
        return fmt_gc
    except:
        return "Error, probably invalid zip"

if __name__ == "__main__":
    print(get_aqi(10020))