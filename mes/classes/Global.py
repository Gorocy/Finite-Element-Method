class Global:
    """
    Klasa przechowująca globalne parametry symulacji metody elementów skończonych (MES).
    Zawiera wszystkie stałe fizyczne i parametry czasowe potrzebne do obliczeń.
    """
    
    def __init__(self, simTime, simStepTime, conductivity, alfa, tot, initialTemp, 
                 density, specificHeat, nodesNo, elementsNo):
        """
        Inicjalizacja parametrów globalnych symulacji.
        
        Args:
            simTime (float): Całkowity czas symulacji [s]
            simStepTime (float): Krok czasowy symulacji [s]
            conductivity (float): Współczynnik przewodzenia ciepła [W/(m·K)]
            alfa (float): Współczynnik wymiany ciepła [W/(m²·K)]
            tot (float): Temperatura otoczenia [°C]
            initialTemp (float): Temperatura początkowa [°C]
            density (float): Gęstość materiału [kg/m³]
            specificHeat (float): Ciepło właściwe materiału [J/(kg·K)]
            nodesNo (int): Liczba węzłów w siatce
            elementsNo (int): Liczba elementów w siatce
        """
        self.simTime = simTime
        self.simStepTime = simStepTime
        self.conductivity = conductivity
        self.alfa = alfa
        self.tot = tot
        self.initialTemp = initialTemp
        self.density = density
        self.specificHeat = specificHeat
        self.nodesNo = nodesNo
        self.elementsNo = elementsNo

    def print_values(self):
        """
        Wyświetla wszystkie parametry globalne symulacji.
        Funkcja pomocnicza do debugowania i weryfikacji danych wejściowych.
        """
        print("SimulationTime:", self.simTime)
        print("SimulationStepTime:", self.simStepTime)
        print("Conductivity:", self.conductivity)
        print("Alfa:", self.alfa)
        print("Tot:", self.tot)
        print("InitialTemp:", self.initialTemp)
        print("Density:", self.density)
        print("SpecificHeat:", self.specificHeat)
        print("Nodes number:", self.nodesNo)
        print("Elements number:", self.elementsNo)