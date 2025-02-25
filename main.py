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

def separate_data():
    """Funkcja pomocnicza do wizualnego oddzielenia sekcji wyników"""
    print("="*111)

# Słowniki i listy do przechowywania danych
data = {}          # Parametry symulacji
nodes = {}         # Węzły siatki
elements = []      # Elementy siatki
node_section = False # Flaga do identyfikacji sekcji węzłów
element_section = False # Flaga do identyfikacji sekcji elementów
bc_section = False # Flaga do identyfikacji sekcji warunków brzegowych
bc_nodes = set()   # Zbiór węzłów z warunkami brzegowymi
h_matrices = []    # Lista lokalnych macierzy H
hbc_matrices = []  # Lista lokalnych macierzy HBC
summed_matrices = []  # Lista zsumowanych macierzy H+HBC
p_vectors = []     # Lista lokalnych wektorów P
c_matrices = []    # Lista lokalnych macierzy C

# Wczytanie danych z pliku
plik = "data/Test1_4_4.txt"
# plik = "data/Test2_4_4_MixGrid.txt"
# plik = "data/Test3_31_31_kwadrat.txt"

# Pierwsza iteracja - wczytanie węzłów i elementów
with open(plik, "r") as file:
    for line in file:
        line = line.strip()

        # Sekcja węzłów
        if line.startswith("*Node"):
            node_section = True
            element_section = False
            bc_section = False
            continue

        # Sekcja elementów
        elif line.startswith("*Element"):
            element_section = True
            node_section = False
            bc_section = False
            continue

        elif line.startswith("*"):
            node_section = False
            element_section = False

        # Wczytywanie węzłów
        if node_section:
            parts = line.split(',')
            if len(parts) == 3:
                node_id, x, y = [int(parts[0]), float(parts[1]), float(parts[2])]
                node = Node(node_id, x, y)
                nodes[node_id] = node

        # Wczytywanie elementów
        if element_section:
            if line:
                element_id, *element_nodes = map(int, line.split(','))
                element = Element(element_id)
                nodes_in_element = [nodes[node_id] for node_id in element_nodes]
                for node in nodes_in_element:
                    element.addNode(node)
                elements.append(element)

        # Wczytywanie parametrów symulacji
        parts = line.split()
        if len(parts) < 3:
            key = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            data[key] = value
        else:
            key = parts[0] + " " + parts[1]
            value = parts[2]
            data[key] = value

# Druga iteracja - wczytanie warunków brzegowych
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

# Ustawienie warunków brzegowych dla węzłów
for node_id in bc_nodes:
    if node_id in nodes:
        nodes[node_id].BC = 1

# Inicjalizacja parametrów globalnych symulacji
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

# Utworzenie siatki MES
grid = Grid(global_data.nodesNo, global_data.elementsNo)
for node in nodes.values():
    grid.addNode(node)

# Obliczenia dla każdego elementu
for element in elements:
    grid.addElement(element)

    # Obliczenie lokalnej macierzy H
    # to macierz opisująca transport ciepła między poszczególnymi węzłami siatki
    temp_h = MatrixH(element, no_integration_nodes, global_data.conductivity)
    h_matrices.append(temp_h)

    # Obliczenie lokalnej macierzy HBC
    # to macierz opisująca transport ciepła wnikającego przez ściany objęte warunkiem brzegowym konwekcji, 
    # HBC jest zbiorem wartości opisujących wpływ konwekcji na układ na powierzchni elementu 
    # zależy od zmiennej temperatury tej powierzchni.
    temp_hbc = MacierzHBC(element, no_integration_nodes, global_data.alfa)
    hbc_matrices.append(temp_hbc.hbc_matrix)

    # Obliczenie lokalnego wektora P
    # to wektor obciążeń opisujący wpływ temperatury otoczenia na poszczególne węzły siatki elementu
    temp_p_vector = WektorP(element, no_integration_nodes, global_data.alfa, global_data.tot)
    p_vectors.append(temp_p_vector)

    # Obliczenie lokalnej macierzy C
    # to macierz opisująca stopień akumulacji energii cieplnej przez węzły
    temp_c = MacierzC(global_data.specificHeat, global_data.density, element)
    c_matrices.append(temp_c)

# Sumowanie macierzy H i HBC
for h_matrix, hbc_matrix in zip(h_matrices, hbc_matrices):

    summed_matrix = MatrixH(h_matrix.element, no_integration_nodes, global_data.conductivity)

    summed_matrix.add_hbc_matrix(hbc_matrix)

    summed_matrices.append(summed_matrix)

# Wyświetlenie wyników
separate_data()
grid.printGrid()
separate_data()

# Agregacja macierzy globalnych
print("\n Macierz H Globalna")
h_glob = MacierzHGlobalna(global_data.elementsNo, global_data.nodesNo, summed_matrices)
h_glob.print_global_matrix()

print("\n Wektor P Globalny")
p_glob = WektorPGlobalny(global_data.elementsNo, global_data.nodesNo, p_vectors)
p_glob.print_global_vector()

print("\n Macierz C Globalna")
c_glob = MacierzCGlobalna(global_data.elementsNo, global_data.nodesNo, c_matrices)
c_glob.print_global_matrix()

print("\n Macierz C Globalna po podzieleniu przez dtau")
c_glob.divide_matrix_by_dtau(global_data.simStepTime)
c_glob.print_global_matrix()

# Symulacja czasowa
t0_vector = [global_data.initialTemp] * global_data.nodesNo
current_time = global_data.simStepTime

headers = [f"Node {i+1}" for i in range(len(t0_vector))]
table_data = []
min_max_table_data = []

# Główna pętla symulacji
while current_time <= global_data.simTime:
    # Pobranie aktualnych macierzy globalnych
    macierz_h_globalna = h_glob
    wektor_p_globalny = p_glob
    macierz_c_globalna = c_glob

    # Obliczenie układu równań do rozwiązania
    matrix_c_h_summed = sum_matrices(macierz_c_globalna.c_matrix_global, macierz_h_globalna.h_matrix_global)
    matrix_c_multiplied = macierz_c_globalna.multiply_matrix_by_vector(t0_vector)
    vectors_summed = sum_vectors(matrix_c_multiplied, wektor_p_globalny.p_vector_global)

    # Rozwiązanie układu równań
    solution = gaussian_elimination(matrix_c_h_summed, vectors_summed)
    
    # Zapisanie wyników
    row = [f"{value:.2f}" for value in solution]
    table_data.append([f"Time {current_time}"] + row)
    
    # Tablica z min i max temperaturami
    min_value = min(solution)
    max_value = max(solution)
    min_max_table_data.append([f"Time {current_time}", f"Min: {min_value:.9f}", f"Max: {max_value:.9f}"])
    print("time: ", current_time, "min: ", min_value, "max: ", max_value)
    # Przygotowanie do następnego kroku czasowego
    t0_vector = solution
    current_time += global_data.simStepTime

# Wyświetlenie wyników symulacji
print(tabulate(table_data, headers=["Time"] + headers, tablefmt="grid"))
print(tabulate(min_max_table_data, headers=["Time", "Min", "Max"], tablefmt="grid"))