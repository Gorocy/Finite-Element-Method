from mes.gauss.GaussFunction import functionX, functionXY
import math

class GaussianIntegral2Nodes:
    """
    Klasa implementująca dwupunktową kwadraturę Gaussa.
    Specjalizowana wersja dla dokładnie dwóch węzłów całkowania,
    używana do całkowania jedno- i dwuwymiarowego.
    """
    
    def __init__(self):
        """
        Inicjalizacja dwupunktowej kwadratury Gaussa.
        Węzły są symetryczne względem środka przedziału [-1,1],
        a wagi są równe 1 dla obu węzłów.
        """
        self.nodes = [-(1/math.sqrt(3)), 1/math.sqrt(3)]  # Węzły Gaussa dla n=2
        self.weight = 1  # Waga jest równa 1 dla obu węzłów

    def Integrate1D(self):
        """
        Wykonuje całkowanie jednowymiarowe funkcji zdefiniowanej w functionX
        używając dwupunktowej kwadratury Gaussa.
        
        Returns:
            float: Wynik całkowania jednowymiarowego
        """
        result = functionX(self.nodes[0])*self.weight + functionX(self.nodes[1])*self.weight
        print(f"Integration result - 2Nodes (1D): {result}")
        return result

    def Integrate2D(self):
        """
        Wykonuje całkowanie dwuwymiarowe funkcji zdefiniowanej w functionXY
        używając dwupunktowej kwadratury Gaussa w obu wymiarach.
        Wykorzystuje iloczyn tensorowy węzłów i wag.
        
        Returns:
            float: Wynik całkowania dwuwymiarowego
        """
        result = 0
        for i in range(2):
            for j in range(2):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weight * self.weight

        print(f"Integration result - 2Nodes (2D): {result}")
        return result