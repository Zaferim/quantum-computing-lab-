"""
Quantum Computing Lab
Linear algebra foundations for quantum computing.
"""


def matrix_vector_multiply(matrix, vector):
    """Multiply a matrix by a vector."""

    if not matrix:
        return []

    if len(matrix[0]) != len(vector):
        raise ValueError("Matrix and vector dimensions do not match.")

    result = []

    for row in matrix:
        value = 0

        for i in range(len(vector)):
            value += row[i] * vector[i]

        result.append(value)

    return result


def matrix_multiply(matrix_a, matrix_b):
    """Multiply two matrices."""

    if not matrix_a or not matrix_b:
        return []

    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Matrix dimensions do not match.")

    result = []

    for row in matrix_a:

        new_row = []

        for column in range(len(matrix_b[0])):

            value = 0

            for i in range(len(matrix_b)):
                value += row[i] * matrix_b[i][column]

            new_row.append(value)

        result.append(new_row)

    return result


def transpose(matrix):
    """Return the transpose of a matrix."""

    if not matrix:
        return []

    return [
        list(column)
        for column in zip(*matrix)
    ]


def identity_matrix(size):
    """Create an identity matrix."""

    if size <= 0:
        raise ValueError("Matrix size must be positive.")

    return [
        [
            1 if row == column else 0
            for column in range(size)
        ]
        for row in range(size)
    ]


if __name__ == "__main__":

    print("Linear Algebra")
    print("==============")

    matrix = [
        [1, 2],
        [3, 4]
    ]

    vector = [1, 1]

    print("Matrix:", matrix)
    print("Vector:", vector)

    print(
        "Matrix × Vector:",
        matrix_vector_multiply(matrix, vector)
    )

    print(
        "Transpose:",
        transpose(matrix)
    )

    print(
        "Identity Matrix:",
        identity_matrix(2)
    )