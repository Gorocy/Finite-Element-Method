from tabulate import tabulate

class MacierzCGlobalna:
    """
    Klasa implementująca globalną macierz pojemności cieplnej dla całej siatki MES.
    Agreguje lokalne macierze pojemności cieplnej w jedną macierz globalną.
    """
    
    def __init__(self, no_elements, no_nodes, c_matrices):
        """
        Inicjalizacja i agregacja globalnej macierzy pojemności cieplnej.
        
        Args:
            no_elements (int): Liczba elementów w siatce MES
            no_nodes (int): Liczba węzłów w siatce MES
            c_matrices (list[MacierzC]): Lista lokalnych macierzy pojemności cieplnej
        """
        self.no_nodes = no_nodes
        self.c_matrices = c_matrices
        self.elements = []  # Lista elementów skończonych
        # Tablica indeksów węzłów dla każdego elementu
        self.element_IDs = [[0] * 4 for _ in range(no_elements)]
        # Inicjalizacja globalnej macierzy C
        self.c_matrix_global = [[0] * no_nodes for _ in range(no_nodes)]

        # Pobranie elementów z macierzy lokalnych
        for matrix in self.c_matrices:
            self.elements.append(matrix.element)

        # Utworzenie tablicy indeksów węzłów dla każdego elementu
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Agregacja macierzy lokalnych w macierz globalną
        for k in range(no_elements):
            c_matrix = self.c_matrices[k].total_matrix
            for i in range(4):
                for j in range(4):
                    global_row = self.element_IDs[k][i]
                    global_col = self.element_IDs[k][j]
                    # Dodanie wartości z macierzy lokalnej do odpowiedniej pozycji w macierzy globalnej
                    self.c_matrix_global[global_row - 1][global_col - 1] += c_matrix[i][j]

    def print_global_matrix(self):
        """
        Wyświetla globalną macierz pojemności cieplnej w sformatowanej tabeli.
        Używa biblioteki tabulate do formatowania wydruku.
        """
        headers = [""] + list(range(1, self.no_nodes + 1))
        table = [[i + 1] + row for i, row in enumerate(self.c_matrix_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def divide_matrix_by_dtau(self, dtau):
        """
        Dzieli wszystkie elementy macierzy globalnej przez krok czasowy.
        Operacja wymagana w metodzie różnic skończonych.
        
        Args:
            dtau (float): Krok czasowy [s]
        """
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                self.c_matrix_global[i][j] /= dtau

    def multiply_matrix_by_vector(self, t0_vector):
        """
        Mnoży globalną macierz C przez wektor temperatur.
        
        Args:
            t0_vector (list[float]): Wektor temperatur w węzłach
            
        Returns:
            list[float]: Wektor wynikowy mnożenia macierzy przez wektor
        """
        result_vector = [0] * self.no_nodes
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                result_vector[i] += self.c_matrix_global[i][j] * t0_vector[j]
        return result_vector