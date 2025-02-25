from mes.gauss.GaussFunction import functionX, functionXY
import math

class GaussianIntegral3Nodes:
    """
    Klasa implementująca trzypunktową kwadraturę Gaussa.
    Specjalizowana wersja dla dokładnie trzech węzłów całkowania,
    używana do całkowania jedno- i dwuwymiarowego.
    """
    
    def __init__(self):
        """
        Inicjalizacja trzypunktowej kwadratury Gaussa.
        Węzły są symetryczne względem środka przedziału [-1,1] plus węzeł centralny.
        Wagi są symetryczne dla węzłów bocznych (5/9) i większa dla węzła centralnego (8/9).
        """
        self.nodes = [-(math.sqrt(3/5)), 0, math.sqrt(3/5)]  # Węzły Gaussa dla n=3
        self.weights = [5/9, 8/9, 5/9]  # Wagi dla węzłów: lewy, środkowy, prawy

    def integrate1d(self):
        """
        Wykonuje całkowanie jednowymiarowe funkcji zdefiniowanej w functionX
        używając trzypunktowej kwadratury Gaussa.
        
        Returns:
            float: Wynik całkowania jednowymiarowego
        """
        result = 0
        for i in range(3):
            result += functionX(self.nodes[i]) * self.weights[i]
        print(f"Integration result - 3Nodes (1D): {result}")
        return result

    def integrate2d(self):
        """
        Wykonuje całkowanie dwuwymiarowe funkcji zdefiniowanej w functionXY
        używając trzypunktowej kwadratury Gaussa w obu wymiarach.
        Wykorzystuje iloczyn tensorowy węzłów i wag, dając 9 punktów całkowania.
        
        Returns:
            float: Wynik całkowania dwuwymiarowego
        """
        result = 0
        for i in range(3):
            for j in range(3):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weights[i] * self.weights[j]
        print(f"Integration result - 3Nodes (2D): {result}")
        return result