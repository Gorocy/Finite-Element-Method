from mes.classes.Node import Node
from mes.macierz.UniversalElement import UniversalElement
from mes.classes.Element import Element
from tabulate import tabulate
from typing import List

no_integration_nodes: int = 4  # Number of integration nodes

# Definition of the test finite element
n1 = Node(1, 0.1, 0.005)        # Node 1
n2 = Node(2, 0.0546918, 0.005)  # Node 2
n3 = Node(6, 0.0623899, -0.0326101)  # Node 3
n4 = Node(5, 0.1, -0.0403082)   # Node 4
elem = Element(1)
elem.addNode(n1)
elem.addNode(n2)
elem.addNode(n3)
elem.addNode(n4)

_universal = UniversalElement(no_integration_nodes)
ksi = _universal.ksi_derivatives  # Derivatives of the shape functions with respect to ksi
eta = _universal.eta_derivatives  # Derivatives of the shape functions with respect to eta

def dx_dksi(element: Element, no_nodes: int, integration_point: int) -> float:
    """
    Calculates the derivative of the x coordinate with respect to ksi.
    
    Args:
        element (Element): Finite element
        no_nodes (int): Number of integration nodes
        integration_point (int): Integration point number
        
    Returns:
        float: Value of the derivative dx/dksi
    """
    temp = UniversalElement(no_nodes)
    result = 0.0
    temporary = 0.0
    for i in range(len(element.connected_nodes)):
        temporary = element.connected_nodes[i].x * ksi[i][integration_point]
        result += temporary
    return result

# Analogiczne funkcje dla pozostałych pochodnych
def dy_dksi(element: Element, no_nodes: int, integration_point: int) -> float:
    """
    Calculates the derivative of the y coordinate with respect to ksi.
    
    Args:
        element (Element): Finite element
        no_nodes (int): Number of integration nodes
        integration_point (int): Integration point number
    """
    temp = UniversalElement(no_nodes)
    result = 0.0
    for i in range(len(element.connected_nodes)):
        temporary = element.connected_nodes[i].y * ksi[i][integration_point]
        result += temporary
    return result

def dx_deta(element: Element, no_nodes: int, integration_point: int) -> float:
    """
    Calculates the derivative of the x coordinate with respect to eta.
    
    Args:
        element (Element): Finite element
        no_nodes (int): Number of integration nodes
        integration_point (int): Integration point number
    """
    temp = UniversalElement(no_nodes)
    result = 0.0
    for i in range(len(element.connected_nodes)):
        temporary = element.connected_nodes[i].x * eta[i][integration_point]
        result += temporary
    return result

def dy_deta(element: Element, no_nodes: int, integration_point: int) -> float:
    """
    Calculates the derivative of the y coordinate with respect to eta.
    
    Args:
        element (Element): Finite element
        no_nodes (int): Number of integration nodes
        integration_point (int): Integration point number
    """
    temp = UniversalElement(no_nodes)
    result = 0.0
    for i in range(len(element.connected_nodes)):
        temporary = element.connected_nodes[i].y * eta[i][integration_point]
        result += temporary
    return result


