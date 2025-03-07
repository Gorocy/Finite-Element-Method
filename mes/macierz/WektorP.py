from mes.classes.Node import Node
from mes.classes.Element import Element
from mes.macierz.UniversalElement import UniversalElement
from mes.macierz.MacierzH import no_integration_nodes
from typing import List

n1 = Node(1, 0.1, 0.005, 1)
n2 = Node(2, 0.0546918, 0.005, 1)
n3 = Node(6, 0.0623899, -0.0326101, 0)
n4 = Node(5, 0.1, -0.0403082, 1)

elem = Element(1)
elem.addNode(n1)
elem.addNode(n2)
elem.addNode(n3)
elem.addNode(n4)

_universal = UniversalElement(no_integration_nodes)

def print_matrix(matrix: List[List[float]], name: str) -> None:
    print(f"{name}:")
    for row in matrix:
        print(row)
    print()

def N1(ksi: float, eta: float) -> float:
    result = 0.25 * (1-ksi) * (1-eta)
    return result

def N2(ksi: float, eta: float) -> float:
    result = 0.25 * (1+ksi) * (1-eta)
    return result

def N3(ksi: float, eta: float) -> float:
    result = 0.25 * (1+ksi) * (1+eta)
    return result

def N4(ksi: float, eta: float) -> float:
    result = 0.25 * (1-ksi) * (1+eta)
    return result


def calculate_distance(node1: Node, node2: Node) -> float:
    x1 = node1.x
    y1 = node1.y

    x2 = node2.x
    y2 = node2.y

    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


def powierzchnie_bc(element: Element) -> List[int]:
    """
    Identifies the surfaces of the element with boundary conditions.
    
    Args:
        element (Element): Finite element to analyze
        
    Returns:
        list[int]: List of 4 values specifying the boundary conditions on each side
                  (0 - no boundary condition, >0 - boundary condition)
    """
    # Initialization of arrays of boundary conditions for nodes and surfaces
    punkty_z_bc = [0,  # point 0 (First point in element ->  Bottom left)
                   0,  # point 1 (Node with MaxID - 1  ->  Bottom right)
                   0,  # point 2 (Node with MinID      ->  Top right)
                   0]  # point 3 (Node with MinID + 1  ->  Top left)

    powierzchnie_z_bc = [0,  # wall 0 (Between Node 0 and Node 1 ->  Bottom wall)
                         0,  # wall 1 (Between Node 1 and Node 2 ->  Right wall)
                         0,  # wall 2 (Between Node 2 and Node 3 ->  Top wall)
                         0]  # wall 3 (Between Node 3 and Node 0 -> Left wall)

    # Checking the boundary conditions in the nodes
    if element.connected_nodes[0].BC > 0:                        # point 0 bottom left
        punkty_z_bc[0] = element.connected_nodes[0].BC

    if element.connected_nodes[1].BC > 0:                        # point 1
        punkty_z_bc[1] = element.connected_nodes[1].BC

    if element.connected_nodes[2].BC > 0:                        # point 2
        punkty_z_bc[2] = element.connected_nodes[2].BC

    if element.connected_nodes[3].BC > 0:                        # point 3
        punkty_z_bc[3] = element.connected_nodes[3].BC

    # Identifying surfaces with boundary conditions
    # A surface has a boundary condition if both its nodes have the same condition
    if punkty_z_bc[0] > 0 and punkty_z_bc[0] == punkty_z_bc[1]:     # wall 0 *bottom* (node 0,1)
        powierzchnie_z_bc[0] = punkty_z_bc[0]

    if punkty_z_bc[1] > 0 and punkty_z_bc[1] == punkty_z_bc[2]:     # wall 1 *right* (node 1,2)
        powierzchnie_z_bc[1] = punkty_z_bc[1]

    if punkty_z_bc[2] > 0 and punkty_z_bc[2] == punkty_z_bc[3]:     # wall 2 *top* (node 2,3)
        powierzchnie_z_bc[2] = punkty_z_bc[2]

    if punkty_z_bc[3] > 0 and punkty_z_bc[3] == punkty_z_bc[0]:     # wall 3 *left* (node 3,0)
        powierzchnie_z_bc[3] = punkty_z_bc[3]

    return powierzchnie_z_bc


