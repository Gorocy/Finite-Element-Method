import math

def functionX(x):
    """
    Funkcja jednowymiarowa używana w obliczeniach całkowania metodą Gaussa.
    Reprezentuje wielomian drugiego stopnia.
    
    Args:
        x (float): Zmienna niezależna
    
    Returns:
        float: Wartość funkcji 5x² + 3x + 6
    """
    return 5 * x ** 2 + 3 * x + 6


def functionXY(x, y):
    """
    Funkcja dwuwymiarowa używana w obliczeniach całkowania metodą Gaussa.
    Reprezentuje wielomian drugiego stopnia względem obu zmiennych.
    
    Args:
        x (float): Pierwsza zmienna niezależna
        y (float): Druga zmienna niezależna
    
    Returns:
        float: Wartość funkcji 5x²y² + 3xy + 6
    """
    return 5 * x ** 2 * y ** 2 + 3 * x * y + 6