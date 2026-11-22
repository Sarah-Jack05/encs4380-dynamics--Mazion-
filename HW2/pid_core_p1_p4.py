import numpy as np

############# Simulate_PID Starts #################
### Key Words: Parameters (Kp, Ki, Kd) and u(t): control signal and y(t): system response
def simulate_pid(plant_type, plant_params, Kp, Ki, Kd, setpoint=1.0, 
                 u_min=-10.0, u_max=10.0, dt=0.005, t_end=10.0, noise_std=0.0):
    t = np.arange(0, t_end + dt, dt)
    n = len(t)
    y = np.zeros(n)
    u = np.zeros(n)
    r = np.full(n, setpoint)
    
    x1, x2 = 0.0, 0.0
    integral = 0.0
    prev_error = setpoint - 0.0
    
    rng = np.random.default_rng(42) if noise_std > 0 else None

    for i in range(n):
        y_meas = x1 + (rng.normal(0, noise_std) if noise_std > 0 else 0.0)
        y[i] = y_meas
        
        error = r[i] - y_meas
        derivative = (error - prev_error) / dt if i > 0 else 0.0
        
        u_raw = Kp * error + Ki * integral + Kd * derivative
        u_sat = np.clip(u_raw, u_min, u_max)
        u[i] = u_sat
        
        if u_raw == u_sat:
            integral += error * dt
            
        prev_error = error
        
        if i < n - 1:
            if plant_type == "first_order":
                K, tau = plant_params["K"], plant_params["tau"]
                f = lambda val: (K * u_sat - val) / tau
                k1 = f(x1)
                k2 = f(x1 + 0.5 * dt * k1)
                k3 = f(x1 + 0.5 * dt * k2)
                k4 = f(x1 + dt * k3)
                x1 += (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
                
            elif plant_type == "second_order":
                m, b, k = plant_params["m"], plant_params["b"], plant_params["k"]
                def f2(s1, s2):
                    return s2, (u_sat - b * s2 - k * s1) / m
                k1_1, k1_2 = f2(x1, x2)
                k2_1, k2_2 = f2(x1 + 0.5*dt*k1_1, x2 + 0.5*dt*k1_2)
                k3_1, k3_2 = f2(x1 + 0.5*dt*k2_1, x2 + 0.5*dt*k2_2)
                k4_1, k4_2 = f2(x1 + dt*k3_1, x2 + dt*k3_2)
                x1 += (dt / 6.0) * (k1_1 + 2*k2_1 + 2*k3_1 + k4_1)
                x2 += (dt / 6.0) * (k1_2 + 2*k2_2 + 2*k3_2 + k4_2)

    return t, r, y, u
############# Simulate_PID Ends #################
############# compute_metrics Starts #################
## Key Words: extract 4 metrics required in P1-to show them directly
############# and P4 to judge (Fail/Pass) and these metrics are
################################################ Rise Time, Overshoot, Settling Time, Steady-state Error

def compute_metrics(t, y, setpoint):
    if setpoint == 0:
        return {"rise_time": "N/A", "overshoot": 0.0, "settling_time": "N/A", "ss_error": round(abs(y[-1]), 4)}
        
    y_norm = y / setpoint
    
    idx_10 = np.where(y_norm >= 0.1)[0]
    idx_90 = np.where(y_norm >= 0.9)[0]
    rise_time = (t[idx_90[0]] - t[idx_10[0]]) if (len(idx_10) > 0 and len(idx_90) > 0) else None
    
    peak = np.max(y_norm)
    overshoot = max(0.0, (peak - 1.0) * 100.0)
    
    out_of_band = np.where(np.abs(y_norm - 1.0) > 0.02)[0]
    if len(out_of_band) == 0:
        settling_time = 0.0
    elif out_of_band[-1] < len(t) - 1:
        settling_time = t[out_of_band[-1] + 1]
    else:
        settling_time = None
        
    ss_error = abs(setpoint - y[-1])
    
    return {
        "rise_time": round(rise_time, 3) if rise_time is not None else "N/A",
        "overshoot": round(overshoot, 2),
        "settling_time": round(settling_time, 3) if settling_time is not None else "Unsettled",
        "ss_error": round(ss_error, 4)
    }
