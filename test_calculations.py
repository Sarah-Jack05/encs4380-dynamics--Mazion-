# This file contains test cases only.
# All calculation functions are implemented in calculations.py.
# This file depends on calculations.py and cannot run independently.
# Make sure both files are in the same directory before running the tests.

#===============================================
#Testing Module 1 (Using AI-Generated Test Code)
#===============================================

#=================step response test=================#
#Test 1: Single time value
result = calculate_step_response(2, 3, 3)
print("Step response at t = tau:", result)
# Test 2: Multiple time values
time = np.arange(0, 10.1, 0.1)
response = calculate_step_response(2, 3, time)
print("First response:", response[0])
print("Response at tau:", response[30])
print("Response at 3tau:", response[90])


#====================ramp response test====================#
# Test 1: At t = 0
result = calculate_ramp_response(2, 3, 0)
print("Response at t = 0:", result)
# Test 2: At t = tau
result = calculate_ramp_response(2, 3, 3)
print("Response at t = tau:", result)
# Test 3: At t = 3*tau
result = calculate_ramp_response(2, 3, 9)
print("Response at t = 3tau:", result)
# Test 4: Multiple time values
time = np.arange(0, 10.1, 0.1)
response = calculate_ramp_response(2, 3, time)
print("First response:", response[0])
print("Response at tau:", response[30])
print("Response at 3tau:", response[90])



#===============important points test===============#
points = calculate_important_points(2, 3)
print("At tau:")
print("Time:", points[0][0])
print("Response:", points[0][1])
print("\nAt 3tau:")
print("Time:", points[1][0])
print("Response:", points[1][1])


#====================Ramp lag test====================#
lag = calculate_ramp_lag(3)
print("Ramp Lag:", lag)


#=============== steady state error test ==============#
error = calculate_steady_state_error(2, 3, 1)
print("Steady-State Error:", error)


#=============== error fraction test ===============#
# Test 1: At t = 0
print(calculate_error_fraction(3, 0))
# Test 2: At t = tau
print(calculate_error_fraction(3, 3))
# Test 3: At t = 3tau
print(calculate_error_fraction(3, 9))

################################################
#Expected Outputs for Module 1 calculation Code 
################################################
# Step response at t = tau: 1.2642411176571153
# First response: 0.0
# Response at tau: 1.2642411176571153
# Response at 3tau: 1.900425863264272
# Response at t = 0: 0.0
# Response at t = tau: 2.207276647028654
# Response at t = 3tau: 12.298722410207183
# First response: 0.0
# Response at tau: 2.207276647028654
# Response at 3tau: 12.298722410207183
# At tau:
# Time: 3
# Response: 1.2642411176571153

# At 3tau:
# Time: 9
# Response: 1.900425863264272
# Ramp Lag: 3
# Steady-State Error: 6
# 1.0
# 0.36787944117144233
# 0.049787068367863944



#===============================================
#Testing Module 2 (Using AI-Generated Test Code)
#===============================================

#=============== amplitude ratio test ===============#
print(calculate_amplitude_ratio(2, 0.2))

#=============== phase lag test ===============#
print(calculate_phase_lag(2, 0.2))

#=============== output amplitude test ===============#
print(calculate_output_amplitude(0.2, 2))
print(calculate_output_amplitude(0.2, 2, 5))

#=============== cutoff frequency test ===============#
print(calculate_cutoff_frequency(0.2))

#=============== dynamic error test ===============#
print(calculate_dynamic_error(0.2,2))


################################################
#Expected Outputs for Module 2 calculation Code 
################################################
# 0.9284766908852592
# -21.80140948635181
# 0.9284766908852592
# 4.642383454426296
# 5.0
# -0.07152330911474081


#===============================================
#Testing Module 3 (Using AI-Generated Test Code)
#===============================================

#=============== damping type test ===============#
print (calculate_damping_type(0.5))
print (calculate_damping_type(1))
print (calculate_damping_type(2))

#=============== overshoot test ===============#
print(calculate_overshoot(0.5))
print(calculate_overshoot(1))

#=======Testing Second-Order Step Response=======#
K = 2
omega_n = 2

# Test 1: Underdamped
result1 = calculate_second_order_step_response(
    K, 0.5, omega_n, np.array([0, 1, 5])
)

print("Underdamped:", result1)

# Test 2: Critically Damped
result2 = calculate_second_order_step_response(
    K, 1, omega_n, np.array([0, 1, 5])
)

print("Critically Damped:", result2)

# Test 3: Overdamped
result3 = calculate_second_order_step_response(
    K, 2, omega_n, np.array([0, 1, 5])
)

print("Overdamped:", result3)

