import '@kitware/vtk.js/Rendering/Profiles/Geometry'
import '@kitware/vtk.js/Rendering/Profiles/Glyph'

import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow'

import vtkActor           from '@kitware/vtk.js/Rendering/Core/Actor'
import vtkMapper          from '@kitware/vtk.js/Rendering/Core/Mapper'
import vtkGlyph3DMapper from '@kitware/vtk.js/Rendering/Core/Glyph3DMapper'
import vtkSphereSource from '@kitware/vtk.js/Filters/Sources/SphereSource'
import vtkPolyData from '@kitware/vtk.js/Common/DataModel/PolyData'
import vtkPoints from '@kitware/vtk.js/Common/Core/Points'
import vtkDataArray from '@kitware/vtk.js/Common/Core/DataArray'
import vtkColorTransferFunction from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps'
import vtkScalarBarActor from '@kitware/vtk.js/Rendering/Core/ScalarBarActor'
import vtkSTLReader from '@kitware/vtk.js/IO/Geometry/STLReader'
import { getArray } from '@kitware/vtk.js/macros'


const controlPanel = `
<div style = 'font-weight:bold'>Model: </div>
<table>
    <tr>
        <td>
            <div>Opacity: </div>
            <input id="opacity_model" type="range" min="0" max="1" step ="0.1" value=".3" />
        </td>
    </tr>
    <tr>
        <td>
            <div>Visibility: </div>
            <input id="visibility_model" type="checkbox" checked/>
        </td>
    </tr>
</table>
<div style = 'font-weight:bold'>Sensors: </div>
<table>
    <tr>
        <td>
            <div>Opacity: </div>
            <input id="opacity_sensors" type="range" min="0" max="1" step ="0.1" value="1"/>
        </td>
    </tr>
    <tr>
        <td>
            <div>Visibility: </div>
            <input id="visibility_sensors" type="checkbox" checked/>
        </td>
    </tr>
</table>
<div style = 'font-weight:bold'>Simulation: </div>
<table>
    <tr>
        <td>
            <div>Opacity: </div>
            <input id="opacity_simulation" type="range" min="0" max="1" step ="0.1" value="1"/>
        </td>
    </tr>
    <tr>
        <td>
            <div>Visibility: </div>
            <input id="visibility_simulation" type="checkbox" checked/>
        </td>
    </tr>
</table>

`

// ----------------------------------------------------------------------------
// Constants
// ----------------------------------------------------------------------------
const refreshRate = 5000 // ms
const sensors = {
    location : [
        [0,100,35],//h35mm ...
        [0,100,65],
        [0,100,95],
        [0,100,125],
        [0,100,155],
        [0,100,185],
        [0,100,215],
        [100,0,0],//Twarm
        [-100,0,100],//Tcold
        [100,0,200]//Tout
    ],
    scalar : {
        name : "temperature",
        values : [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]
    }
}
var simulationLocation = [[0,0,0]]
var simulationValues = [0]

// sensors
const sensorDataUrl = "/data"
var sensorPoints = vtkPoints.newInstance()
const sensorPolydata = vtkPolyData.newInstance()
const sensorSphereSource = vtkSphereSource.newInstance({radius:5})
var sensorGlyph = vtkGlyph3DMapper.newInstance()
const sensorActor = vtkActor.newInstance()
const sensorScalars = vtkDataArray.newInstance({size : sensors.scalar.values.length})
// simulation
const simulationDataUrl = "/simulation"
var simulationPoints = vtkPoints.newInstance()
var simulationPolydata = vtkPolyData.newInstance()
const simulationSphereSource = vtkSphereSource.newInstance({radius:2})
var simulationGlyph = vtkGlyph3DMapper.newInstance()
const simulationActor = vtkActor.newInstance()
var simulationScalars = vtkDataArray.newInstance({size : 1})

// model
const modelReader = vtkSTLReader.newInstance()
const modelMapper = vtkMapper.newInstance()
const modelActor = vtkActor.newInstance()

// ----------------------------------------------------------------------------
// misc variables
// ----------------------------------------------------------------------------
var interval
var t = 20
// ----------------------------------------------------------------------------
// Standard rendering code setup
// ----------------------------------------------------------------------------

