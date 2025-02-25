def gaussian_elimination(matrix_c_h_summed, vectors_summed):
    """
    Implementacja metody eliminacji Gaussa do rozwiązywania układu równań liniowych.
    Używana do obliczenia rozkładu temperatur w węzłach siatki MES.
    
    Args:
        matrix_c_h_summed (list[list[float]]): Macierz współczynników układu równań (suma macierzy C i H)
        vectors_summed (list[float]): Wektor wyrazów wolnych
    
    Returns:
        list[float]: Wektor rozwiązań (temperatury w węzłach)
    """
    # Utworzenie macierzy rozszerzonej przez połączenie macierzy współczynników z wektorem wyrazów wolnych
    augmented_matrix = [row + [val] for row, val in zip(matrix_c_h_summed, vectors_summed)]

    # Wyrównanie długości wszystkich wierszy macierzy rozszerzonej
    max_row_length = max(len(row) for row in augmented_matrix)
    augmented_matrix = [row + [0] * (max_row_length - len(row)) for row in augmented_matrix]

    # Właściwa eliminacja Gaussa
    n = len(augmented_matrix)

    for i in range(n):
        # Znajdowanie wiersza z największym elementem w kolumnie i (pivot)
        # Zabezpieczenie przed dzieleniem przez zero poprzez wybór największego elementu
        pivot_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]) 
                       if isinstance(augmented_matrix[k][i], (int, float)) else 0)

        # Zamiana miejscami bieżącego wiersza z wierszem zawierającym największy element
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]

        # Normalizacja wiersza - dzielenie przez element na przekątnej
        pivot = augmented_matrix[i][i]
        augmented_matrix[i] = [x / pivot if isinstance(x, (int, float)) else x 
                              for x in augmented_matrix[i]]

        # Eliminacja elementów pod i nad przekątną
        for j in range(n):
            if i != j:  # Pomijamy wiersz zawierający pivot
                factor = augmented_matrix[j][i]
                # Odejmowanie odpowiednich wielokrotności wiersza z pivotem
                augmented_matrix[j] = [x - factor * y if isinstance(x, (int, float)) else x 
                                     for x, y in zip(augmented_matrix[j], augmented_matrix[i])]

    # Wyodrębnienie wektora rozwiązań (temperatur)
    temp_solution = [row[-1] for row in augmented_matrix]

    return temp_solution
