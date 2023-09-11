from labjack import ljm
from sensors import rCFD_Sensors
import json
from flask import Flask

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
@app.route('/')
def index():
    return json.dumps(rCFD.data)
app.run(port=5000, host='0.0.0.0')