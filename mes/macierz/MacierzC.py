from mes.macierz.WektorP import N1, N2, N3, N4
from mes.macierz.MacierzH import no_integration_nodes, JacobianMatrix
from mes.macierz.UniversalElement import UniversalElement
from mes.classes.Node import Node
from mes.classes.Element import Element
from tabulate import tabulate

# Initialization of the universal element for a given number of integration nodes
el = UniversalElement(no_integration_nodes)

# Definition of the test finite element nodes
n1 = Node(1, 0, 0, 1)          # Lower left node
n2 = Node(2, 0.025, 0, 1)      # Lower right node
n3 = Node(3, 0.025, 0.025, 1)  # Upper right node
n4 = Node(4, 0, 0.025, 1)      # Upper left node

# Creation of the element and adding the nodes to it
elem = Element(1)
elem.addNode(n1)
elem.addNode(n2)
elem.addNode(n3)
elem.addNode(n4)


class MacierzC:
    """
    Class implementing the matrix of thermal capacity [C] for MES.
    Calculates the matrix of thermal capacity for a four-node finite element.
    """
    
    def __init__(self, specific_heat, density, element):
        """
        Initialization and calculation of the matrix of thermal capacity.
        
        Args:
            specific_heat (float): Specific heat of the material [J/(kg·K)]
            density (float): Material density [kg/m³]
            element (Element): Finite element for which the matrix is calculated
        """
        # Initialization of the array of shape functions for all integration points
        self.n_functions = [[0] * 4 for _ in range(no_integration_nodes ** 2)]
        self.c_matrices = []  # List of C matrices for each integration point
        self.element = element

        # Calculation of the shape function values at the integration points
        for i in range(no_integration_nodes ** 2):
            self.n_functions[i][0] = N1(el.integration_points[i].x, el.integration_points[i].y)
            self.n_functions[i][1] = N2(el.integration_points[i].x, el.integration_points[i].y)
            self.n_functions[i][2] = N3(el.integration_points[i].x, el.integration_points[i].y)
            self.n_functions[i][3] = N4(el.integration_points[i].x, el.integration_points[i].y)

        # Calculation of the Jacobian determinants for each integration point
        self.jacobian_determinants = []
        for i in range(no_integration_nodes ** 2):
            temporary_jacobian = JacobianMatrix(element, no_integration_nodes, i)
            self.jacobian_determinants.append(temporary_jacobian.detJ)

        # Getting the integration weights from the universal element
        self.weights = []
        for weight in range(len(el.weights)):
            tmp = el.weights[weight]
            self.weights.append(tmp)

        # Calculation of the C matrix for each integration point
        for i in range(no_integration_nodes ** 2):
            matrix_c_temp = [[0] * 4 for _ in range(4)]

            for row in range(4):
                for col in range(4):
                    matrix_c_temp[row][col] += (self.n_functions[i][row] * 
                                              self.n_functions[i][col] * 
                                              specific_heat * 
                                              density * 
                                              self.jacobian_determinants[i])

            self.c_matrices.append(matrix_c_temp)

        # Calculation of the final C matrix by summing
        self.total_matrix = self.sum_matrices()

    def sum_matrices(self):
        """
        Sums the C matrices from all integration points with consideration of weights.
        
        Returns:
            list[list[float]]: Final matrix of thermal capacity
        """
        total_matrix = [[0] * 4 for _ in range(4)]

        for i, matrix in enumerate(self.c_matrices):
            for row in range(4):
                for col in range(4):
                    total_matrix[row][col] += (matrix[row][col] * 
                                             self.weights[i].x * 
                                             self.weights[i].y)

        return total_matrix

    def print_N_functions(self):
        """
        Displays the values of the shape functions at all integration points.
        """
        for i in range(no_integration_nodes ** 2):
            for j in range(4):
                value = self.n_functions[i][j]
                print(f"{value: .6f}", end="\t")
            print()

    def print_c_matrices(self):
        """
        Displays the C matrices for all integration points.
        Uses the tabulate library for formatting the output.
        """
        for i, matrix in enumerate(self.c_matrices):
            print(f"Integration Point {i + 1} Matrix:")
            print(tabulate(matrix, tablefmt="grid", floatfmt=".6f"))
            print()

    def print_total_matrix(self):
        """
        Displays the final (summed) matrix of thermal capacity.
        Uses the tabulate library for formatting the output.
        """
        print("Total Matrix C:")
        print(tabulate(self.total_matrix, tablefmt="grid", floatfmt=".6f"))