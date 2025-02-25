class Grid:
    """
    Class representing a finite element mesh.
    Stores nodes and elements forming the mesh and manages their addition.
    """
    
    def __init__(self, nNodes, nElements):
        """
        Initializes the finite element mesh.
        
        Args:
            nNodes (int): Maximum number of nodes in the mesh
            nElements (int): Maximum number of elements in the mesh
        """
        self.nNodes = nNodes
        self.nElements = nElements
        self.nodes = []        # List storing all nodes in the mesh
        self.elements = []     # List storing all elements in the mesh

    def addNode(self, node):
        """
        Adds a new node to the mesh, if the maximum number of nodes is not exceeded.
        
        Args:
            node (Node): Node object to add to the mesh
        """
        if len(self.nodes) > self.nNodes:
            print("Too many nodes")
        else:
            self.nodes.append(node)

    def addElement(self, element):
        """
        Adds a new element to the mesh, if the maximum number of elements is not exceeded.
        
        Args:
            element (Element): Element object to add to the mesh
        """
        if len(self.elements) > self.nElements:
            print("Too many elements")
        else:
            self.elements.append(element)

    def printGrid(self):
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

