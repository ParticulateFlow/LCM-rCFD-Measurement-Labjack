// creating empty arrays for sensor data
var start_time = null
var x_time = []
var y_Twarm = []
var y_Tcold = []
var y_Tout = []
var y_h35 = []
var y_h65 = []
var y_h95 = []
var y_h125 = []
var y_h155 = []
var y_h185 = []
var y_h215 = []
var plotDat = []
var shapes =  []
var stirrer_rpm	= 30
// variables for autoranging
var range_min
var range_max

// variable for starting and stopping interval handler
let intervalID
const interval_ms = 1000 // 1 second
var start_block = 0
var curr_bypass = null
// constant for data endpoint
const data_url = "http://140.78.134.203:5000/data"

plotLayout = {
    title: "Messdaten",
    xaxis: {
        title: "Time in s",
        rangemode: "tozero"
    },
    yaxis: {
        range: [20, 40],
        title: "Temperature in °C",
        position: 0
    }
}

function updateLayout(){
    // plotLayout = {
    //     title: "Messdaten",
    //     xaxis: {
    //         title: "Time in s",
    //         rangemode: "tozero"
    //     },
    //     yaxis: {
    //         range: [20, 40],
    //         title: "Temperature in C°",
    //         position: 0
    //     },
    //     shapes: shapes
    // }
    plotLayout.shapes = shapes
    plotLayout.yaxis.range = [range_min-5,range_max+5]
}
// variables for HTML elements
div_plot = document.getElementById("plot");
// --- measurement
toggle_recording = document.getElementById("t_recording")
button_reset = document.getElementById("b_reset")
// --- stirrer
slider_stirrer = document.getElementById("rpm_stirrer")
div_stirrer = document.getElementById("div_stirrer")
toggle_stirrer = document.getElementById("t_stirrer")
// --- massflow div's
div_massflow_cold = document.getElementById("div_mass_cold")
div_massflow_warm = document.getElementById("div_mass_warm")

