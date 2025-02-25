from tabulate import tabulate

class MacierzHGlobalna:
    """
    Klasa implementująca globalną macierz przewodzenia ciepła [H] dla całej siatki MES.
    Agreguje lokalne macierze H w jedną macierz globalną, uwzględniając połączenia między elementami.
    """
    
    def __init__(self, no_elements, no_nodes, h_matrices):
        """
        Inicjalizacja i agregacja globalnej macierzy przewodzenia ciepła.
        
        Args:
            no_elements (int): Liczba elementów w siatce MES
            no_nodes (int): Liczba węzłów w siatce MES
            h_matrices (list[MatrixH]): Lista lokalnych macierzy H dla każdego elementu
        """
        self.no_nodes = no_nodes
        self.h_matrices = h_matrices
        self.elements = []  # Lista elementów skończonych
        # Tablica indeksów węzłów dla każdego elementu (4 węzły na element)
        self.element_IDs = [[0] * 4 for _ in range(no_elements)]
        # Inicjalizacja globalnej macierzy H zerami
        self.h_matrix_global = [[0] * no_nodes for _ in range(no_nodes)]

        # Pobranie elementów z macierzy lokalnych
        for matrix in self.h_matrices:
            self.elements.append(matrix.element)

        # Utworzenie tablicy indeksów węzłów dla każdego elementu
        # Mapowanie lokalnych indeksów węzłów na globalne
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Agregacja macierzy lokalnych w macierz globalną
        for k in range(no_elements):
            h_matrix = self.h_matrices[k].total_matrix
            for i in range(4):
                for j in range(4):
                    # Mapowanie indeksów lokalnych (0-3) na globalne (1-n)
                    global_row = self.element_IDs[k][i]
                    global_col = self.element_IDs[k][j]
                    # Dodanie wartości z macierzy lokalnej do odpowiedniej pozycji w macierzy globalnej
                    self.h_matrix_global[global_row - 1][global_col - 1] += h_matrix[i][j]

    def print_global_matrix(self):
        """
        Wyświetla globalną macierz H w sformatowanej tabeli.
        Używa biblioteki tabulate do formatowania wydruku.
        Numeruje wiersze i kolumny zgodnie z globalnymi indeksami węzłów.
        """
        headers = [""] + list(range(1, self.no_nodes + 1))
        table = [[i + 1] + row for i, row in enumerate(self.h_matrix_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))
