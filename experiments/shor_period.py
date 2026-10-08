"""
Shor's Algorithm - Classical Period Finding
First experiment: N = 15, a = 2

Find the smallest r such that:

    a^r ≡ 1 (mod N)
"""

from math import gcd


def find_period(a: int, N: int) -> int:
    """Find the multiplicative order (period) of a modulo N."""
    if N <= 1:
        raise ValueError("N must be greater than 1.")

    if gcd(a, N) != 1:
        raise ValueError("a and N must be coprime.")

    value = 1

    for r in range(1, N + 1):
        value = (value * a) % N

        if value == 1:
            return r

    raise RuntimeError("Period not found.")


def main() -> None:
    N = 15
    a = 2

    print("Shor's Algorithm - Classical Period Finding")
    print("---------------------------------------------")
    print(f"N = {N}")
    print(f"a = {a}")
    print()

    print("Powers modulo N:")

    for x in range(1, 9):
        result = pow(a, x, N)
        print(f"{a}^{x} mod {N} = {result}")

    r = find_period(a, N)

    print()
    print(f"Period r = {r}")
    print(f"Verification: {a}^{r} mod {N} = {pow(a, r, N)}")

    assert r == 4
    assert pow(a, r, N) == 1

    print()
    print("✓ Classical period-finding test passed.")


if __name__ == "__main__":
    main()


def factor_from_period(a: int, N: int, r: int) -> tuple[int, int]:
    """Derive non-trivial factors of N from an even period r."""
    if r % 2 != 0:
        raise ValueError("Period r must be even.")

    x = pow(a, r // 2, N)

    factor1 = gcd(x - 1, N)
    factor2 = gcd(x + 1, N)

    if factor1 in (1, N) or factor2 in (1, N):
        raise ValueError("Period did not produce non-trivial factors.")

    return factor1, factor2


def factorization_demo() -> None:
    N = 15
    a = 2
    r = find_period(a, N)

    factor1, factor2 = factor_from_period(a, N, r)

    print()
    print("Classical Shor factorization")
    print("----------------------------")
    print(f"r = {r}")
    print(f"a^(r/2) mod N = {pow(a, r // 2, N)}")
    print(f"gcd(a^(r/2) - 1, N) = {factor1}")
    print(f"gcd(a^(r/2) + 1, N) = {factor2}")
    print(f"{N} = {factor1} × {factor2}")

    assert {factor1, factor2} == {3, 5}

    print("✓ Classical Shor factorization test passed.")


if __name__ == "__main__":
    factorization_demo()
