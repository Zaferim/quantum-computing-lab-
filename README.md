# Quantum Computing Lab

A Python-based laboratory for learning, implementing, and testing quantum computing algorithms.

## Project Goals

- Learn quantum computing fundamentals.
- Explore qubits, quantum gates, and quantum circuits.
- Implement quantum algorithms using Python and Qiskit.
- Verify mathematical results with automated tests.
- Study classical and quantum computational methods.

## Topics

- Python and Linear Algebra
- Probability Theory
- Qubits and Quantum Gates
- Quantum Circuits
- Qiskit
- Deutsch-Jozsa Algorithm
- Quantum Fourier Transform (QFT)
- Grover's Algorithm
- Shor's Algorithm
- Quantum Optimization
- Quantum Machine Learning

## Project Structure

```text
quantum-computing-lab/
├── quantum/
├── classical/
├── experiments/
├── tests/
├── README.md
├── pytest.ini
└── requirements.txt
Requirements

* Python 3.10 or newer is recommended.
* Git
* Python dependencies listed in requirements.txt

Installation

1. Clone the Repository

git clone https://github.com/Zaferim/quantum-computing-lab-.git
cd quantum-computing-lab-

2. Create a Virtual Environment

python -m venv .venv

3. Activate the Virtual Environment

On Linux or macOS:

source .venv/bin/activate

4. Install Dependencies

python -m pip install -r requirements.txt

Running Experiments

Quantum Fourier Transform

python -m experiments.qft

Shor Quantum Period Finding

python -m experiments.shor_quantum

Generalized Shor Algorithm

python -m experiments.shor_quantum_general

Controlled Modular Exponentiation

python -m experiments.shor_quantum_period

Running Tests

Run the complete test suite:

pytest -q

The latest verified test run completed with 87 passing tests.

Shor Algorithm Demonstration

The current simulator-based demonstration uses the following parameters:

* Number to factor: N = 15
* Base: a = 2
* Input register: 8 qubits
* Work register: 4 qubits
* Extracted period: r = 4

The input-register probability distribution has four peaks:

Input value	Probability
0	0.25
64	0.25
128	0.25
192	0.25

Classical post-processing derives the non-trivial factors:

15 = 3 × 5

This is an educational simulation. It does not claim to factor large numbers on real quantum hardware.

Development Status

The project includes implementations and automated tests for quantum computing experiments, including:

* Quantum Fourier Transform
* Grover’s algorithm
* Shor’s algorithm
* Quantum period finding
* Controlled modular exponentiation
* Classical period finding
* Generalized factorization experiments

Automated tests help verify mathematical behavior and prevent regressions.

Verification

After installing the dependencies, run:

pytest -q

To run the main Shor demonstration:

python -m experiments.shor_quantum

The expected demonstration result is:

15 = 3 × 5

Development Environment

The project can be developed locally or in GitHub Codespaces.

To continue working on another computer:

1. Sign in to GitHub.
2. Open the project repository.
3. Clone the repository or open it in GitHub Codespaces.
4. Install the required Python dependencies.
5. Run the tests before making further changes.

Always commit and push important changes to GitHub to keep the repository synchronized.

Limitations

The project is intended for education, experimentation, and research.

Quantum circuit simulations can become computationally expensive as the number of qubits increases. Successful simulation of small examples does not imply that the same computations can currently be performed efficiently on real quantum hardware.

License

No license has been specified yet. Contact the repository owner before reusing, modifying, or distributing this project.