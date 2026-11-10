// ============================================================
// plot.js — every Plotly drawing of the toolkit.
// Each function takes the numbers from calc.js and redraws one
// graph. All layouts are saved in PLOT_LAYOUT so the plots
// resize with the page and look the same.
// ============================================================

const PLOT_CONFIG = { responsive: true, displayModeBar: false };

const AXIS_STYLE = {
  gridcolor: "rgba(128,128,128,0.25)",
  zerolinecolor: "rgba(128,128,128,0.5)",
};

// ---------- Module 1: step or ramp response ----------

function plotModule1(K, tau, inputType) {
  const tEnd = Math.max(6 * tau, 5);
  const t = linspace(0, tEnd, 600);
  const A = 1.0;
  const finalValue = K * A;

  const traces = [];
  if (inputType === "step") {
    const y = stepResponse(K, tau, t, A);
    traces.push({
      x: t, y: y, mode: "lines", name: "Output y(t)",
      line: { color: "#1f77b4", width: 3 },
    });
    // dashed final value
    traces.push({
      x: [0, tEnd], y: [finalValue, finalValue], mode: "lines",
      name: "Final value KA", line: { color: "gray", dash: "dash", width: 1.5 },
    });
    // markers at tau (63.2%) and 3tau (95%)
    const yTau = K * A * (1 - Math.exp(-1));
    const y3Tau = K * A * (1 - Math.exp(-3));
    traces.push({
      x: [tau, 3 * tau], y: [yTau, y3Tau], mode: "markers",
      name: "63.2% at τ, 95% at 3τ",
      marker: { color: ["#d62728", "#2ca02c"], size: 10, symbol: "circle" },
    });
    traces.push({
      x: [tau, tau], y: [0, yTau], mode: "lines", showlegend: false,
      line: { color: "#d62728", dash: "dot", width: 1.5 },
    });
    traces.push({
      x: [3 * tau, 3 * tau], y: [0, y3Tau], mode: "lines", showlegend: false,
      line: { color: "#2ca02c", dash: "dot", width: 1.5 },
    });
  } else {
    // ramp: input (dashed) vs output, plus the lag
    const input = t.map((tv) => K * A * tv);
    const y = rampResponse(K, tau, t, A);
    traces.push({
      x: t, y: input, mode: "lines", name: "Input x(t) = A·t",
      line: { color: "gray", dash: "dash", width: 2 },
    });
    traces.push({
      x: t, y: y, mode: "lines", name: "Output y(t)",
      line: { color: "#1f77b4", width: 3 },
    });
    // the constant vertical gap = steady-state error K*A*tau
    const tGap = tEnd * 0.75;
    const yAtGap = K * A * (tGap - tau + tau * Math.exp(-tGap / tau));
    traces.push({
      x: [tGap, tGap], y: [yAtGap, K * A * tGap], mode: "lines",
      name: "Steady-state error = K·A·τ",
      line: { color: "#d62728", width: 4 },
    });
  }

  Plotly.react("graph1", traces, {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title: inputType === "step" ? "Step response" : "Ramp response",
    xaxis: { title: "Time (s)", ...AXIS_STYLE },
    yaxis: { title: inputType === "step" ? "y(t)" : "Amplitude", ...AXIS_STYLE },
  }, PLOT_CONFIG);
}

// ---------- Module 1: error fraction on a log axis ----------

function plotErrorFraction(tau) {
  const t = linspace(0, 6 * tau, 500);
  const ef = errorFraction(tau, t);
  const marks = [1, 3, 5].map((m) => m * tau);
  const vals = marks.map((tm) => Math.exp(-tm / tau));

  Plotly.react("graph1_error", [
    {
      x: t, y: ef, mode: "lines", name: "e(t)/e(0) = e^(−t/τ)",
      line: { color: "#1f77b4", width: 3 },
    },
    {
      x: marks, y: vals, mode: "markers", name: "t = τ, 3τ, 5τ",
      marker: { color: "#d62728", size: 10 },
    },
  ], {
    margin: { t: 40, r: 20, b: 45, l: 70 },
    title: "Error fraction (log scale) — a straight line with slope −1/τ",
    xaxis: { title: "Time (s)", ...AXIS_STYLE },
    yaxis: { title: "Error fraction", type: "log", ...AXIS_STYLE },
  }, PLOT_CONFIG);
}

