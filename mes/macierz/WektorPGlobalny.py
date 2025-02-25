from tabulate import tabulate

class WektorPGlobalny:
    """
    Klasa implementująca globalny wektor obciążeń cieplnych {P} dla całej siatki MES.
    Agreguje lokalne wektory obciążeń w jeden wektor globalny, uwzględniając połączenia między elementami.
    """
    
    def __init__(self, no_elements, no_nodes, p_vectors):
        """
        Inicjalizacja i agregacja globalnego wektora obciążeń cieplnych.
        
        Args:
            no_elements (int): Liczba elementów w siatce MES
            no_nodes (int): Liczba węzłów w siatce MES
            p_vectors (list): Lista lokalnych wektorów obciążeń dla każdego elementu
        """
        self.p_vectors = p_vectors
        # Inicjalizacja globalnego wektora P zerami
        self.p_vector_global = [0 for _ in range(no_nodes)]

        # Lista elementów skończonych i ich indeksów węzłów
        self.elements = []
        # Tablica indeksów węzłów dla każdego elementu (4 węzły na element)
        self.element_IDs = [[0] * 4 for _ in range(no_elements)]

        # Pobranie elementów z wektorów lokalnych
        for vector in self.p_vectors:
            self.elements.append(vector.element)

        # Utworzenie tablicy indeksów węzłów dla każdego elementu
        # Mapowanie lokalnych indeksów węzłów na globalne
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Agregacja wektorów lokalnych w wektor globalny
        for k in range(no_elements):
            p_vector = self.p_vectors[k].p_vector
            for i in range(4):
                # Mapowanie indeksu lokalnego na globalny (z korektą na indeksowanie od 0)
                global_index = self.element_IDs[k][i] - 1
                # Dodanie wartości z wektora lokalnego do odpowiedniej pozycji w wektorze globalnym
                self.p_vector_global[global_index] += p_vector[i]

    def print_global_vector(self):
        """
        Wyświetla globalny wektor P w sformatowanej tabeli.
        Używa biblioteki tabulate do formatowania wydruku.
        Pokazuje ID węzła i odpowiadającą mu wartość wektora P.
        """
        headers = ["Node ID", "P Vector Value"]
        table = [[i + 1, value] for i, value in enumerate(self.p_vector_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))