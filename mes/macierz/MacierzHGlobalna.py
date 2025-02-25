from tabulate import tabulate

class MacierzHGlobalna:
    """
    Class implementing the global matrix of heat conduction [H] for the entire MES grid.
    Aggregates local H matrices into a global matrix, considering the connections between elements.
    """
    
    def __init__(self, no_elements, no_nodes, h_matrices):
        """
        Initialization and aggregation of the global matrix of heat conduction.
        
        Args:
            no_elements (int): Number of elements in the MES grid
            no_nodes (int): Number of nodes in the MES grid
            h_matrices (list[MatrixH]): List of local H matrices for each element
        """
        self.no_nodes = no_nodes
        self.h_matrices = h_matrices
        self.elements = []  # List of finite elements
        # Array of node indices for each element (4 nodes per element)
        self.element_IDs = [[0] * 4 for _ in range(no_elements)]
        # Initialization of the global matrix H with zeros
        self.h_matrix_global = [[0] * no_nodes for _ in range(no_nodes)]

        # Getting the elements from the local matrices
        for matrix in self.h_matrices:
            self.elements.append(matrix.element)

        # Creating an array of node indices for each element
        # Mapping local node indices to global indices
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Aggregation of local matrices into a global matrix
        for k in range(no_elements):
            h_matrix = self.h_matrices[k].total_matrix
            for i in range(4):
                for j in range(4):
                    # Mapping local indices (0-3) to global indices (1-n)
                    global_row = self.element_IDs[k][i]
                    global_col = self.element_IDs[k][j]
                    # Adding the value from the local matrix to the corresponding position in the global matrix
                    self.h_matrix_global[global_row - 1][global_col - 1] += h_matrix[i][j]

    def print_global_matrix(self):
        """
        Displays the global matrix H in a formatted table.
        Uses the tabulate library for formatting the output.
        Numbers the rows and columns according to the global node indices.
        """
        headers = [""] + list(range(1, self.no_nodes + 1))
        table = [[i + 1] + row for i, row in enumerate(self.h_matrix_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))
