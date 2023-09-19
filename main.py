from labjack import ljm
from sensors import rCFD_Sensors
from stirrer import IKA_Ministar40
import json 
from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
from time import sleep
import threading
import csv

DEVICE = "T7"
CONNECTION = "USB" # USB or ETHERNET
CONFIGFILE = 'labjack.yml'
PATHTOSAVE = r'\\pfm-daten\scratch\LCM-Demonstrator\Michael\themes\4_experiments\202309xx_ByPass_2Pumps_Webserver'

try:
    labjack = ljm.openS(DEVICE, CONNECTION, "ANY")
    print(f"Connected to {DEVICE} via {CONNECTION}")
except:
    print(f'Failure - could not connected to {DEVICE}')
    exit()

try:
    rCFD = rCFD_Sensors(device=labjack,configFile=CONFIGFILE)
    print('All sensors initialized')
except:
    print('Could not initialize Sensors')

try:
    stirrer = IKA_Ministar40(usbName = 'USB', speedLimit=120)
    print(f"Stirrer {stirrer.deviceName} connected")
except:
    print("Could not connect to stirrer")

# Global parameters for stirrer
stirrerStatus = 'OFF'
stirrerRPM = 30

HEADER = list()
DATA_SAVING = list()
# thread for saving data
def thread_saveData():
    global HEADER, DATA_SAVING
    while True:
        d = rCFD.data
        d["stirrerStatus"] = stirrerStatus
        d["stirrerRPM"] = stirrerRPM
        DATA_SAVING.append(list(d.values()))
        HEADER = list(d.keys())
        sleep(1)

thread = threading.Thread(target=thread_saveData, daemon=True)
thread.start()

app = Flask(__name__)
@app.route('/data')
def data():
    return json.dumps(rCFD.data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stirrer_startStop', methods = ['POST'])
def startStopStirrer():
    global stirrerStatus
    response = request.get_json()
    t_stirr = response['type']
    if t_stirr == 'start':
        stirrer.start()
        stirrer.set_ratedSpeed(stirrerRPM)
        stirrerStatus = 'ON'
    elif t_stirr == 'stop':
        stirrer.stop()
        stirrerStatus = 'OFF'
    status = True
    return json.dumps({'status': status})

@app.route('/stirrer_update', methods = ['POST'])
def updateStirrer():
    global stirrerRPM
    response = request.get_json()
    stirrerRPM = int(response['rpm'])
    stirrer.set_ratedSpeed(stirrerRPM)
    status = True
    return json.dumps({'status': status, 'rpm':stirrerRPM})

@app.route('/recording', methods = ['POST'])
def updateRecording():
    response = request.get_json()
    t_rec = response['type']
    global DATA_SAVING, HEADER
    if t_rec == 'start':
        # start saving -> clear DATA
        DATA_SAVING = []
        #print("Start saving")
    elif t_rec == 'stop':
        # create folder and save DATA
        dirname = datetime.now().strftime('%Y%m%d_%H%M%S') + '_Experiment'
        dirPath = Path(PATHTOSAVE, dirname)
        dirPath.mkdir(parents=True, exist_ok=True)
        filename = str(dirPath / 'data.csv')
        with open(filename, 'a', newline = '') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(HEADER)
            csvwriter.writerows(DATA_SAVING) 
        DATA_SAVING = []
        #print(f"Session saved to {dirname}")
    status = True
    return json.dumps({'status': status})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')