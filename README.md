# rCFD Webservice
Scripts for providing the rCFD Measurement Data as an API. For the data aquisition a Labjack T7Pro is used. For fast and uncomplex aquisition all sensors retrieve analog signals, which are linear equal to the physical value.

## Webservice

## Visualisation

### Setup
+ installl npm
+ install packages from "package.json"
+ install python packages from "requirements.txt"

### Workflow for JS changes
+ change VTK code in "static/src/index.js"
+ on Linux:
  +  run build.sh
+ on Windows:
  +  run "npm run build"
  +  copy "static/dist/main.js" to "static/js/main.js"
+ run main.py


