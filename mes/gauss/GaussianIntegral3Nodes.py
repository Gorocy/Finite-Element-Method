from mes.gauss.GaussFunction import functionX, functionXY
import math
from typing import List

class GaussianIntegral3Nodes:
    """
    Class implementing three-point Gaussian quadrature.
    Specialized version for exactly three integration nodes,
    used for one- and two-dimensional integration.
    """
    
    def __init__(self):
        """
        Initialization of three-point Gaussian quadrature.
        Nodes are symmetric with respect to the center of the interval [-1,1] plus the central node.
        Weights are symmetric for the side nodes (5/9) and larger for the central node (8/9).
        """
        self.nodes: List[float] = [-(math.sqrt(3/5)), 0, math.sqrt(3/5)]  # Gauss nodes for n=3
        self.weights: List[float] = [5/9, 8/9, 5/9]  # Weights for nodes: left, central, right

    def integrate1d(self) -> float:
        """
        Performs one-dimensional integration of the function defined in functionX
        using three-point Gaussian quadrature.
        
        Returns:
            float: Result of one-dimensional integration
        """
        result: float = 0
        for i in range(3):
            result += functionX(self.nodes[i]) * self.weights[i]
        print(f"Integration result - 3Nodes (1D): {result}")
        return result

    def integrate2d(self) -> float:
        """
        Performs two-dimensional integration of the function defined in functionXY
        using three-point Gaussian quadrature in both dimensions.
        Uses the tensor product of nodes and weights, giving 9 integration points.
        
        Returns:
            float: Result of two-dimensional integration
        """
        result: float = 0
        for i in range(3):
            for j in range(3):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weights[i] * self.weights[j]
        print(f"Integration result - 3Nodes (2D): {result}")
        return result