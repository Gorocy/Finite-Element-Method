from mes.classes.Node import Node
from mes.classes.Element import Element
from mes.classes.Global import Global
from mes.classes.Grid import Grid
from mes.macierz.MacierzH import MatrixH, no_integration_nodes
from mes.macierz.WektorP import MacierzHBC, WektorP
from mes.macierz.MacierzHGlobalna import MacierzHGlobalna
from mes.macierz.WektorPGlobalny import WektorPGlobalny
from mes.macierz.MacierzCGlobalna import MacierzCGlobalna
from mes.macierz.MacierzOperacje import sum_matrices, sum_vectors
from mes.gauss.Eliminacja import gaussian_elimination
from mes.macierz.MacierzC import MacierzC
from tabulate import tabulate
from typing import Dict, List, Set

def separate_data() -> None:
    """Helper function to visually separate sections of results"""
    print("="*111)

# Dictionaries and lists to store data
data: Dict[str, str] = {}          # Simulation parameters
nodes: Dict[int, Node] = {}        # Nodes of the grid
elements: List[Element] = []       # Elements of the grid
node_section: bool = False         # Flag to identify the node section
element_section: bool = False      # Flag to identify the element section
bc_section: bool = False           # Flag to identify the boundary condition section
bc_nodes: Set[int] = set()         # Set of nodes with boundary conditions
h_matrices: List[MatrixH] = []     # List of local H matrices
hbc_matrices: List[MacierzHBC] = []# List of local HBC matrices
summed_matrices: List[MatrixH] = []# List of summed H+HBC matrices
p_vectors: List[WektorP] = []      # List of local P vectors
c_matrices: List[MacierzC] = []    # List of local C matrices

# Reading data from a file
plik: str = "data/Test1_4_4.txt"
# plik: str = "data/Test2_4_4_MixGrid.txt"
# plik: str = "data/Test3_31_31_kwadrat.txt"

# First iteration - reading nodes and elements
with open(plik, "r") as file:
    for line in file:
        line = line.strip()

        # Node section
        if line.startswith("*Node"):
            node_section = True
            element_section = False
            bc_section = False
            continue

        # Element section
        elif line.startswith("*Element"):
            element_section = True
            node_section = False
            bc_section = False
            continue

        elif line.startswith("*"):
            node_section = False
            element_section = False

        # Reading nodes
        if node_section:
            parts = line.split(',')
            if len(parts) == 3:
                node_id, x, y = [int(parts[0]), float(parts[1]), float(parts[2])]
                node = Node(node_id, x, y)
                nodes[node_id] = node

        # Reading elements
        if element_section:
            if line:
                element_id, *element_nodes = map(int, line.split(','))
                element = Element(element_id)
                nodes_in_element = [nodes[node_id] for node_id in element_nodes]
                for node in nodes_in_element:
                    element.addNode(node)
                elements.append(element)

        # Reading simulation parameters
        parts = line.split()
        if len(parts) < 3:
            key = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            data[key] = value
        else:
            key = parts[0] + " " + parts[1]
            value = parts[2]
            data[key] = value

