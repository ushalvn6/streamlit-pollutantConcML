import streamlit as st
import threading
import global_vars
import pandas as pd
from main import DataReader
from google.cloud import firestore



def main():
    st.title('Air Quality Predictor')

    if st.button('Balloons?'):
        st.balloons()
        st.write(global_vars.TEMPERATURE_VALS)
    
    if st.button('Data'):
        d = {'temp': global_vars.TEMPERATURE_VALS, 'humidity': global_vars.HUMIDITY_VALS, 'pressure':global_vars.PRESSURE_VALS, 'PM2.5':global_vars.PM2_point_5_VALS, 'PM10':global_vars.PM10_VALS, 'O3':global_vars.O3_VALS, 'SO2':global_vars.SO2_VALS, 'CO':global_vars.CO_VALS, 'CO2':global_vars.CO2_VALS, 'NHx':global_vars.NHX_VALS}
        chart_data = pd.DataFrame(data=d)
        st.line_chart(chart_data)
    


if __name__ == '__main__':
    main()
    DataReader()
    