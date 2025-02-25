class Node:
    """
    Klasa reprezentująca węzeł w metodzie elementów skończonych (MES).
    Przechowuje informacje o położeniu węzła oraz warunkach brzegowych.
    """
    
    def __init__(self, node_id, x, y, bc = 0):
        """
        Inicjalizacja węzła.
        
        Args:
            node_id (int): Unikalny identyfikator węzła
            x (float): Współrzędna X węzła w układzie kartezjańskim
            y (float): Współrzędna Y węzła w układzie kartezjańskim
            bc (int, optional): Warunek brzegowy (boundary condition).
                              0 oznacza brak warunku brzegowego,
                              wartość > 0 oznacza węzeł z warunkiem brzegowym
        """
        self.node_id = node_id
        self.x = x
        self.y = y
        self.BC = bc  # Warunek brzegowy (Boundary Condition)

    def printNode(self):
        """
        Wyświetla informacje o węźle, w tym jego identyfikator, 
        współrzędne oraz informację o warunku brzegowym.
        
        Format wyświetlania:
        - Dla węzłów z warunkiem brzegowym: "BC {wartość}"
        - Dla węzłów bez warunku brzegowego: "Without BC"
        """
        bc_info = f"BC {self.BC}" if self.BC > 0 else "Without BC"
        print(f"NodeID: {self.node_id}, x: {self.x}, y: {self.y}, {bc_info}")

