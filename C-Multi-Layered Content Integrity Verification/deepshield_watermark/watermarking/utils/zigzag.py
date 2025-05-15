#!/usr/bin/env python

"""zigzag.py: Perform zigzag and inverse zigzag traversal on a 2D matrix."""

import numpy as np


def zig_zag(mat: np.ndarray) -> np.ndarray:
    """Perform zigzag traversal on a 2D matrix.

    Parameters:
        mat (numpy.ndarray): A 2D matrix to perform zigzag traversal on.

    Returns:
        numpy.ndarray: The zigzag traversal of the matrix in 1D.

    Raises:
        ValueError: If the input matrix has more than 3 dimensions.
    """
    if mat.ndim != 2:
        raise ValueError("Input must be a 2-dimensional array.")

    rows, cols = mat.shape
    total_diagonals = rows + cols - 1  # Total number of diagonals

    # Initialize the zigzag list and pattern matrix
    zigzag_list = []  # List to store elements in zigzag order

    # Matrix to track positions, Counter for tracking the index in zigzag order
    pattern_matrix, counter = np.zeros((rows, cols)), 0

    for diagonal in range(total_diagonals):
        # Traverse upwards (bottom-left to top-right)
        if diagonal % 2 == 0:
            # Determine the start point of the upward diagonal
            r = min(diagonal, rows - 1)
            c = max(0, diagonal - rows + 1)

            # Iterate over the diagonal from bottom-left to top-right
            while r >= 0 and c < cols:
                zigzag_list.append(mat[r, c])
                pattern_matrix[r, c] = counter
                counter += 1
                r -= 1
                c += 1
        else:
            # Traverse downwards (top-right to bottom-left)
            # Determine the start point of the downward diagonal
            r = max(0, diagonal - cols + 1)
            c = min(diagonal, cols - 1)

            # Iterate over the diagonal from top-right to bottom-left
            while r < rows and c >= 0:
                zigzag_list.append(mat[r, c])
                pattern_matrix[r, c] = counter
                counter += 1
                r += 1
                c -= 1

    # Convert list to NumPy array
    zigzag = np.array(zigzag_list, dtype=float)
    return zigzag, pattern_matrix


def inverse_zigzag(input_array: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """
    Perform inverse zigzag traversal to reconstruct a 2D matrix from a 1D array.

    Parameters:
        input_array (numpy.ndarray): A 1D array to be transformed into a 2D matrix.
        rows (int): Number of rows in the output matrix.
        cols (int): Number of columns in the output matrix.

    Returns:
        numpy.ndarray: The reconstructed 2D matrix from the zigzag input.
    """
    if len(input_array) != rows * cols:
        raise ValueError("Input array size does not match the dimensions of the output matrix.")

    output_matrix = np.zeros((rows, cols), dtype=float)

    # Total number of diagonals
    total_diagonals = rows + cols - 1

    # Pointer for the input array
    index = 0

    for diag in range(total_diagonals):
        # Even diagonals move bottom-left to top-right
        if diag % 2 == 0:
            r = min(diag, rows - 1)
            c = max(0, diag - rows + 1)
            while r >= 0 and c < cols:
                output_matrix[r, c] = input_array[index]
                index += 1
                r -= 1
                c += 1
        else:
            # Odd diagonals move top-right to bottom-left
            r = max(0, diag - cols + 1)
            c = min(diag, cols - 1)
            while r < rows and c >= 0:
                output_matrix[r, c] = input_array[index]
                index += 1
                r += 1
                c -= 1

    return output_matrix
