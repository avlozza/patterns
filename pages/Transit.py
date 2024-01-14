import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import jyotishyamitra as jsm
import plotly.express as px

# Function to display planets details for a given date
def get_planet_details(date, name, gender, lat, long, tz):
    # Providing input birth data for the current date
    inputdata = jsm.input_birthdata(name=name, gender=gender, year=date.year, month=date.month, 
                                    day=date.day, place="", longitude=long, lattitude=lat, timezone=tz, 
                                    hour=12, min=0, sec=0)

    # Validate Birthdata
    jsm.validate_birthdata()

    # If Birthdata is valid, get birthdata
    if jsm.IsBirthdataValid():
        birthdata = jsm.get_birthdata()

        # Invoke the API generate_astrologicalData with returnval desired to be dictionary
        astrodata = jsm.generate_astrologicalData(birthdata, returnval="ASTRODATA_DICTIONARY")

        # Display details for the selected chart (D1 in this case)
        if astrodata and "D1" in astrodata:
            planets_details = astrodata["D1"].get('planets', {})
            df_planets = pd.DataFrame(planets_details).T
             # Formatting aspects data in a readable format
            df_planets['Aspects_Houses'] = df_planets['Aspects'].apply(lambda x: x.get('houses', []))
            df_planets['Aspects_Planets'] = df_planets['Aspects'].apply(lambda x: x.get('planets', []))
            df_planets['Aspects_Signs'] = df_planets['Aspects'].apply(lambda x: x.get('signs', []))

            # Dropping the original 'Aspects' column
            df_planets.drop(['Aspects','pos','rashi','house-nature','gender','house-num','friends','enemies','nuetral','varna','guna','status',df_planets.columns[0]], axis=1, inplace=True)
            df_planets['date'] = date  # Add a column for the date
            return df_planets

    return pd.DataFrame()

# Main Streamlit app
st.title("Planets Details for Date Range")

# User input for Date Range
with st.expander('Date Range'):
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')

    # User input for Birth Details
    name = st.text_input("Name", "Garima")
    gender = st.radio("Gender", ["Male", "Female"], key='gender')

    # Get latitude, longitude, and timezone details using geopy
    lat = st.number_input("Enter Latitude:", -90.0, 90.0, +28.6444, 0.0001)
    long = st.number_input("Enter Longitude:", -180.0, 180.0, +77.216, 0.0001)
    tz = st.number_input("Enter Timezone:", -12.0, 12.0, 5.5, 0.5)

    # Initialize an empty list to store DataFrames
    all_planet_details = []

    # Iterate through the date range
    current_date = start_date
    while current_date <= end_date:
        all_planet_details.append(get_planet_details(current_date, name, gender, lat, long, tz))
        current_date += timedelta(days=1)

    # Combine all DataFrames into a single DataFrame
    result_df = pd.concat(all_planet_details, ignore_index=True)

# Display the combined DataFrame
if not result_df.empty:
    with st.expander('Combined Planets Details:'):
        st.write(result_df)
else:
    st.write("No planet details available for the specified date range.")

# # Plot using Plotly
# fig1 = px.line(result_df, x="date", y="sign", color="symbol", title="Planets Details", labels={"Sign": "Zodiac Sign"})
# st.plotly_chart(fig1)
# # Plot using Plotly
# fig2 = px.line(result_df, x="date", y="nakshatra", color="symbol", title="Planets Details", labels={"Sign": "Zodiac Sign"})
# st.plotly_chart(fig2)

