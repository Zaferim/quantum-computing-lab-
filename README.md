# Quantum Computing Lab

A Python-based laboratory for learning, implementing, testing, and documenting quantum computing algorithms, quantum noise models, and error-correction techniques.

Repository: https://github.com/Zaferim/quantum-computing-lab-

Primary language: Python
Quantum framework: Qiskit
Testing framework: pytest
Development environment: GitHub Codespaces

---

1. Project Goals

The purpose of this project is to build a structured, testable laboratory for exploring quantum computing concepts and algorithms.

The main objectives are:

* Learn quantum computing fundamentals.
* Study qubits, quantum gates, quantum circuits, and measurement.
* Implement quantum algorithms using Python and Qiskit.
* Verify mathematical results with automated tests.
* Compare classical and quantum computational methods.
* Explore quantum period finding and factorization.
* Investigate quantum noise and bit-flip error correction.
* Model environmental disturbances using educational simulations.
* Explore mechanical resonance and its potential relationship to environmental disturbances.
* Maintain a reproducible development workflow using Git, GitHub, and pytest.

2. Topics Covered

Quantum Computing Fundamentals

* Python and linear algebra
* Complex numbers and probability
* Qubits and quantum states
* Quantum gates
* Quantum circuits
* Measurement and probability distributions
* Quantum Fourier Transform (QFT)

Quantum Algorithms

* Deutsch–Jozsa algorithm
* Grover’s algorithm
* Shor’s algorithm
* Quantum period finding
* Simon’s algorithm
* Quantum teleportation
* Superdense coding
* Variational Quantum Eigensolver (VQE)
* Quantum Approximate Optimization Algorithm (QAOA)

Noise and Error Correction

* Bit-flip noise simulation
* Three-bit repetition-code error correction
* Noise comparison experiments
* Environmental noise modeling
* Temperature and humidity effects
* Pressure and airflow disturbances
* Electromagnetic noise
* Voltage fluctuations
* Mechanical stress
* Mechanical resonance

---

3. Development Environment

The project is developed in GitHub Codespaces.

Project directory:

/workspaces/quantum-computing-lab-

Git branch:

main

GitHub repository:

https://github.com/Zaferim/quantum-computing-lab-

Basic Terminal Commands

Check the current directory:

pwd

Check the Git branch and working-tree status:

git status --short --branch

Display the project files:

find . -maxdepth 2 -type f -not -path './.git/*' | sort

Check the Python version:

python --version

Check the installed pytest version:

pytest --version

---

## 4. Project Structure

The project contains quantum algorithm implementations, supporting classical calculations, experiments, and automated tests.

quantum-computing-lab-/
├── quantum/
│   ├── deutsch_jozsa.py
│   ├── qft.py
│   ├── grover.py
│   ├── error_correction.py
│   ├── noise.py
│   ├── noise_experiment.py
│   ├── environmental_noise.py
│   └── environmental_experiment.py
├── classical/
├── experiments/
├── tests/
│   ├── test_error_correction.py
│   ├── test_noise.py
│   ├── test_noise_experiment.py
│   └── test_environmental_noise.py
├── README.md
├── pytest.ini
└── requirements.txt

Important: This is a representative structure, not a guaranteed complete file listing. The repository may contain additional modules and test files, including Shor, Simon, teleportation, superdense coding, VQE, and QAOA implementations. Use the actual project directory to verify the complete current structure.

---

## 5. Installation and Setup

Step 1: Open the Project

Open the GitHub Codespace associated with the repository.

cd /workspaces/quantum-computing-lab-

Step 2: Install Dependencies

python -m pip install -r requirements.txt

Step 3: Run the Tests

pytest -q

Step 4: Check the Git Status

git status --short --branch

These commands establish the working directory, install the declared dependencies, run the automated tests, and display the current Git state.

---

## 6. Quantum Algorithm Experiments

The project includes implementations and experiments covering several important quantum algorithms.

Deutsch–Jozsa Algorithm

Explores how a quantum circuit can distinguish between constant and balanced Boolean functions under the algorithm’s promised conditions.

Quantum Fourier Transform

Studies the quantum Fourier Transform and its role in quantum period-finding algorithms.

Grover’s Algorithm

