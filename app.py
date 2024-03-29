import streamlit as st
import global_vars
import pandas as pd
from main import DataReader
from data_updater import DataUpdater
from streamlit_autorefresh import st_autorefresh


# Method to add the background image, and other css formatting
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://www.pixelstalk.net/wp-content/uploads/images6/Aesthetic-White-Wallpaper-Cloud.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         div[data-testid="metric-container"] {{
            background-color:#F4FFFF;
            border: 1px solid black;
            padding: 5% 5% 5% 10%;
            border-radius: 5px;
            color: rgb(30, 103, 119);
            overflow-wrap: break-word;
        }}

         /* breakline for metric text         */
        div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {{
        overflow-wrap: break-word;
        white-space: break-spaces;
        color: purple;
        }}
         </style>
         """,
         unsafe_allow_html=True
     )




def main():
    st.title('Air Quality Pollutant Concentration Data')
    add_bg_from_url() 
    tab1, tab2, tab3 = st.tabs(['Data', 'Indicator', 'Trend'])
    
   # Indicator Tab
    with tab2:
        st.image ("api.jpg",caption="API Chart")
        st.image('status.jpg',caption="Pollutant Classification Chart")
        
    # Data tab
    with tab1:
        # Displays the current value & difference with previous values to 2 d.p
        st.metric("API", '%.2f' % float(global_vars.CURRENT_AQI), '%.2f' % float(global_vars.CURRENT_AQI-global_vars.PREVIOUS_AQI), delta_color='inverse')
        col4, col5, col6 = st.columns(3)
        col4.metric("CO (ppm)", '%.2f' % global_vars.CO_VALS[-1], 0 if len(global_vars.CO_VALS)<=1 else (global_vars.CO_VALS[-1]-global_vars.CO_VALS[-2]), delta_color='inverse')
        col5.metric("CO2 (ppm)",  '%.2f' % global_vars.CO2_VALS[-1], 0 if len(global_vars.CO2_VALS)<=1 else (global_vars.CO2_VALS[-1]-global_vars.CO2_VALS[-2]), delta_color='inverse')
        col6.metric("NHx (ppm)", '%.2f' % global_vars.NHX_VALS[-1], 0 if len(global_vars.NHX_VALS)<=1 else (global_vars.NHX_VALS[-1]-global_vars.NHX_VALS[-2]), delta_color='inverse')
        col7, col8, col9, col10 = st.columns(4)
        col7.metric("PM2.5 (ug/m3)", global_vars.PM2_point_5_VALS[-1], 0 if len(global_vars.PM2_point_5_VALS)<=1 else (global_vars.PM2_point_5_VALS[-1]-global_vars.PM2_point_5_VALS[-2]), delta_color='inverse')
        col8.metric("PM10 (ug/m3)", global_vars.PM10_VALS[-1], 0 if len(global_vars.PM10_VALS)<=1 else (global_vars.PM10_VALS[-1]-global_vars.PM10_VALS[-2]), delta_color='inverse')
        col9.metric("O3 (ppb)", global_vars.O3_VALS[-1], 0 if len(global_vars.O3_VALS)<=1 else (global_vars.O3_VALS[-1]-global_vars.O3_VALS[-2]), delta_color='inverse')
        col10.metric("SO2 (ppm)", '%.2f' % global_vars.SO2_VALS[-1], 0 if len(global_vars.SO2_VALS)<=1 else (global_vars.SO2_VALS[-1]-global_vars.SO2_VALS[-2]), delta_color='inverse')

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (degree Celsius)", '%.2f' % global_vars.TEMPERATURE_VALS[-1], 0 if len(global_vars.TEMPERATURE_VALS)<=1 else (global_vars.TEMPERATURE_VALS[-1]-global_vars.TEMPERATURE_VALS[-2]), delta_color='inverse')
        col2.metric("Pressure (hPa)", '%.2f' % global_vars.PRESSURE_VALS[-1], 0 if len(global_vars.PRESSURE_VALS)<=1 else (global_vars.PRESSURE_VALS[-1]-global_vars.PRESSURE_VALS[-2]), delta_color='inverse')
        col3.metric("Humidity (%)", '%.2f' % global_vars.HUMIDITY_VALS[-1], 0 if len(global_vars.HUMIDITY_VALS)<=1 else (global_vars.HUMIDITY_VALS[-1]-global_vars.HUMIDITY_VALS[-2]), delta_color='inverse')

    # Trend tab
    with tab3:
        
        # Plots the chart for each data set. Some of the data are grouped together as they show similar values.
        if len(global_vars.TEMPERATURE_VALS)>=20:
            st.header('Data trend of the previous 20 readings')
            d1 = {'temperature': global_vars.TEMPERATURE_VALS, 'humidity': global_vars.HUMIDITY_VALS}
            chart_data1 = pd.DataFrame(data=d1)
            d2 = {'pressure': global_vars.PRESSURE_VALS}
            chart_data2 = pd.DataFrame(data=d2)
            d3 = {'CO': global_vars.CO_VALS, 'NHx': global_vars.NHX_VALS, 'SO2': global_vars.SO2_VALS }
            chart_data4 = pd.DataFrame(data=d3)
            d4 = {'CO2': global_vars.CO2_VALS}
            chart_data5 = pd.DataFrame(data=d4)
            d5 = {'PM2.5': global_vars.PM2_point_5_VALS, 'PM10': global_vars.PM10_VALS}
            chart_data7 = pd.DataFrame(data=d5)
            d6 = {'O3': global_vars.O3_VALS}
            chart_data9 = pd.DataFrame(data=d6)
            st.line_chart(chart_data1)
            st.line_chart(chart_data2)
            st.line_chart(chart_data4)
            st.line_chart(chart_data5)
            st.line_chart(chart_data7)
            st.line_chart(chart_data9)
        else:
            st.write("Insufficient data to be presented")
    

    st_autorefresh(interval=6000)   # refresh every 6 seconds
    


if __name__ == '__main__':
    main()
    DataReader()    # Class that reads data from firestore
    DataUpdater()   # Class that updates data to firestore
    