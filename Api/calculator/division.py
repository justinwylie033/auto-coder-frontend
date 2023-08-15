
# import dependencies
from .addition import add
from .subtraction import subtract
from .multiplication import multiply
from .percentage import percentage
from .square import square
from .squareroot import sqrt

def divide(num1, num2):
    """
    This function divides one number by another.
    
    Parameters:
    num1 (float): The dividend
    num2 (float): The divisor
    Returns:
    float: The quotient of the division.
    Errors:
    ValueError: If division by zero is attempted.
    """

    # Check if num2 is zero because division by zero is undefined
    if num2 == 0:
        raise ValueError("Error! Division by zero is undefined.")
    
    # Perform division and return quotient
    return num1 / num2
