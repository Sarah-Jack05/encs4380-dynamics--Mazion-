import numpy as np
import matplotlib.pyplot as plt
from pyscript import document, display, when

# ============================================================
# 1. Core Calculation Functions
# ============================================================
def calculate_damping_type(zeta):
    if zeta <= 0:
        raise ValueError("Damping Ratio must be positive")
    if np.isclose(zeta, 1.0):
        return "Critically Damped"
    elif zeta < 1:
        return "Underdamped"
    else:
        return "Overdamped"

def calculate_second_order_step_response(K, zeta, omega_n, t, A=1.0):
    if zeta <= 0:
        raise ValueError("Damping Ratio must be positive")
    if omega_n <= 0:
        raise ValueError("Natural Frequency must be positive")

    t = np.asarray(t)

    if zeta < 1:
        omega_d = omega_n * np.sqrt(1 - zeta**2)
        return K * A * (
            1 - np.exp(-zeta * omega_n * t) * (
                np.cos(omega_d * t) +
                (zeta / np.sqrt(1 - zeta**2)) * np.sin(omega_d * t)
            )
        )
    elif np.isclose(zeta, 1.0):
        return K * A * (
            1 - np.exp(-omega_n * t) * (1 + omega_n * t)
        )
    else:
        alpha = np.sqrt(zeta**2 - 1)
        return K * A * (
            1 - (
                (zeta + alpha) * np.exp(-omega_n * (zeta - alpha) * t)
                - (zeta - alpha) * np.exp(-omega_n * (zeta + alpha) * t)
            ) / (2 * alpha)
        )

def calculate_state_space(m, b, k):
    if m <= 0:
        raise ValueError("Mass must be positive")
    if b < 0:
        raise ValueError("Damping Coefficient must be non-negative")
    if k <= 0:
        raise ValueError("Spring Constant must be positive")

    A = np.array([
        [0.0, 1.0],
        [-k / m, -b / m]
    ])
    B = np.array([
        [0.0],
        [1.0 / m]
    ])
    return A, B

def calculate_eigenvalues(A):
    return np.linalg.eigvals(A)

def calculate_poles(zeta, omega_n):
    if zeta <= 0:
        raise ValueError("Damping Ratio must be positive")
    if omega_n <= 0:
        raise ValueError("Natural Frequency must be positive")

    if zeta < 1:
        return (
            -zeta * omega_n + omega_n * np.sqrt(1 - zeta**2) * 1j,
            -zeta * omega_n - omega_n * np.sqrt(1 - zeta**2) * 1j
        )
    elif np.isclose(zeta, 1.0):
        return (-zeta * omega_n, -zeta * omega_n)
    else:
        return (
            -zeta * omega_n + omega_n * np.sqrt(zeta**2 - 1),
            -zeta * omega_n - omega_n * np.sqrt(zeta**2 - 1)
        )

def interpolate_crossing(t1, y1, t2, y2, target):
    if np.isclose(y2, y1):
        return float(t2)
    return float(t1 + (target - y1) * (t2 - t1) / (y2 - y1))

def format_complex(val):
    real_part = np.real(val)
    imag_part = np.imag(val)
    if np.isclose(imag_part, 0.0, atol=1e-4):
        return f"{real_part:.3f}"
    sign = "+" if imag_part >= 0 else "-"
    return f"{real_part:.3f} {sign} j{abs(imag_part):.3f}"

