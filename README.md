# ENCS4380 – Dynamic Characteristics & PID Control Toolkit

Interactive toolkit for **ENCS4380 – Interfacing Techniques**, Birzeit University, under the supervision of Dr. Wasel Ghanem.

The project extends the original Dynamic Characteristics Toolkit (Homework 1) with PID Control features (Homework 2), combining mathematical calculations, Python simulations, interactive visualizations, and control-system analysis.

**Live site:** [https://sarah-jack05.github.io/encs4380-dynamics--Mazion-/](https://sarah-jack05.github.io/encs4380-dynamics--Mazion-/)

---

## Team

| Member | ID | Homework 1 Contribution | Homework 2 Contribution |
|---|---|---|---|
| Sarah Abd Al-Muhsen | 1230170 | Modules 1–4: Python calculations | Team contribution to PID Control Toolkit |
| Beesan Abutouq | 1230819 | Modules 1–4: Python plotting and simulations | Partner 3: My System, PID validation, motor parameter identification, and documentation |
| Omayma Altaweel | 1230099 | Modules 1–4: HTML, CSS, integration, and validation | Team contribution to the website integration |

---

## Homework 1 – Dynamic Characteristics Toolkit

Homework 1 focuses on understanding and analyzing the dynamic behavior of systems through four interactive modules.

### Project Files

- `index.html` – Main webpage containing the module cards, simulators, and validation table.
- `calculations.py` – Python reference calculations.
- `python/` – Jupyter/Colab simulations for Modules 1–4.
- `CSS_codes/` – Website and simulator styles.
- `validation.py` – Validation functions.
- `module1.py` – Module 1 calculations and simulation.
- `module2.py` – Module 2 calculations and simulation.
- `module3.py` – Module 3 calculations and simulation.
- `module4.py` – Module 4 calculations and simulation.
- `test_calculations.py` – Tests for the reference calculations.

### Main Features

- Dynamic system calculations and analysis.
- Python-based simulations and plots.
- Interactive modules for studying system behavior.
- Validation checks to verify mathematical results.

---

## Homework 2 – PID Control Toolkit

Homework 2 extends the toolkit by introducing feedback control and PID controller design.

The new control section covers four modules:

| Module | Description |
|---|---|
| P1 – PID Playground | Explore how proportional, integral, and derivative gains affect system response. |
| P2 – A Slow Sensor in the Loop | Study how sensor delay affects feedback control, overshoot, and oscillations. |
| P3 – Digital PID | Explore sampling time, digital control signals, anti-windup, and generated Arduino code. |
| P4 – Tuning Challenge | Tune PID gains to satisfy specified control-system performance requirements. |

### PID Validation Checks

The toolkit includes three required validation checks for the first-order plant:

\[
G(s)=\frac{K}{\tau s+1}
\]

Using \(K=1\) and \(\tau=1\) second:

1. **P-only controller:** With \(K_p=9\), verify a closed-loop time constant of 0.1 seconds and a steady-state error of 10%.
2. **PI controller:** With \(K_p=1\) and \(K_i=1\), verify a natural frequency of 1 rad/s and a damping ratio of 1.
3. **Zero steady-state error:** Verify that a PI controller eliminates steady-state error for a step input.

### Partner 3 – My System and PID Validation

Beesan Abutouq is responsible for the following Homework 2 tasks:

- Developing the My System section for the Micromouse project.
- Identifying the motor plant parameters \(K\) and \(\tau\) using PWM step-test data and encoder measurements.
- Designing and simulating the motor speed PID controller.
- Targeting a damping ratio between 0.6 and 0.8.
- Ensuring the PWM control signal remains within 0–100%.
- Implementing the required PID validation checks.
- Generating Arduino PID controller code.
- Preparing technical documentation and updating the project README.

### Motor Plant Model

The Micromouse drive motor is modeled as a first-order system:

\[
G(s)=\frac{K}{\tau s+1}
\]

The plant parameters are obtained from motor step-test measurements:

- \(K\): Motor steady-state gain.
- \(\tau\): Motor time constant.

The PID controller is designed using the identified plant parameters and evaluated through numerical simulation using the Euler method.

The controller includes PWM saturation and conditional integration anti-windup.

**Important:** Actual motor measurements must be used for the final plant model. Placeholder values used during software testing are not considered experimental measurements.

---

## Running the Project

The website is fully static and hosted using GitHub Pages.

### Run locally

1. Clone or download the repository.
2. Open `index.html` in a web browser.
3. An internet connection is required for external Plotly and KaTeX CDNs.

### Run Python simulations

Python simulations require the following libraries:

```bash
pip install numpy pandas matplotlib
```

Run a Python module using:

```bash
python filename.py
```

For the Micromouse motor identification, the CSV file must contain:

```csv
time_s,pwm_percent,speed_mm_s
```

The measurements should be collected from the actual motor using encoder feedback.

---

## GitHub and Deployment

The project uses GitHub for version control and GitHub Pages for hosting.

Homework 2 extends the existing repository rather than creating a separate project.

The final Homework 2 submission requires a GitHub release tagged:

```text
v2.0
```

The updated website should include a Control section linked from the landing page.

---

## AI Use

AI coding assistants were used to support development, debugging, and explanation of Python calculations and PID control code, as well as to assist with connecting Python simulations and calculations to the HTML interface.

All team members are responsible for understanding the code, mathematical equations, and simulation results included in the project and must be able to explain their contributions during the demonstration.

---

## Course Information

- **Course:** ENCS4380 – Interfacing Techniques
- **University:** Birzeit University
- **Instructor:** Dr. Wasel Ghanem
- **Project:** Dynamic Characteristics & PID Control Toolkit
- **Homework:** Homework 1 – Dynamic Characteristics; Homework 2 – PID Control Toolkit
