import math

def functionX(x: float) -> float:
    """
    One-dimensional function used in Gaussian integration calculations.
    Represents a second-degree polynomial.
    
    Args:
        x (float): Independent variable
    
    Returns:
        float: Value of the function 5x² + 3x + 6
    """
    return 5 * x ** 2 + 3 * x + 6


def functionXY(x: float, y: float) -> float:
    """
    Two-dimensional function used in Gaussian integration calculations.
    Represents a second-degree polynomial with respect to both variables.
    
    Args:
        x (float): First independent variable
        y (float): Second independent variable
    
    Returns:
        float: Value of the function 5x²y² + 3xy + 6
    """
    return 5 * x ** 2 * y ** 2 + 3 * x * y + 6