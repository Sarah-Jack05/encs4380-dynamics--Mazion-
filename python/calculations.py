import numpy as np

#===================================
#Module 1: First-Order Time Response
#===================================

def calculate_step_response(K,tau,t,A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")

    return K * A * (1 - np.exp(-np.asarray(t) / tau))

def calculate_ramp_response(K,tau,t,A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    
    return K * A * (np.asarray(t) - tau + tau*np.exp(-np.asarray(t) / tau))

def calculate_important_points(K,tau,A=1.0):
    t1=tau
    y1 = calculate_step_response(K,t1,tau,A)
    t2 = 3*tau
    y2 = calculate_step_response(K,tau,t2,A)

    return (t1, y1), (t2, y2)

def calculate_ramp_lag(tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return tau;

def calculate_steady_state_error(K,tau,A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return (K*A*tau)

def calculate_error_fraction(tau,t):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return np.exp(-np.asarray(t) / tau)

#====================================
#Module 2: First-Order Time Response
#====================================

def calculate_amplitude_ratio(omega, tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")

    return 1 / np.sqrt(1 + (omega * tau)**2)


def calculate_phase_lag(omega,tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    
    return np.degrees(-np.arctan(omega*tau))

def calculate_output_amplitude(tau,omega,A=1.0):    
    return (A*calculate_amplitude_ratio(omega,tau))

def calculate_cutoff_frequency(tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return (1/tau)

def calculate_dynamic_error(tau,omega):
    return (calculate_amplitude_ratio(omega,tau)-1)

