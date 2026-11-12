import numpy as np
import matplotlib.pyplot as plt
from pyscript import document, display, when

from module1 import calculate_step_response
from module3 import calculate_second_order_step_response, calculate_overshoot

# ============================================================
# 1. Game State Storage
# ============================================================
game_state = {
    "sensor": None,
    "t": None,
    "true_response": None,
    "noisy_response": None,
    "input_type": "step",
    "frequency": None,
    "total_score": 0,
    "rounds": 0,
    "answered": False,
}

# ============================================================
# 2. Core Calculation & Generation Functions
# ============================================================
def generate_random_sensor():
    sensor_type = np.random.choice(["first_order", "second_order"])
    if sensor_type == "first_order":
        K = float(np.random.uniform(1.0, 5.0))
        tau = float(np.random.uniform(0.5, 5.0))
        return {"type": "first_order", "K": K, "tau": tau}
    else:
        damping_type = np.random.choice(["underdamped", "critically_damped", "overdamped"])
        if damping_type == "underdamped":
            zeta = float(np.random.uniform(0.2, 0.95))
        elif damping_type == "critically_damped":
            zeta = 1.0
        else:
            zeta = float(np.random.uniform(1.05, 2.0))
        omega_n = float(np.random.uniform(1.0, 10.0))
        return {
            "type": "second_order",
            "damping_type": damping_type,
            "zeta": zeta,
            "omega_n": omega_n,
        }

def generate_true_response(sensor, t, A=1.0, input_type="step", frequency=1.0):
    if sensor["type"] == "first_order":
        if input_type == "step":
            return calculate_step_response(sensor["K"], sensor["tau"], t, A)
        elif input_type == "sine":
            omega = 2.0 * np.pi * frequency
            M = 1.0 / np.sqrt(1.0 + (omega * sensor["tau"])**2)
            phi = np.arctan(omega * sensor["tau"])
            return sensor["K"] * A * M * np.sin(omega * t - phi)
        else:
            raise ValueError("Invalid input type")
    elif sensor["type"] == "second_order":
        return calculate_second_order_step_response(1.0, sensor["zeta"], sensor["omega_n"], t, A)
    else:
        raise ValueError("Invalid sensor type")

def add_noise(response, noise_level=0.03):
    response = np.asarray(response)
    noise_std = noise_level * np.max(np.abs(response))
    noise = np.random.normal(0.0, noise_std, size=response.shape)
    return response + noise

def calculate_guess_error(true_value, guessed_value):
    if true_value == 0:
        raise ValueError("True value cannot be zero")
    return (abs(true_value - guessed_value) / abs(true_value)) * 100.0

# ============================================================
# 3. Plotting Function (#plot4)
# ============================================================
def render_game_plot(show_solution=False):
    t = game_state["t"]
    noisy = game_state["noisy_response"]
    true_resp = game_state["true_response"]
    sensor = game_state["sensor"]
    input_type = game_state["input_type"]
    freq = game_state["frequency"]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=110)
    ax.plot(t, noisy, color="slategray", linewidth=1.5, alpha=0.85, label="Measured Noisy Signal")

    if show_solution:
        ax.plot(t, true_resp, color="crimson", linewidth=2.5, label="True Clean Response")
        if sensor["type"] == "first_order" and input_type == "step":
            tau = sensor["tau"]
            y_632 = 0.6321 * sensor["K"]
            ax.axhline(y_632, color="green", linestyle="--", linewidth=1.2, label="63.2% Final Value")
            ax.axvline(tau, color="orange", linestyle="--", linewidth=1.2, label=f"τ = {tau:.2f} s")
        ax.set_title("Solution: True vs Measured Response", fontsize=12, fontweight="bold")
    else:
        title_str = "Unknown Sensor (Step Input)" if input_type == "step" else f"Unknown Sensor (Sine Input, f = {freq:.2f} Hz)"
        ax.set_title(title_str, fontsize=12, fontweight="bold")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Sensor Output")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()

    plot4_div = document.querySelector("#plot4")
    if plot4_div:
        plot4_div.innerHTML = ""
        display(fig, target="plot4")
    plt.close(fig)