// UI element handler
div_stirrer.innerHTML = stirrer_rpm // set init value
toggle_recording.onchange = function(){
    var type
    if(this.checked){
        type = "start"
    }else{
        type = "stop"
    }
    recording(type)
}
toggle_stirrer.onchange = function(){
    var type
    if(this.checked){
        type = "start"
    }else{
        type = "stop"
    }
    stirrer_startStop(type)
}
button_reset.onclick = function () {
    x_time = []
    y_Twarm = []
    y_Tcold = []
    y_Tout = []
    y_h35 = []
    y_h65 = []
    y_h95 = []
    y_h125 = []
    y_h155 = []
    y_h185 = []
    y_h215 = []
    shapes = []
    updateLayout()
    curr_bypass = null
    start_time = null
    renderPlot()
}
slider_stirrer.onchange = function () {
    stirrer_rpm = this.value
    div_stirrer.innerHTML = stirrer_rpm
    stirrer_update(stirrer_rpm)

}
// general functions
function loadData() {
    getData()
    renderPlot()
}
function renderPlot() {
    // create traces for the plot
    var trace_Twarm = {
        x: x_time,
        y: y_Twarm,
        type: "scatter",
        name: "Twarm",
        line: {
            color: "#FF0000", //red
            width: 3
        },
        yaxis: "y1"

    };
    var trace_Tcold = {
        x: x_time,
        y: y_Tcold,
        type: "scatter",
        name: "Tcold",
        line: {
            color: "#0000FF", //blue
            width: 3
        }
    };
    var trace_Tout = {
        x: x_time,
        y: y_Tout,
        type: "scatter",
        name: "Tout",
        line: {
            color: "#000000", //black
            width: 3
        }
    };
    var trace_h35 = {
        x: x_time,
        y: y_h35,
        type: "scatter",
        name: "h=35mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h65 = {
        x: x_time,
        y: y_h65,
        type: "scatter",
        name: "h=65mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h95 = {
        x: x_time,
        y: y_h95,
        type: "scatter",
        name: "h=95mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h125 = {
        x: x_time,
        y: y_h125,
        type: "scatter",
        name: "h=125mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h155 = {
        x: x_time,
        y: y_h155,
        type: "scatter",
        name: "h=155mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h185 = {
        x: x_time,
        y: y_h185,
        type: "scatter",
        name: "h=185mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var trace_h215 = {
        x: x_time,
        y: y_h215,
        type: "scatter",
        name: "h=215mm",
        line: {
            // color: "#FF0000", //red
            width: 1
        }
    };
    var rect1 = {
        name:"warm bypass",
        type: "rect",
        xref: "x",
        yref: "paper",
        x0: 0,
        y0: 0,
        x1: 3,
        y1: 1,
        fillcolor: "#639fff",
        opacity: 0.2,
        line:{
            width: 0
        }
    };
    // add traces to Array
    plotDat = [
        trace_Twarm,
        trace_Tcold,
        trace_Tout,
        trace_h215,
        trace_h185,
        trace_h155,
        trace_h125,
        trace_h95,
        trace_h65,
        trace_h35
    ]
    Plotly.newPlot(div_plot, plotDat, plotLayout) //create plot with trace array and layout
}
function drawRectangle(bypass){
    if (bypass =="cold"){
        colorcode = "#6ec0ff"
    }else{
        colorcode = "#c23000"
    }
    var rect = {
        name:"bypass",
        type: "rect",
        xref: "x",
        yref: "paper",
        x0: start_block,
        y0: 0,
        x1: start_block,
        y1: 1,
        fillcolor: colorcode,
        opacity: 0.2,
        line:{
            width: 0
        }
    }
    shapes.push(rect)
}
function updateRectangle(time){
    shapes[shapes.length-1].x1 = time
}
async function getData() {
    // fetch json data
    const response = await fetch(data_url)
    const data = await response.json()
    // add json data to corresponding array
    var time = 0
    if (start_time == null) {
        start_time = Date.parse(data.timestamp)
        x_time.push(time)
    } else {
        time = (Date.parse(data.timestamp) - start_time) / 1000
        x_time.push(time)
    }
    y_Twarm.push(data.Twarm)
    y_Tcold.push(data.Tcold)
    y_Tout.push(data.Tout)
    y_h35.push(data.h35mm)
    y_h65.push(data.h65mm)
    y_h95.push(data.h95mm)
    y_h125.push(data.h125mm)
    y_h155.push(data.h155mm)
    y_h185.push(data.h185mm)
    y_h215.push(data.h215mm)
    div_massflow_cold.innerHTML = data.coldMassflow
    div_massflow_warm.innerHTML = data.warmMassflow
    var bypass = data.bypass
    if (curr_bypass == null){
        start_block = time
        
        drawRectangle(bypass)
        updateLayout()
        curr_bypass = bypass
    }else if (curr_bypass != bypass){
        start_block = time
        updateRectangle(time)
        drawRectangle(bypass)
        updateLayout()
        curr_bypass = bypass
        
    }else{
        updateRectangle(time)
        updateLayout()
    }
    data_list = [
        data.Twarm, 
        data.Tcold, 
        data.Tout, 
        data.h35mm, 
        data.h65mm, 
        data.h95mm, 
        data.h125mm, 
        data.h155mm, 
        data.h185mm, 
        data.h215mm
    ]
    if (max(data_list) > range_max || min(data_list) < range_min){
        range_max = max(data_list)
        range_min = min(data_list)
        updateLayout()
    }
}
// control functions
async function stirrer_startStop(type){
    var obj = {}
    obj["type"] = type  // start/stop
    jsonString = JSON.stringify(obj)
    const response = await fetch("/stirrer_startStop",{
        method: "POST",
        body: jsonString,
        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    const data = await response.json()
    if(!data.status){
        alert("something went wrong")
    }
}

async function stirrer_update(rpm){
    var obj = {}
    obj["rpm"] = rpm
    jsonString = JSON.stringify(obj)
    const response = await fetch("/stirrer_update",{
        method: "POST",
        body: jsonString,
        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    const data = await response.json()
    if(!data.status){
        alert("something went wrong")
    }
}
async function recording(type){
    var obj = {}
    obj["type"] = type  // start/stop
    jsonString = JSON.stringify(obj)
    const response = await fetch("/recording",{
        method: "POST",
        body: jsonString,
        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    const data = await response.json()
    if(!data.status){
        alert("something went wrong")
    }
}
// page load function
window.onload = function(){
    toggle_recording.checked = false
    toggle_stirrer.checked = false
    loadData()
    intervalID = setInterval(loadData,interval_ms)
}