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
// var y_Mwarm = []
// var y_Mcold = []
// var cnt = 0 //temporary for Timestamp
var stirrer_rpm	= 0

// variable for starting and stopping interval handler
let intervalID
const interval_ms = 1000 // 1 second

// constant for data endpoint
const data_url = "/data"

plotLayout = {
    title: 'Messdaten',
    xaxis: {
        title: 'Time in s',
        rangemode: "tozero",
        domain: [0.1, 1]
    },
    yaxis: {
        range: [20, 40],
        title: 'Temperature in C°',
        position: 0
    },
    // yaxis2: {
    //     range: [0, 200],
    //     title: 'Massflow in l/hr',
    //     overlaying: "y",
    //     side: "left",
    //     position: 0.07,
    //     anchor: "free"
    // }


}
// variables for HTML elements
plotDiv = document.getElementById('plot');
// --- measurement
button_start = document.getElementById('b_start')
button_stop = document.getElementById('b_stop')
button_reset = document.getElementById('b_reset')
// --- stirrer
button_start_stirrer = document.getElementById('b_start_stirrer')
button_stop_stirrer = document.getElementById('b_stop_stirrer')
slider_stirrer = document.getElementById('stirrer_rpm')
status_stirrer = document.getElementById('stirrer_status')

// UI element functions
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
    status_stirrer.innerHTML = stirrer_rpm

}
button_start_stirrer.onclick = function () {
    //TODO
}
button_stop_stirrer.onclick = function () {
    //TODO
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
        type: 'scatter',
        name: 'Twarm',
        line: {
            color: '#FF0000' //red
        },
        yaxis: "y1"

    };
    var trace_Tcold = {
        x: x_time,
        y: y_Tcold,
        type: 'scatter',
        name: 'Tcold',
        line: {
            color: '#0000FF' //blue
        }
    };
    var trace_Tout = {
        x: x_time,
        y: y_Tout,
        type: 'scatter',
        name: 'Tout',
        line: {
            color: '#800080' //purple
        }
    };
    var trace_h35 = {
        x: x_time,
        y: y_h35,
        type: 'scatter',
        name: 'h=35mm'
    };
    var trace_h65 = {
        x: x_time,
        y: y_h65,
        type: 'scatter',
        name: 'h=65mm'
    };
    var trace_h95 = {
        x: x_time,
        y: y_h95,
        type: 'scatter',
        name: 'h=95mm'
    };
    var trace_h125 = {
        x: x_time,
        y: y_h125,
        type: 'scatter',
        name: 'h=125mm'
    };
    var trace_h155 = {
        x: x_time,
        y: y_h155,
        type: 'scatter',
        name: 'h=35mm'
    };
    var trace_h185 = {
        x: x_time,
        y: y_h185,
        type: 'scatter',
        name: 'h=185mm'
    };
    var trace_h215 = {
        x: x_time,
        y: y_h215,
        type: 'scatter',
        name: 'h=215mm'
    };
    // var trace_Mwarm = {
    //     x: x_time,
    //     y: y_Mwarm,
    //     type: 'scatter',
    //     name: 'warmMassflow',
    //     yaxis: "y2"
    // };
    // var trace_Mcold = {
    //     x: x_time,
    //     y: y_Mcold,
    //     type: 'scatter',
    //     name: 'coldMassflow',
    //     yaxis: "y2"
    // };
    // add traces to Array
    var plotDat = [
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
    Plotly.newPlot(plotDiv, plotDat, plotLayout) //create plot with trace array and layout
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
        x_time.push((Date.parse(data.timestamp) - start_time) / 1000)
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
    // y_Mwarm.push(data.warmMassflow)
}

async function startStirrer(){
    
}

renderPlot()