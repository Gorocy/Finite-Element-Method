from tabulate import tabulate
from typing import List
from mes.macierz.WektorP import WektorP
from mes.classes.Element import Element

class WektorPGlobalny:
    """
    Class implementing the global vector of thermal loads {P} for the entire MES grid.
    Aggregates local vectors of loads into a global vector, considering the connections between elements.
    """
    
    def __init__(self, no_elements: int, no_nodes: int, p_vectors: List[WektorP]):
        """
        Initialization and aggregation of the global vector of thermal loads.
        
        Args:
            no_elements (int): Number of elements in the MES grid
            no_nodes (int): Number of nodes in the MES grid
            p_vectors (list[WektorP]): List of local vectors of loads for each element
        """
        self.p_vectors: List[WektorP] = p_vectors
        # Initialization of the global vector P with zeros
        self.p_vector_global: List[float] = [0 for _ in range(no_nodes)]

        # List of finite elements and their node indices
        self.elements: List[Element] = []
        # Array of node indices for each element (4 nodes per element)
        self.element_IDs: List[List[int]] = [[0] * 4 for _ in range(no_elements)]

        # Getting the elements from the local vectors
        for vector in self.p_vectors:
            self.elements.append(vector.element)

        # Creating an array of node indices for each element
        # Mapping local node indices to global indices
        for i in range(no_elements):
            for j in range(4):
                self.element_IDs[i][j] = self.elements[i].connected_nodes[j].node_id

        # Aggregation of local vectors into a global vector
        for k in range(no_elements):
            p_vector = self.p_vectors[k].p_vector
            for i in range(4):
                # Mapping the local index to the global index (with correction for zero-based indexing)
                global_index = self.element_IDs[k][i] - 1
                # Adding the value from the local vector to the corresponding position in the global vector
                self.p_vector_global[global_index] += p_vector[i]

    def print_global_vector(self) -> None:
        """
        Displays the global vector P in a formatted table.
        Uses the tabulate library for formatting the output.
        Shows the node ID and the corresponding value of the P vector.
        """
        headers = ["Node ID", "P Vector Value"]
        table = [[i + 1, value] for i, value in enumerate(self.p_vector_global)]
        print(tabulate(table, headers=headers, tablefmt="grid"))