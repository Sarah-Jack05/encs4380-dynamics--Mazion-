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

def calculate_poles(zeta, omega_n):
    if zeta <= 0:
        raise ValueError("Damping Ratio must be positive")
    if omega_n <= 0:
        raise ValueError("Natural Frequency must be positive")
    if (zeta < 1):
        return (-zeta*omega_n + omega_n*np.sqrt(1-(zeta**2))*1j,-zeta*omega_n - omega_n*np.sqrt(1-(zeta**2))*1j)
    
    if (zeta == 1):
        return (-zeta*omega_n,-zeta*omega_n)
        
    if (zeta > 1):
        return (-zeta*omega_n + omega_n*np.sqrt((zeta**2) - 1),-zeta*omega_n - omega_n*np.sqrt((zeta**2) - 1))

def calculate_state_space(m, b, k):
    if m <= 0:
        raise ValueError("Mass must be positive")
    
    if b < 0:
        raise ValueError("Damping Coefficient cannot be negative")
    
    if k <= 0:
        raise ValueError("Spring Stiffness must be positive")
    A = np.array([
        [0, 1],
        [-k/m, -b/m]
    ])

    B = np.array([
        [0],
        [1/m]
    ])

    return A, B

def calculate_eigenvalues(A):
    return np.linalg.eigvals(A)

def calculate_phase_plane(m, b, k, t, F=1.0):

    # Validation
    if m <= 0:
        raise ValueError("Mass must be positive")

    if b < 0:
        raise ValueError("Damping Coefficient cannot be negative")

    if k <= 0:
        raise ValueError("Spring Stiffness must be positive")

    t = np.asarray(t)

    # State-Space Matrices
    A, B = calculate_state_space(m, b, k)

    # System Parameters
    omega_n = np.sqrt(k / m)
    zeta = b / (2 * np.sqrt(m * k))

    # Displacement
    x1 = calculate_second_order_step_response(
        1/k, zeta, omega_n, t, A=F
    )

    # Velocity
    if zeta < 1:

        omega_d = omega_n * np.sqrt(1 - zeta**2)

        x2 = (F / k) * (
            omega_n / np.sqrt(1 - zeta**2)
        ) * np.exp(-zeta * omega_n * t) * np.sin(omega_d * t)

    elif zeta == 1:

        x2 = (F / k) * (omega_n**2) * t * np.exp(-omega_n * t)

    else:

        alpha = np.sqrt(zeta**2 - 1)

        x2 = (F / k) * (
            omega_n / (2 * alpha)
        ) * (
            np.exp(-omega_n * (zeta - alpha) * t)
            - np.exp(-omega_n * (zeta + alpha) * t)
        )

    return x1, x2



