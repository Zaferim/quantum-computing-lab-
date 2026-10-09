# Quantum Computing Lab — Project Status

## Project Information

- Repository: https://github.com/Zaferim/quantum-computing-lab-
- Main branch: main
- Last verified commit before this status file: e792277
- Project language: Python
- Main purpose: Educational implementation and testing of quantum computing algorithms.

## Latest Verified State

- Automated tests: 87 passed
- Git branch: main
- Local branch and origin/main were synchronized at commit e792277.
- README.md was updated and pushed to GitHub.
- An untracked local backup file exists: quantum/grover.py.bak
- Do not delete or commit the backup file without reviewing it first.

Important: The test count and repository state must be verified again when work resumes.

## Completed Work

- Quantum computing fundamentals and quantum circuit experiments
- Deutsch-Jozsa algorithm
- Quantum Fourier Transform (QFT)
- Grover's algorithm and amplitude amplification
- Classical period finding
- Shor's algorithm experiments
- Quantum period-finding experiments
- Generalized Shor algorithm experiments
- Controlled modular exponentiation
- Automated tests for quantum algorithms and supporting calculations
- Project documentation in README.md

## Shor Demonstration

The previously verified demonstration used:

- Number to factor: N = 15
- Base: a = 2
- Input register: 8 qubits
- Work register: 4 qubits
- Extracted period: r = 4
- Observed input-register peaks: 0, 64, 128, and 192
- Probability at each listed peak: 0.25
- Factors obtained during post-processing: 3 and 5

Expected demonstration result:

15 = 3 * 5

This is a small educational simulation. It does not demonstrate efficient factoring of large numbers on real quantum hardware.

## Important Project Files

- quantum/: Quantum computing implementations
- classical/: Classical algorithms and supporting calculations
- experiments/: Runnable algorithm demonstrations
- tests/: Automated tests
- README.md: Project overview and usage instructions
- requirements.txt: Python dependencies, if present
- pytest.ini: Pytest configuration, if present

## How to Resume Work

1. Open the GitHub repository or its Codespace.
2. Confirm the current directory and Git branch.
3. Inspect the latest commit and working-tree status.
4. Review this file and README.md.
5. Run the automated tests with:

   pytest -q

6. Run the Shor demonstration with:

   python -m experiments.shor_quantum

7. Review any failures before modifying the implementation.

## Git Safety Rules

- Work on the main branch unless a separate branch is deliberately created.
- Run tests before committing important changes.
- Commit and push completed work to GitHub regularly.
- Do not commit quantum/grover.py.bak without reviewing its contents.
- Check git status before and after each commit.
- Never assume a change has reached GitHub until git push succeeds.

## Potential Next Steps

- Review the overall project structure and identify missing documentation.
- Inspect algorithm implementations for mathematical correctness and edge cases.
- Improve test coverage where necessary.
- Verify installation instructions against the actual dependency files.
- Document the assumptions and limitations of each experiment.
- Continue with additional quantum algorithms only after verifying the existing work.

## Handoff Notes

This file records the last known project state. It is not a substitute for checking the actual repository, running tests, and verifying the latest Git history when resuming work.