// ---------- Module 2: input and output sines ----------

function plotModule2Time(tau, omega) {
  const { t, input, output, M } = sineSignals(tau, omega);
  Plotly.react("graph2_time", [
    {
      x: t, y: input, mode: "lines", name: "Input x(t)",
      line: { color: "gray", width: 2 },
    },
    {
      x: t, y: output, mode: "lines", name: "Output y(t)",
      line: { color: "#1f77b4", width: 3 },
    },
  ], {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title: `Input and output sines (amplitude ratio M = ${fmt(M, 3)})`,
    xaxis: { title: "Time (s)", ...AXIS_STYLE },
    yaxis: { title: "Amplitude", ...AXIS_STYLE },
  }, PLOT_CONFIG);
}

// ---------- Module 2: Bode plot (magnitude + phase) ----------

function plotModule2Bode(tau) {
  const omega = linspace(-3, 3, 400).map((e) => Math.pow(10, e)); // 1e-3 .. 1e3
  const M = omega.map((w) => amplitudeRatio(w, tau));
  const phase = omega.map((w) => phaseLagDeg(w, tau));
  const wc = cutoffFrequency(tau);

  Plotly.react("graph2_bode", [
    {
      x: omega, y: M.map((m) => 20 * Math.log10(m)), mode: "lines",
      name: "Magnitude (dB)", line: { color: "#1f77b4", width: 3 },
    },
    {
      x: omega, y: phase, mode: "lines", name: "Phase (°)", yaxis: "y2",
      line: { color: "#d62728", width: 3, dash: "dash" },
    },
    {
      x: [wc, wc], y: [-3, -3], mode: "markers", name: "Cutoff ω = 1/τ (−3 dB)",
      marker: { color: "#2ca02c", size: 10, symbol: "x" },
    },
  ], {
    margin: { t: 40, r: 55, b: 45, l: 60 },
    title: "Bode plot — cutoff at ω = 1/τ",
    xaxis: { title: "ω (rad/s)", type: "log", ...AXIS_STYLE },
    yaxis: { title: "20·log₁₀(M) (dB)", ...AXIS_STYLE },
    yaxis2: {
      title: "Phase (°)", overlaying: "y", side: "right",
      gridcolor: "rgba(0,0,0,0)", ...AXIS_STYLE,
    },
    legend: { orientation: "h", y: -0.25 },
  }, PLOT_CONFIG);
}

// ---------- Module 3: step response with metrics ----------

function plotModule3Step(K, zeta, wn) {
  const metrics = stepMetrics(K, zeta, wn);
  const t = metrics.tArr;
  const y = metrics.yArr;
  const traces = [
    {
      x: t, y: y, mode: "lines", name: "Step response",
      line: { color: "#1f77b4", width: 3 },
    },
    {
      x: [t[0], t[t.length - 1]], y: [metrics.final, metrics.final],
      mode: "lines", name: "Final value K",
      line: { color: "gray", dash: "dash", width: 1.5 },
    },
  ];
  if (metrics.peakTime !== null) {
    traces.push({
      x: [metrics.peakTime], y: [metrics.tPeakValue], mode: "markers",
      name: "Peak", marker: { color: "#d62728", size: 10 },
    });
  }
  traces.push({
    x: [metrics.settling, metrics.settling], y: [0, metrics.final * 1.1],
    mode: "lines", name: "Settling time (2% band)",
    line: { color: "#2ca02c", dash: "dot", width: 2 },
  });

  Plotly.react("graph3_step", traces, {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title: `Step response — ${dampingType(zeta)} (ζ = ${fmt(zeta, 2)})`,
    xaxis: { title: "Time (s)", ...AXIS_STYLE },
    yaxis: { title: "y(t)", ...AXIS_STYLE },
  }, PLOT_CONFIG);
  return metrics;
}

