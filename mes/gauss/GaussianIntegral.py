from mes.gauss.GaussFunction import functionX, functionXY
import math

class GaussianIntegral:
    """
    Klasa implementująca całkowanie numeryczne metodą Gaussa.
    Obsługuje całkowanie jedno- i dwuwymiarowe dla różnej liczby węzłów (1-5).
    """
    
    def __init__(self, no_nodes):
        """
        Inicjalizacja kwadratury Gaussa dla zadanej liczby węzłów.
        
        Args:
            no_nodes (int): Liczba węzłów całkowania (1-5)
            
        Raises:
            ValueError: Gdy podana liczba węzłów nie jest obsługiwana (spoza zakresu 1-5)
        """
        self.no_nodes = no_nodes

        # Definicje węzłów i wag dla różnej liczby punktów całkowania
        if no_nodes == 1:
            # Całkowanie jednopunktowe
            self.nodes = [0]  # Węzeł w środku przedziału
            self.weights = [2]  # Waga dla węzła

        elif no_nodes == 2:
            # Całkowanie dwupunktowe
            self.nodes = [-(1 / math.sqrt(3)), 1 / math.sqrt(3)]  # Węzły symetryczne
            self.weights = [1, 1]  # Równe wagi dla obu węzłów

        elif no_nodes == 3:
            # Całkowanie trzypunktowe
            self.nodes = [-(math.sqrt(3 / 5)), 0, math.sqrt(3 / 5)]  # Węzły symetryczne + środek
            self.weights = [5 / 9, 8 / 9, 5 / 9]  # Wagi dla węzłów

        elif no_nodes == 4:
            # Całkowanie czteropunktowe
            self.nodes = [-(math.sqrt(3 / 7 + 2 / 7 * math.sqrt(6 / 5))),
                          -(math.sqrt(3 / 7 - 2 / 7 * math.sqrt(6 / 5))),
                          (math.sqrt(3 / 7 - 2 / 7 * math.sqrt(6 / 5))),
                          (math.sqrt(3 / 7 + 2 / 7 * math.sqrt(6 / 5)))]
            self.weights = [(18 - math.sqrt(30)) / 36, (18 + math.sqrt(30)) / 36,
                            (18 + math.sqrt(30)) / 36, (18 - math.sqrt(30)) / 36]

        elif no_nodes == 5:
            # Całkowanie pięciopunktowe
            self.nodes = [-math.sqrt(5 + 2 * math.sqrt(10 / 7)) / 3,
                          -math.sqrt(5 - 2 * math.sqrt(10 / 7)) / 3,
                          0,
                          math.sqrt(5 - 2 * math.sqrt(10 / 7)) / 3,
                          math.sqrt(5 + 2 * math.sqrt(10 / 7)) / 3]

            self.weights = [(322 - 13 * math.sqrt(70)) / 900,
                            (322 + 13 * math.sqrt(70)) / 900,
                            128 / 225,
                            (322 + 13 * math.sqrt(70)) / 900,
                            (322 - 13 * math.sqrt(70)) / 900]

        else:
            raise ValueError("Unsupported number of nodes.")

    def integrate1d(self):
        """
        Wykonuje całkowanie jednowymiarowe funkcji zdefiniowanej w functionX.
        
        Returns:
            float: Wynik całkowania jednowymiarowego
        """
        result = 0
        for i in range(self.no_nodes):
            result += functionX(self.nodes[i]) * self.weights[i]
        print(f"Integration result - {self.no_nodes} Nodes (1D): {result}")
        return result

    def integrate2d(self):
        """
        Wykonuje całkowanie dwuwymiarowe funkcji zdefiniowanej w functionXY.
        Wykorzystuje iloczyn tensorowy węzłów i wag dla obu wymiarów.
        
        Returns:
            float: Wynik całkowania dwuwymiarowego
        """
        result = 0
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weights[i] * self.weights[j]
        print(f"Integration result - {self.no_nodes} Nodes (2D): {result}")
        return result