const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance()
const renderer = fullScreenRenderer.getRenderer()
const renderWindow = fullScreenRenderer.getRenderWindow()

// ----------------------------------------------------------------------------
// VTK
// ----------------------------------------------------------------------------
// LUT init
vtkColorMaps.addPreset(
    {
		ColorSpace: "RGB",
		Name: "Rainbow",
		NanColor: [
			1,
			1,
			0
		],
		RGBPoints: [
            0,
            0,
            0,
            1,
            0.5,
            0,
            1,
            0,
            1,
            1,
            0,
            0
		]
	}
)
const preset = vtkColorMaps.getPresetByName("Rainbow")
const lut = vtkColorTransferFunction.newInstance()
lut.applyColorMap(preset)
lut.setMappingRange(20,80)
lut.updateRange()
// Scalar bar
const scalarBarActor = vtkScalarBarActor.newInstance()
scalarBarActor.setScalarsToColors(lut)
scalarBarActor.setAxisLabel("Temperature in C  ")
scalarBarActor.setDrawNanAnnotation(false)


// Sensors init
for(const p in sensors.location){
    // console.log(sensors.location[p][2])
    sensorPoints.insertNextPoint(sensors.location[p][0],sensors.location[p][1],sensors.location[p][2])
}
sensorPolydata.setPoints(sensorPoints)
for(var i = 0 ; i < sensors.scalar.values.length ; i++){
    sensorScalars.insertTuple(i,[sensors.scalar.values[i]])
}
sensorScalars.setName(sensors.scalar.name)
sensorPolydata.getPointData().setScalars(sensorScalars)
sensorGlyph.setScaleMode(false)
sensorGlyph.addInputData(sensorPolydata)
sensorGlyph.addInputConnection(sensorSphereSource.getOutputPort(),1)
sensorGlyph.setLookupTable(lut)
sensorGlyph.setScalarRange(20,80)
sensorGlyph.setColorModeToDefault()
sensorActor.setMapper(sensorGlyph)

// model init
await modelReader.setUrl('static/data/model.stl')
modelMapper.setInputConnection(modelReader.getOutputPort())
modelActor.setMapper(modelMapper)
modelMapper.setScalarVisibility(false)
modelActor.getProperty().setOpacity(0.3)
modelActor.getProperty().setColor(0.3,0.3,0.3)

// Simulation init
for(const p in simulationLocation){
    // console.log(sensors.location[p][2])
    simulationPoints.insertNextPoint(simulationLocation[p][0],simulationLocation[p][1],simulationLocation[p][2])
}
simulationPolydata.setPoints(simulationPoints)
for(var i = 0 ; i < simulationValues ; i++){
    simulationScalars.insertTuple(i,[simulationValues[i]])
}
simulationScalars.setName("Temperature")
simulationPolydata.getPointData().setScalars(simulationScalars)
simulationGlyph.setScaleMode(false)
simulationGlyph.addInputData(simulationPolydata)
simulationGlyph.addInputConnection(simulationSphereSource.getOutputPort(),1)
simulationGlyph.setLookupTable(lut)
simulationGlyph.setScalarRange(20,80)
simulationGlyph.setColorModeToDefault()
simulationActor.setMapper(simulationGlyph)


// -----------------------------------------------------------
// adding views
// -----------------------------------------------------------

renderer.addActor(sensorActor)
renderer.addActor(simulationActor)
renderer.addActor(modelActor)
renderer.addActor(scalarBarActor)
renderer.resetCamera()
renderWindow.render()

// -----------------------------------------------------------
// UI control handling
// -----------------------------------------------------------
fullScreenRenderer.addController(controlPanel)
const opacityModel = document.querySelector('#opacity_model')
const opacitySensors = document.querySelector('#opacity_sensors')
const opacitySimulation = document.querySelector('#opacity_simulation')
const visibilityModel = document.querySelector('#visibility_model')
const visibilitySensors = document.querySelector('#visibility_sensors')
const visibilitySimulation = document.querySelector('#visibility_simulation')

