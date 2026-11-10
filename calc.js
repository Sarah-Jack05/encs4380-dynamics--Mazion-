// ============================================================
// calc.js — all the math of the toolkit.
// JavaScript port of calculations.py (same formulas, same names).
// Every module reads its numbers from here; plot.js draws them,
// ui.js wires the sliders.
// ============================================================

// ---------- small helpers ----------

// like np.linspace(a, b, n)
function linspace(a, b, n) {
  const arr = new Array(n);
  const step = (b - a) / (n - 1);
  for (let i = 0; i < n; i++) arr[i] = a + i * step;
  return arr;
}

function fmt(x, digits = 3) {
  if (x === null || x === undefined || Number.isNaN(x)) return "–";
  if (Math.abs(x) >= 1000 || (Math.abs(x) < 0.001 && x !== 0)) {
    return x.toExponential(2);
  }
  return parseFloat(x.toFixed(digits)).toString();
}

// gaussian noise (Box-Muller), used by Module 4
function gaussianNoise(sigma) {
  let u = 0, v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v) * sigma;
}

// ============================================================
// Module 1: First-order time response
// tau*dy + y = K*x   ->   G(s) = K / (tau*s + 1)
// ============================================================

// step of size A: y(t) = K*A*(1 - e^(-t/tau))
function stepResponse(K, tau, tArr, A = 1.0) {
  return tArr.map((t) => K * A * (1 - Math.exp(-t / tau)));
}

// unit-ramp input x(t) = A*t:
// y(t) = K*A*(t - tau + tau*e^(-t/tau))
function rampResponse(K, tau, tArr, A = 1.0) {
  return tArr.map((t) => K * A * (t - tau + tau * Math.exp(-t / tau)));
}

// error fraction e(t)/e(0) = e^(-t/tau)
function errorFraction(tau, tArr) {
  return tArr.map((t) => Math.exp(-t / tau));
}

// ramp lag for a first-order sensor = tau
function rampLag(tau) {
  return tau;
}

// steady-state error for a ramp = K*A*tau
function steadyStateError(K, tau, A = 1.0) {
  return K * A * tau;
}

// ============================================================
// Module 2: First-order frequency response
// M = 1/sqrt(1+(w*tau)^2),  phi = -atan(w*tau)
// ============================================================

function amplitudeRatio(omega, tau) {
  return 1 / Math.sqrt(1 + Math.pow(omega * tau, 2));
}

// phase lag in degrees (negative number = output lags input)
function phaseLagDeg(omega, tau) {
  return (-Math.atan(omega * tau) * 180) / Math.PI;
}

function outputAmplitude(A, omega, tau) {
  return A * amplitudeRatio(omega, tau);
}

function cutoffFrequency(tau) {
  return 1 / tau;
}

// dynamic error delta = M - 1
function dynamicError(omega, tau) {
  return amplitudeRatio(omega, tau) - 1;
}

// largest tau that keeps the dynamic error of a sine of
// frequency f (Hz) below maxError (fraction, e.g. 0.05)
function maxTauForError(frequencyHz, maxError = 0.05) {
  const omega = 2 * Math.PI * frequencyHz;
  const Mmin = 1 - maxError;
  return Math.sqrt(1 / (Mmin * Mmin) - 1) / omega;
}

// phase lag (deg) at a frequency given in Hz
function phaseLagAtFrequencyHz(tau, frequencyHz) {
  return phaseLagDeg(2 * Math.PI * frequencyHz, tau);
}

// time-domain sine response: input A*sin(wt), output A*M*sin(wt + phi)
function sineSignals(tau, omega, A = 1.0) {
  const periods = 4;
  const T = (2 * Math.PI) / omega;
  const t = linspace(0, periods * T, 1200);
  const M = amplitudeRatio(omega, tau);
  const phiRad = (phaseLagDeg(omega, tau) * Math.PI) / 180;
  const input = t.map((tv) => A * Math.sin(omega * tv));
  const output = t.map((tv) => A * M * Math.sin(omega * tv + phiRad));
  return { t, input, output, M, phiRad };
}

// ============================================================
// Module 3: Second-order response
// G(s) = K*wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
// (mass-spring-damper: m*x'' + b*x' + k*x = F)
// ============================================================

