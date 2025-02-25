from mes.gauss.GaussianIntegral import GaussianIntegral
from mes.classes.Node import Node

# Funkcje obliczające pochodne funkcji kształtu względem ksi
def n1_ksi(eta):
    """Pochodna pierwszej funkcji kształtu względem ksi"""
    return -(1 / 4) * (1 - eta)

def n2_ksi(eta):
    """Pochodna drugiej funkcji kształtu względem ksi"""
    return (1 / 4) * (1 - eta)

def n3_ksi(eta):
    """Pochodna trzeciej funkcji kształtu względem ksi"""
    return (1 / 4) * (1 + eta)

def n4_ksi(eta):
    """Pochodna czwartej funkcji kształtu względem ksi"""
    return -(1 / 4) * (1 + eta)

# Funkcje obliczające pochodne funkcji kształtu względem eta
def n1_eta(ksi):
    """Pochodna pierwszej funkcji kształtu względem eta"""
    return -(1/4) * (1-ksi)

def n2_eta(ksi):
    """Pochodna drugiej funkcji kształtu względem eta"""
    return -(1/4) * (1+ksi)

def n3_eta(ksi):
    """Pochodna trzeciej funkcji kształtu względem eta"""
    return (1/4) * (1+ksi)

def n4_eta(ksi):
    """Pochodna czwartej funkcji kształtu względem eta"""
    return (1/4) * (1-ksi)


class UniversalElement:
    """
    Klasa implementująca element uniwersalny dla MES.
    Zawiera definicje funkcji kształtu i ich pochodnych w punktach całkowania.
    """
    
    def __init__(self, no_int_nodes):
        """
        Inicjalizacja elementu uniwersalnego.
        
        Args:
            no_int_nodes (int): Liczba węzłów całkowania w każdym kierunku
        """
        self.no_int_nodes = no_int_nodes
        self.temp = GaussianIntegral(no_int_nodes)
        
        # Inicjalizacja tablic pochodnych funkcji kształtu
        rows, cols = (4, no_int_nodes * no_int_nodes)
        self.ksi_derivatives = [[None for _ in range(cols)] for _ in range(rows)]
        self.eta_derivatives = [[None for _ in range(cols)] for _ in range(rows)]
        
        # Listy punktów całkowania i ich wag
        self.integration_points = []
        self.weights = []

        # Generowanie punktów całkowania i ich wag
        iterations = 1
        for i in range(no_int_nodes):
            for j in range(no_int_nodes):
                # Tworzenie punktu całkowania i jego wagi
                point = Node(iterations, self.temp.nodes[j], self.temp.nodes[i])
                weight = Node(iterations, self.temp.weights[j], self.temp.weights[i])
                self.integration_points.append(point)
                self.weights.append(weight)
                iterations += 1

        # Obliczanie pochodnych funkcji kształtu w punktach całkowania
        for i in range(cols):
            # Pochodne względem eta
            self.eta_derivatives[0][i] = n1_eta(self.integration_points[i].x)
            self.ksi_derivatives[0][i] = n1_ksi(self.integration_points[i].y)
            self.eta_derivatives[1][i] = n2_eta(self.integration_points[i].x)
            self.ksi_derivatives[1][i] = n2_ksi(self.integration_points[i].y)
            self.eta_derivatives[2][i] = n3_eta(self.integration_points[i].x)
            self.ksi_derivatives[2][i] = n3_ksi(self.integration_points[i].y)
            self.eta_derivatives[3][i] = n4_eta(self.integration_points[i].x)
            self.ksi_derivatives[3][i] = n4_ksi(self.integration_points[i].y)

    def print_ksi_array(self):
        """
        Wyświetla tablicę pochodnych funkcji kształtu względem ksi
        dla wszystkich punktów całkowania.
        """
        print("Ksi:")
        for col in range(self.no_int_nodes ** 2):
            for row in range(4):
                value = self.ksi_derivatives[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_eta_array(self):
        """
        Wyświetla tablicę pochodnych funkcji kształtu względem eta
        dla wszystkich punktów całkowania.
        """
        print("Eta:")
        for col in range(self.no_int_nodes ** 2):
            for row in range(4):
                value = self.eta_derivatives[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_integration_points(self):
        """
        Wyświetla współrzędne wszystkich punktów całkowania
        w elemencie uniwersalnym.
        """
        print("Integration Points: ")
        for i in range(len(self.integration_points)):
            value = self.integration_points[i]
            value.printNode()
        print()