class JacobianMatrix:
    """
    Class implementing the Jacobian matrix for coordinate transformation.
    """
    
    def __init__(self, element: Element, no_nodes: int, integration_point: int):
        """
        Initialization and calculation of the Jacobian matrix.
        
        Args:
            element (Element): Finite element
            no_nodes (int): Number of integration nodes
            integration_point (int): Integration point number
        """
        self.matrix: List[List[float]] = [[0.0, 0.0], [0.0, 0.0]]
        
        # Calculation of the elements of the Jacobian matrix
        self.matrix[0][0] = dx_dksi(element, no_nodes, integration_point)
        self.matrix[0][1] = dx_deta(element, no_nodes, integration_point)
        self.matrix[1][0] = dy_dksi(element, no_nodes, integration_point)
        self.matrix[1][1] = dy_deta(element, no_nodes, integration_point)

        # Calculation of the determinant and its inverse
        self.detJ: float = self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        self.inverse_detJ: float = 1 / self.detJ

    def print_matrix(self) -> None:
        for row in self.matrix:
            print(row)
        print()
        print("det(J) - ", self.detJ)
        print("1/det(J) - ", self.inverse_detJ)

    def multiply_by_inverse(self) -> None:
        self.matrix[0][0] *= self.inverse_detJ
        self.matrix[0][1] *= self.inverse_detJ
        self.matrix[1][0] *= self.inverse_detJ
        self.matrix[1][1] *= self.inverse_detJ

    def get_matrix_ready_for_DNi(self) -> 'JacobianMatrix':
        temp00 = self.matrix[0][0]
        temp01 = self.matrix[0][1]
        temp10 = self.matrix[1][0]
        temp11 = self.matrix[1][1]
        self.matrix[0][0] = temp11
        self.matrix[0][1] = -temp10
        self.matrix[1][0] = -temp01
        self.matrix[1][1] = temp00
        self.multiply_by_inverse()
        return self

    def get_matrix(self) -> List[List[float]]:
        return self.matrix


