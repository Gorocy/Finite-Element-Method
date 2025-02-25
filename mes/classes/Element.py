from mes.classes.Node import Node

class Element:
    """
    Klasa reprezentująca element w metodzie elementów skończonych (MES).
    Przechowuje identyfikator elementu oraz listę połączonych z nim węzłów.
    """
    
    def __init__(self, id):
        """
        Inicjalizacja nowego elementu.
        
        Args:
            id: Unikalny identyfikator elementu
        """
        self.id = id
        self.connected_nodes = []  # Lista przechowująca węzły połączone z elementem

    def addNode(self, node: Node):
        """
        Dodaje węzeł do listy węzłów połączonych z elementem.
        
        Args:
            node (Node): Obiekt węzła do dodania
        """
        self.connected_nodes.append(node)

    def printElement(self):
        """
        Wyświetla informacje o elemencie, w tym jego ID oraz 
        współrzędne wszystkich połączonych węzłów.
        """
        print("Element ID: ", self.id, end="")
        print(", Nodes: ", end="")
        for node in self.connected_nodes:
            print(f"{node.node_id} ({node.x}, {node.y})", end=", ")
        print()