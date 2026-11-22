# Tuning Challenge (P4)

import random
import matplotlib.pyplot as plt
from pyscript import document, display, when
from pid_core import simulate_pid, compute_metrics

challenge_state = {
    "plant_type": "first_order",
    "params": {"K": 1.5, "tau": 1.2},
    "max_tr": 1.0,
    "max_os": 10.0,
    "max_ts": 3.0,
    "max_ess": 0.02,
    "score": 0,
    "solved": False
}

def generate_challenge(event=None):
    ptype = random.choice(["first_order", "second_order"])
    challenge_state["plant_type"] = ptype
    challenge_state["solved"] = False

    if ptype == "first_order":
        challenge_state["params"] = {
            "K": round(random.uniform(0.8, 2.5), 2),
            "tau": round(random.uniform(0.5, 2.0), 2)
        }
    else:
        challenge_state["params"] = {
            "m": round(random.uniform(0.5, 2.0), 2),
            "b": round(random.uniform(0.5, 3.0), 2),
            "k": round(random.uniform(1.0, 5.0), 2)
        }

    challenge_state["max_tr"] = round(random.uniform(0.6, 1.5), 2)
    challenge_state["max_os"] = random.choice([5.0, 10.0, 15.0])
    challenge_state["max_ts"] = round(challenge_state["max_tr"] * 3.0, 2)
    challenge_state["max_ess"] = 0.02

    # FIX 1: plain text only. KaTeX runs once when the page loads, so "$t_r$" put
    # here later would stay as raw dollar signs on the page.
    specs_html = f"""
    <li>Plant type: <strong>{ptype.replace('_', ' ').title()}</strong> (parameters hidden)</li>
    <li>Rise time &le; <strong>{challenge_state['max_tr']} s</strong></li>
    <li>Overshoot &le; <strong>{challenge_state['max_os']}%</strong></li>
    <li>Settling time &le; <strong>{challenge_state['max_ts']} s</strong></li>
    <li>Steady-state error &le; <strong>{challenge_state['max_ess']}</strong></li>
    """
    document.getElementById("p4-specs-list").innerHTML = specs_html
    document.getElementById("p4-status").innerText = "Waiting for your test..."

    # FIX 2: clear the old result when a new challenge starts
    for key in ("tr", "os", "ts", "ess"):
        document.getElementById(f"p4-{key}").innerText = "–"
    document.getElementById("p4-checks").innerHTML = ""
    document.getElementById("p4-plot").innerHTML = ""

def test_challenge(event=None):
    kp = float(document.getElementById("p4-kp").value or 0.0)
    ki = float(document.getElementById("p4-ki").value or 0.0)
    kd = float(document.getElementById("p4-kd").value or 0.0)

    t, r, y, u = simulate_pid(
        challenge_state["plant_type"],
        challenge_state["params"],
        kp, ki, kd,
        setpoint=1.0,
        u_min=-15.0,
        u_max=15.0
    )

    m = compute_metrics(t, y, 1.0)
    document.getElementById("p4-tr").innerText = str(m["rise_time"])
    document.getElementById("p4-os").innerText = str(m["overshoot"])
    document.getElementById("p4-ts").innerText = str(m["settling_time"])
    document.getElementById("p4-ess").innerText = str(m["ss_error"])

    tr_ok = isinstance(m["rise_time"], float) and m["rise_time"] <= challenge_state["max_tr"]
    os_ok = m["overshoot"] <= challenge_state["max_os"]
    ts_ok = isinstance(m["settling_time"], float) and m["settling_time"] <= challenge_state["max_ts"]
    ess_ok = m["ss_error"] <= challenge_state["max_ess"]

    # FIX 3: the PDF asks for pass or fail on EACH part of the spec
    parts = [
        ("Rise time", m["rise_time"], f"{challenge_state['max_tr']} s", tr_ok),
        ("Overshoot", f"{m['overshoot']}%", f"{challenge_state['max_os']}%", os_ok),
        ("Settling time", m["settling_time"], f"{challenge_state['max_ts']} s", ts_ok),
        ("Steady-state error", m["ss_error"], f"{challenge_state['max_ess']}", ess_ok),
    ]
    rows = ""
    for name, value, limit, ok in parts:
        cls = "pass" if ok else "fail"
        word = "PASS" if ok else "FAIL"
        rows += f"<li><span class='{cls}'>{word}</span> {name}: {value} (limit {limit})</li>"
    document.getElementById("p4-checks").innerHTML = rows

    # FIX 4: colors come from the CSS classes .pass and .fail (no inline style)
    if tr_ok and os_ok and ts_ok and ess_ok:
        document.getElementById("p4-status").innerHTML = "<span class='pass'>PASS! All specs met.</span>"
        if not challenge_state["solved"]:
            challenge_state["score"] += 1
            challenge_state["solved"] = True
            document.getElementById("p4-score").innerText = str(challenge_state["score"])
    else:
        reasons = []
        if not tr_ok: reasons.append("Rise time too slow")
        if not os_ok: reasons.append("Overshoot too high")
        if not ts_ok: reasons.append("Settling time too long")
        if not ess_ok: reasons.append("Steady-state error too large")
        document.getElementById("p4-status").innerHTML = f"<span class='fail'>FAIL: {', '.join(reasons)}</span>"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, r, 'k--', label="Target Setpoint")
    ax.plot(t, y, 'b-', linewidth=2, label="Your Tuned Response")
    ax.axhline(1.0 + challenge_state["max_os"] / 100.0, color='r', linestyle=':', label="Max Allowed Overshoot")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Output y(t)")
    ax.set_title("Tuning Challenge Response")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_div = document.getElementById("p4-plot")
    plot_div.innerHTML = ""
    display(fig, target="p4-plot")
    plt.close(fig)

@when("click", "#p4-new-btn")
def on_new_challenge(event):
    generate_challenge()

@when("click", "#p4-test-btn")
def on_test_challenge(event):
    test_challenge()

generate_challenge()