Explores amplitude amplification and the enhancement of the probability of measuring a marked state.

Shor’s Algorithm

Studies integer factorization through quantum period finding, followed by classical post-processing.

Additional Algorithms

The project also contains work involving Simon’s algorithm, quantum teleportation, superdense coding, VQE, and QAOA.

For the precise implementation and current status of each algorithm, inspect its corresponding Python module and tests.

---

## 7. Quantum Noise Simulation

The module quantum/noise.py provides functionality for simulating bit-flip noise.

The work includes:

* Applying bit-flip noise to computational-basis states.
* Simulating noise under specified conditions.
* Examining how noise probability affects measurement outcomes.

The related test file is:

tests/test_noise.py

The implementation is an educational simulation. It should not be interpreted as a complete physical model of noise in real quantum hardware.

Run the Noise Tests

pytest -q tests/test_noise.py

---

## 8. Quantum Error Correction

The module quantum/error_correction.py implements a three-bit repetition-code approach to correcting bit-flip errors in computational-basis information.

Related tests:

tests/test_error_correction.py

The educational experiment examines how redundancy can help recover a computational-basis bit when a correctable bit-flip error occurs.

Important Limitation

The current repetition-code implementation is limited to the bit-flip correction model described by the code. It should not be presented as a complete quantum error-correction system.

In particular, correcting computational-basis bit-flip errors is not equivalent to correcting arbitrary quantum states or all possible phase and general quantum errors.

Run the Error-Correction Tests

pytest -q tests/test_error_correction.py

---

## 9. Noise Comparison Experiment

The module quantum/noise_experiment.py compares a single-bit approach with a three-bit repetition-code approach under bit-flip noise.

Related tests:

tests/test_noise_experiment.py

The purpose is to explore how redundancy and error correction can affect outcomes under the simulated conditions.

Run the Experiment Tests

pytest -q tests/test_noise_experiment.py

The experiment’s conclusions apply to the model and assumptions implemented in the project, rather than automatically generalizing to real quantum processors.

---

## 10. Environmental Noise Model

The module quantum/environmental_noise.py provides an illustrative model for estimating an environmental noise probability from a collection of environmental conditions.

The model can consider factors such as:

* Vibration amplitude
* Vibration frequency deviation
* Vibration duration
* Vibration forcing frequency
* Mechanical natural frequency
* Damping ratio
* Temperature deviation
* Temperature change rate
* Humidity
* Pressure
* Airflow
* Electromagnetic noise
* Voltage fluctuations
* Mechanical stress

The estimator combines the configured contributions into an estimated probability.

The main interface includes:

estimate_environmental_noise(conditions, weights=None)

The result is represented by an EnvironmentalNoiseResult, which contains the estimated probability and contribution information.

Scientific Limitation

This is an educational model. Its inputs, weights, and probability calculations are not calibrated against experimental measurements from a specific quantum processor.

Consequently, its output must not be interpreted as a validated prediction of the error rate of real quantum hardware.

---

## 11. Mechanical Resonance

The environmental model includes a simplified mechanical resonance calculation.

The function is:

resonance_factor(frequency_hz, natural_frequency_hz, damping_ratio)

Its inputs represent:

* Forcing frequency: the frequency of the applied mechanical disturbance, in hertz.
* Natural frequency: the natural frequency of the modeled mechanical system, in hertz.
* Damping ratio: a dimensionless parameter describing damping in the simplified model.

The model uses the relationship between forcing frequency and natural frequency to represent the potential amplification associated with mechanical resonance.

The resonance calculation is a simplified single-degree-of-freedom model. It is not a complete structural, mechanical, or quantum-device simulation.

Run the Environmental Noise Tests

pytest -q tests/test_environmental_noise.py

---

## 12. Environmental Noise Experiments

The module quantum/environmental_experiment.py contains experiments using the environmental noise model.

The experiments are intended to compare illustrative environmental scenarios and explore how changing model inputs can affect the estimated noise probability.

The results depend on the assumptions, parameters, and calculations defined in the implementation.

They do not establish that any particular environmental factor causes a measured error rate in a real quantum processor.

---

## 13. Shor’s Algorithm: N = 15, a = 2

One of the project’s demonstrations examines the classical and quantum concepts behind Shor’s factorization algorithm.

