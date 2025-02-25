from tabulate import tabulate

class MacierzCGlobalna:
    """
    Class implementing the global matrix of thermal capacity for the entire MES grid.
    Aggregates local thermal capacity matrices into a global matrix.
    """
    
    def __init__(self, no_elements, no_nodes, c_matrices):
        """
        Initialization and aggregation of the global matrix of thermal capacity.
        
        Args:
            no_elements (int): Number of elements in the MES grid
            no_nodes (int): Number of nodes in the MES grid
            c_matrices (list[MacierzC]): List of local thermal capacity matrices
        """
        self.no_nodes = no_nodes
        self.c_matrices = c_matrices
        self.elements = []  # List of finite elements
        # Array of node indices for each element
        self.element_IDs = [[0] * 4 for _ in range(no_elements)]
        # Initialization of the global matrix C
        self.c_matrix_global = [[0] * no_nodes for _ in range(no_nodes)]

        # Getting the elements from the local matrices
        for matrix in self.c_matrices:
            self.elements.append(matrix.element)

        # Creating an array of node indices for each element
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Aggregation of local matrices into a global matrix
        for k in range(no_elements):
            c_matrix = self.c_matrices[k].total_matrix
            for i in range(4):
                for j in range(4):
                    global_row = self.element_IDs[k][i]
                    global_col = self.element_IDs[k][j]
                    # Adding the value from the local matrix to the corresponding position in the global matrix
                    self.c_matrix_global[global_row - 1][global_col - 1] += c_matrix[i][j]

    def print_global_matrix(self):
        """
        Displays the global matrix of thermal capacity in a formatted table.
        Uses the tabulate library for formatting the output.
        """
        headers = [""] + list(range(1, self.no_nodes + 1))
        table = [[i + 1] + row for i, row in enumerate(self.c_matrix_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))

    def divide_matrix_by_dtau(self, dtau):
        """
        Divides all elements of the global matrix by the time step.
        Operation required in the finite difference method.
        
        Args:
            dtau (float): Time step [s]
        """
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                self.c_matrix_global[i][j] /= dtau

    def multiply_matrix_by_vector(self, t0_vector):
        """
        Multiplies the global matrix C by the temperature vector.
        
        Args:
            t0_vector (list[float]): Temperature vector at nodes
            
        Returns:
            list[float]: Result vector of the multiplication of the matrix by the vector
        """
        result_vector = [0] * self.no_nodes
        for i in range(self.no_nodes):
            for j in range(self.no_nodes):
                result_vector[i] += self.c_matrix_global[i][j] * t0_vector[j]
        return result_vector