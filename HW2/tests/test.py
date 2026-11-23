from pid_core_p2_p3 import simulate_pid_sensor
from pid_core_p1_p4 import compute_metrics

#pid_core_p2_p3.py test
plant = {"K": 1.0, "tau": 1.0}

for tau_s in [0.0, 0.5, 2.0]:
    t, r, y, ys, u = simulate_pid_sensor(
        "first_order", plant, Kp=9, Ki=0, Kd=0, tau_s=tau_s
    )
    m = compute_metrics(t, y, 1.0)
    print("tau_s =", tau_s, m)
