from mes.gauss.GaussFunction import functionX, functionXY
import math

class GaussianIntegral2Nodes:
    """
    Class implementing two-point Gaussian quadrature.
    Specialized version for exactly two integration nodes,
    used for one- and two-dimensional integration.
    """
    
    def __init__(self):
        """
        Initialization of two-point Gaussian quadrature.
        Nodes are symmetric with respect to the center of the interval [-1,1],
        and weights are equal to 1 for both nodes.
        """
        self.nodes = [-(1/math.sqrt(3)), 1/math.sqrt(3)]  # Gauss nodes for n=2
        self.weight = 1  # Weight is equal to 1 for both nodes

    def Integrate1D(self):
        """
        Performs one-dimensional integration of the function defined in functionX
        using two-point Gaussian quadrature.
        
        Returns:
            float: Result of one-dimensional integration
        """
        result = functionX(self.nodes[0])*self.weight + functionX(self.nodes[1])*self.weight
        print(f"Integration result - 2Nodes (1D): {result}")
        return result

    def Integrate2D(self):
        """
        Performs two-dimensional integration of the function defined in functionXY
        using two-point Gaussian quadrature in both dimensions.
        Uses the tensor product of nodes and weights.
        
        Returns:
            float: Result of two-dimensional integration
        """
        result = 0
        for i in range(2):
            for j in range(2):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weight * self.weight

        print(f"Integration result - 2Nodes (2D): {result}")
        return result