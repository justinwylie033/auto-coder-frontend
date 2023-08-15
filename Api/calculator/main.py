
# Importing necessary functions
from addition import add
from subtraction import subtract
from multiplication import multiply
from division import divide
from percentage import percentage
from square import square
from sqroot import sqrt

# Dictionary for operators
operators = {
    'add': add,
    'subtract': subtract,
    'multiply': multiply,
    'divide': divide,
    'percentage': percentage,
    'square': square,
    'sqrt': sqrt
}

def calculate(operand1, operand2, operator):
    '''
    This function chooses the correct function to execute based on the operator provided,
    eg. if the operator is "sqrt" it will compute the square root of the operand.

    Parameters:
    operand1 (int/float): The first operand
    operand2 (int/float): The second operand
    operator (str): The operator

    Returns:
    calculation result or throws an error if operator is not recognized
    '''

    if operator not in operators:
        raise ValueError(f'Unknown operator: {operator} is not a recognized operator')  

    # Using the square and sqrt functions
    if operator in ['square', 'sqrt']:
         return operators[operator](operand1)

    return operators[operator](operand1, operand2)
