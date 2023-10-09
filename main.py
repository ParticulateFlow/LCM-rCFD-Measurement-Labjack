from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
from time import sleep
import threading
import json 
import csv

from rCFDdevices import rCFD_Experiment
rCFD = rCFD_Experiment()


#PATHTOSAVE = r'\\pfm-daten\scratch\LCM-Demonstrator\Michael\themes\4_experiments\202309xx_ByPass_2Pumps_Webserver'
PATHTOSAVE = r'C:\Users\weiss\Downloads'
print("+ Path to save")
print(PATHTOSAVE)

print(f"{'FLASK':-^40}")
SAVEFLAG = False
def thread_saveData():
    ''' thread for saving data '''
    
    global SAVEFLAG
    while True:
        sleep(0.2)
        if not SAVEFLAG:
            imgIndex = 0
            newsession = True
            continue

        if newsession:
            # create folders
            dir = datetime.now().strftime('%Y%m%d_%H%M%S') + '_Experiment'
            csvDir = Path(PATHTOSAVE, dir)
            imgDir = Path(csvDir, "images")

            print(f"Session data saved to {csvDir}")
            csvDir.mkdir(parents=True, exist_ok=True)
            csvFilename = str(csvDir / 'data.csv')

            imgDir.mkdir(parents=True, exist_ok=True)

        # Save everything
        data = rCFD.data
        with open(csvFilename, 'a', newline = '') as file:
            csvwriter = csv.writer(file)
            if newsession: 
                csvwriter.writerow(rCFD.header)
                newsession = False
            csvwriter.writerow(data.values())
        imgFilename = Path(f'{imgIndex}.jpg')
        imgFilename = str(imgDir / imgFilename)
        rCFD.saveFrame(filename=imgFilename)
        imgIndex += 1


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
    response = request.get_json()
    state = response['type']

    if state == 'start': rCFD.stirrer_start(rpm=int(response['rpm']))
    elif state == 'stop': rCFD.stirrer_stop()

    return json.dumps({'status': True})

@app.route('/stirrer_update', methods = ['POST'])
def updateStirrer():
    response = request.get_json()
    rCFD.stirrer_update(rpm=int(response['rpm']))
    return json.dumps({'status': True})

@app.route('/recording', methods = ['POST'])
def updateRecording():
    response = request.get_json()
    t_rec = response['type']
    global SAVEFLAG
    if t_rec == 'start': SAVEFLAG = True
    elif t_rec == 'stop': SAVEFLAG = False

    return json.dumps({'status': True})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')