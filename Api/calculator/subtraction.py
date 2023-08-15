
# Import any necessary dependencies
from calculator.multiplication import multiply
from calculator.addition import add
from calculator.subtraction import subtract
from calculator.division import divide
from calculator.square import square
from calculator.squareroot import sqrt
from calculator.percentage import percentage

def subtract(num1, num2):
    """
    This function subtracts one number from another.

    Parameters:
    num1 (float): The first number.
    num2 (float): The second number.

    Returns:
    difference (float): The result of subtracting the second number from the first.
    """

    # Validate the input parameters
    if not (isinstance(num1, (int, float)) and isinstance(num2, (int, float))):
        raise ValueError("Both num1 and num2 must be numbers")

    # Logic to subtract one number from another
    difference = num1 - num2
    difference = round(difference, 2)  # round to 2 decimal places for consistency
    
    return difference  # Returns the calculated value
