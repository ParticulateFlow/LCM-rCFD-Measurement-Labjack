from labjack import ljm
from sensors import rCFD_Sensors
import json
from flask import Flask

DEVICE = "T7"
CONNECTION = "ETHERNET" # USB or ETHERNET
configFile = 'labjack.yml'

try:
    rCFD = rCFD_Sensors(
        device=ljm.openS(DEVICE, CONNECTION, "ANY"),
        configFile=configFile)
    print(f"Connected to {DEVICE} via {CONNECTION}")
except:
    print(f'Failure - could not connected to {DEVICE}')


app = Flask(__name__)
@app.route('/')
def index():
    return json.dumps(rCFD.data)
app.run()