# ============================================================
# 4. Interactive Game Actions
# ============================================================
def start_new_round(event=None):
    sensor = generate_random_sensor()
    input_type = "step"
    frequency = None

    if sensor["type"] == "first_order":
        input_type = str(np.random.choice(["step", "sine"]))
        if input_type == "sine":
            frequency = float(np.random.uniform(0.2, 1.5))

    t = np.linspace(0, 10, 500)
    true_resp = generate_true_response(
        sensor, t, input_type=input_type, frequency=frequency if frequency else 1.0
    )
    noisy_resp = add_noise(true_resp, noise_level=0.03)

    game_state["sensor"] = sensor
    game_state["t"] = t
    game_state["true_response"] = true_resp
    game_state["noisy_response"] = noisy_resp
    game_state["input_type"] = input_type
    game_state["frequency"] = frequency
    game_state["answered"] = False

    # Update #sensor_info label
    info_el = document.querySelector("#sensor_info")
    if info_el:
        if input_type == "step":
            info_el.innerText = "Step input (u(t) = 1)"
        else:
            omega = 2.0 * np.pi * frequency
            info_el.innerText = f"Sine input (f = {frequency:.2f} Hz, ω = {omega:.2f} rad/s)"

    # Clear input fields
    for field_id in ["#guess_tau", "#guess_zeta", "#guess_wn"]:
        el = document.querySelector(field_id)
        if el:
            el.value = ""

    # Hide true values box until user submits
    out_box = document.querySelector("#output_values")
    if out_box:
        out_box.setAttribute("hidden", "")

    render_game_plot(show_solution=False)

def submit_guess(event=None):
    if game_state["sensor"] is None or game_state["answered"]:
        return

    tau_str = document.querySelector("#guess_tau").value.strip()
    zeta_str = document.querySelector("#guess_zeta").value.strip()
    wn_str = document.querySelector("#guess_wn").value.strip()

    # Determine guessed sensor type from filled inputs
    if tau_str != "" and zeta_str == "" and wn_str == "":
        guessed_type = "first_order"
        try:
            g_tau = float(tau_str)
        except ValueError:
            return
    elif zeta_str != "" and wn_str != "" and tau_str == "":
        guessed_type = "second_order"
        try:
            g_zeta = float(zeta_str)
            g_wn = float(wn_str)
        except ValueError:
            return
    else:
        # Prompt user if fields are ambiguous or empty
        out_box = document.querySelector("#output_values")
        if out_box:
            out_box.removeAttribute("hidden")
            document.querySelector("#score_round").innerText = "Fill either τ (for 1st-order) OR both ζ and ωn (for 2nd-order)."
        return

    game_state["answered"] = True
    sensor = game_state["sensor"]
    round_score = 0

    # Evaluate guess and populate true values
    if sensor["type"] == "first_order":
        document.querySelector("#true_tau").innerText = f"{sensor['tau']:.3f} s (K = {sensor['K']:.2f})"
        document.querySelector("#true_zeta").innerText = "N/A (First-order)"
        document.querySelector("#true_wn").innerText = "N/A (First-order)"

        if guessed_type == "first_order":
            err_tau = calculate_guess_error(sensor["tau"], g_tau)
            round_score = 100 if err_tau <= 10.0 else (50 if err_tau <= 20.0 else 0)
            round_msg = f"{round_score}/100 (τ error: {err_tau:.1f}%)"
        else:
            round_msg = "0/100 (Wrong order — sensor was First-order)"

    else:
        os_pct = calculate_overshoot(sensor["zeta"])
        document.querySelector("#true_tau").innerText = "N/A (Second-order)"
        document.querySelector("#true_zeta").innerText = f"{sensor['zeta']:.3f} ({sensor['damping_type']}, OS: {os_pct:.1f}%)"
        document.querySelector("#true_wn").innerText = f"{sensor['omega_n']:.3f} rad/s"

        if guessed_type == "second_order":
            err_zeta = calculate_guess_error(sensor["zeta"], g_zeta)
            err_wn = calculate_guess_error(sensor["omega_n"], g_wn)
            if err_zeta <= 10.0:
                round_score += 50
            if err_wn <= 10.0:
                round_score += 50
            round_msg = f"{round_score}/100 (ζ error: {err_zeta:.1f}%, ωn error: {err_wn:.1f}%)"
        else:
            round_msg = "0/100 (Wrong order — sensor was Second-order)"

    game_state["total_score"] += round_score
    game_state["rounds"] += 1

    # Reveal true values & update scores
    out_box = document.querySelector("#output_values")
    if out_box:
        out_box.removeAttribute("hidden")

    document.querySelector("#score_round").innerText = round_msg
    document.querySelector("#score_total").innerText = f"{game_state['total_score']} / {game_state['rounds'] * 100}"

    render_game_plot(show_solution=True)

# ============================================================
# 5. Event Listeners & Initial Round
# ============================================================
@when("click", "#btn_new")
def on_new_sensor_click(event):
    start_new_round()

@when("click", "#btn_submit")
def on_submit_guess_click(event):
    submit_guess()

# Start first round on page load
start_new_round()
