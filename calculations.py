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

#===========================
#Module 4: Guess the sensor
#===========================
def generate_random_sensor():
    sensor_type = np.random.choice(["first_order", "second_order"])
    if sensor_type == "first_order":
        K = np.random.uniform(1, 5)
        tau = np.random.uniform(0.5, 5)

        return {
            "type": sensor_type,
            "K": K,
            "tau": tau
        }
    elif sensor_type == "second_order":
        damping_type = np.random.choice([
            "underdamped",
            "critically_damped",
            "overdamped"
        ])
        if damping_type == "underdamped":
            zeta = np.random.uniform(0.2, 1)

        elif damping_type == "critically_damped":
            zeta = 1.0

        else:
            zeta = np.random.uniform(1, 2)

        omega_n = np.random.uniform(1, 10)
        return {
            "type": sensor_type,
            "damping_type": damping_type,
            "zeta": zeta,
            "omega_n": omega_n
        }


def generate_true_response(sensor, t, A=1.0, input_type="step", frequency=1.0):

    if sensor["type"] == "first_order":

        if input_type == "step":
            return calculate_step_response(
                sensor["K"], sensor["tau"], t, A
            )

        elif input_type == "sine":
            omega = 2 * np.pi * frequency

            M = 1 / np.sqrt(1 + (omega * sensor["tau"])**2)

            phi = np.arctan(omega * sensor["tau"])

            return sensor["K"] * A * M * np.sin(omega * t - phi)

        else:
            raise ValueError("Invalid input type")

    elif sensor["type"] == "second_order":

        return calculate_second_order_step_response(
            1.0, sensor["zeta"], sensor["omega_n"], t, A
        )

    else:
        raise ValueError("Invalid sensor type")



def add_noise(response, noise_level=0.02):
    noise = np.random.normal(
        0,
        noise_level * np.max(np.abs(response)),
        size=np.asarray(response).shape
    )

    return response + noise

def calculate_guess_error(true_value, guessed_value):
    if true_value == 0:
        raise ValueError("True value cannot be zero")

    return (abs(true_value - guessed_value) / abs(true_value)) * 100

def calculate_score(errors):
    score = 0

    for error in errors.values():
        if error <= 10:
            score += 50

    return score

def evaluate_guess(sensor, guessed_parameters):

    if sensor["type"] == "first_order":

        errors = {
            "K": calculate_guess_error(
                sensor["K"], guessed_parameters["K"]
            ),

            "tau": calculate_guess_error(
                sensor["tau"], guessed_parameters["tau"]
            )
        }

    elif sensor["type"] == "second_order":

        errors = {
            "zeta": calculate_guess_error(
                sensor["zeta"], guessed_parameters["zeta"]
            ),

            "omega_n": calculate_guess_error(
                sensor["omega_n"], guessed_parameters["omega_n"]
            )
        }

    else:
        raise ValueError("Invalid sensor type")

    score = calculate_score(errors)

    return errors, score

def update_running_score(total_score, rounds, new_score):

    total_score += new_score
    rounds += 1

    average_score = total_score / rounds

    return total_score, rounds, average_score

def generate_new_round(duration=10, points=100, noise_level=0.02):

    sensor = generate_random_sensor()

    input_type = "step"
    frequency = None

    if sensor["type"] == "first_order":
        input_type = np.random.choice(["step", "sine"])

        if input_type == "sine":
            frequency = np.random.uniform(0.1, 2)

    t = np.linspace(0, duration, points)

    true_response = generate_true_response(
        sensor, t,
        input_type=input_type,
        frequency=frequency if frequency is not None else 1.0
    )

    noisy_response = add_noise(true_response, noise_level)

    return sensor, t, true_response, noisy_response, input_type, frequency


def generate_hint(sensor, input_type="step"):

    if sensor["type"] == "first_order":

        if input_type == "step":
            return "At t = tau, the response reaches 63.2% of its final value."

        elif input_type == "sine":
            return "Amplitude ratio and phase lag depend on omega and tau."

    elif sensor["type"] == "second_order":

        return "Overshoot depends only on zeta, while peak time depends on zeta and omega_n."

    else:
        raise ValueError("Invalid sensor type")
