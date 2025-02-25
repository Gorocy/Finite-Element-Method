from mes.gauss.GaussFunction import functionX, functionXY
import math

class GaussianIntegral:
    """
    Class implementing numerical integration using the Gaussian method.
    Handles one- and two-dimensional integration for different numbers of nodes (1-5).
    """
    
    def __init__(self, no_nodes):
        """
        Initialization of the Gaussian quadrature for a given number of nodes.
        
        Args:
            no_nodes (int): Number of integration nodes (1-5)
            
        Raises:
            ValueError: When the number of nodes is not supported (outside the range 1-5)
        """
        self.no_nodes = no_nodes

        # Definitions of nodes and weights for different numbers of integration points
        if no_nodes == 1:
            # One-point integration
            self.nodes = [0]  # Node in the center of the interval
            self.weights = [2]  # Weight for the node

        elif no_nodes == 2:
            # Two-point integration
            self.nodes = [-(1 / math.sqrt(3)), 1 / math.sqrt(3)]  # Symmetric nodes
            self.weights = [1, 1]  # Equal weights for both nodes

        elif no_nodes == 3:
            # Three-point integration
            self.nodes = [-(math.sqrt(3 / 5)), 0, math.sqrt(3 / 5)]  # Symmetric nodes + center
            self.weights = [5 / 9, 8 / 9, 5 / 9]  # Weights for the nodes

        elif no_nodes == 4:
            # Four-point integration
            self.nodes = [-(math.sqrt(3 / 7 + 2 / 7 * math.sqrt(6 / 5))),
                          -(math.sqrt(3 / 7 - 2 / 7 * math.sqrt(6 / 5))),
                          (math.sqrt(3 / 7 - 2 / 7 * math.sqrt(6 / 5))),
                          (math.sqrt(3 / 7 + 2 / 7 * math.sqrt(6 / 5)))]
            self.weights = [(18 - math.sqrt(30)) / 36, (18 + math.sqrt(30)) / 36,
                            (18 + math.sqrt(30)) / 36, (18 - math.sqrt(30)) / 36]

        elif no_nodes == 5:
            # Five-point integration
            self.nodes = [-math.sqrt(5 + 2 * math.sqrt(10 / 7)) / 3,
                          -math.sqrt(5 - 2 * math.sqrt(10 / 7)) / 3,
                          0,
                          math.sqrt(5 - 2 * math.sqrt(10 / 7)) / 3,
                          math.sqrt(5 + 2 * math.sqrt(10 / 7)) / 3]

            self.weights = [(322 - 13 * math.sqrt(70)) / 900,
                            (322 + 13 * math.sqrt(70)) / 900,
                            128 / 225,
                            (322 + 13 * math.sqrt(70)) / 900,
                            (322 - 13 * math.sqrt(70)) / 900]

        else:
            raise ValueError("Unsupported number of nodes.")

    def integrate1d(self):
        """
        Performs one-dimensional integration of the function defined in functionX.
        
        Returns:
            float: Result of one-dimensional integration
        """
        result = 0
        for i in range(self.no_nodes):
            result += functionX(self.nodes[i]) * self.weights[i]
        print(f"Integration result - {self.no_nodes} Nodes (1D): {result}")
        return result

    def integrate2d(self):
        """
        Performs two-dimensional integration of the function defined in functionXY.
        Uses the tensor product of nodes and weights for both dimensions.
        
        Returns:
            float: Result of two-dimensional integration
        """
        result = 0
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                result += functionXY(self.nodes[i], self.nodes[j]) * self.weights[i] * self.weights[j]
        print(f"Integration result - {self.no_nodes} Nodes (2D): {result}")
        return result