function dampingType(zeta) {
  if (zeta < 1) return "Underdamped";
  if (Math.abs(zeta - 1) < 1e-9) return "Critically damped";
  return "Overdamped";
}

// percent overshoot of the step response
function overshootPercent(zeta) {
  if (zeta < 1) {
    return (
      Math.exp((-Math.PI * zeta) / Math.sqrt(1 - zeta * zeta)) * 100
    );
  }
  return 0;
}

// closed-form step response (same three cases as calculations.py)
function secondOrderStep(K, zeta, wn, tArr, A = 1.0) {
  return tArr.map((t) => {
    if (zeta < 1) {
      const wd = wn * Math.sqrt(1 - zeta * zeta);
      return (
        K * A *
        (1 -
          Math.exp(-zeta * wn * t) *
            (Math.cos(wd * t) +
              (zeta / Math.sqrt(1 - zeta * zeta)) * Math.sin(wd * t)))
      );
    }
    if (Math.abs(zeta - 1) < 1e-9) {
      return K * A * (1 - Math.exp(-wn * t) * (1 + wn * t));
    }
    // overdamped
    const alpha = Math.sqrt(zeta * zeta - 1);
    return (
      K * A *
      (1 -
        ((zeta + alpha) * Math.exp(-wn * (zeta - alpha) * t) -
          (zeta - alpha) * Math.exp(-wn * (zeta + alpha) * t)) /
          (2 * alpha))
    );
  });
}

// metrics read off the curve:
// - rise time: 0->100% of final value when underdamped, 10->90% otherwise
// - peak time: time of the first maximum (only exists when there is overshoot)
// - overshoot: (max - final)/final * 100
// - settling time: last time the curve is outside the 2% band
function stepMetrics(K, zeta, wn, A = 1.0) {
  const final = K * A;
  // window long enough for slow overdamped cases
  const tEnd = zeta < 1 ? 12 / (zeta * wn) : 12 / (wn * (zeta - Math.sqrt(zeta * zeta - 1)));
  const n = 4000;
  const t = linspace(0, tEnd, n);
  const y = secondOrderStep(K, zeta, wn, t, A);

  let yMax = -Infinity, tPeak = null;
  for (let i = 0; i < n; i++) {
    if (y[i] > yMax) { yMax = y[i]; tPeak = t[i]; }
  }
  const overshoot = yMax > final ? ((yMax - final) / final) * 100 : 0;

  // rise time
  let rise = null;
  if (zeta < 1) {
    // first time the curve reaches the final value
    for (let i = 1; i < n; i++) {
      if (y[i] >= final) { rise = t[i]; break; }
    }
  } else {
    const y10 = 0.1 * final, y90 = 0.9 * final;
    let t10 = null, t90 = null;
    for (let i = 1; i < n; i++) {
      if (t10 === null && y[i] >= y10) t10 = t[i];
      if (t90 === null && y[i] >= y90) { t90 = t[i]; break; }
    }
    if (t10 !== null && t90 !== null) rise = t90 - t10;
  }

  // settling time (2% band)
  let settle = 0;
  for (let i = 0; i < n; i++) {
    if (Math.abs(y[i] - final) > 0.02 * final) settle = t[i];
  }
  settle = settle > 0 ? settle : t[1]; // settles (almost) immediately

  return {
    rise: rise,
    peakTime: overshoot > 0 ? tPeak : null,
    overshoot: overshoot,
    settling: settle,
    tPeakValue: yMax,
    tArr: t,
    yArr: y,
    final: final,
  };
}

// poles of G(s): s = -zeta*wn +- wn*sqrt(zeta^2-1)  (complex pair if zeta<1)
function polesOfSecondOrder(zeta, wn) {
  if (zeta < 1) {
    const wd = wn * Math.sqrt(1 - zeta * zeta);
    const re = -zeta * wn;
    return [
      { re: re, im: wd },
      { re: re, im: -wd },
    ];
  }
  if (Math.abs(zeta - 1) < 1e-9) {
    return [
      { re: -wn, im: 0 },
      { re: -wn, im: 0 },
    ];
  }
  const alpha = wn * Math.sqrt(zeta * zeta - 1);
  return [
    { re: -zeta * wn + alpha, im: 0 },
    { re: -zeta * wn - alpha, im: 0 },
  ];
}

