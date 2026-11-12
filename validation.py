import numpy as np
from pyscript import document

# Import existing calculation functions directly from your modules
from module1 import calculate_step_response
from module2 import (
    calculate_amplitude_ratio,
    calculate_phase_lag,
    calculate_max_tau_for_error,
    calculate_phase_lag_at_frequency,
)
from module3 import (
    calculate_second_order_step_response,
    calculate_state_space,
    calculate_eigenvalues,
    calculate_poles,
)

def set_validation_row(row_num, mine_text, passed):
    mine_el = document.querySelector(f"#v{row_num}_mine")
    res_el = document.querySelector(f"#v{row_num}_res")
    
    if mine_el:
        mine_el.innerText = mine_text
    if res_el:
        if passed:
            res_el.innerText = "✓ PASS"
            res_el.style.color = "green"
            res_el.style.fontWeight = "bold"
        else:
            res_el.innerText = "✗ FAIL"
            res_el.style.color = "red"
            res_el.style.fontWeight = "bold"

def run_validation_checks():
    # --- Check 1: First-order step (from module1) ---
    K, tau, A = 1.0, 2.0, 1.0
    y_tau = calculate_step_response(K, tau, tau, A)
    y_3tau = calculate_step_response(K, tau, 3 * tau, A)
    pass_1 = np.isclose(y_tau, 0.6321, atol=1e-3) and np.isclose(y_3tau, 0.9502, atol=1e-3)
    set_validation_row(1, f"y(τ) = {y_tau:.3f} KA, y(3τ) = {y_3tau:.3f} KA", pass_1)

    # --- Check 2: Frequency response at tau = 0.2 s, omega = 2 rad/s (from module2) ---
    M_2 = calculate_amplitude_ratio(omega=2.0, tau=0.2)
    lag_2 = abs(calculate_phase_lag(omega=2.0, tau=0.2))
    pass_2 = np.isclose(M_2, 0.9285, atol=0.01) and np.isclose(lag_2, 21.80, atol=0.1)
    set_validation_row(2, f"amplitude {M_2:.2f}, lag {lag_2:.1f}°", pass_2)

    # --- Check 3: Max tau for 5% error at 100 Hz & lag at 50 Hz (from module2) ---
    tau_max = calculate_max_tau_for_error(frequency_hz=100.0, max_error=0.05)
    tau_max_ms = tau_max * 1000.0
    lag_50 = abs(calculate_phase_lag_at_frequency(tau=tau_max, frequency_hz=50.0))
    pass_3 = np.isclose(tau_max_ms, 0.523, atol=0.01) and np.isclose(lag_50, 9.33, atol=0.1)
    set_validation_row(3, f"τmax = {tau_max_ms:.2f} ms, lag {lag_50:.1f}° at 50 Hz", pass_3)

    # --- Check 4: Second order overshoot at zeta = 0.5 (from module3) ---
    t = np.linspace(0, 10, 1500)
    y_05 = calculate_second_order_step_response(K=1.0, zeta=0.5, omega_n=2.0, t=t, A=1.0)
    os_05 = max(0.0, (np.max(y_05) - 1.0) * 100.0)
    pass_4 = np.isclose(os_05, 16.303, atol=0.1)
    set_validation_row(4, f"overshoot = {os_05:.1f}%", pass_4)

    # --- Check 5: Second order overshoot at zeta = 1.0 (from module3) ---
    y_10 = calculate_second_order_step_response(K=1.0, zeta=1.0, omega_n=2.0, t=t, A=1.0)
    os_10 = max(0.0, (np.max(y_10) - 1.0) * 100.0)
    pass_5 = np.isclose(os_10, 0.0, atol=1e-4)
    set_validation_row(5, f"overshoot = {os_10:.1f}% (no overshoot)", pass_5)

    # --- Check 6: State space eigenvalues vs poles (from module3) ---
    m, b, k = 1.0, 2.0, 4.0
    A_mat, _ = calculate_state_space(m, b, k)
    eigs = calculate_eigenvalues(A_mat)
    
    omega_n = np.sqrt(k / m)
    zeta = b / (2.0 * np.sqrt(m * k))
    poles = np.asarray(calculate_poles(zeta, omega_n), dtype=complex)
    
    pass_6 = np.allclose(np.sort_complex(eigs), np.sort_complex(poles), atol=1e-4)
    real_p = np.real(eigs[0])
    imag_p = abs(np.imag(eigs[0]))
    set_validation_row(6, f"eigs = {real_p:.0f} ± j{imag_p:.3f} = poles", pass_6)

run_validation_checks()
