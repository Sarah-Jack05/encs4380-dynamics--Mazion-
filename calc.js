
// calc.js
let pyodide = null;
let pythonReady = null;

// Initialize Python and load calculations.py
async function initializePython() {
    if (pythonReady) return pythonReady;

    pythonReady = (async () => {
        pyodide = await loadPyodide();

        // NumPy is required by calculations.py
        await pyodide.loadPackage("numpy");

        const response = await fetch("./calculations.py");
        if (!response.ok) {
            throw new Error("Could not load calculations.py");
        }

        const pythonCode = await response.text();
        await pyodide.runPythonAsync(pythonCode);

        // Convert NumPy arrays and values into JSON-safe results
        await pyodide.runPythonAsync(`
import json
import numpy as np

def _json_call(function_name, args_json):
    args = json.loads(args_json)
    result = globals()[function_name](*args)

    def convert(value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, (tuple, list)):
            return [convert(item) for item in value]
        return value

    return json.dumps(convert(result))
`);

        console.log("Python calculations are ready.");
        return pyodide;
    })();

    return pythonReady;
}

// Run a Python function and return a normal JavaScript value
async function callPython(functionName, args = []) {
    await initializePython();

    const result = await pyodide.runPythonAsync(
        `_json_call(${JSON.stringify(functionName)}, ${JSON.stringify(JSON.stringify(args))})`
    );

    return JSON.parse(result);
}

// MODULE 1
async function calcStepResponse(K, tau, t, A = 1) {
    return callPython("calculate_step_response", [K, tau, t, A]);
}

async function calcRampResponse(K, tau, t, A = 1) {
    return callPython("calculate_ramp_response", [K, tau, t, A]);
}

async function calcImportantPoints(K, tau, A = 1) {
    return callPython("calculate_important_points", [K, tau, A]);
}

async function calcRampLag(tau) {
    return callPython("calculate_ramp_lag", [tau]);
}

async function calcSteadyStateError(K, tau, A = 1) {
    return callPython("calculate_steady_state_error", [K, tau, A]);
}

async function calcErrorFraction(tau, t) {
    return callPython("calculate_error_fraction", [tau, t]);
}

// MODULE 2
async function calcAmplitudeRatio(omega, tau) {
    return callPython("calculate_amplitude_ratio", [omega, tau]);
}

async function calcPhaseLag(omega, tau) {
    return callPython("calculate_phase_lag", [omega, tau]);
}

async function calcOutputAmplitude(tau, omega, A = 1) {
    return callPython("calculate_output_amplitude", [tau, omega, A]);
}

async function calcCutoffFrequency(tau) {
    return callPython("calculate_cutoff_frequency", [tau]);
}

async function calcDynamicError(tau, omega) {
    return callPython("calculate_dynamic_error", [tau, omega]);
}

// Compatibility aliases for the existing interface
async function calcFrequency(tau, omega) {
    const [M, phase, cutoff] = await Promise.all([
        calcAmplitudeRatio(omega, tau),
        calcPhaseLag(omega, tau),
        calcCutoffFrequency(tau)
    ]);

    return { M, phase, cutoff };
}
