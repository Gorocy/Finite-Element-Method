from mes.gauss.GaussianIntegral import GaussianIntegral
from mes.classes.Node import Node
from typing import List

# Functions calculating the derivatives of the shape functions with respect to ksi
def n1_ksi(eta: float) -> float:
    """Derivative of the first shape function with respect to ksi"""
    return -(1 / 4) * (1 - eta)

def n2_ksi(eta: float) -> float:
    """Derivative of the second shape function with respect to ksi"""
    return (1 / 4) * (1 - eta)

def n3_ksi(eta: float) -> float:
    """Derivative of the third shape function with respect to ksi"""
    return (1 / 4) * (1 + eta)

def n4_ksi(eta: float) -> float:
    """Derivative of the fourth shape function with respect to ksi"""
    return -(1 / 4) * (1 + eta)

# Functions calculating the derivatives of the shape functions with respect to eta
def n1_eta(ksi: float) -> float:
    """Derivative of the first shape function with respect to eta"""
    return -(1/4) * (1-ksi)

def n2_eta(ksi: float) -> float:
    """Derivative of the second shape function with respect to eta"""
    return -(1/4) * (1+ksi)

def n3_eta(ksi: float) -> float:
    """Derivative of the third shape function with respect to eta"""
    return (1/4) * (1+ksi)

def n4_eta(ksi: float) -> float:
    """Derivative of the fourth shape function with respect to eta"""
    return (1/4) * (1-ksi)


class UniversalElement:
    """
    Class implementing a universal element for MES.
    Contains definitions of shape functions and their derivatives at integration points.
    """
    
    def __init__(self, no_int_nodes: int):
        """
        Initialization of the universal element.
        
        Args:
            no_int_nodes (int): Number of integration nodes in each direction
        """
        self.no_int_nodes: int = no_int_nodes
        self.temp: GaussianIntegral = GaussianIntegral(no_int_nodes)
        
        # Initializing arrays of shape function derivatives
        rows, cols = (4, no_int_nodes * no_int_nodes)
        self.ksi_derivatives: List[List[float]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.eta_derivatives: List[List[float]] = [[None for _ in range(cols)] for _ in range(rows)]
        
        # Lists of integration points and their weights
        self.integration_points: List[Node] = []
        self.weights: List[Node] = []

        # Generating integration points and their weights
        iterations = 1
        for i in range(no_int_nodes):
            for j in range(no_int_nodes):
                # Creating an integration point and its weight
                point = Node(iterations, self.temp.nodes[j], self.temp.nodes[i])
                weight = Node(iterations, self.temp.weights[j], self.temp.weights[i])
                self.integration_points.append(point)
                self.weights.append(weight)
                iterations += 1

        # Calculating the derivatives of the shape functions at the integration points
        for i in range(cols):
            # Derivatives with respect to eta
            self.eta_derivatives[0][i] = n1_eta(self.integration_points[i].x)
            self.ksi_derivatives[0][i] = n1_ksi(self.integration_points[i].y)
            self.eta_derivatives[1][i] = n2_eta(self.integration_points[i].x)
            self.ksi_derivatives[1][i] = n2_ksi(self.integration_points[i].y)
            self.eta_derivatives[2][i] = n3_eta(self.integration_points[i].x)
            self.ksi_derivatives[2][i] = n3_ksi(self.integration_points[i].y)
            self.eta_derivatives[3][i] = n4_eta(self.integration_points[i].x)
            self.ksi_derivatives[3][i] = n4_ksi(self.integration_points[i].y)

    def print_ksi_array(self) -> None:
        """
        Displays the array of derivatives of the shape functions with respect to ksi
        for all integration points.
        """
        print("Ksi:")
        for col in range(self.no_int_nodes ** 2):
            for row in range(4):
                value = self.ksi_derivatives[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_eta_array(self) -> None:
        """
        Displays the array of derivatives of the shape functions with respect to eta
        for all integration points.
        """
        print("Eta:")
        for col in range(self.no_int_nodes ** 2):
            for row in range(4):
                value = self.eta_derivatives[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_integration_points(self) -> None:
        """
        Displays the coordinates of all integration points in the universal element.
        """
        print("Integration Points: ")
        for i in range(len(self.integration_points)):
            value = self.integration_points[i]
            value.printNode()
        print()

