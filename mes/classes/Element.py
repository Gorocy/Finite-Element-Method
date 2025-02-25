from mes.classes.Node import Node
from typing import List

class Element:
    """
    Class representing an element in the finite element method (FEM).
    Stores the element ID and a list of connected nodes.
    """
    
    def __init__(self, id: int):
        """
        Initializes a new element.
        
        Args:
            id: Unique identifier of the element
        """
        self.id: int = id
        self.connected_nodes: List[Node] = []  # List storing nodes connected to the element

    def addNode(self, node: Node) -> None:
        """
        Adds a node to the list of connected nodes.
        
        Args:
            node (Node): Node object to add
        """
        self.connected_nodes.append(node)

    def printElement(self) -> None:
        """
        Displays information about the element, including its ID and the coordinates of all connected nodes.
        """
        print("Element ID: ", self.id, end="")
        print(", Nodes: ", end="")
        for node in self.connected_nodes:
            print(f"{node.node_id} ({node.x}, {node.y})", end=", ")
        print()