The example uses:

* Integer to factor: N = 15
* Base: a = 2
* Input register: 8 qubits
* Work register: 4 qubits
* Expected period: r = 4

Classical Period Finding

The period is the smallest positive integer r satisfying:

a^r mod N = 1

For the example:

* 2^1 mod 15 = 2
* 2^2 mod 15 = 4
* 2^3 mod 15 = 8
* 2^4 mod 15 = 1

Therefore, the period is:

r = 4

Expected Quantum Fourier Transform Peaks

For an 8-qubit input register, the measurement distribution associated with an idealized period-four example has expected peaks at the following indices:

Measurement index	Expected probability
0	0.25
64	0.25
128	0.25
192	0.25

These values describe the expected idealized distribution for the stated example. Actual simulation results depend on the circuit, measurement procedure, and implementation details.

Classical Post-Processing

Since r = 4 is even, calculate:

a^(r/2) = 2^2 = 4

Then:

* gcd(4 - 1, 15) = gcd(3, 15) = 3
* gcd(4 + 1, 15) = gcd(5, 15) = 5

The non-trivial factors are:

15 = 3 × 5

This small example demonstrates the relationship between period finding and classical factor extraction.

---

## 14. Automated Testing

The project uses pytest to verify the behavior of its modules.

Run the Complete Test Suite

pytest -q

Run a Specific Test File

For example:

pytest -q tests/test_environmental_noise.py

Check Which Tests Exist

find tests -maxdepth 2 -type f | sort

Recorded Test Result

The latest recorded full-suite result before this README update was:

286 tests passed.

This is a historical checkpoint, not a claim that the current working tree has already been tested after every subsequent change.

After modifying code, rerun the tests and update this section only after verifying the actual result.

---

## 15. Git and GitHub Workflow

The project uses Git for version control and GitHub for remote storage.

Step 1: Inspect the Working Tree

git status --short

Step 2: Review Changes

git diff --check
git diff --stat

Step 3: Stage Only the Intended Files

For example, when only the README should be committed:

git add README.md

Do not stage unrelated files unintentionally.

In particular, preserve quantum/grover.py.bak. Do not delete it or include it in a commit unless there is a specific, separately agreed reason to do so.

Step 4: Check the Staged Changes

git diff --cached --check
git diff --cached --stat

Step 5: Commit the Changes

git commit -m "Update project documentation"

Step 6: Push to GitHub

git push origin main

Step 7: Verify the Result

git status --short --branch
git log -1 --oneline


---

## 16. Development Status

The project has progressed through several stages:

1. Quantum algorithm implementations and experiments.
2. Automated testing of the algorithm modules.
3. Bit-flip noise simulation.
4. Three-bit repetition-code error correction for the implemented computational-basis model.
5. Comparison experiments for noise and error correction.
6. An illustrative environmental noise estimator.
7. A simplified mechanical resonance calculation.
8. Environmental noise experiment scenarios.
9. Documentation and verification through Git and GitHub.

The repository’s actual source code, tests, and Git history remain the authoritative record of which features are currently implemented and committed.

---

## 17. Known Limitations

The project is primarily an educational and experimental laboratory.

Important limitations include:

* Simulations are not automatically equivalent to physical quantum hardware.
* Environmental noise estimates are illustrative unless calibrated against experimental data.
* The repetition-code implementation does not provide universal quantum error correction.
* Idealized algorithm demonstrations may differ from results obtained with noisy circuits or different simulator configurations.
* A successful test suite establishes that the tested behavior passes the current tests; it does not establish that a model is physically accurate.
* Feature descriptions must be kept consistent with the current implementation.

---

## 18. Future Development

Potential next steps include:

* Expanding quantum algorithm tests.
* Improving experiment documentation.
* Adding reproducible benchmark reports.
* Comparing different noise models.
* Extending error-correction experiments.
* Validating environmental models against suitable experimental data.
* Improving plots and experiment output summaries.
* Recording software versions and simulation parameters.
* Maintaining regular Git commits and remote backups.

These are possible future improvements, not claims that the features have already been implemented.

---

## 19. License

Check the repository for an existing license file before distributing or reusing the project.

If no license has been added, the project’s reuse and redistribution terms have not yet been explicitly established.