class MacierzHBC:
    def __init__(self, element: Element, no_int_nodes: int, alfa: float):
        self.element: Element = element
        self.no_int_nodes: int = no_int_nodes
        self.sciany_z_bc: List[int] = powierzchnie_bc(element)
        self.punkty_bc0: List[Node] = []     #integration points - bottom wall
        self.punkty_bc1: List[Node] = []     #integration points - right wall
        self.punkty_bc2: List[Node] = []     #integration points - top wall
        self.punkty_bc3: List[Node] = []     #integration points - left wall
        self.hbc_side_matrices: List[List[List[float]]] = []
        self.hbc_matrix: List[List[float]] = [[0 for _ in range(4)] for _ in range(4)]

        self.weights: List[float] = []
        for weight in range(no_int_nodes):
            tmp = _universal.weights[weight].x
            self.weights.append(tmp)

        # for weight in self.weights:
        #     print(weight)

        x_cords: List[float] = []
        y_cords: List[float] = []

        for i in range(no_int_nodes ** 2):
            y_cords.append(_universal.integration_points[i].y)
            x_cords.append(_universal.integration_points[i].x)

        x_cords = list(set(x_cords))        # unique values
        y_cords = list(set(y_cords))

        if self.sciany_z_bc[0] > 0:     #if bottom wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, x_cords[i], -1, self.sciany_z_bc[0])
                self.punkty_bc0.append(temp)

        if self.sciany_z_bc[1] > 0:     #if right wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, 1, y_cords[i], self.sciany_z_bc[1])
                self.punkty_bc1.append(temp)

        if self.sciany_z_bc[2] > 0:  # if top wall has bc
            for i in range(no_int_nodes):
                # Reverse the x_cords list for the top wall
                temp = Node(i, x_cords[no_int_nodes - 1 - i], 1, self.sciany_z_bc[2])
                self.punkty_bc2.append(temp)

        if self.sciany_z_bc[3] > 0:  # if left wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, -1, y_cords[no_int_nodes - 1 - i], self.sciany_z_bc[3])
                self.punkty_bc3.append(temp)

        for i in range(4):
            self.hbc_side_matrices.append(self.calculate_surface(i, alfa))

        self.calculate_hbc()

    def print_matrix_hbc(self) -> None:
        for i in range(len(self.hbc_side_matrices)):
            print("Matrix HBC", i+1)
            for col in range(4):
                for row in range(4):
                    value = self.hbc_side_matrices[i][row][col]
                    print(f"{value:.6f}", end="\t")
                print()

    def print_integration_points(self) -> None:
        # Print points
        print("Points on the Bottom Wall (bc0):")
        for point in self.punkty_bc0:
            point.printNode()

        print("\nPoints on the Right Wall (bc1):")
        for point in self.punkty_bc1:
            point.printNode()

        print("\nPoints on the Top Wall (bc2):")
        for point in self.punkty_bc2:
            point.printNode()

        print("\nPoints on the Left Wall (bc3):")
        for point in self.punkty_bc3:
            point.printNode()

    def outer_product(self, vec1: List[float], vec2: List[float]) -> List[List[float]]:
        # Calculate the outer product of two vectors
        return [[vec1[i] * vec2[j] for j in range(len(vec2))] for i in range(len(vec1))]

    def calculate_surface(self, nr_boku: int, conductivity: float) -> List[List[float]]:
        hbc: List[List[float]] = [[0 for j in range(4)] for i in range(self.no_int_nodes)]
        matrixHBC: List[List[float]] = [[0 for j in range(4)] for i in range(4)]

        if self.sciany_z_bc[nr_boku] > 0:
            if nr_boku == 0:
                detJ = calculate_distance(self.element.connected_nodes[0], self.element.connected_nodes[1]) * 0.5
                for i in range(len(hbc)):
                    hbc[i][0] = N1(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    hbc[i][1] = N2(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    hbc[i][2] = N3(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    hbc[i][3] = N4(self.punkty_bc0[i].x, self.punkty_bc0[i].y)

            elif nr_boku == 1:
                detJ = calculate_distance(self.element.connected_nodes[1], self.element.connected_nodes[2]) * 0.5
                for i in range(len(hbc)):
                    hbc[i][0] = N1(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    hbc[i][1] = N2(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    hbc[i][2] = N3(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    hbc[i][3] = N4(self.punkty_bc1[i].x, self.punkty_bc1[i].y)

            elif nr_boku == 2:
                detJ = calculate_distance(self.element.connected_nodes[2], self.element.connected_nodes[3]) * 0.5
                for i in range(len(hbc)):
                    hbc[i][0] = N1(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    hbc[i][1] = N2(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    hbc[i][2] = N3(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    hbc[i][3] = N4(self.punkty_bc2[i].x, self.punkty_bc2[i].y)

            elif nr_boku == 3:
                detJ = calculate_distance(self.element.connected_nodes[3], self.element.connected_nodes[0]) * 0.5
                for i in range(len(hbc)):
                    hbc[i][0] = N1(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    hbc[i][1] = N2(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    hbc[i][2] = N3(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    hbc[i][3] = N4(self.punkty_bc3[i].x, self.punkty_bc3[i].y)

            for row_index, row in enumerate(hbc):
                multiplied_transposed = self.outer_product(row, row)

                # Scale the outer product
                for mt_row_index, mt_row in enumerate(multiplied_transposed):
                    for mt_value_index, mt_value in enumerate(mt_row):
                        scaled_value = conductivity * self.weights[row_index] * mt_value
                        multiplied_transposed[mt_row_index][mt_value_index] = scaled_value

                # Accumulate scaled outer product in matrixHBC
                for hbc_row_index, hbc_row in enumerate(matrixHBC):
                    for hbc_value_index, hbc_value in enumerate(hbc_row):
                        updated_value = matrixHBC[hbc_row_index][hbc_value_index] + \
                                        multiplied_transposed[hbc_row_index][hbc_value_index]
                        matrixHBC[hbc_row_index][hbc_value_index] = updated_value


            # Multiply matrixHBC by detJ after accumulation
            for hbc_row_index, hbc_row in enumerate(matrixHBC):
                for hbc_value_index, hbc_value in enumerate(hbc_row):
                    matrixHBC[hbc_row_index][hbc_value_index] *= detJ

        return matrixHBC

    def calculate_hbc(self) -> None:
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.hbc_matrix[i][j] += self.hbc_side_matrices[k][i][j]

    def print_total_matrix(self) -> None:
        print("\nTotal Matrix HBC:")
        for row in self.hbc_matrix:
            for value in row:
                print(f"{value:.6f}" if isinstance(value, (float, int)) else value, end="\t")
            print()


class WektorP:
    """
    Class implementing the vector of thermal loads {P} for a finite element.
    Considers convective boundary conditions on the surfaces of the element.
    """
    
    def __init__(self, element: Element, no_int_nodes: int, alfa: float, ambient_temp: float):
        self.element: Element = element
        self.no_int_nodes: int = no_int_nodes
        self.alfa: float = alfa
        self.ambient_temp: float = ambient_temp
        self.sciany_z_bc: List[int] = powierzchnie_bc(element)
        self.punkty_bc0: List[Node] = []     #integration points - bottom wall
        self.punkty_bc1: List[Node] = []     #integration points - right wall
        self.punkty_bc2: List[Node] = []     #integration points - top wall
        self.punkty_bc3: List[Node] = []     #integration points - left wall
        self.p_side_vectors: List[List[float]] = []
        self.p_vector: List[float] = [0 for _ in range(4)]

        self.weights: List[float] = []
        for weight in range(no_int_nodes):
            tmp = _universal.weights[weight].x
            self.weights.append(tmp)

        x_cords: List[float] = []
        y_cords: List[float] = []

        for i in range(no_int_nodes ** 2):
            y_cords.append(_universal.integration_points[i].y)
            x_cords.append(_universal.integration_points[i].x)

        x_cords = list(set(x_cords))        # unique values
        y_cords = list(set(y_cords))

        if self.sciany_z_bc[0] > 0:     #if bottom wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, x_cords[i], -1, self.sciany_z_bc[0])
                self.punkty_bc0.append(temp)

        if self.sciany_z_bc[1] > 0:     #if right wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, 1, y_cords[i], self.sciany_z_bc[1])
                self.punkty_bc1.append(temp)

        if self.sciany_z_bc[2] > 0:  # if top wall has bc
            for i in range(no_int_nodes):
                # Reverse the x_cords list for the top wall
                temp = Node(i, x_cords[no_int_nodes - 1 - i], 1, self.sciany_z_bc[2])
                self.punkty_bc2.append(temp)

        if self.sciany_z_bc[3] > 0:  # if left wall has bc
            for i in range(no_int_nodes):
                temp = Node(i, -1, y_cords[no_int_nodes - 1 - i], self.sciany_z_bc[3])
                self.punkty_bc3.append(temp)

        for i in range(4):
            self.p_side_vectors.append(self.calculate_surface(i))

        self.calculate_p_vector()

    def print_p_vectors(self) -> None:
        """
        Displays the vectors P for all surfaces of the element.
        """
        for i in range(len(self.p_side_vectors)):
            print("Vector P", i+1)
            for row in range(4):
                value = self.p_side_vectors[i][row]
                print(f"{value:.6f}", end="\t")
            print()

    def print_integration_points(self) -> None:
        """
        Displays the integration points on all surfaces of the element.
        """
        print("Points on the Bottom Wall (bc0):")
        for point in self.punkty_bc0:
            point.printNode()

        print("\nPoints on the Right Wall (bc1):")
        for point in self.punkty_bc1:
            point.printNode()

        print("\nPoints on the Top Wall (bc2):")
        for point in self.punkty_bc2:
            point.printNode()

        print("\nPoints on the Left Wall (bc3):")
        for point in self.punkty_bc3:
            point.printNode()

    def calculate_surface(self, nr_boku: int) -> List[float]:
        """
        Calculates the vector of thermal loads for a given surface of the element.
        
        Args:
            nr_boku (int): Number of the surface (0-3)
            
        Returns:
            list[float]: Vector of thermal loads for a given surface
        """
        n_funcs: List[List[float]] = [[0 for j in range(4)] for i in range(self.no_int_nodes)]
        p_vector: List[float] = [0 for j in range(4)]

        if self.sciany_z_bc[nr_boku] > 0:
            # Calculations for each surface of the element
            if nr_boku == 0:  # Bottom wall
                # Calculation of the Jacobian for the given surface
                detJ = calculate_distance(self.element.connected_nodes[0], 
                                       self.element.connected_nodes[1]) * 0.5
                # Calculation of the shape functions at the integration points
                for i in range(len(n_funcs)):
                    n_funcs[i][0] = N1(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    n_funcs[i][1] = N2(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    n_funcs[i][2] = N3(self.punkty_bc0[i].x, self.punkty_bc0[i].y)
                    n_funcs[i][3] = N4(self.punkty_bc0[i].x, self.punkty_bc0[i].y)

            elif nr_boku == 1:
                detJ = calculate_distance(self.element.connected_nodes[1], self.element.connected_nodes[2]) * 0.5
                # Calculation of the shape functions at the integration points
                for i in range(len(n_funcs)):
                    n_funcs[i][0] = N1(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    n_funcs[i][1] = N2(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    n_funcs[i][2] = N3(self.punkty_bc1[i].x, self.punkty_bc1[i].y)
                    n_funcs[i][3] = N4(self.punkty_bc1[i].x, self.punkty_bc1[i].y)

            elif nr_boku == 2:
                detJ = calculate_distance(self.element.connected_nodes[2], self.element.connected_nodes[3]) * 0.5
                # Calculation of the shape functions at the integration points
                for i in range(len(n_funcs)):
                    n_funcs[i][0] = N1(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    n_funcs[i][1] = N2(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    n_funcs[i][2] = N3(self.punkty_bc2[i].x, self.punkty_bc2[i].y)
                    n_funcs[i][3] = N4(self.punkty_bc2[i].x, self.punkty_bc2[i].y)

            elif nr_boku == 3:
                detJ = calculate_distance(self.element.connected_nodes[3], self.element.connected_nodes[0]) * 0.5
                # Calculation of the shape functions at the integration points
                for i in range(len(n_funcs)):
                    n_funcs[i][0] = N1(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    n_funcs[i][1] = N2(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    n_funcs[i][2] = N3(self.punkty_bc3[i].x, self.punkty_bc3[i].y)
                    n_funcs[i][3] = N4(self.punkty_bc3[i].x, self.punkty_bc3[i].y)

            for i in range(self.no_int_nodes):
                for j in range(4):
                    temp = n_funcs[i][j] * self.weights[i] * self.ambient_temp
                    p_vector[j] += temp

            # Consider the convective coefficient and Jacobian
            for i in range(4):
                temp = p_vector[i] * self.alfa * detJ
                p_vector[i] = temp

        return p_vector

    def calculate_p_vector(self) -> None:
        for i in range(4):
            for j in range(4):
                    self.p_vector[i] += self.p_side_vectors[j][i]

    def print_total_vector(self) -> None:
        print("\nTotal P Vector:")
        for value in self.p_vector:
            print(f"{value:.3f}" if isinstance(value, (float, int)) else value, end="\t")
