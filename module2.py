import numpy as np
import matplotlib.pyplot as plt
from pyscript import document, display, when

# ============================================================
# 1. Core Calculation Functions
# ============================================================
def calculate_amplitude_ratio(omega, tau):
    if tau <= 0:
        raise ValueError("Tau must be positive.")
    return 1 / np.sqrt(1 + (omega * tau)**2)

def calculate_phase_lag(omega, tau):
    if tau <= 0:
        raise ValueError("Tau must be positive.")
    return np.degrees(-np.arctan(omega * tau))

def calculate_output_amplitude(A, omega, tau):
    return A * calculate_amplitude_ratio(omega, tau)

def calculate_cutoff_frequency(tau):
    if tau <= 0:
        raise ValueError("Tau must be positive.")
    return 1 / tau

def calculate_dynamic_error(omega, tau):
    return calculate_amplitude_ratio(omega, tau) - 1

def calculate_max_tau_for_error(frequency_hz, max_error=0.05):
    if frequency_hz <= 0 or not 0 < max_error < 1:
        raise ValueError("Invalid frequency or error.")
    omega = 2 * np.pi * frequency_hz
    M_min = 1 - max_error
    return np.sqrt(1 / M_min**2 - 1) / omega

def calculate_phase_lag_at_frequency(tau, frequency_hz):
    if tau <= 0 or frequency_hz <= 0:
        raise ValueError("Tau and frequency must be positive.")
    return calculate_phase_lag(2 * np.pi * frequency_hz, tau)

# ============================================================
# 2. Update Plots and Values (Sliders Interaction)
# ============================================================
def update_module2(event=None):
    tau = float(document.querySelector("#tau2").value)
    omega = float(document.querySelector("#w2").value)
    A = 1.0

    # Update slider output labels
    document.querySelector("#tau2_out").innerText = f"{tau:.1f}"
    document.querySelector("#w2_out").innerText = f"{omega:.1f}"

    # Calculate frequency response metrics
    M = calculate_amplitude_ratio(omega, tau)
    phi_deg = calculate_phase_lag(omega, tau)
    phi_rad = np.radians(phi_deg)
    A_out = calculate_output_amplitude(A, omega, tau)
    omega_c = calculate_cutoff_frequency(tau)
    delta = calculate_dynamic_error(omega, tau)

    # Display calculated values in the HTML list
    document.querySelector("#val_M").innerText = f"{M:.3f}"
    document.querySelector("#val_phase").innerText = f"{phi_deg:.2f}°"
    document.querySelector("#val_cutoff").innerText = f"{omega_c:.2f} rad/s"
    document.querySelector("#val_delta").innerText = f"{delta:.3f} ({delta * 100:.1f}%)"

    # 1. Plot Input and Output Sine Waves in #plot2
    period = 2 * np.pi / omega
    t = np.linspace(0, max(10, 3 * period), 1000)
    x = A * np.sin(omega * t)
    y = A_out * np.sin(omega * t + phi_rad)

    fig1, ax1 = plt.subplots(figsize=(6.5, 4))
    ax1.plot(t, x, "--", label="Input x(t)", color="gray")
    ax1.plot(t, y, linewidth=2.5, label="Output y(t)", color="blue")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Input and Output Signals")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    plt.tight_layout()

    plot2_div = document.querySelector("#plot2")
    plot2_div.innerHTML = ""
    display(fig1, target="plot2")
    plt.close(fig1)

    # 2. Plot Bode Magnitude and Phase in #bode
    omega_values = np.logspace(-2, 2, 500)
    M_values = calculate_amplitude_ratio(omega_values, tau)
    phase_values = calculate_phase_lag(omega_values, tau)

    fig2, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(6.5, 4), sharex=True)

    # Magnitude subplot
    ax_mag.semilogx(omega_values, 20 * np.log10(M_values), linewidth=2, label="Magnitude")
    ax_mag.axvline(omega_c, linestyle="--", color="red", label=f"Cutoff = {omega_c:.2f} rad/s")
    ax_mag.axhline(-3.01, linestyle=":", color="gray", label="-3 dB")
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_mag.set_title("Bode Plot")
    ax_mag.grid(True, which="both", alpha=0.3)
    ax_mag.legend()

    # Phase subplot
    ax_phase.semilogx(omega_values, phase_values, linewidth=2, color="green", label="Phase")
    ax_phase.axvline(omega_c, linestyle="--", color="red")
    ax_phase.axhline(-45, linestyle=":", color="gray", label="-45°")
    ax_phase.set_xlabel("Angular Frequency ω (rad/s)")
    ax_phase.set_ylabel("Phase Lag (degrees)")
    ax_phase.grid(True, which="both", alpha=0.3)
    ax_phase.legend()

    plt.tight_layout()

    bode_div = document.querySelector("#bode")
    bode_div.innerHTML = ""
    display(fig2, target="bode")
    plt.close(fig2)

# ============================================================
# 3. Update Dynamic-Error Calculator
# ============================================================
def update_calculator(event=None):
    try:
        freq_hz = float(document.querySelector("#calc_f").value)
        err_percent = float(document.querySelector("#calc_err").value)
        freq_phase = float(document.querySelector("#calc_fphase").value)

        max_err = err_percent / 100.0
        tau_max = calculate_max_tau_for_error(freq_hz, max_err)
        phase_lag = calculate_phase_lag_at_frequency(tau_max, freq_phase)

        document.querySelector("#calc_taumax").innerText = f"{tau_max * 1000:.3f} ms ({tau_max:.5f} s)"
        document.querySelector("#calc_phase").innerText = f"{abs(phase_lag):.2f}°"
    except ValueError:
        document.querySelector("#calc_taumax").innerText = "Invalid input"
        document.querySelector("#calc_phase").innerText = "-"

# ============================================================
# 4. Event Listeners and Initial Run
# ============================================================
@when("input", "#tau2")
@when("input", "#w2")
def on_slider_change(event):
    update_module2()

@when("input", "#calc_f")
@when("input", "#calc_err")
@when("input", "#calc_fphase")
def on_calc_change(event):
    update_calculator()

# Run initial calculations and plots on page load
update_module2()
update_calculator()