#==========calculate poles test ==========#
#Underdamped
print(calculate_poles(0.5, 2))
#Critically Damped
print(calculate_poles(1, 2))
#Overdamped
print(calculate_poles(2, 2))

#==========calculate state space test ==========#

A, B = calculate_state_space(1, 2, 4)

print("Matrix A:")
print(A)

print("Matrix B:")
print(B)

#========== calculate eigenvalues test ==========#
print(calculate_eigenvalues(A))


#========== calculate phase plane test ==========#
t = np.linspace(0, 5, 101)

x1, x2 = calculate_phase_plane(
    m=1,
    b=4,
    k=4,
    t=t,
    F=1
)

print("Displacement (x1):", x1)
print("Velocity (x2):", x2)

print("Initial displacement:", x1[0])
print("Initial velocity:", x2[0])

print("Final displacement:", x1[-1])
print("Final velocity:", x2[-1])

x1, x2 = calculate_phase_plane(1, 1, 4, t, F=1)

print(x1)
print(x2)

x1, x2 = calculate_phase_plane(1, 6, 4, t, F=1)

print(x1)
print(x2)

t = np.linspace(0, 5, 101)

x1, x2 = calculate_phase_plane(1, 4, 4, t, F=1)

print("Initial x1:", x1[0])
print("Initial x2:", x2[0])

print("Final x1:", x1[-1])
print("Final x2:", x2[-1])

################################################
#Expected Outputs for Module 3 calculation Code 
################################################

# # =============== Damping Type Test ===============
# Underdamped
# Critically Damped
# Overdamped

# # =============== Overshoot Test ===============
# 16.303353482158048
# 0

# # =============== Second-Order Step Response Test ===============
# Underdamped: [0.         1.69885127 2.00434023]
# Critically Damped: [0.        1.1879883 1.9990012]
# Overdamped: [0.         0.73927996 1.85219186]

# # =============== Calculate Poles Test ===============
# Underdamped:
# (np.complex128(-1+1.7320508075688772j),
#  np.complex128(-1-1.7320508075688772j))

# Critically Damped:
# (-2, -2)

# Overdamped:
# (np.float64(-0.5358983848622456),
#  np.float64(-7.464101615137754))

# # =============== State Space Test ===============
# Matrix A:
# [[ 0.  1.]
#  [-4. -2.]]

# Matrix B:
# [[0.]
#  [1.]]

# # =============== Eigenvalues Test ===============
# [-1.+1.73205081j -1.-1.73205081j]

# # =============== Phase Plane Test ===============

# # Critically Damped
# Initial x1: 0.0
# Initial x2: 0.0
# Final x1: 0.24987515019315318
# Final x2: 0.00022699964881242428

# # Underdamped
# x1: Starts at 0, oscillates around 0.25
# x2: Starts at 0, changes sign and approaches 0

# # Overdamped
# x1: Starts at 0, increases gradually toward 0.25
# x2: Starts at 0, remains positive and approaches 0


#===============================================
#Testing Module 4 (Using AI-Generated Test Code)
#===============================================

print("\n========== MODULE 4 TESTING ==========")


# 1. Random Sensor Test
print("\n--- Random Sensor Test ---")

for i in range(5):
    sensor = generate_random_sensor()
    print(sensor)

    assert sensor["type"] in ["first_order", "second_order"]


# 2. First Order Response Test
print("\n--- First Order Response Test ---")

first_sensor = {
    "type": "first_order",
    "K": 3.0,
    "tau": 2.0
}

t = np.linspace(0, 10, 100)

step_response = generate_true_response(
    first_sensor, t
)

print("Step response at t=0:", step_response[0])
print("Step response at t=tau:",
      calculate_step_response(3, 2, 2))
print("Step response at final time:", step_response[-1])

assert np.isclose(step_response[0], 0)


# 3. First Order Sine Test
print("\n--- Sine Response Test ---")

sine_response = generate_true_response(
    first_sensor, t,
    input_type="sine",
    frequency=1.0
)

print("Sine response shape:", sine_response.shape)
print("First sine value:", sine_response[0])

assert sine_response.shape == t.shape


# 4. Second Order Response Test
print("\n--- Second Order Response Test ---")

second_sensor = {
    "type": "second_order",
    "damping_type": "underdamped",
    "zeta": 0.5,
    "omega_n": 2.0
}

second_response = generate_true_response(
    second_sensor, t
)

print("Response shape:", second_response.shape)
print("Initial response:", second_response[0])

assert second_response.shape == t.shape


# 5. Noise Test
print("\n--- Noise Test ---")

noisy_response = add_noise(step_response)

print("Original response:", step_response[:5])
print("Noisy response:", noisy_response[:5])

