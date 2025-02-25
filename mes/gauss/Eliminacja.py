def gaussian_elimination(matrix_c_h_summed, vectors_summed):
    """
    Implementation of the Gaussian elimination method to solve a system of linear equations.
    Used to calculate the temperature distribution in the nodes of the MES mesh.
    
    Args:
        matrix_c_h_summed (list[list[float]]): Matrix of coefficients of the system of equations (sum of matrices C and H)
        vectors_summed (list[float]): Free term vector
    
    Returns:
        list[float]: Solution vector (temperatures in nodes)
    """
    # Creating an extended matrix by combining the coefficient matrix with the free term vector
    augmented_matrix = [row + [val] for row, val in zip(matrix_c_h_summed, vectors_summed)]

    # Equalizing the length of all rows of the extended matrix
    max_row_length = max(len(row) for row in augmented_matrix)
    augmented_matrix = [row + [0] * (max_row_length - len(row)) for row in augmented_matrix]

    # Proper Gaussian elimination
    n = len(augmented_matrix)

    for i in range(n):
        # Finding the row with the largest element in column i (pivot)
        # Protection against division by zero by selecting the largest element
        pivot_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]) 
                       if isinstance(augmented_matrix[k][i], (int, float)) else 0)

        # Swapping the current row with the row containing the largest element
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]

        # Normalization of the row - division by the element on the diagonal
        pivot = augmented_matrix[i][i]
        augmented_matrix[i] = [x / pivot if isinstance(x, (int, float)) else x 
                              for x in augmented_matrix[i]]

        # Elimination of elements under and above the diagonal
        for j in range(n):
            if i != j:  # Skipping the row containing the pivot
                factor = augmented_matrix[j][i]
                # Subtracting the appropriate multiples of the row with the pivot
                augmented_matrix[j] = [x - factor * y if isinstance(x, (int, float)) else x 
                                     for x, y in zip(augmented_matrix[j], augmented_matrix[i])]

    # Extracting the solution vector (temperatures)
    temp_solution = [row[-1] for row in augmented_matrix]

    return temp_solution
