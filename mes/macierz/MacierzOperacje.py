def sum_matrices(c_matrix_total, h_matrix_total):
    """
    Sumuje globalne macierze C i H do postaci [C]/dτ + [H].
    Operacja wymagana w metodzie różnic skończonych.
    
    Args:
        c_matrix_total (list[list[float]]): Globalna macierz pojemności cieplnej [C]
        h_matrix_total (list[list[float]]): Globalna macierz przewodzenia ciepła [H]
        
    Returns:
        list[list[float]]: Suma macierzy [C]/dτ + [H]
        
    Note:
        Zakłada się, że obie macierze mają te same wymiary (no_nodes x no_nodes)
    """
    # Pobranie rozmiaru macierzy (liczba węzłów)
    no_nodes = len(c_matrix_total)
    # Inicjalizacja macierzy wynikowej zerami
    total_matrix_sum = [[0] * no_nodes for _ in range(no_nodes)]

    # Sumowanie odpowiadających sobie elementów macierzy
    for i in range(no_nodes):
        for j in range(no_nodes):
            total_matrix_sum[i][j] = c_matrix_total[i][j] + h_matrix_total[i][j]

    return total_matrix_sum

def sum_vectors(c_multiplied, p_vector):
    """
    Sumuje wektor {[C]/dτ}·{T0} z wektorem {P}.
    Operacja wymagana w metodzie różnic skończonych.
    
    Args:
        c_multiplied (list[float]): Wektor powstały z mnożenia [C]/dτ przez {T0}
        p_vector (list[float]): Wektor obciążeń cieplnych {P}
        
    Returns:
        list[float]: Suma wektorów {[C]/dτ}·{T0} + {P}
        
    Note:
        Zakłada się, że oba wektory mają tę samą długość (no_nodes)
    """
    # Pobranie długości wektorów (liczba węzłów)
    no_nodes = len(c_multiplied)
    # Inicjalizacja wektora wynikowego zerami
    total_vector_sum = [0] * no_nodes

    # Sumowanie odpowiadających sobie elementów wektorów
    for i in range(no_nodes):
        total_vector_sum[i] = c_multiplied[i] + p_vector[i]

    return total_vector_sum