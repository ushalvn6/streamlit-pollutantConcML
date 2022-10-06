"""This file contains the class that will run the app and data collector to make predictions"""
from glob import glob
import numpy as np
import pickle
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import threading
import global_vars
from google.cloud import firestore
# Create an Event for notifying main thread.


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
	Frame a time series as a supervised learning dataset.
	Arguments:
		data: Sequence of observations as a list or NumPy array.
		n_in: Number of lag observations as input (X).
		n_out: Number of observations as output (y).
		dropnan: Boolean whether or not to drop rows with NaN values.
	Returns:
		Pandas DataFrame of series framed for supervised learning.
	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

def get_data ():
    # Authenticate to Firestore with the JSON account key.
    # Create a callback on_snapshot function to capture changes
    delete_done = threading.Event()
        # Create a callback on_snapshot function to capture changes
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                if global_vars.DATA_NO <= 25:
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
                    if global_vars.PREDICT is False:
                        global_vars.PREDICT = temp_values['predict']
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
                    delete_done.set()
                    if global_vars.PREDICT and len(global_vars.TEMPERATURE_VALS)==25:
                        np.savetxt('data.csv', [p for p in zip(global_vars.TEMPERATURE_VALS, global_vars.PRESSURE_VALS,global_vars.HUMIDITY_VALS, global_vars.PM2_point_5_VALS,global_vars.PM10_VALS,global_vars.O3_VALS,global_vars.SO2_VALS,global_vars.CO_VALS,global_vars.CO2_VALS,global_vars.NHX_VALS)], delimiter=',', fmt='%s', header=','.join(["Temperature","Pressure" ,"Humidity", "PM2.5", "PM10", "O3","SO2","CO","CO2","NHx"]))
                        model_in = open('test_model2.pkl', 'rb')
                        model = pickle.load(model_in)
                        series = read_csv('data.csv', header=0)
                        values = series.values
                        data = series_to_supervised(values, 9)
                        df = DataFrame(data)
                        print(df)
                        pred_result = model.predict(df.iloc[[0]])
                        print(pred_result)
                        ls_result = pred_result.tolist()
                        # Update age and favorite color
                        doc_ref.update({
                            u'temperature': ls_result[0][0],
                            u'pressure': ls_result[0][1],
                            u'humidity': ls_result[0][2],
                            u'PM2_5': ls_result[0][3],
                            u'PM10': ls_result[0][4],
                            u'O3': ls_result[0][5],
                            u'SO2': ls_result[0][6],
                            u'CO': ls_result[0][7],
                            u'CO2': ls_result[0][8],
                            u'NHx': ls_result[0][9],
                            u'predict': False
                        })
                        global_vars.TEMPERATURE_VALS = []
                        global_vars.HUMIDITY_VALS = []
                        global_vars.PRESSURE_VALS = []
                        global_vars.CO_VALS = []
                        global_vars.CO2_VALS = []
                        global_vars.NHX_VALS = []
                        global_vars.SO2_VALS = []
                        global_vars.O3_VALS = []
                        global_vars.PM2_point_5_VALS = []
                        global_vars.PM10_VALS = []
                        
                else:   
                    global_vars.DATA_NO = 0
                    global_vars.TEMPERATURE_VALS = []
                    global_vars.HUMIDITY_VALS = []
                    global_vars.PRESSURE_VALS = []
                    global_vars.CO_VALS = []
                    global_vars.CO2_VALS = []
                    global_vars.NHX_VALS = []
                    global_vars.SO2_VALS = []
                    global_vars.O3_VALS = []
                    global_vars.PM2_point_5_VALS = []
                    global_vars.PM10_VALS = []
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

    




