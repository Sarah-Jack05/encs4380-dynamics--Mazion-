#======================================
#Testing (Using AI-Generated Test Code)
#======================================

from 
 
#=================step response test=================#
# Test 1: Single time value
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


#=============== error fraction===============#
# Test 1: At t = 0
print(calculate_error_fraction(3, 0))
# Test 2: At t = tau
print(calculate_error_fraction(3, 3))
# Test 3: At t = 3tau
print(calculate_error_fraction(3, 9))