assert noisy_response.shape == step_response.shape


# 6. Guess Error Test
print("\n--- Guess Error Test ---")

error = calculate_guess_error(5, 5.5)

print("Expected error: 10%")
print("Actual error:", error)

assert np.isclose(error, 10)


# 7. Score Test
print("\n--- Score Test ---")

errors = {
    "K": 5,
    "tau": 15
}

score = calculate_score(errors)

print("Expected score: 50")
print("Actual score:", score)

assert score == 50


# 8. First Order Evaluation Test
print("\n--- First Order Evaluation Test ---")

first_guess = {
    "K": 3.0,
    "tau": 2.0
}

errors, score = evaluate_guess(
    first_sensor, first_guess
)

print("Errors:", errors)
print("Score:", score)

assert score == 100


# 9. Second Order Evaluation Test
print("\n--- Second Order Evaluation Test ---")

second_guess = {
    "zeta": 0.5,
    "omega_n": 2.0
}

errors, score = evaluate_guess(
    second_sensor, second_guess
)

print("Errors:", errors)
print("Score:", score)

assert score == 100


# 10. Running Score Test
print("\n--- Running Score Test ---")

total, rounds, average = update_running_score(
    100, 2, 50
)

print("Total score:", total)
print("Rounds:", rounds)
print("Average score:", average)

assert total == 150
assert rounds == 3
assert average == 50


# 11. Hint Test
print("\n--- Hint Test ---")

print("First Order Step:",
      generate_hint(first_sensor))

print("First Order Sine:",
      generate_hint(first_sensor, "sine"))

print("Second Order:",
      generate_hint(second_sensor))


# 12. New Round Test
print("\n--- New Round Test ---")

sensor, t, true_response, noisy_response, input_type, frequency = (
    generate_new_round()
)

print("Sensor:", sensor)
print("Input type:", input_type)
print("Frequency:", frequency)
print("Time points:", len(t))
print("True response shape:", true_response.shape)
print("Noisy response shape:", noisy_response.shape)

assert true_response.shape == t.shape
assert noisy_response.shape == t.shape

print("\n========== ALL TESTS COMPLETED ==========")


# ################################################
# #Expected Outputs for Module 4 calculation Code 
# ################################################
# ========== MODULE 4 TESTING ==========

# --- Random Sensor Test ---
# {'type': np.str_('first_order'), 'K': 1.0602338366092021, 'tau': 2.4671904382865666}
# {'type': np.str_('second_order'), 'damping_type': np.str_('underdamped'), 'zeta': 0.27402544252535393, 'omega_n': 2.3974543936372883}
# {'type': np.str_('first_order'), 'K': 4.6551852472728585, 'tau': 1.538794144894534}
# {'type': np.str_('first_order'), 'K': 3.183564167814539, 'tau': 1.875941759382544}
# {'type': np.str_('first_order'), 'K': 2.360092832336181, 'tau': 1.371797655433594}

# --- First Order Response Test ---
# Step response at t=0: 0.0
# Step response at t=tau: 1.896361676485673
# Step response at final time: 2.9797861590027437

# --- Sine Response Test ---
# Sine response shape: (100,)
# First sine value: -0.23723013724401812

# --- Second Order Response Test ---
# Response shape: (100,)
# Initial response: 0.0

# --- Noise Test ---
# Original response: [0.         0.14775262 0.28822829 0.42178542 0.54876474]
# Noisy response: [0.07118042 0.16731153 0.19985948 0.52334074 0.53227099]

# --- Guess Error Test ---
# Expected error: 10%
# Actual error: 10.0

# --- Score Test ---
# Expected score: 50
# Actual score: 50

# --- First Order Evaluation Test ---
# Errors: {'K': 0.0, 'tau': 0.0}
# Score: 100

# --- Second Order Evaluation Test ---
# Errors: {'zeta': 0.0, 'omega_n': 0.0}
# Score: 100

# --- Running Score Test ---
# Total score: 150
# Rounds: 3
# Average score: 50.0

# --- Hint Test ---
# First Order Step: At t = tau, the response reaches 63.2% of its final value.
# First Order Sine: Amplitude ratio and phase lag depend on omega and tau.
# Second Order: Overshoot depends only on zeta, while peak time depends on zeta and omega_n.

# --- New Round Test ---
# Sensor: {'type': np.str_('second_order'), 'damping_type': np.str_('critically_damped'), 'zeta': 1.0, 'omega_n': 6.235350502602804}
# Input type: step
# Frequency: None
# Time points: 100
# True response shape: (100,)
# Noisy response shape: (100,)

# ========== ALL TESTS COMPLETED ==========
