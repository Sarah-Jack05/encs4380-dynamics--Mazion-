import matplotlib.pyplot as plt

from pyscript import document, display, when
from pid_core_p2_p3 import simulate_pid_sensor
from pid_core import compute_metrics

def update_p2(event=None):
    plant_type = "first_order"
    r_val = 1.0
    u_max = 10.0
    
    kp = float(document.getElementById("p2-kp").value)
    ki = float(document.getElementById("p2-ki").value)
    kd = float(document.getElementById("p2-kd").value)
    tau_s = float(document.getElementById("p2-taus").value)
    
    document.getElementById("p2-kp-val").innerText = f"{kp:.1f}"
    document.getElementById("p2-ki-val").innerText = f"{ki:.1f}"
    document.getElementById("p2-kd-val").innerText = f"{kd:.1f}"
    document.getElementById("p2-taus-val").innerText = f"{tau_s:.2f}"
    
    params = {"K": 1.0, "tau": 1.0}
    t, r, y, ys,u = simulate_pid_sensor(plant_type, params, kp, ki, kd, tau_s,
                                        setpoint=r_val, u_min=-u_max, u_max=u_max)    
    metrics = compute_metrics(t, y, r_val)
    document.getElementById("p2-os").innerText = str(metrics["overshoot"])
    document.getElementById("p2-ts").innerText = str(metrics["settling_time"])

    tail = y[-400:]
    if max(tail) - min(tail) > 0.05:
        status = "Oscillating"
    else:
        status = "Stable"
    document.getElementById("p2-status").innerText = status
    
    fig, ax = plt.subplots(figsize=(8, 4))    
    ax.plot(t, r, 'k--', label="Setpoint r(t)")
    ax.plot(t, y, 'b-', linewidth=2, label="True output y(t)")
    ax.plot(t, ys, 'r-', linewidth=2, label="Sensor reading")
    ax.axhline(r_val * 1.02, color='gray', linestyle=':', alpha=0.6)
    ax.axhline(r_val * 0.98, color='gray', linestyle=':', alpha=0.6)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Time (s)")
    ax.set_title("Slow Sensor in the Loop")
    ax.set_ylabel("Output")

    
    
    plt.tight_layout()
    plot_div = document.getElementById("p2-plot")
    plot_div.innerHTML = ""
    display(fig, target="p2-plot")
    plt.close(fig)

@when("input", "#p2-taus, #p2-kp, #p2-ki, #p2-kd")
def on_p2_slider(event):
    update_p2()

update_p2()



