import streamlit as st
import threading
import global_vars
import pandas as pd
from main import DataReader
from google.cloud import firestore



def main():
    st.title('Air Quality Pollutant Concentration Data')

    col4, col5, col6 = st.columns(3)
    col4.metric("CO (ppm)", global_vars.CO_VALS[-1], 0 if len(global_vars.CO_VALS)<=1 else (global_vars.CO_VALS[-1]-global_vars.CO_VALS[-2]))
    col5.metric("CO2 (ppm)", global_vars.CO2_VALS[-1], 0 if len(global_vars.CO2_VALS)<=1 else (global_vars.CO2_VALS[-1]-global_vars.CO2_VALS[-2]))
    col6.metric("NHx (ppm)", global_vars.NHX_VALS[-1], 0 if len(global_vars.NHX_VALS)<=1 else (global_vars.NHX_VALS[-1]-global_vars.NHX_VALS[-2]))
    col7, col8, col9, col10 = st.columns(4)
    col7.metric("PM2.5 (ug/m3)", global_vars.PM2_point_5_VALS[-1], 0 if len(global_vars.PM2_point_5_VALS)<=1 else (global_vars.PM2_point_5_VALS[-1]-global_vars.PM2_point_5_VALS[-2]))
    col8.metric("PM10 (ug/m3)", global_vars.PM10_VALS[-1], 0 if len(global_vars.PM10_VALS)<=1 else (global_vars.PM10_VALS[-1]-global_vars.PM10_VALS[-2]))
    col9.metric("O3 (ppb)", global_vars.O3_VALS[-1], 0 if len(global_vars.O3_VALS)<=1 else (global_vars.O3_VALS[-1]-global_vars.O3_VALS[-2]))
    col10.metric("SO2 (ppm)", global_vars.SO2_VALS[-1], 0 if len(global_vars.SO2_VALS)<=1 else (global_vars.SO2_VALS[-1]-global_vars.SO2_VALS[-2]))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (degree Celsius)", global_vars.TEMPERATURE_VALS[-1], 0 if len(global_vars.TEMPERATURE_VALS)<=1 else (global_vars.TEMPERATURE_VALS[-1]-global_vars.TEMPERATURE_VALS[-2]))
    col2.metric("Pressure (hPa)", global_vars.PRESSURE_VALS[-1], 0 if len(global_vars.PRESSURE_VALS)<=1 else (global_vars.PRESSURE_VALS[-1]-global_vars.PRESSURE_VALS[-2]))
    col3.metric("Humidity (%)", global_vars.HUMIDITY_VALS[-1], 0 if len(global_vars.HUMIDITY_VALS)<=1 else (global_vars.HUMIDITY_VALS[-1]-global_vars.HUMIDITY_VALS[-2]))
    
    if st.button('CHART'):
        d1 = {'temp': global_vars.TEMPERATURE_VALS}
        chart_data1 = pd.DataFrame(data=d1)
        d2 = {'pressure': global_vars.PRESSURE_VALS}
        chart_data2 = pd.DataFrame(data=d2)
        d3 = {'humidity': global_vars.HUMIDITY_VALS}
        chart_data3 = pd.DataFrame(data=d3)
        d4 = {'CO': global_vars.CO_VALS}
        chart_data4 = pd.DataFrame(data=d4)
        d5 = {'CO2': global_vars.CO2_VALS}
        chart_data5 = pd.DataFrame(data=d5)
        st.area_chart(chart_data1)
        st.area_chart(chart_data2)
        st.area_chart(chart_data3)
        st.area_chart(chart_data4)
        st.area_chart(chart_data5)
    


if __name__ == '__main__':
    main()
    DataReader()
    