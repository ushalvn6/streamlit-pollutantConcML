import threading
import global_vars
from google.cloud import firestore


# prints the newly obtained values
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

# calculates CO subindex based on it's current value
def calcCOIndex (var):
    if var < 4.4:
        return var * 11.3636
    elif var <= 9.4:
        return 10 * (var - 4.5) + 51
    elif var <= 12.4:
        return 16.8965 * (var - 9.5) + 101
    elif var <= 15.4:
        return 16.8965 * (var - 12.5) + 151
    elif var <= 30.4:
        return 6.6443 * (var - 15.5) + 201
    elif var <= 40.4:
        return 10 * (var - 30.5) + 301
    elif var <= 50.4:
        return 10 * (var - 40.5) + 401
    else:
        return 0

# calculates O3 subindex based on it's current value
def calcO3Index (var):
    var = var / 1000
    if var < 0.059:
        return var * 847.4576
    elif var <= 0.075:
        return 3266.6667 * (var - 0.060) + 51
    elif var <= 0.164:
        return 1256.4103 * (var - 0.125) + 101
    elif var <= 0.204:
        return 1256.4103 * (var - 0.165) + 151
    elif var <= 0.404:
        return 497.4874 * (var - 0.205) + 201
    elif var <= 0.504:
        return 1000 * (var - 0.405) + 301
    elif var <= 0.604:
        return 1000 * (var - 0.505) + 401
    else:
        return 0

# calculates SO2 subindex based on it's current value
def calcSO2Index (var):
    if var < 0.035:
        return var * 1428.5714
    elif var <= 0.075:
        return 1256.4103 * (var - 0.036) + 51
    elif var <= 0.185:
        return 449.5413 * (var - 0.076) + 101
    elif var <= 0.304:
        return 415.2542 * (var - 0.186) + 151
    elif var <= 0.604:
        return 331.1037 * (var - 0.305) + 201
    elif var <= 0.804:
        return 497.4874 * (var - 0.605) + 301
    elif var <= 1.004:
        return 497.4874 * (var - 0.805) + 401
    else:
        return 0

# calculates PM2.5 subindex based on it's current value
def calcPM25Index (var):
    if var < 12:
        return 4.1667 * var
    elif var <= 35.4:
        return 2.1030 * (var - 12.1) + 51
    elif var <= 55.4:
        return 2.4623 * (var - 35.5) + 101
    elif var <= 150.4:
        return 0.5163 * (var - 55.5) + 151
    elif var <= 250.4:
        return 0.9909 * (var - 150.5) + 201
    elif var <= 350.4:
        return 0.9909 * (var - 250.5) + 301
    elif var <= 500.4:
        return 0.6604 * (var - 350.5) + 401
    else:
        return 0

# calculates PM10 subindex based on it's current value
def calcPM10Index (var):
    if var < 54:
        return var * 0.9259
    elif var <= 154:
        return 0.4949 * (var - 55) + 51
    elif var <= 254:
        return 0.4949 * (var - 155) + 101
    elif var <= 354:
        return 0.4949 * (var - 255) + 151
    elif var <= 424:
        return 1.4348 * (var - 355) + 201
    elif var <= 504:
        return 1.2532 * (var - 425) + 301
    elif var <= 604:
        return 1 * (var - 505) + 401
    else:
        return 0

# calculates and returns the AQI
def calcAQI (co, o3, so2, pm2_5, pm10):
    coIndex = calcCOIndex(co)
    o3Index = calcO3Index(o3)
    so2Index = calcSO2Index (so2)
    pm2_5index = calcPM25Index (pm2_5)
    pm10index = calcPM10Index (pm10)
    global_vars.PREVIOUS_AQI = global_vars.CURRENT_AQI
    global_vars.CURRENT_AQI = max(coIndex, o3Index, so2Index, pm2_5index, pm10index)

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
                calcAQI(temp_values["CO"], temp_values["O3"],  temp_values["SO2"], temp_values["PM2_5"], temp_values["PM10"])   # calculate AQI
                # attach the new values to the end of the list
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
                
                        
    db = firestore.Client.from_service_account_json("firestore-key.json")   # accesses the firestore

    # Create a reference to the Google post.
    doc_ref = db.collection("sensor_params").document("output_parameters")

    # Then get the data at that reference.
    doc = doc_ref.get()
    
    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)      
    

    # Initial readings
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
    print("The contents are: ", initial_values)
   
    


class DataReader:
    # runs the get_data method as a background method
    data_read = threading.Thread(target = get_data, daemon=True)
    data_read.start()

    




