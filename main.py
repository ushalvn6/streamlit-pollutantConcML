"""This file contains the class that will run the app and data collector to make predictions"""
from glob import glob
import threading
import global_vars
from google.cloud import firestore
# Create an Event for notifying main thread.




def get_data ():
    # Authenticate to Firestore with the JSON account key.
    # Create a callback on_snapshot function to capture changes
    delete_done = threading.Event()
        # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                if global_vars.DATA_NO <= 20:
                    update_doc = doc_ref.get()
                    temp_values = update_doc.to_dict()
                    global_vars.TEMPERATURE_VALS.append(temp_values["temperature"])
                    global_vars.HUMIDITY_VALS.append(temp_values["humidity"])
                    print(f'Temperature readings: {global_vars.TEMPERATURE_VALS}')
                    print(f'Humidity readings: {global_vars.HUMIDITY_VALS}')
                    delete_done.set()
                else:
                    global_vars.DATA_NO = 0
                    global_vars.TEMPERATURE_VALS = []
                    global_vars.HUMIDITY_VALS = []
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
    global_vars.DATA_NO += 1
    print("The contents are: ", initial_values)


class DataReader:
    
    data_read = threading.Thread(target = get_data, daemon=True)
    data_read.start()

    




