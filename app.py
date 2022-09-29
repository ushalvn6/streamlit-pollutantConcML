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
        d = {'temp': global_vars.TEMPERATURE_VALS, 'humidity': global_vars.HUMIDITY_VALS}
        chart_data = pd.DataFrame(data=d)
        st.line_chart(chart_data)
    


if __name__ == '__main__':
    main()
    DataReader()
    