opacityModel.addEventListener('change',(e)=>{
    const opacity = Number(e.target.value)
    modelActor.getProperty().setOpacity(opacity)
    renderWindow.render()
})
opacitySensors.addEventListener('change',(e)=>{
    const opacity = Number(e.target.value)
    sensorActor.getProperty().setOpacity(opacity)
    renderWindow.render()
})
opacitySimulation.addEventListener('change',(e)=>{
    const opacity = Number(e.target.value)
    simulationActor.getProperty().setOpacity(opacity)
    renderWindow.render()
})
visibilityModel.addEventListener('change',(e)=>{
    modelActor.setVisibility(e.target.checked)
    renderWindow.render()
})
visibilitySensors.addEventListener('change',(e)=>{
    sensorActor.setVisibility(e.target.checked)
    renderWindow.render()
})
visibilitySimulation.addEventListener('change',(e)=>{
    simulationActor.setVisibility(e.target.checked)
    renderWindow.render()
})


// -----------------------------------------------------------
// Functions
// -----------------------------------------------------------
async function refresh(){
    // sensor
    await updateSensorData()
    sensorPolydata.getPointData().removeAllArrays()
    // sensorPolydata.setPoints(sensorPoints)
    for(var i = 0 ; i < sensors.scalar.values.length ; i++){
        sensorScalars.insertTuple(i,[sensors.scalar.values[i]])
    }
    sensorPolydata.getPointData().setScalars(sensorScalars)  
    sensorGlyph = vtkGlyph3DMapper.newInstance()
    sensorGlyph.setScaleMode(false)
    sensorGlyph.addInputData(sensorPolydata)
    sensorGlyph.addInputConnection(sensorSphereSource.getOutputPort(),1)
    sensorGlyph.setLookupTable(lut)
    sensorGlyph.setScalarRange(20,80)
    sensorGlyph.setColorModeToDefault()
    sensorActor.setMapper(sensorGlyph)
    // simulation
    await updateSimulation()
    var simulationPoints = vtkPoints.newInstance()
    var simulationPolydata = vtkPolyData.newInstance()
    var simulationGlyph = vtkGlyph3DMapper.newInstance()
    var simulationScalars = vtkDataArray.newInstance({size : simulationValues.length})
    for(const p in simulationLocation){
        simulationPoints.insertNextPoint(simulationLocation[p][0],simulationLocation[p][1],simulationLocation[p][2])
    }
    simulationPolydata.setPoints(simulationPoints)
    for(var i = 0 ; i < simulationValues.length ; i++){
        simulationScalars.insertTuple(i,[simulationValues[i]])
    }
    simulationScalars.setName("Temperature")
    simulationPolydata.getPointData().setScalars(simulationScalars)
    simulationGlyph.setScaleMode(false)
    simulationGlyph.addInputData(simulationPolydata)
    simulationGlyph.addInputConnection(simulationSphereSource.getOutputPort(),1)
    simulationGlyph.setLookupTable(lut)
    simulationGlyph.setScalarRange(20,80)
    simulationGlyph.setColorModeToDefault()
    simulationActor.setMapper(simulationGlyph)
    renderWindow.render()
}
async function updateSensorData(){
    const response = await fetch(sensorDataUrl)
    const data = await response.json()
    sensors.scalar.values[0] = data.h35mm
    sensors.scalar.values[1] = data.h65mm
    sensors.scalar.values[2] = data.h95mm
    sensors.scalar.values[3] = data.h125mm
    sensors.scalar.values[4] = data.h155mm
    sensors.scalar.values[5] = data.h185mm
    sensors.scalar.values[6] = data.h215mm
    sensors.scalar.values[7] = data.Twarm
    sensors.scalar.values[8] = data.Tcold
    sensors.scalar.values[9] = data.Tout
}
async function updateSimulation(){
    const response = await fetch(simulationDataUrl)
    const data = await response.json()
    simulationLocation = data.location
    simulationValues = data.values
}



// -----------------------------------------------------------
// Boilerplate
// -----------------------------------------------------------

interval = setInterval(refresh,refreshRate)
window.onload = refresh()