# Second iteration - reading boundary conditions
with open(plik, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith("*BC"):
            bc_section = True
            node_section = False
            element_section = False
            continue

        if bc_section:
            if line:
                bc_nodes.update(map(int, line.split(',')))

# Setting boundary conditions for nodes
for node_id in bc_nodes:
    if node_id in nodes:
        nodes[node_id].BC = 1

# Initializing simulation parameters
global_data = Global(
    simTime=int(data.get('SimulationTime', 0)),
    simStepTime=int(data.get('SimulationStepTime', 0)),
    conductivity=int(data.get('Conductivity', 0)),
    alfa=int(data.get('Alfa', 0)),
    tot=int(data.get('Tot', 0)),
    initialTemp=int(data.get('InitialTemp', 0)),
    density=int(data.get('Density', 0)),
    specificHeat=int(data.get('SpecificHeat', 0)),
    nodesNo=int(data.get('Nodes number', 0)),
    elementsNo=int(data.get('Elements number', 0))
)
global_data.print_values()

# Creating the MES grid
grid = Grid(global_data.nodesNo, global_data.elementsNo)
for node in nodes.values():
    grid.addNode(node)

# Calculations for each element
for element in elements:
    grid.addElement(element)

    # Calculation of the local H matrix
    # matrix describing the heat transfer between individual nodes of the grid
    temp_h = MatrixH(element, no_integration_nodes, global_data.conductivity)
    h_matrices.append(temp_h)

    # Calculation of the local HBC matrix
    # matrix describing the heat transfer through the walls subject to a convective boundary condition, 
    # HBC is a set of values describing the influence of convection on the system on the surface of the element 
    # depends on the variable temperature of this surface.
    temp_hbc = MacierzHBC(element, no_integration_nodes, global_data.alfa)
    hbc_matrices.append(temp_hbc.hbc_matrix)

    # Calculation of the local P vector
    # vector describing the influence of the ambient temperature on the individual nodes of the element grid
    temp_p_vector = WektorP(element, no_integration_nodes, global_data.alfa, global_data.tot)
    p_vectors.append(temp_p_vector)

    # Calculation of the local C matrix
    # matrix describing the degree of heat energy accumulation by nodes
    temp_c = MacierzC(global_data.specificHeat, global_data.density, element)
    c_matrices.append(temp_c)

# Summing matrices H and HBC
for h_matrix, hbc_matrix in zip(h_matrices, hbc_matrices):

    summed_matrix = MatrixH(h_matrix.element, no_integration_nodes, global_data.conductivity)

    summed_matrix.add_hbc_matrix(hbc_matrix)

    summed_matrices.append(summed_matrix)

# Displaying results
separate_data()
grid.printGrid()
separate_data()

# Aggregation of global matrices
print("\n Global H Matrix")
h_glob = MacierzHGlobalna(global_data.elementsNo, global_data.nodesNo, summed_matrices)
h_glob.print_global_matrix()

print("\n Global P Vector")
p_glob = WektorPGlobalny(global_data.elementsNo, global_data.nodesNo, p_vectors)
p_glob.print_global_vector()

print("\n Global C Matrix")
c_glob = MacierzCGlobalna(global_data.elementsNo, global_data.nodesNo, c_matrices)
c_glob.print_global_matrix()

print("\n Global C Matrix after dividing by dtau")
c_glob.divide_matrix_by_dtau(global_data.simStepTime)
c_glob.print_global_matrix()

# Time simulation
t0_vector: List[float] = [global_data.initialTemp] * global_data.nodesNo
current_time: int = global_data.simStepTime

headers: List[str] = [f"Node {i+1}" for i in range(len(t0_vector))]
table_data: List[List[str]] = []
min_max_table_data: List[List[str]] = []

# Main simulation loop
while current_time <= global_data.simTime:
    # Getting the current global matrices
    macierz_h_globalna = h_glob
    wektor_p_globalny = p_glob
    macierz_c_globalna = c_glob

    # Calculation of the system of equations to solve
    matrix_c_h_summed = sum_matrices(macierz_c_globalna.c_matrix_global, macierz_h_globalna.h_matrix_global)
    matrix_c_multiplied = macierz_c_globalna.multiply_matrix_by_vector(t0_vector)
    vectors_summed = sum_vectors(matrix_c_multiplied, wektor_p_globalny.p_vector_global)

    # Solving the system of equations
    solution = gaussian_elimination(matrix_c_h_summed, vectors_summed)
    
    # Saving results
    row = [f"{value:.2f}" for value in solution]
    table_data.append([f"Time {current_time}"] + row)
    
    # Array with min and max temperatures
    min_value = min(solution)
    max_value = max(solution)
    min_max_table_data.append([f"Time {current_time}", f"Min: {min_value:.9f}", f"Max: {max_value:.9f}"])
    print("time: ", current_time, "min: ", min_value, "max: ", max_value)
    # Preparing for the next time step
    t0_vector = solution
    current_time += global_data.simStepTime

# Displaying simulation results
print(tabulate(table_data, headers=["Time"] + headers, tablefmt="grid"))
print(tabulate(min_max_table_data, headers=["Time", "Min", "Max"], tablefmt="grid"))