from labjack import ljm
from sensors import rCFD_Sensors
import  functions.stirrer as stirrer
import json 
from flask import Flask, render_template, request

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
def startStirrer():
    status = True
    # TODO starting function in stirrer file 'start()->boolean'
    return json.dumps({'status': status})

@app.route('/update-stirrer', methods = ['POST'])
def startStirrer():
    response = request.get_json()
    rpm = int(response['rpm'])
    status = True
    # TODO: rpm update function in stirrer file 'set_rpm(rpm)->boolean'
    return json.dumps({'status': status, 'rpm':rpm})

@app.route('/stop-stirrer')
def stopStirrer():
    # TODO stopping function in stirrer file 'stop()->boolean'
    status = True
    return json.dumps({'status': status})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')