// eigenvalues of A = [[0, 1], [-k/m, -b/m]]
// char. polynomial: s^2 + (b/m)s + k/m = 0
function eigenvaluesOfA(m, b, k) {
  if (m <= 0) throw new Error("Mass must be positive");
  const p = b / m; // coefficient of s
  const q = k / m; // constant term
  const disc = p * p - 4 * q;
  if (disc < 0) {
    const re = -p / 2;
    const im = Math.sqrt(-disc) / 2;
    return [
      { re: re, im: im },
      { re: re, im: -im },
    ];
  }
  const root = Math.sqrt(disc);
  return [
    { re: (-p + root) / 2, im: 0 },
    { re: (-p - root) / 2, im: 0 },
  ];
}

// eigenvalue -> string, e.g. "-1 + j1.732"
function eigenToString(e) {
  const reS = fmt(e.re, 3);
  if (Math.abs(e.im) < 1e-9) return reS;
  const sign = e.im >= 0 ? "+" : "-";
  return `${reS} ${sign} j${fmt(Math.abs(e.im), 3)}`;
}

// ============================================================
// Module 4: "Guess the sensor"
// ============================================================

// pick a hidden sensor at random
function randomSensor() {
  if (Math.random() < 0.5) {
    // first order: random K and tau
    return {
      order: 1,
      K: 0.5 + Math.random() * 1.5,      // 0.5 .. 2
      tau: 0.5 + Math.random() * 4.5,    // 0.5 .. 5 s
      inputType: Math.random() < 0.3 ? "sine" : "step",
    };
  }
  // second order: random zeta and wn
  return {
    order: 2,
    K: 1,
    zeta: 0.15 + Math.random() * 1.2,    // 0.15 .. 1.35
    wn: 1 + Math.random() * 9,           // 1 .. 10 rad/s
    inputType: "step",
  };
}

// the (noisy) response shown to the user
function sensorResponse(sensor) {
  if (sensor.order === 1) {
    if (sensor.inputType === "sine") {
      const omega = 2 * Math.PI * (0.2 + Math.random() * 0.5); // stated frequency
      sensor.sineOmega = omega;
      const T = (2 * Math.PI) / omega;
      const t = linspace(0, 6 * T, 900);
      const M = amplitudeRatio(omega, sensor.tau);
      const phiRad = Math.atan(-omega * sensor.tau);
      const sigma = 0.03;
      const y = t.map(
        (tv) =>
          sensor.K * M * Math.sin(omega * tv + phiRad) + gaussianNoise(sigma)
      );
      const x = t.map((tv) => sensor.K * Math.sin(omega * tv));
      return { t, y, input: x };
    }
    // step
    const t = linspace(0, 6 * sensor.tau, 900);
    const sigma = 0.02 * sensor.K;
    const y = stepResponse(sensor.K, sensor.tau, t).map(
      (v) => v + gaussianNoise(sigma)
    );
    return { t, y, input: null };
  }
  // second order step
  const tEnd = 10 / sensor.wn;
  const t = linspace(0, tEnd, 900);
  const sigma = 0.02 * sensor.K;
  const y = secondOrderStep(sensor.K, sensor.zeta, sensor.wn, t).map(
    (v) => v + gaussianNoise(sigma)
  );
  return { t, y, input: null };
}

// true curve of the sensor (no noise) for the reveal overlay
function sensorTrueCurve(sensor) {
  if (sensor.order === 1) {
    if (sensor.inputType === "sine") {
      const omega = sensor.sineOmega;
      const T = (2 * Math.PI) / omega;
      const t = linspace(0, 6 * T, 900);
      const M = amplitudeRatio(omega, sensor.tau);
      const phiRad = Math.atan(-omega * sensor.tau);
      const y = t.map((tv) => sensor.K * M * Math.sin(omega * tv + phiRad));
      return { t, y };
    }
    const t = linspace(0, 6 * sensor.tau, 900);
    return { t, y: stepResponse(sensor.K, sensor.tau, t) };
  }
  const t = linspace(0, 10 / sensor.wn, 900);
  return { t, y: secondOrderStep(sensor.K, sensor.zeta, sensor.wn, t) };
}

// is the guess within 10% of the true value?
function withinTenPercent(guess, truth) {
  if (guess === null || guess === undefined || Number.isNaN(guess)) return false;
  return Math.abs(guess - truth) <= 0.1 * Math.abs(truth);
}
