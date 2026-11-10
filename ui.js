// ============================================================
// ui.js — connects the sliders, buttons and the validation
// table to the math (calc.js) and the plots (plot.js).
// ============================================================

function $(id) {
  return document.getElementById(id);
}

function setOutput(id, value) {
  const el = $(id);
  if (el) el.textContent = value;
}

function setResult(id, value, pass) {
  const mine = $(id);
  const res = $(id.replace("_mine", "_res"));
  if (mine) mine.textContent = value;
  if (res) {
    res.textContent = pass ? "PASS ✓" : "FAIL ✗";
    res.style.color = pass ? "#2ca02c" : "#d62728";
    res.style.fontWeight = "bold";
  }
}

// ============================================================
// Module 1
// ============================================================

function updateModule1() {
  const K = parseFloat($("k").value);
  const tau = parseFloat($("tau").value);
  const inputType = document.querySelector('input[name="input"]:checked').value;

  setOutput("k_out", fmt(K, 1));
  setOutput("tau_out", fmt(tau, 1));

  plotModule1(K, tau, inputType);
  plotErrorFraction(tau);

  // values panel
  const A = 1.0;
  const yTau = K * A * (1 - Math.exp(-1));
  const y3Tau = K * A * (1 - Math.exp(-3));
  setOutput("val_tau", `${fmt(yTau)} = 63.2% of KA (at t = ${fmt(tau, 1)} s)`);
  setOutput("val_3tau", `${fmt(y3Tau)} = 95% of KA (at t = ${fmt(3 * tau, 1)} s)`);
  setOutput("val_lag", `${fmt(rampLag(tau), 1)} s`);
  setOutput("val_ess", fmt(steadyStateError(K, tau, A)));
}

// ============================================================
// Module 2
// ============================================================

function updateModule2() {
  const tau = parseFloat($("tau2").value);
  const omega = parseFloat($("w2").value);

  setOutput("tau2_out", fmt(tau, 1));
  setOutput("w2_out", fmt(omega, 1));

  const M = amplitudeRatio(omega, tau);
  const phi = phaseLagDeg(omega, tau);

  plotModule2Time(tau, omega);
  plotModule2Bode(tau);

  setOutput("val_M", fmt(M, 3));
  setOutput("val_phase", `${fmt(phi, 1)}°`);
  setOutput("val_cutoff", `${fmt(cutoffFrequency(tau), 3)} rad/s`);
  setOutput("val_delta", fmt(dynamicError(omega, tau), 3));
}

function updateDynamicErrorCalculator() {
  const f = parseFloat($("calc_f").value);
  const errPct = parseFloat($("calc_err").value);
  const fPhase = parseFloat($("calc_fphase").value);

  if (!(f > 0) || !(errPct > 0) || !(fPhase > 0)) return;
  const tauMax = maxTauForError(f, errPct / 100);
  setOutput("calc_taumax", `${fmt(tauMax * 1000, 2)} ms (${fmt(tauMax * 1e6, 0)} µs)`);
  setOutput("calc_phase", `${fmt(Math.abs(phaseLagAtFrequencyHz(tauMax, fPhase)), 1)}° at ${fmt(fPhase, 1)} Hz (with τ = τmax)`);
}

// ============================================================
// Module 3
// ============================================================

function updateModule3() {
  const m = parseFloat($("m3").value);
  const b = parseFloat($("b3").value);
  const k = parseFloat($("k3").value);

  setOutput("m3_out", fmt(m, 1));
  setOutput("b3_out", fmt(b, 1));
  setOutput("k3_out", fmt(k, 1));

  const zeta = b / (2 * Math.sqrt(k * m));
  const wn = Math.sqrt(k / m);
  const K = 1; // unity gain: F is a unit step force

  const metrics = plotModule3Step(K, zeta, wn);
  plotModule3Phase(K, zeta, wn);

  const poles = polesOfSecondOrder(zeta, wn);
  const eig = eigenvaluesOfA(m, b, k);
  plotModule3SPlane(poles, eig);

  setOutput("val_zeta", `${fmt(zeta, 3)} (${dampingType(zeta)})`);
  setOutput("val_wn", `${fmt(wn, 3)} rad/s`);
  setOutput("val_rise", metrics.rise === null ? "–" : `${fmt(metrics.rise)} s`);
  setOutput("val_peak", metrics.peakTime === null ? "– (no overshoot)" : `${fmt(metrics.peakTime)} s`);
  setOutput("val_os", `${fmt(metrics.overshoot, 1)}%`);
  setOutput("val_settle", `${fmt(metrics.settling)} s (2% band)`);

  // state-space panel: A = [[0,1],[-k/m,-b/m]], B = [[0],[1/m]], C = [1 0]
  setOutput("ss_a21", fmt(-k / m, 3));
  setOutput("ss_a22", fmt(-b / m, 3));
  setOutput("ss_b2", fmt(1 / m, 3));
  setOutput("ss_eig1", eigenToString(eig[0]));
  setOutput("ss_eig2", eigenToString(eig[1]));
  setOutput("ss_pole1", eigenToString(poles[0]));
  setOutput("ss_pole2", eigenToString(poles[1]));
}

// ============================================================
// Module 4: guess the sensor
// ============================================================

const game4 = {
  sensor: null,
  response: null,
  revealed: false,
  sessionScore: 0,
};

function newSensor4() {
  game4.sensor = randomSensor();
  game4.response = sensorResponse(game4.sensor);
  game4.revealed = false;

  $("result4").hidden = true;
  $("btn_submit").disabled = false;
  const s = game4.sensor;
  $("sensor_info").textContent =
    s.order === 1
      ? `A FIRST-ORDER sensor, ${s.inputType} input${s.inputType === "sine" ? ` (ω = ${fmt(s.sineOmega, 2)} rad/s)` : ""}. Estimate τ.`
      : "A SECOND-ORDER sensor, step input. Estimate ζ and ωn.";

  plotModule4(game4.sensor, game4.response, false);
}

