from labjack import ljm
from sensors import rCFD_Sensors
from stirrer import IKA_Ministar40
import json 
from flask import Flask, render_template, request

DEVICE = "T7"
CONNECTION = "USB" # USB or ETHERNET
configFile = 'labjack.yml'

try:
    labjack = ljm.openS(DEVICE, CONNECTION, "ANY")
    print(f"Connected to {DEVICE} via {CONNECTION}")
except:
    print(f'Failure - could not connected to {DEVICE}')
    exit()

try:
    rCFD = rCFD_Sensors(device=labjack,configFile=configFile)
    print('All sensors initialized')
except:
    print('Could not initialize Sensors')

try:
    stirrer = IKA_Ministar40(usbName = 'USB', speedLimit=120)
    print(f"{stirrer.device} connected")
except:
    print("Could not connect to stirrer")

app = Flask(__name__)
@app.route('/data')
def data():
    return json.dumps(rCFD.data)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-stirrer')
def startStirrer():
    stirrer.start()
    status = True
    # TODO starting function in stirrer file 'start()->boolean'
    return json.dumps({'status': status})

@app.route('/update-stirrer', methods = ['POST'])
def updateStirrer():
    response = request.get_json()
    rpm = int(response['rpm'])
    stirrer.set_ratedSpeed(rpm)
    status = True
    # TODO: rpm update function in stirrer file 'set_rpm(rpm)->boolean'
    return json.dumps({'status': status, 'rpm':rpm})

@app.route('/stop-stirrer')
def stopStirrer():
    # TODO stopping function in stirrer file 'stop()->boolean'
    stirrer.stop()
    status = True
    return json.dumps({'status': status})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')