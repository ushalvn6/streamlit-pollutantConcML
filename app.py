import streamlit as st
import threading
import global_vars
import pandas as pd
from main import DataReader
from data_updater import DataUpdater
from google.cloud import firestore
from streamlit_autorefresh import st_autorefresh



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
    
    
    if st.button('TREND') and (len(global_vars.TEMPERATURE_VALS)>=20):
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
        d6 = {'NHx': global_vars.NHX_VALS}
        chart_data6= pd.DataFrame(data=d6)
        d7 = {'PM2.5': global_vars.PM2_point_5_VALS}
        chart_data7 = pd.DataFrame(data=d7)
        d8 = {'PM10': global_vars.PM10_VALS}
        chart_data8 = pd.DataFrame(data=d8)
        d9 = {'O3': global_vars.O3_VALS}
        chart_data9 = pd.DataFrame(data=d9)
        d10 = {'SO2': global_vars.SO2_VALS}
        chart_data10 = pd.DataFrame(data=d10)
        st.line_chart(chart_data1)
        st.line_chart(chart_data2)
        st.line_chart(chart_data3)
        st.line_chart(chart_data4)
        st.line_chart(chart_data5)
        st.line_chart(chart_data6)
        st.line_chart(chart_data7)
        st.line_chart(chart_data8)
        st.line_chart(chart_data9)
        st.line_chart(chart_data10)
    else:
        st.write("Insufficient data to be presented")

    st_autorefresh(interval=6000)
    


if __name__ == '__main__':
    main()
    DataReader()
    DataUpdater()
    