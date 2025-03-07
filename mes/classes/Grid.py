from typing import List
from mes.classes.Node import Node
from mes.classes.Element import Element

class Grid:
    """
    Class representing a finite element mesh.
    Stores nodes and elements forming the mesh and manages their addition.
    """
    
    def __init__(self, nNodes: int, nElements: int):
        """
        Initializes the finite element mesh.
        
        Args:
            nNodes (int): Maximum number of nodes in the mesh
            nElements (int): Maximum number of elements in the mesh
        """
        self.nNodes: int = nNodes
        self.nElements: int = nElements
        self.nodes: List[Node] = []        # List storing all nodes in the mesh
        self.elements: List[Element] = []  # List storing all elements in the mesh

    def addNode(self, node: Node) -> None:
        """
        Adds a new node to the mesh, if the maximum number of nodes is not exceeded.
        
        Args:
            node (Node): Node object to add to the mesh
        """
        if len(self.nodes) > self.nNodes:
            print("Too many nodes")
        else:
            self.nodes.append(node)

    def addElement(self, element: Element) -> None:
        """
        Adds a new element to the mesh, if the maximum number of elements is not exceeded.
        
        Args:
            element (Element): Element object to add to the mesh
        """
        if len(self.elements) > self.nElements:
            print("Too many elements")
        else:
            self.elements.append(element)

    def printGrid(self) -> None:
        """
        Displays information about all nodes and elements in the mesh.
        Helper function for visualizing and debugging the mesh structure.
        """
        print("Nodes:")
        count = 1
        for node in self.nodes:
            node.printNode()
            count += 1

        print("Elements:")
        for element in self.elements:
            element.printElement()

