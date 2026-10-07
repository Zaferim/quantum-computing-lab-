"""
Quantum Computing Lab
Tensor product foundations for quantum computing.
"""


def tensor_product(vector_a, vector_b):
    """
    Calculate the tensor product of two vectors.
    """

    result = []

    for value_a in vector_a:
        for value_b in vector_b:
            result.append(value_a * value_b)

    return result


def matrix_tensor_product(matrix_a, matrix_b):
    """
    Calculate the tensor product of two matrices.
    """

    result = []

    for row_a in matrix_a:

        for row_b in matrix_b:

            row = []

            for value_a in row_a:

                for value_b in row_b:
                    row.append(value_a * value_b)

            result.append(row)

    return result


def kron_power(vector, power):
    """
    Calculate the tensor product of a vector with itself.
    """

    if power < 1:
        raise ValueError("Power must be at least 1.")

    result = vector

    for _ in range(power - 1):
        result = tensor_product(result, vector)

    return result


if __name__ == "__main__":

    print("Tensor Products")
    print("===============")

    zero = [1, 0]
    one = [0, 1]

    print("|0> ⊗ |0> =", tensor_product(zero, zero))
    print("|0> ⊗ |1> =", tensor_product(zero, one))

    print(
        "|0> ⊗ |0> ⊗ |0> =",
        kron_power(zero, 3)
    )

    matrix = [
        [1, 0],
        [0, 1]
    ]

    print(
        "I ⊗ I =",
        matrix_tensor_product(matrix, matrix)
    )