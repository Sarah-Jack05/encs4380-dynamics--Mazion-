# PID Playground

import matplotlib.pyplot as plt
from pyscript import document, display, when
from pid_core import simulate_pid, compute_metrics

def update_p1(event=None):
    plant_type = document.getElementById("p1-plant").value
    r_val = float(document.getElementById("p1-r").value or 1.0)
    u_max = float(document.getElementById("p1-umax").value or 10.0)
    
    kp = float(document.getElementById("p1-kp").value)
    ki = float(document.getElementById("p1-ki").value)
    kd = float(document.getElementById("p1-kd").value)
    
    document.getElementById("p1-kp-val").innerText = f"{kp:.1f}"
    document.getElementById("p1-ki-val").innerText = f"{ki:.1f}"
    document.getElementById("p1-kd-val").innerText = f"{kd:.1f}"
    
    params = {"K": 1.0, "tau": 1.0} if plant_type == "first_order" else {"m": 1.0, "b": 2.0, "k": 4.0}
    t, r, y, u = simulate_pid(plant_type, params, kp, ki, kd, setpoint=r_val, u_min=-u_max, u_max=u_max)
    
    metrics = compute_metrics(t, y, r_val)
    document.getElementById("p1-tr").innerText = str(metrics["rise_time"])
    document.getElementById("p1-os").innerText = str(metrics["overshoot"])
    document.getElementById("p1-ts").innerText = str(metrics["settling_time"])
    document.getElementById("p1-ess").innerText = str(metrics["ss_error"])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    
    # الرسم العلوي: الاستجابة y(t)
    ax1.plot(t, r, 'k--', label="Setpoint r(t)")
    ax1.plot(t, y, 'b-', linewidth=2, label="Output y(t)")
    ax1.axhline(r_val * 1.02, color='gray', linestyle=':', alpha=0.6)
    ax1.axhline(r_val * 0.98, color='gray', linestyle=':', alpha=0.6)
    ax1.set_ylabel("Output y(t)")
    ax1.set_title("Closed-Loop Step Response")
    ax1.legend(loc="lower right")
    ax1.grid(True, alpha=0.3)
    
    # الرسم السفلي: إشارة التحكم u(t)
    ax2.plot(t, u, 'g-', linewidth=2, label="Control Signal u(t)")
    ax2.axhline(u_max, color='r', linestyle='--', label="Actuator Limit (±u_max)")
    ax2.axhline(-u_max, color='r', linestyle='--')
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Control u(t)")
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_div = document.getElementById("p1-plot")
    plot_div.innerHTML = ""
    display(fig, target="p1-plot")
    plt.close(fig)

@when("input", "#p1-kp, #p1-ki, #p1-kd, #p1-r, #p1-umax")
def on_p1_slider(event):
    update_p1()

@when("change", "#p1-plant")
def on_p1_select(event):
    update_p1()

update_p1()
