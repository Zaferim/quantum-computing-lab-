from quantum.deutsch_jozsa import create_constant_oracle, create_balanced_oracle, run_algorithm

def test_constant_oracle():
    counts = run_algorithm(create_constant_oracle(), shots=100)
    assert counts == {"0": 100}

def test_balanced_oracle():
    counts = run_algorithm(create_balanced_oracle(), shots=100)
    assert counts == {"1": 100}

if __name__ == "__main__":
    test_constant_oracle()
    test_balanced_oracle()
    print("All Deutsch-Jozsa tests passed!")