class dNi_dX:
    """
    Class calculating the derivatives of the shape functions with respect to x.
    """
    
    def __init__(self, element: Element, no_nodes: int):
        """
        Initialization and calculation of the derivatives of the shape functions with respect to x.
        
        Args:
            element (Element): Finite element
            no_nodes (int): Number of integration nodes
        """
        self.no_nodes: int = no_nodes

        cols = no_nodes ** 2
        rows = 4
        self.j_matrices: List[JacobianMatrix] = [None for _ in range(cols)]
        self.j_matrices_ready: List[List[List[float]]] = [None for _ in range(cols)]
        self.matrix: List[List[float]] = [[None for _ in range(cols)] for _ in range(rows)]

        for i in range(cols):
            temp = JacobianMatrix(element, no_nodes, i)
            self.j_matrices[i] = temp

        for i in range(cols):
            temp = self.j_matrices[i].get_matrix_ready_for_DNi()
            self.j_matrices_ready[i] = temp.get_matrix()

        for integration_point in range(cols):
            jacobian_matrix = self.j_matrices_ready[integration_point]
            for shape_function in range(rows):
                result = (
                        jacobian_matrix[0][0] * ksi[shape_function][integration_point] +
                        jacobian_matrix[0][1] * eta[shape_function][integration_point]
                )
                self.matrix[shape_function][integration_point] = result

    def print_matrix(self) -> None:
        print("Matrix dN/dX:")
        for col in range(self.no_nodes ** 2):
            for row in range(4):
                value = self.matrix[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_j_matrix_ready(self, integration_point: int) -> None:
        print("Ready J Matrix", integration_point)
        for col in range(2):
            for row in range(2):
                value = self.j_matrices_ready[integration_point][row][col]
                print(f"{value:.6f}", end="\t")
            print()
        print("\n")


class dNi_dY:
    """
    Class calculating the derivatives of the shape functions with respect to y.
    """
    
    def __init__(self, element: Element, no_nodes: int):
        """
        Initialization and calculation of the derivatives of the shape functions with respect to y.
        
        Args:
            element (Element): Finite element
            no_nodes (int): Number of integration nodes
        """
        self.no_nodes: int = no_nodes

        cols = no_nodes ** 2
        rows = 4
        self.j_matrices: List[List[List[float]]] = []
        self.j_matrices_copy: List[JacobianMatrix] = [None for _ in range(cols)]
        self.j_matrices_ready: List[List[List[float]]] = [None for _ in range(cols)]
        self.matrix: List[List[float]] = [[None for _ in range(cols)] for _ in range(rows)]

        for i in range(cols):
            temp1 = JacobianMatrix(element, no_nodes, i)
            temp2 = JacobianMatrix(element, no_nodes, i)
            self.j_matrices.append(temp1.get_matrix())
            self.j_matrices_copy[i] = temp2

        for i in range(cols):
            temp = self.j_matrices_copy[i].get_matrix_ready_for_DNi()
            self.j_matrices_ready[i] = temp.get_matrix()

        for integration_point in range(cols):
            jacobian_matrix = self.j_matrices_ready[integration_point]
            for shape_function in range(rows):
                result = (
                        jacobian_matrix[1][0] * ksi[shape_function][integration_point] +
                        jacobian_matrix[1][1] * eta[shape_function][integration_point]
                )
                self.matrix[shape_function][integration_point] = result

    def print_matrix(self) -> None:
        print("Matrix dN/dY:")
        for col in range(self.no_nodes ** 2):
            for row in range(4):
                value = self.matrix[row][col]
                print(f"{value:.6f}", end="\t")
            print()

    def print_j_matrix(self, integration_point: int) -> None:
        print("J Matrix", integration_point)
        for col in range(2):
            for row in range(2):
                value = self.j_matrices[integration_point][row][col]
                print(f"{value:.6f}", end="\t")
            print()
        print("\n")

    def print_j_matrix_ready(self, integration_point: int) -> None:
        print("Ready J Matrix", integration_point)
        for col in range(2):
            for row in range(2):
                value = self.j_matrices_ready[integration_point][row][col]
                print(f"{value:.6f}", end="\t")
            print()
        print("\n")


class TransposedMatrix:
    """
    Class implementing the transposed matrix and operations on it.
    """
    
    def __init__(self, elem_: Element, no_nodes: int, k_value: float):
        """
        Initialization and calculation of the transposed matrix.
        
        Args:
            elem_ (Element): Finite element
            no_nodes (int): Number of integration nodes
            k_value (float): Thermal conductivity coefficient
        """
        self.temp_dx = dNi_dX(elem_, no_nodes)
        self.temp_dy = dNi_dY(elem_, no_nodes)
        self.no_nodes: int = no_nodes
        self.n_matrices: int = no_nodes ** 2
        self.rows: int = 4
        self.cols: int = no_nodes ** 2
        self.matricesX: List[List[List[float]]] = []
        self.matricesY: List[List[List[float]]] = []
        self.matricesSum: List[List[List[float]]] = []
        self.jacobian_determinants: List[float] = []

        for i in range(no_nodes ** 2):
            temporary_jacobian = JacobianMatrix(elem_, no_nodes, i)
            self.jacobian_determinants.append(temporary_jacobian.detJ)

        for col in range(self.cols):
            matrix_x = self.calculateMatrixX(col)
            matrix_y = self.calculateMatrixY(col)
            self.matricesX.append(matrix_x)
            self.matricesY.append(matrix_y)
            self.matricesSum.append(self.add_matrices(matrix_x, matrix_y))

        for matrix, detJ in zip(self.matricesSum, self.jacobian_determinants):
            self.multiply_matrix(matrix, k_value * detJ)


    def calculateMatrixX(self, integration_point: int) -> List[List[float]]:
        temp_matrix: List[List[float]] = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                temp_matrix[i][j] = self.temp_dx.matrix[i][integration_point] * self.temp_dx.matrix[j][integration_point]


        return temp_matrix

    def calculateMatrixY(self, integration_point: int) -> List[List[float]]:
        temp_matrix: List[List[float]] = [[None for _ in range(4)] for _ in range(4)]
        
        for i in range(4):

            for j in range(4):
                temp_matrix[i][j] = self.temp_dy.matrix[i][integration_point] * self.temp_dy.matrix[j][integration_point]

        return temp_matrix

    def print_matrices(self) -> None:
        print("MatricesX:")
        for matrix_index, matrix in enumerate(self.matricesX):
            print(f"MatrixX {matrix_index + 1}:")
            for row in matrix:
                for value in row:
                    print(f"{value:.6f}" if isinstance(value, (float, int)) else value, end="\t")
                print()

        print("\nMatricesY:")
        for matrix_index, matrix in enumerate(self.matricesY):
            print(f"MatrixY {matrix_index + 1}:")
            for row in matrix:
                for value in row:
                    print(f"{value:.6f}" if isinstance(value, (float, int)) else value, end="\t")
                print()

        print("\nMatricesSum:")
        for matrix_index, matrix in enumerate(self.matricesSum):
            print(f"MatrixSum {matrix_index + 1}:")
            for row in matrix:
                for value in row:
                    print(f"{value:.6f}" if isinstance(value, (float, int)) else value, end="\t")
                print()

    def add_matrices(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
        result_matrix: List[List[float]] = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                result_matrix[i][j] = matrix_a[i][j] + matrix_b[i][j]
        return result_matrix

    def multiply_matrix(self, matrix: List[List[float]], factor: float) -> None:
        for i in range(4):
            for j in range(4):
                matrix[i][j] *= factor

class MatrixH:
    """
    Class implementing the matrix H (heat conduction).
    """
    
    def __init__(self, _elem: Element, no_nodes: int, k: float):
        """
        Initialization and calculation of the matrix H.
        
        Args:
            _elem (Element): Finite element
            no_nodes (int): Number of integration nodes
            k (float): Thermal conductivity coefficient
        """
        self.element: Element = _elem
        self.matrices: TransposedMatrix = TransposedMatrix(_elem, no_nodes, k)
        self.k: float = k
        self.matrices_with_weights: List[List[List[float]]] = []

        universal_el = UniversalElement(no_nodes)
        self.weights: List[float] = []
        for weight in range(len(universal_el.weights)):
            tmp = universal_el.weights[weight]
            self.weights.append(tmp)

        # Multiply each matrix by its corresponding weight and add to matrices_with_weights
        for matrix, weight in zip(self.matrices.matricesSum, self.weights):
            weighted_matrix = [[element * weight.x * weight.y for element in row] for row in matrix]
            self.matrices_with_weights.append(weighted_matrix)

        self.total_matrix: List[List[float]] = self.calculate_total_matrix()

    def print_matrices_with_weights(self) -> None:
        print("Matrices with Weights:")
        for matrix_index, matrix in enumerate(self.matrices_with_weights):
            print(f"Matrix with Weight {matrix_index + 1}:")
            for row in matrix:
                for value in row:
                    print(f"{value:.6f}" if isinstance(value, (float, int)) else value, end="\t")
                print()

    def calculate_total_matrix(self) -> List[List[float]]:
        temp_matrix: List[List[float]] = [[0 for _ in range(4)] for _ in range(4)]

        # Sum up all matrices in self.matrices_with_weights
        for matrix in self.matrices_with_weights:
            for i in range(4):
                for j in range(4):
                    temp_matrix[i][j] += matrix[i][j]

        return temp_matrix

    def print_total_matrix(self) -> None:
        headers = [""] + list(range(1, len(self.total_matrix[0]) + 1))
        table = [[i + 1] + row for i, row in enumerate(self.total_matrix)]
        print("\nTotal Matrix:")
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def get_matrix_h(self) -> List[List[float]]:
        return self.total_matrix

    def add_hbc_matrix(self, hbc_matrix: List[List[float]]) -> None:
        """
        Adds the matrix of convective boundary conditions to the matrix H.
        
        Args:
            hbc_matrix (list[list[float]]): Matrix of convective boundary conditions 4x4
            
        Raises:
            ValueError: When the dimensions of the matrix are incorrect
        """
        if len(hbc_matrix) != 4 or any(len(row) != 4 for row in hbc_matrix):
            raise ValueError("The provided matrix should be a 4x4 matrix")

        for i in range(4):
            for j in range(4):
                self.total_matrix[i][j] += hbc_matrix[i][j]