# ============================================================
# 2. Main Interactive Simulation Update Function
# ============================================================
def update_module3(event=None):
    # Read values from HTML sliders
    m = float(document.querySelector("#mass").value)
    b = float(document.querySelector("#b").value)
    k = float(document.querySelector("#spring").value)

    # Update slider output labels
    document.querySelector("#mass_out").innerText = f"{m:.1f}"
    document.querySelector("#b_out").innerText = f"{b:.1f}"
    document.querySelector("#spring_out").innerText = f"{k:.1f}"

    # Calculate system parameters (Assuming unit step force F = 1.0)
    omega_n = np.sqrt(k / m)
    zeta = b / (2.0 * np.sqrt(m * k))
    K = 1.0 / k
    A_amp = 1.0
    final_value = K * A_amp
    damping_type = calculate_damping_type(zeta)

    # Automatic simulation time window
    if zeta > 1:
        slow_pole_rate = omega_n * (zeta - np.sqrt(zeta**2 - 1))
        t_end = 10.0 / slow_pole_rate
    else:
        t_end = 10.0 / (zeta * omega_n)
    t_end = min(max(t_end, 2.0), 100.0)

    t = np.linspace(0, t_end, 1500)
    y = calculate_second_order_step_response(K, zeta, omega_n, t, A_amp)

    # Performance Metrics: Peak & Overshoot
    peak_index = int(np.argmax(y))
    peak_value = float(y[peak_index])
    peak_time = float(t[peak_index])
    overshoot = max(0.0, (peak_value - final_value) / final_value * 100.0)
    has_peak = overshoot >= 0.01

    # Performance Metrics: Rise Time (10% to 90%)
    level_10 = 0.10 * final_value
    level_90 = 0.90 * final_value
    idx_10 = np.where(y >= level_10)[0]
    idx_90 = np.where(y >= level_90)[0]

    t_10, t_90, rise_time = None, None, None
    if len(idx_10) > 0 and len(idx_90) > 0:
        i10 = int(idx_10[0])
        i90 = int(idx_90[0])
        t_10 = float(t[0]) if i10 == 0 else interpolate_crossing(t[i10 - 1], y[i10 - 1], t[i10], y[i10], level_10)
        t_90 = float(t[0]) if i90 == 0 else interpolate_crossing(t[i90 - 1], y[i90 - 1], t[i90], y[i90], level_90)
        rise_time = float(t_90 - t_10)

    # Performance Metrics: Settling Time (2% criterion)
    tol = 0.02 * abs(final_value)
    upper_lim = final_value + tol
    lower_lim = final_value - tol
    within_band = (y >= lower_lim) & (y <= upper_lim)
    outside_idx = np.where(~within_band)[0]

    settling_time = None
    if len(outside_idx) == 0:
        settling_time = 0.0
    elif outside_idx[-1] < len(t) - 1:
        last_out = int(outside_idx[-1])
        boundary = upper_lim if y[last_out] > upper_lim else lower_lim
        settling_time = interpolate_crossing(t[last_out], y[last_out], t[last_out + 1], y[last_out + 1], boundary)

    # Update Values list in HTML
    document.querySelector("#val_zeta").innerText = f"{zeta:.3f} ({damping_type})"
    document.querySelector("#val_wn").innerText = f"{omega_n:.3f} rad/s"
    document.querySelector("#val_rise").innerText = f"{rise_time:.3f} s" if rise_time is not None else "N/A"
    document.querySelector("#val_peak").innerText = f"{peak_time:.3f} s" if has_peak else "None"
    document.querySelector("#val_os").innerText = f"{overshoot:.2f}%"
    document.querySelector("#val_settle").innerText = f"{settling_time:.3f} s" if settling_time is not None else "N/A"

    # Update State-Space Matrices and Poles in HTML
    A_mat, B_mat = calculate_state_space(m, b, k)
    eigs = calculate_eigenvalues(A_mat)
    poles = calculate_poles(zeta, omega_n)

    document.querySelector("#ss_a21").innerText = f"{A_mat[1, 0]:.2f}"
    document.querySelector("#ss_a22").innerText = f"{A_mat[1, 1]:.2f}"
    document.querySelector("#ss_b2").innerText = f"{B_mat[1, 0]:.2f}"
    document.querySelector("#ss_eig1").innerText = format_complex(eigs[0])
    document.querySelector("#ss_eig2").innerText = format_complex(eigs[1])
    document.querySelector("#ss_pole1").innerText = format_complex(poles[0])
    document.querySelector("#ss_pole2").innerText = format_complex(poles[1])

    # --------------------------------------------------------
    # PLOT 1: Step Response Curve (#plot3)
    # --------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=110)
    ax1.plot(t, y, color="royalblue", linewidth=2.5, label="System Response")
    ax1.axhline(final_value, color="green", linestyle="--", linewidth=1.5, label=f"Final Value = {final_value:.3f}")
    ax1.axhspan(lower_lim, upper_lim, color="orange", alpha=0.15, label="2% Settling Band")

    if has_peak:
        ax1.scatter(peak_time, peak_value, color="red", s=70, zorder=5, label=f"Peak ({overshoot:.1f}%)")
    if t_10 is not None and t_90 is not None:
        ax1.axvline(t_10, color="blue", linestyle="-.", linewidth=1.2, label=f"Rise = {rise_time:.2f}s")
        ax1.axvline(t_90, color="cyan", linestyle="-.", linewidth=1.2)
    if settling_time is not None:
        ax1.axvline(settling_time, color="purple", linestyle="--", linewidth=1.5, label=f"Settling = {settling_time:.2f}s")

    ax1.set_title(f"Step Response - {damping_type}", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Displacement x(t)")
    ax1.set_xlim(0, t_end)
    ax1.set_ylim(min(0, np.min(y) - 0.05 * abs(final_value)), max(upper_lim, np.max(y) + 0.15 * abs(final_value)))
    ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.legend(loc="lower right", fontsize=8)
    plt.tight_layout()

    plot3_div = document.querySelector("#plot3")
    plot3_div.innerHTML = ""
    display(fig1, target="plot3")
    plt.close(fig1)

    # --------------------------------------------------------
    # PLOT 2: S-Plane Pole Plot (#splane)
    # --------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=110)
    ax2.axhline(0, color="black", linewidth=1.2)
    ax2.axvline(0, color="black", linewidth=1.2)

    p_real = [np.real(p) for p in poles]
    p_imag = [np.imag(p) for p in poles]

    ax2.scatter(p_real, p_imag, color="crimson", marker="x", s=120, linewidths=2.5, zorder=5, label="System Poles")

    max_r = max(abs(min(p_real)), 2.0) * 1.3
    max_i = max(max(abs(i) for i in p_imag), 2.0) * 1.3
    ax2.set_xlim(-max_r, max_r * 0.3)
    ax2.set_ylim(-max_i, max_i)

    ax2.set_title("Poles in the s-Plane", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Real Axis (σ)")
    ax2.set_ylabel("Imaginary Axis (jω)")
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(loc="upper right", fontsize=8)
    plt.tight_layout()

    splane_div = document.querySelector("#splane")
    splane_div.innerHTML = ""
    display(fig2, target="splane")
    plt.close(fig2)

    # --------------------------------------------------------
    # PLOT 3: Phase Plane Trajectory (#phase)
    # --------------------------------------------------------
    velocity = np.gradient(y, t)

    fig3, ax3 = plt.subplots(figsize=(6, 4), dpi=110)
    ax3.plot(y, velocity, color="teal", linewidth=2, label="Phase Trajectory")
    ax3.scatter(y[0], velocity[0], color="black", marker="o", s=50, zorder=5, label="Start (0,0)")
    ax3.scatter(y[-1], velocity[-1], color="darkorange", marker="x", s=70, zorder=5, label="Equilibrium")
    ax3.set_title("Phase Plane (Velocity vs Displacement)", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Displacement x(t)")
    ax3.set_ylabel("Velocity dx/dt")
    ax3.grid(True, linestyle="--", alpha=0.35)
    ax3.legend(loc="upper right", fontsize=8)
    plt.tight_layout()

    phase_div = document.querySelector("#phase")
    phase_div.innerHTML = ""
    display(fig3, target="phase")
    plt.close(fig3)


# ============================================================
# 3. Event Listeners and Initial Execution
# ============================================================
@when("input", "#mass, #b, #spring")
def on_m3_slider_change(event):
    update_module3()


# Run the initial simulation on page load
update_module3()
