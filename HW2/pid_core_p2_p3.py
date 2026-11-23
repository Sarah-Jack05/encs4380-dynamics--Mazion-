import numpy as np

def simulate_pid_sensor(plant_type, plant_params, Kp, Ki, Kd, tau_s, setpoint=1.0,
                        u_min=-10.0, u_max=10.0, dt=0.005, t_end=10.0, noise_std=0.0):
    t = np.arange(0, t_end + dt, dt)
    n = len(t)
    y = np.zeros(n)
    u = np.zeros(n)
    ys = np.zeros(n)
    r = np.full(n, setpoint)
    
    x1, x2,xs = 0.0, 0.0 ,0.0
    integral = 0.0
    prev_error = setpoint - xs
    
    rng = np.random.default_rng(42) if noise_std > 0 else None

    for i in range(n):
        y[i] = x1
        ys[i] = xs + (rng.normal(0, noise_std) if noise_std > 0 else 0.0)
        
        error = r[i] - ys[i]
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
            if (tau_s < dt):
                xs = x1
            else: xs += dt * (x1 - xs) / tau_s

    return t, r, y, ys,u
    
#def simulate_pid_digital():