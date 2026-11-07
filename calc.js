
let pyodide;
let pythonReady;

async function initializePython() {
  pyodide = await loadPyodide();

  const response = await fetch("./calculations.py");
  if (!response.ok) {
    throw new Error("Could not load calculations.py");
  }

  const pythonCode = await response.text();
  await pyodide.runPythonAsync(pythonCode);

  console.log("Python calculations loaded successfully.");
  return true;
}

pythonReady = initializePython();

async function callPython(functionName, ...args) {
  await pythonReady;

  const pyArgs = args
    .map(value => JSON.stringify(value))
    .join(", ");

  const result = await pyodide.runPythonAsync(
    `${functionName}(${pyArgs})`
  );

  return result.toJs
    ? result.toJs({ dict_converter: Object.fromEntries })
    : result;
}

window.pythonCalc = {
  stepResponse: (K, tau, t, A = 1) =>
    callPython("calculate_step_response", K, tau, t, A),

  rampResponse: (K, tau, t, A = 1) =>
    callPython("calculate_ramp_response", K, tau, t, A),

  importantPoints: (K, tau, A = 1) =>
    callPython("calculate_important_points", K, tau, A),

  rampLag: tau =>
    callPython("calculate_ramp_lag", tau),

  steadyStateError: (K, tau, A = 1) =>
    callPython("calculate_steady_state_error", K, tau, A),

  errorFraction: (tau, t) =>
    callPython("calculate_error_fraction", tau, t),

  amplitudeRatio: (omega, tau) =>
    callPython("calculate_amplitude_ratio", omega, tau),

  phaseLag: (omega, tau) =>
    callPython("calculate_phase_lag", omega, tau),

  outputAmplitude: (tau, omega, A = 1) =>
    callPython("calculate_output_amplitude", tau, omega, A),

  cutoffFrequency: tau =>
    callPython("calculate_cutoff_frequency", tau),

  dynamicError: (tau, omega) =>
    callPython("calculate_dynamic_error", tau, omega)
};