// ---------- Module 3: poles in the s-plane (+ eigenvalues of A) ----------

function plotModule3SPlane(poles, eig) {
  const traces = [
    {
      x: poles.map((p) => p.re), y: poles.map((p) => p.im), mode: "markers",
      name: "Poles of G(s)", marker: { color: "#d62728", size: 13, symbol: "x" },
    },
    {
      x: eig.map((p) => p.re), y: eig.map((p) => p.im), mode: "markers",
      name: "Eigenvalues of A (hollow circles — same numbers)",
      marker: { color: "#1f77b4", size: 13, symbol: "circle-open" },
    },
  ];
  const maxAbs = Math.max(
    0.5,
    ...poles.map((p) => Math.max(Math.abs(p.re), Math.abs(p.im))),
    ...eig.map((p) => Math.max(Math.abs(p.re), Math.abs(p.im)))
  );
  const lim = maxAbs * 1.3;
  const minRe = Math.min(...poles.map((p) => p.re), ...eig.map((p) => p.re), 0);
  const maxRe = Math.max(...poles.map((p) => p.re), ...eig.map((p) => p.re), 0);

  Plotly.react("graph3_splane", traces, {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title: "s-plane: poles = eigenvalues of A",
    xaxis: { title: "Re(s)", range: [minRe - 0.3 * maxAbs, maxRe + 0.3 * maxAbs], ...AXIS_STYLE },
    yaxis: { title: "Im(s)", range: [-lim, lim], ...AXIS_STYLE },
  }, PLOT_CONFIG);
}

// ---------- Module 3: phase plane (x1 vs x2 during the step) ----------

function plotModule3Phase(K, zeta, wn) {
  // dense closed-form solution, then x2 = velocity by finite difference
  const t = linspace(0, 12 / (zeta * wn), 2500);
  const x1 = secondOrderStep(K, zeta, wn, t);
  const x2 = [0];
  for (let i = 1; i < t.length; i++) {
    x2.push((x1[i] - x1[i - 1]) / (t[i] - t[i - 1]));
  }
  Plotly.react("graph3_phase", [
    {
      x: x1, y: x2, mode: "lines", name: "(x₁, x₂) path",
      line: { color: "#9467bd", width: 2.5 },
    },
    {
      x: [x1[0]], y: [x2[0]], mode: "markers", name: "start",
      marker: { color: "#2ca02c", size: 10 },
    },
    {
      x: [x1[x1.length - 1]], y: [0], mode: "markers", name: "end (rest)",
      marker: { color: "#d62728", size: 10 },
    },
  ], {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title: `Phase plane — ${zeta < 1 ? "spiral (underdamped)" : "no spiral (ζ ≥ 1)"}`,
    xaxis: { title: "x₁ = displacement", ...AXIS_STYLE },
    yaxis: { title: "x₂ = velocity", ...AXIS_STYLE },
  }, PLOT_CONFIG);
}

// ---------- Module 4: hidden sensor + reveal overlay ----------

function plotModule4(sensor, response, reveal) {
  const traces = [
    {
      x: response.t, y: response.y, mode: "lines", name: "Measured response (noisy)",
      line: { color: "#1f77b4", width: 2 },
    },
  ];
  if (response.input !== null) {
    traces.push({
      x: response.t, y: response.input, mode: "lines", name: "Input",
      line: { color: "gray", dash: "dash", width: 1.5 },
    });
  }
  if (reveal) {
    const truth = sensorTrueCurve(sensor);
    traces.push({
      x: truth.t, y: truth.y, mode: "lines", name: "True curve",
      line: { color: "#d62728", dash: "dash", width: 2.5 },
    });
  }
  Plotly.react("graph4", traces, {
    margin: { t: 40, r: 20, b: 45, l: 55 },
    title:
      sensor.order === 1
        ? `Hidden sensor — first order, ${sensor.inputType} input`
        : "Hidden sensor — second order, step input",
    xaxis: { title: "Time (s)", ...AXIS_STYLE },
    yaxis: { title: "y(t)", ...AXIS_STYLE },
  }, PLOT_CONFIG);
}
