class Global:
    """
    Class storing global parameters of the finite element method (FEM) simulation.
    Contains all constant physical properties and time parameters needed for calculations.
    """
    
    def __init__(self, simTime: float, simStepTime: float, conductivity: float, alfa: float, tot: float, 
                 initialTemp: float, density: float, specificHeat: float, nodesNo: int, elementsNo: int):
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
        self.simTime: float = simTime
        self.simStepTime: float = simStepTime
        self.conductivity: float = conductivity
        self.alfa: float = alfa
        self.tot: float = tot
        self.initialTemp: float = initialTemp
        self.density: float = density
        self.specificHeat: float = specificHeat
        self.nodesNo: int = nodesNo
        self.elementsNo: int = elementsNo

    def print_values(self) -> None:
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