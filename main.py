from labjack import ljm
from sensors import rCFD_Sensors
import json 
from flask import Flask, render_template

DEVICE = "T7"
CONNECTION = "USB" # USB or ETHERNET
configFile = 'labjack.yml'

try:
    labjack = ljm.openS(DEVICE, CONNECTION, "ANY")
    print(f"Connected to {DEVICE} via {CONNECTION}")
    rCFD = rCFD_Sensors(device=labjack,configFile=configFile)
    print('All sensors initialized')
except:
    print(f'Failure - could not connected to {DEVICE}')
    exit()


app = Flask(__name__)
@app.route('/data')
def data():
    return json.dumps(rCFD.data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-stirrer')
def startStirrer(rpm:int):
    
    return "started at {} rpm".format(rpm)

@app.route('/stop-stirrer')
def stopStirrer():

    return "stopped"

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')