// Everything is inside (function () { ... })(); so our names stay private.
// Without it, two files that both declare "const $" crash the page.
(function () {
  // ===== helpers =====
  const $ = (id) => document.getElementById(id);

  // number to short text: 0.63200 -> 0.632, missing or NaN -> "–"
  function fmt(x, digits = 3) {
    return Number.isFinite(x) ? Number(x.toFixed(digits)) : "–";
  }

  // {re: -1, im: 1.732} -> "-1 + j1.732"
  function fmtComplex(z) {
    if (!z) return "–";
    const re = fmt(z.re);
    if (Math.abs(z.im) < 1e-9) return String(re);
    return re + (z.im < 0 ? " − j" : " + j") + fmt(Math.abs(z.im));
  }

  // calls a function from calc.js or plot.js IF it exists yet.
  // So the page keeps working while Persons 2 and 3 are still writing.
  const warned = {};
  function call(name, ...args) {
    const fn = window[name];
    if (typeof fn !== "function") {
      if (!warned[name]) {
        console.warn(name + " is not ready yet");
        warned[name] = true;
      }
      return null;
    }
    return fn(...args);
  }

  // attach the same function to many elements
  function on(ids, event, fn) {
    ids.forEach((id) => $(id).addEventListener(event, fn));
  }

  // ===== MODULE 1 =====
  function update1() {
    const K = Number($("k").value);
    const tau = Number($("tau").value);
    const type = document.querySelector('input[name="input"]:checked').value;

    $("k_out").textContent = K;
    $("tau_out").textContent = tau;

    const data = call("calcFirstOrder", K, tau, type);
    if (!data) return;

    $("val_tau").textContent = fmt(data.yTau);
    $("val_3tau").textContent = fmt(data.y3Tau);
    $("val_lag").textContent = fmt(data.lag) + " s";
    $("val_ess").textContent = fmt(data.ess);
    call("plotModule1", data, { K, tau, type });
  }

  // ===== MODULE 2 =====
  function update2() {
    const tau = Number($("tau2").value);
    const w = Number($("w2").value);

    $("tau2_out").textContent = tau;
    $("w2_out").textContent = w;

    const data = call("calcFrequency", tau, w);
    if (!data) return;

    $("val_M").textContent = fmt(data.M);
    $("val_phase").textContent = fmt(data.phaseDeg, 1) + "°";
    $("val_cutoff").textContent = fmt(data.cutoff) + " rad/s";
    $("val_delta").textContent = fmt(data.delta);
    call("plotModule2", data, { tau, w });
  }

  // dynamic-error calculator (numbers typed by the user)
  function updateCalc() {
    const f = Number($("calc_f").value);
    const err = Number($("calc_err").value);
    const fPhase = Number($("calc_fphase").value);

    const r = call("calcDynamicError", f, err, fPhase);
    if (!r) return;

    $("calc_taumax").textContent = fmt(r.tauMax * 1000, 2) + " ms";
    $("calc_phase").textContent = fmt(r.phaseDeg, 1) + "°";
  }

  // ===== MODULE 3 =====
  function update3() {
    const m = Number($("m3").value);
    const b = Number($("b3").value);
    const k = Number($("k3").value);

    $("m3_out").textContent = m;
    $("b3_out").textContent = b;
    $("k3_out").textContent = k;

    // state-space matrices: A = [[0, 1], [-k/m, -b/m]],  B = [0, 1/m]
    $("ss_a21").textContent = fmt(-k / m);
    $("ss_a22").textContent = fmt(-b / m);
    $("ss_b2").textContent = fmt(1 / m);

    const d = call("calcSecondOrder", m, b, k);
    if (!d) return;

    $("val_zeta").textContent = fmt(d.zeta);
    $("val_wn").textContent = fmt(d.wn) + " rad/s";
    $("val_rise").textContent = fmt(d.rise) + " s";
    $("val_peak").textContent = fmt(d.peak) + " s"; // "–" when there is no peak
    $("val_os").textContent = fmt(d.overshoot, 1) + " %";
    $("val_settle").textContent = fmt(d.settle) + " s";

    // eigenvalues of A and poles of G(s): they must show the same numbers
    $("ss_eig1").textContent = fmtComplex(d.eig && d.eig[0]);
    $("ss_eig2").textContent = fmtComplex(d.eig && d.eig[1]);
    $("ss_pole1").textContent = fmtComplex(d.poles && d.poles[0]);
    $("ss_pole2").textContent = fmtComplex(d.poles && d.poles[1]);

    call("plotModule3", d, { m, b, k });
  }

  // ===== MODULE 4 =====
  let sensor = null;
  let answered = false; // stops the same round from being scored twice
  let total = 0;

  function newRound() {
    sensor = call("newSensor");
    answered = false;
    $("result4").hidden = true;
    ["guess_tau", "guess_zeta", "guess_wn"].forEach((id) => {
      $(id).value = "";
    });

    if (!sensor) {
      $("sensor_info").textContent = "–";
      return;
    }
    $("sensor_info").textContent = sensor.info;

    // only the boxes that make sense for this sensor stay enabled
    const first = sensor.type === "first";
    $("guess_tau").disabled = !first;
    $("guess_zeta").disabled = first;
    $("guess_wn").disabled = first;

    call("plotSensor", sensor);
  }

  function submitGuess() {
    if (!sensor || answered) return;

    // Number("") is 0, so check for an empty box FIRST
    const needed =
      sensor.type === "first" ? ["guess_tau"] : ["guess_zeta", "guess_wn"];
    if (needed.some((id) => $(id).value === "")) {
      alert("Enter your guess first.");
      return;
    }

    const guess = {
      tau: Number($("guess_tau").value),
      zeta: Number($("guess_zeta").value),
      wn: Number($("guess_wn").value),
    };

    const result = call("scoreGuess", sensor, guess);
    answered = true;
    total += result ? result.points : 0;

    // the reveal: true values, round score, running score
    $("true_tau").textContent = fmt(sensor.tau);
    $("true_zeta").textContent = fmt(sensor.zeta);
    $("true_wn").textContent = fmt(sensor.wn);
    $("score_round").textContent = result ? result.text : "–";
    $("score_total").textContent = total;
    $("result4").hidden = false;

    call("plotReveal", sensor, guess);
  }

  // ===== VALIDATION TABLE =====
  function fillValidation() {
    const rows = call("runValidation");
    if (!rows) return;
    rows.forEach((row, i) => {
      const n = i + 1;
      $("v" + n + "_mine").textContent = row.mine;
      const res = $("v" + n + "_res");
      res.textContent = row.pass ? "PASS ✓" : "FAIL ✗";
      res.className = row.pass ? "pass" : "fail";
    });
  }

  // ===== CONNECT EVENTS =====
  on(["k", "tau"], "input", update1);
  document
    .querySelectorAll('input[name="input"]')
    .forEach((r) => r.addEventListener("change", update1)); // radios use "change"
  on(["tau2", "w2"], "input", update2);
  on(["calc_f", "calc_err", "calc_fphase"], "input", updateCalc);
  on(["m3", "b3", "k3"], "input", update3);
  $("btn_submit").addEventListener("click", submitGuess);
  $("btn_new").addEventListener("click", newRound);

  // ===== RUN ONCE AT PAGE LOAD =====
  update1();
  update2();
  updateCalc();
  update3();
  newRound();
  fillValidation();
})();
