class Global:
    """
    Class storing global parameters of the finite element method (FEM) simulation.
    Contains all constant physical properties and time parameters needed for calculations.
    """
    
    def __init__(self, simTime, simStepTime, conductivity, alfa, tot, initialTemp, 
                 density, specificHeat, nodesNo, elementsNo):
        """
        Initializes the global parameters of the simulation.
        
        Args:
            simTime (float): Total simulation time [s]
            simStepTime (float): Simulation time step [s]
            conductivity (float): Heat conductivity coefficient [W/(m·K)]
            alfa (float): Heat exchange coefficient [W/(m²·K)]
            tot (float): Ambient temperature [°C]
            initialTemp (float): Initial temperature [°C]
            density (float): Material density [kg/m³]
            specificHeat (float): Material specific heat [J/(kg·K)]
            nodesNo (int): Number of nodes in the mesh
            elementsNo (int): Number of elements in the mesh
        """
        self.simTime = simTime
        self.simStepTime = simStepTime
        self.conductivity = conductivity
        self.alfa = alfa
        self.tot = tot
        self.initialTemp = initialTemp
        self.density = density
        self.specificHeat = specificHeat
        self.nodesNo = nodesNo
        self.elementsNo = elementsNo

    def print_values(self):
        """
        Displays all simulation global parameters.
        Helper function for debugging and verifying input data.
        """
        print("SimulationTime:", self.simTime)
        print("SimulationStepTime:", self.simStepTime)
        print("Conductivity:", self.conductivity)
        print("Alfa:", self.alfa)
        print("Tot:", self.tot)
        print("InitialTemp:", self.initialTemp)
        print("Density:", self.density)
        print("SpecificHeat:", self.specificHeat)
        print("Nodes number:", self.nodesNo)
        print("Elements number:", self.elementsNo)