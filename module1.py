import numpy as np
import matplotlib.pyplot as plt
from pyscript import document, display, when

def calculate_step_response(K, tau, t, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * (1 - np.exp(-np.asarray(t) / tau))

def calculate_ramp_response(K, tau, t, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * (np.asarray(t) - tau + tau * np.exp(-np.asarray(t) / tau))

def calculate_important_points(K, tau, A=1.0):
    t1 = tau
    y1 = calculate_step_response(K, tau, t1, A)
    t2 = 3 * tau
    y2 = calculate_step_response(K, tau, t2, A)
    return (t1, y1), (t2, y2)

def calculate_ramp_lag(tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return tau

def calculate_steady_state_error(K, tau, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * tau

def calculate_error_fraction(tau, t):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return np.exp(-np.asarray(t) / tau)

def update_simulation(event=None):
    K = float(document.querySelector("#k").value)
    tau = float(document.querySelector("#tau").value)
    is_step = document.querySelector("#step").checked

    document.querySelector("#k_out").innerText = f"{K:.1f}"
    document.querySelector("#tau_out").innerText = f"{tau:.1f}"

    (t1, y1), (t2, y2) = calculate_important_points(K, tau)
    ramp_lag = calculate_ramp_lag(tau)
    sse = calculate_steady_state_error(K, tau)

    document.querySelector("#val_tau").innerText = f"{y1:.2f}"
    document.querySelector("#val_3tau").innerText = f"{y2:.2f}"
    document.querySelector("#val_ramp_lag").innerText = f"{ramp_lag:.2f} s"
    document.querySelector("#val_sse").innerText = f"{sse:.2f}"

    t = np.linspace(0, 5 * tau, 200)
    fig, ax = plt.subplots(figsize=(6, 4))

    if is_step:
        y = calculate_step_response(K, tau, t)
        ax.plot(t, y, label="Step Response", color="blue")
        ax.scatter([t1, t2], [y1, y2], color="red", zorder=5)
    else:
        y = calculate_ramp_response(K, tau, t)
        ax.plot(t, t, "--", label="Input (Ramp)", color="gray")
        ax.plot(t, y, label="System Output", color="green")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Response y(t)")
    ax.grid(True)
    ax.legend()

    plot_div = document.querySelector("#plot1")
    plot_div.innerHTML = ""
    display(fig, target="plot1")
    plt.close(fig)

@when("input", "#k")
@when("input", "#tau")
@when("change", "#step")
@when("change", "#ramp")
def on_input_change(event):
    update_simulation()

update_simulation()
