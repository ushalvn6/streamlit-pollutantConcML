"""This file contains the class that will run the app and data collector to make predictions"""
from glob import glob
import numpy as np
import pickle
import time
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import threading
import global_vars
from google.cloud import firestore
# Create an Event for notifying main thread.


def print_vals():
    print(f'Temperature readings: {global_vars.TEMPERATURE_VALS}')
    print(f'Humidity readings: {global_vars.HUMIDITY_VALS}')
    print(f'Pressure readings: {global_vars.PRESSURE_VALS}')
    print(f'PM2.5 readings: {global_vars.PM2_point_5_VALS}')
    print(f'PM10 readings: {global_vars.PM10_VALS}')
    print(f'SO2 readings: {global_vars.SO2_VALS}')
    print(f'O3 readings: {global_vars.O3_VALS}')
    print(f'CO readings: {global_vars.CO_VALS}')
    print(f'CO2 readings: {global_vars.CO2_VALS}')
    print(f'NHx readings: {global_vars.NHX_VALS}')
    print(f'Make prediction?: {global_vars.PREDICT}')
    print(f"Data Length: {len(global_vars.TEMPERATURE_VALS)}")

def get_data ():
    # Authenticate to Firestore with the JSON account key.
    # Create a callback on_snapshot function to capture changes
    delete_done = threading.Event()
        # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':  
                update_doc = doc_ref.get()
                temp_values = update_doc.to_dict()
                global_vars.TEMPERATURE_VALS.append(temp_values["temperature"])
                global_vars.HUMIDITY_VALS.append(temp_values["humidity"])
                global_vars.PRESSURE_VALS.append(temp_values["pressure"])
                global_vars.SO2_VALS.append(temp_values["SO2"])
                global_vars.O3_VALS.append(temp_values["O3"])
                global_vars.CO_VALS.append(temp_values["CO"])
                global_vars.CO2_VALS.append(temp_values["CO2"])
                global_vars.NHX_VALS.append(temp_values["NHx"])
                global_vars.PM2_point_5_VALS.append(temp_values["PM2_5"])
                global_vars.PM10_VALS.append(temp_values["PM10"])   
                global_vars.PREDICT = temp_values['predict']
                print_vals()
                delete_done.set()
                
                        
    db = firestore.Client.from_service_account_json("firestore-key.json")

    # Create a reference to the Google post.
    doc_ref = db.collection("sensor_params").document("output_parameters")

    # Then get the data at that reference.
    doc = doc_ref.get()
    
    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)      
    

    # Let's see what we got!
    print("The id is: ", doc.id)
    initial_values = doc.to_dict()
    global_vars.TEMPERATURE_VALS.append(initial_values["temperature"])
    global_vars.HUMIDITY_VALS.append(initial_values["humidity"])
    global_vars.PRESSURE_VALS.append(initial_values["pressure"])
    global_vars.O3_VALS.append(initial_values["O3"])
    global_vars.SO2_VALS.append(initial_values["SO2"])
    global_vars.PM2_point_5_VALS.append(initial_values["PM2_5"])
    global_vars.PM10_VALS.append(initial_values["PM10"])
    global_vars.CO_VALS.append(initial_values["CO"])
    global_vars.CO2_VALS.append(initial_values["CO2"])
    global_vars.NHX_VALS.append(initial_values["NHx"])
    global_vars.DATA_NO += 1
    print("The contents are: ", initial_values)
   
    


class DataReader:
    
    data_read = threading.Thread(target = get_data, daemon=True)
    data_read.start()

    




