# rCFD Webservice
Scripts for providing the rCFD Measurement Data as an API. For the data aquisition a [Labjack T7Pro](https://labjack.com/products/labjack-t7-pro) is used.
For fast and simple aquisition all sensors retrieve analog signals, which depend linearly on the physical properties.

## Webservice

## Visualisation

### Installation
+ install `nodejs` and `npm` (Node.js package manager)
```bash
$ apt install nodejs npm
```
+ install packages from `static/package.json`
```bash
$ npm install
```
+ install python packages from `requirements.txt`
```bash
$ pip install -r requirements.txt
```
### Workflow for JS changes
+ change VTK code in `static/src/index.js`
+ on Linux:
  +  execute `build.sh`
+ on Windows:
  +  execute `npm run build`
  +  copy `static/dist/main.js` to `static/js/main.js`
+ execute `main.py`


