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

#====================================
#Module 3: Second-Order Time Response
#====================================
def calculate_damping_type(zeta):
    if zeta <= 0:
        raise ValueError("Damping Ratio must be positive")
    if (zeta < 1):
        return "Underdamped"
    elif (zeta == 1):
        return "Critically Damped"
    else: return "Overdamped"

def calculate_overshoot(zeta):
    if (calculate_damping_type(zeta) == "Underdamped"):
        return (np.exp((-np.pi*zeta)/np.sqrt(1-(zeta**2)))*100)
    return 0


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

    elif zeta == 1:
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


