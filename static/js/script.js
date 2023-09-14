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
// var y_Mwarm = []
// var y_Mcold = []
// var cnt = 0 //temporary for Timestamp
var stirrer_rpm	= 0

// variable for starting and stopping interval handler
let intervalID
const interval_ms = 1000 // 1 second
var start_block = null
var end_block = null
var curr_bypass = null

// constant for data endpoint
const data_url = "/data"

plotLayout = {
    title: "Messdaten",
    xaxis: {
        title: "Time in s",
        rangemode: "tozero"
    },
    yaxis: {
        range: [20, 40],
        title: "Temperature in C°",
        position: 0
    },
    // yaxis2: {
    //     range: [0, 200],
    //     title: "Massflow in l/hr",
    //     overlaying: "y",
    //     side: "left",
    //     position: 0.07,
    //     anchor: "free"
    // }

}
// variables for HTML elements
div_plot = document.getElementById("plot");
// --- measurement
button_start = document.getElementById("b_start")
button_stop = document.getElementById("b_stop")
button_reset = document.getElementById("b_reset")
// --- stirrer
button_start_stirrer = document.getElementById("b_start_stirrer")
button_update_stirrer = document.getElementById("b_update_stirrer")
button_stop_stirrer = document.getElementById("b_stop_stirrer")
slider_stirrer = document.getElementById("rpm_stirrer")
div_stirrer = document.getElementById("div_stirrer")

// --- massflow div's
div_massflow_cold = document.getElementById("div_mass_cold")
div_massflow_warm = document.getElementById("div_mass_warm")


// UI element handler
button_start.onclick = function () {
    if (!intervalID) {
        loadData()
        intervalID = setInterval(loadData, interval_ms)
    }
}
button_stop.onclick = function () {
    clearInterval(intervalID)
    intervalID = null
}
button_reset.onclick = function () {
    if (intervalID) {
        clearInterval(intervalID)
    }
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
    // y_Mwarm = []
    // y_Mcold = []

    start_time = null
    renderPlot()
}
slider_stirrer.onchange = function () {
    stirrer_rpm = this.value
    div_stirrer.innerHTML = stirrer_rpm

}
button_start_stirrer.onclick = function () {
    startStirrer()
}
button_update_stirrer.onclick = function () {
    updateStirrer()
}
button_stop_stirrer.onclick = function () {
    stopStirrer()
}

// GENERAL FUNCTIONS
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
    // var trace_Mwarm = {
    //     x: x_time,
    //     y: y_Mwarm,
    //     type: "scatter",
    //     name: "warmMassflow",
    //     yaxis: "y2"
    // };
    // var trace_Mcold = {
    //     x: x_time,
    //     y: y_Mcold,
    //     type: "scatter",
    //     name: "coldMassflow",
    //     yaxis: "y2"
    // };
    // add traces to Array
    plotDat = [
        trace_Twarm,
        trace_Tcold,
        trace_Tout,
        trace_h35,
        trace_h65,
        trace_h95,
        trace_h125,
        trace_h155,
        trace_h185,
        trace_h215,
        // trace_Mwarm,
        // trace_Mcold
    ]
    Plotly.newPlot(div_plot, plotDat, plotLayout) //create plot with trace array and layout
}
function drawRectangle(){
    var rect = {
        type: "rect",
        xref: "x",
        yref: "paper",
        x0: start_block,
        y0: 0,
        x1: end_block,
        y1: 1,
        fillcolor: "#639fff",
        opacity: 0.2,
        line:{
            width: 0
        }
    }
    plotDat.push(rect)
}

async function getData() {
    // fetch json data
    const response = await fetch(data_url)
    const data = await response.json()
    // add json data to corresponding array
    if (start_time == null) {
        start_time = Date.parse(data.timestamp)
        x_time.push(0)
    } else {
        var time = (Date.parse(data.timestamp) - start_time) / 1000
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
    // y_Mcold.push(data.coldMassflow)
    div_massflow_cold.innerHTML = data.coldMassflow
    // y_Mwarm.push(data.warmMassflow)
    div_massflow_warm.innerHTML = data.warmMassflow
    if (curr_bypass != data.bypass){
        if(curr_bypass == "warm"){
            start_block = time
        }else{
            end_block = time
            drawRectangle()
        }
        curr_bypass = data.bypasss
    }
}

// stirrer functions

async function updateStirrer(){
    var obj = {}
    obj["rpm"] = stirrer_rpm
    jsonString = JSON.stringify(obj)
    console.log(jsonString)
    const response = await fetch("/update-stirrer",{
        method: "POST",
        body: jsonString,
        headers:{
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    const data = await response.json()
    console.log(data.rpm)
}
async function startStirrer(){
    const response = await fetch("/start-stirrer")
    const data = await response.json()
    if(!data.status){
        alert("something went wrong")
    }
}
async function stopStirrer(){
    const response = await fetch("/stop-stirrer")
    const data = await response.json()
    if(!data.status){
        alert("something went wrong")
    }
}

// renders plot on load
renderPlot()