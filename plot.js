

// plot.js

function plotModule1(t, response, title, yLabel = "Output") {
    const trace = {
        x: t,
        y: response,
        type: "scatter",
        mode: "lines",
        name: "Response"
    };

    Plotly.newPlot("graph1", [trace], {
        title,
        xaxis: { title: "Time (s)" },
        yaxis: { title: yLabel },
        margin: { t: 45, r: 20, b: 50, l: 55 },
        responsive: true
    });
}

function plotModule1Error(t, error) {
    Plotly.newPlot("graph1_error", [{
        x: t,
        y: error,
        type: "scatter",
        mode: "lines",
        name: "Error fraction"
    }], {
        title: "Error Fraction vs Time",
        xaxis: { title: "Time (s)" },
        yaxis: { title: "Error Fraction", type: "log" },
        margin: { t: 45, r: 20, b: 50, l: 55 },
        responsive: true
    });
}

function plotModule2Time(t, input, output) {
    Plotly.newPlot("graph2_time", [
        {
            x: t,
            y: input,
            type: "scatter",
            mode: "lines",
            name: "Input"
        },
        {
            x: t,
            y: output,
            type: "scatter",
            mode: "lines",
            name: "Output"
        }
    ], {
        title: "Input and Output Signals",
        xaxis: { title: "Time (s)" },
        yaxis: { title: "Amplitude" },
        margin: { t: 45, r: 20, b: 50, l: 55 },
        responsive: true
    });
}

function plotModule2Bode(frequencies, magnitude, phase) {
    const traces = [
        {
            x: frequencies,
            y: magnitude,
            type: "scatter",
            mode: "lines",
            name: "Magnitude"
        },
        {
            x: frequencies,
            y: phase,
            type: "scatter",
            mode: "lines",
            name: "Phase",
            yaxis: "y2"
        }
    ];

    Plotly.newPlot("graph2_bode", traces, {
        title: "Bode Plot",
        xaxis: {
            title: "Frequency (Hz)",
            type: "log"
        },
        yaxis: {
            title: "Magnitude Ratio"
        },
        yaxis2: {
            title: "Phase (degrees)",
            overlaying: "y",
            side: "right"
        },
        margin: { t: 45, r: 60, b: 50, l: 60 },
        responsive: true
    });
}