function submitGuess4() {
  if (game4.revealed || !game4.sensor) return;
  const s = game4.sensor;
  let correct = 0, needed = 0, details = [];

  if (s.order === 1) {
    needed = 1;
    const g = parseFloat($("guess_tau").value);
    const ok = withinTenPercent(g, s.tau);
    if (ok) correct++;
    details.push(`τ: you said ${fmt(g, 2)}, true ${fmt(s.tau, 2)} ${ok ? "✓" : "✗"}`);
  } else {
    needed = 2;
    const gz = parseFloat($("guess_zeta").value);
    const gw = parseFloat($("guess_wn").value);
    const okZ = withinTenPercent(gz, s.zeta);
    const okW = withinTenPercent(gw, s.wn);
    if (okZ) correct++;
    if (okW) correct++;
    details.push(`ζ: you said ${fmt(gz, 2)}, true ${fmt(s.zeta, 2)} ${okZ ? "✓" : "✗"}`);
    details.push(`ωn: you said ${fmt(gw, 2)}, true ${fmt(s.wn, 2)} ${okW ? "✓" : "✗"} rad/s`);
  }

  game4.revealed = true;
  game4.sessionScore += correct;

  $("true_tau").textContent = s.order === 1 ? `${fmt(s.tau, 2)} s (K = ${fmt(s.K, 2)})` : "not used this round";
  $("true_zeta").textContent = s.order === 2 ? fmt(s.zeta, 2) : "not used this round";
  $("true_wn").textContent = s.order === 2 ? `${fmt(s.wn, 2)} rad/s` : "not used this round";
  $("score_round").textContent = `${correct} of ${needed} within 10% — ${details.join("; ")}`;
  $("score_total").textContent = game4.sessionScore;

  $("result4").hidden = false;
  $("btn_submit").disabled = true;
  plotModule4(game4.sensor, game4.response, true);
}

// ============================================================
// Validation checks (section 3.2 of the homework)
// ============================================================

function runValidation() {
  const K = 1, A = 1;

  // 1. first-order step: y(tau) = 0.632 KA and y(3tau) = 0.95 KA
  const yTau = K * A * (1 - Math.exp(-1));
  const y3Tau = K * A * (1 - Math.exp(-3));
  setResult("v1_mine",
    `y(τ) = ${fmt(yTau, 3)}, y(3τ) = ${fmt(y3Tau, 3)}`,
    Math.abs(yTau - 0.632) < 0.001 && Math.abs(y3Tau - 0.95) < 0.001);

  // 2. tau = 0.2 s, input sin 2t: M = 0.93, lag 21.8°
  const M2 = amplitudeRatio(2, 0.2);
  const phi2 = Math.abs(phaseLagDeg(2, 0.2));
  setResult("v2_mine",
    `M = ${fmt(M2, 3)}, lag = ${fmt(phi2, 1)}°`,
    Math.abs(M2 - 0.93) < 0.005 && Math.abs(phi2 - 21.8) < 0.15);

  // 3. 100 Hz with at most 5% error: tauMax ≈ 0.52 ms, 9.3° at 50 Hz
  const tauMax = maxTauForError(100, 0.05);
  const phi50 = Math.abs(phaseLagAtFrequencyHz(tauMax, 50));
  setResult("v3_mine",
    `τmax = ${fmt(tauMax * 1000, 3)} ms, lag at 50 Hz = ${fmt(phi50, 1)}°`,
    Math.abs(tauMax * 1000 - 0.52) < 0.01 && Math.abs(phi50 - 9.3) < 0.15);

  // 4. zeta = 0.5: overshoot 16.3%
  const os5 = overshootPercent(0.5);
  setResult("v4_mine", `overshoot = ${fmt(os5, 1)}%`, Math.abs(os5 - 16.3) < 0.1);

  // 5. zeta = 1: no overshoot
  const os1 = overshootPercent(1);
  setResult("v5_mine", `overshoot = ${fmt(os1, 1)}%`, os1 === 0);

  // 6. state space m=1, b=2, k=4: eigenvalues -1 ± j1.732 = poles
  const eig = eigenvaluesOfA(1, 2, 4);
  setResult("v6_mine",
    `${eigenToString(eig[0])}, ${eigenToString(eig[1])}`,
    Math.abs(eig[0].re + 1) < 1e-9 && Math.abs(Math.abs(eig[0].im) - Math.sqrt(3)) < 1e-9);
}

// ============================================================
// wire everything up
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  // Module 1
  ["k", "tau"].forEach((id) => $(id).addEventListener("input", updateModule1));
  document.querySelectorAll('input[name="input"]').forEach((r) =>
    r.addEventListener("change", updateModule1)
  );

  // Module 2
  ["tau2", "w2"].forEach((id) => $(id).addEventListener("input", updateModule2));
  ["calc_f", "calc_err", "calc_fphase"].forEach((id) =>
    $(id).addEventListener("input", updateDynamicErrorCalculator)
  );

  // Module 3
  ["m3", "b3", "k3"].forEach((id) => $(id).addEventListener("input", updateModule3));

  // Module 4
  $("btn_submit").addEventListener("click", submitGuess4);
  $("btn_new").addEventListener("click", newSensor4);

  // initial draw
  updateModule1();
  updateModule2();
  updateDynamicErrorCalculator();
  updateModule3();
  runValidation();
  newSensor4();
});
