class Grid:
    """
    Klasa reprezentująca siatkę elementów skończonych.
    Przechowuje węzły i elementy tworzące siatkę MES oraz zarządza ich dodawaniem.
    """
    
    def __init__(self, nNodes, nElements):
        """
        Inicjalizacja siatki MES.
        
        Args:
            nNodes (int): Maksymalna liczba węzłów w siatce
            nElements (int): Maksymalna liczba elementów w siatce
        """
        self.nNodes = nNodes
        self.nElements = nElements
        self.nodes = []        # Lista przechowująca wszystkie węzły siatki
        self.elements = []     # Lista przechowująca wszystkie elementy siatki

    def addNode(self, node):
        """
        Dodaje nowy węzeł do siatki, jeśli nie przekroczono maksymalnej liczby węzłów.
        
        Args:
            node (Node): Obiekt węzła do dodania do siatki
        """
        if len(self.nodes) > self.nNodes:
            print("Too many nodes")
        else:
            self.nodes.append(node)

    def addElement(self, element):
        """
        Dodaje nowy element do siatki, jeśli nie przekroczono maksymalnej liczby elementów.
        
        Args:
            element (Element): Obiekt elementu do dodania do siatki
        """
        if len(self.elements) > self.nElements:
            print("Too many elements")
        else:
            self.elements.append(element)

    def printGrid(self):
        """
        Wyświetla informacje o wszystkich węzłach i elementach w siatce.
        Funkcja pomocnicza do wizualizacji i debugowania struktury siatki.
        """
        print("Nodes:")
        count = 1
        for node in self.nodes:
            node.printNode()
            count += 1

        print("Elements:")
        for element in self.elements:
            element.printElement()

