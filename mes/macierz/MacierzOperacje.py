from typing import List

def sum_matrices(c_matrix_total: List[List[float]], h_matrix_total: List[List[float]]) -> List[List[float]]:
    """
    Sums the global matrices C and H to form [C]/dτ + [H].
    Operation required in the finite difference method.
    
    Args:
        c_matrix_total (list[list[float]]): Global matrix of thermal capacity [C]
        h_matrix_total (list[list[float]]): Global matrix of heat conduction [H]
        
    Returns:
        list[list[float]]: Suma macierzy [C]/dτ + [H]
        
    Note:
        Assumes that both matrices have the same dimensions (no_nodes x no_nodes)
    """
    # Getting the size of the matrix (number of nodes)
    no_nodes = len(c_matrix_total)
    # Initializing the result matrix with zeros
    total_matrix_sum = [[0] * no_nodes for _ in range(no_nodes)]

    # Summing the corresponding elements of the matrices
    for i in range(no_nodes):
        for j in range(no_nodes):
            total_matrix_sum[i][j] = c_matrix_total[i][j] + h_matrix_total[i][j]

    return total_matrix_sum

def sum_vectors(c_multiplied: List[float], p_vector: List[float]) -> List[float]:
    """
    Sums the vector {[C]/dτ}·{T0} with the vector {P}.
    Operation required in the finite difference method.
    
    Args:
        c_multiplied (list[float]): Vector obtained from multiplying [C]/dτ by {T0}
        p_vector (list[float]): Vector of thermal loads {P}
        
    Returns:
        list[float]: Sum of vectors {[C]/dτ}·{T0} + {P}
        
    Note:
        Assumes that both vectors have the same length (no_nodes)
    """
    # Getting the length of the vectors (number of nodes)
    no_nodes = len(c_multiplied)
    # Initializing the result vector with zeros
    total_vector_sum = [0] * no_nodes

    # Summing the corresponding elements of the vectors
    for i in range(no_nodes):
        total_vector_sum[i] = c_multiplied[i] + p_vector[i]

    return total_vector_sum