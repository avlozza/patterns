import streamlit as st
import pandas as pd
from datetime import datetime
import jyotishyamitra as jsm
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from timezonefinder import TimezoneFinder

def display_chart_details(chart_details):
    col1, col2 = st.columns(2)
    with col1:
        # Displaying Ascendant details
        ascendant_details = chart_details['ascendant']
        # Format the position in DDD° MM' SS.S" format
        pos_deg = ascendant_details['pos']['deg']
        pos_min = ascendant_details['pos']['min']
        pos_sec = ascendant_details['pos']['sec']
        formatted_pos = f"{pos_deg}° {pos_min}' {pos_sec:.1f}\""
        # Create a new dictionary with the formatted position
        ascendant_details['pos'] = {'formatted': formatted_pos}
        df_ascendant = pd.DataFrame([ascendant_details]).T
        st.write("Ascendant Details:")
        st.write(df_ascendant)
    with col2:
        # Displaying Classifications details
        classifications_details = chart_details['classifications']
        df_classifications = pd.DataFrame([classifications_details]).T
        st.write("Classifications Details:")
        st.write(df_classifications)

    # Displaying Planets details
    planets_details = chart_details['planets']
    df_planets = pd.DataFrame(planets_details).T

    # Formatting aspects data in a readable format
    df_planets['Aspects_Houses'] = df_planets['Aspects'].apply(lambda x: x.get('houses', []))
    df_planets['Aspects_Planets'] = df_planets['Aspects'].apply(lambda x: x.get('planets', []))
    df_planets['Aspects_Signs'] = df_planets['Aspects'].apply(lambda x: x.get('signs', []))

    # Dropping the original 'Aspects' column
    df_planets.drop(['Aspects', 'status'], axis=1, inplace=True)

    # Displaying the modified Planets details DataFrame
    st.write("Planets Details:")
    st.write(df_planets)

    # Displaying Houses details
    houses_details = chart_details['houses']
    df_houses = pd.DataFrame(houses_details)
    st.write("Houses Details:")
    st.write(df_houses)

with st.sidebar.expander("Birth Details"):
    # User input for Name
    name = st.text_input("Name","Garima")

    # User input for Gender
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    # User input for Date of Birth
    dob = st.date_input("Birth Date", value=datetime(1992,4,27),min_value=datetime(1990, 1, 1))
    tob = st.time_input("Birth Time")

    # User input for Place of Birth
    pob = st.text_input("Place of Birth","New Delhi,India")

    # Get latitude, longitude, and timezone details using geopy
    lat = st.number_input("Enter Latitude:", -90.0, 90.0, +28.6444, 0.0001)
    long = st.number_input("Enter Longitude:", -180.0, 180.0, +77.216, 0.0001)
    tz = st.number_input("Enter Timezone:", -12.0, 12.0, 5.5, 0.5)

    # Providing input birth data
    inputdata = jsm.input_birthdata(name=name, gender=gender,year=dob.year, month=dob.month, day=dob.day,place=pob, longitude=long, lattitude=lat, timezone=tz,hour=tob.hour, min=tob.minute, sec=tob.second)

    # Validate Birthdata
    jsm.validate_birthdata()

# If Birthdata is valid, get birthdata
if jsm.IsBirthdataValid():
    birthdata = jsm.get_birthdata()

    # Invoke the API generate_astrologicalData with returnval desired to be dictionary
    astrodata = jsm.generate_astrologicalData(birthdata, returnval="ASTRODATA_DICTIONARY")

    # Display a dropdown to select a specific chart
    if astrodata:
        selected_chart = st.sidebar.selectbox("Select Chart:", list(astrodata.keys()))

        # Display details for the selected chart
        chart_details = astrodata[selected_chart]
        st.sidebar.write(chart_details)

        # Extracting specific information for display in 6 dataframes
        if selected_chart in ["D1", "D2", "D3", "D4", "D7","D9", "D10","D12","D16","D20","D24","D27","D30","D40","D45","D60","Balas","AshtakaVarga","Dashas","special_points","user_details"]:  # Add other charts as needed
            display_chart_details(chart_details)
