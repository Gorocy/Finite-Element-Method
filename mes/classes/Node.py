class Node:
    """
    Class representing a node in the finite element method (FEM).
    Stores information about the node's position and boundary conditions.
    """
    
    def __init__(self, node_id: int, x: float, y: float, bc: int = 0):
        """
        Initializes the node.
        
        Args:
            node_id (int): Unique identifier of the node
            x (float): X coordinate of the node in the Cartesian coordinate system
            y (float): Y coordinate of the node in the Cartesian coordinate system
            bc (int, optional): Boundary condition.
                              0 means no boundary condition,
                              value > 0 means node with boundary condition
        """
        self.node_id: int = node_id
        self.x: float = x
        self.y: float = y
        self.BC: int = bc  # Boundary Condition

    def printNode(self) -> None:
        """
        Displays information about the node, including its identifier, 
        coordinates, and information about the boundary condition.
        
        Format display:
        - For nodes with boundary condition: "BC {value}"
        - For nodes without boundary condition: "Without BC"
        """
        bc_info = f"BC {self.BC}" if self.BC > 0 else "Without BC"
        print(f"NodeID: {self.node_id}, x: {self.x}, y: {self.y}, {bc_info}")

