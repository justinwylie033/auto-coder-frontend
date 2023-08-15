
from .addition import add
from .subtraction import subtract
from .multiplication import multiply as multiply_func
from .division import divide

def multiply(num1, num2):
    """
    This function multiplies two numbers.
    
    Args:
    num1 (float or int): The first number.
    num2 (float or int): The second number.
    
    Returns:
    float or int: The product of the two numbers, None: If invalid inputs.
    """
    
    if not isinstance(num1, (int, float)):
        raise TypeError("(multiply) num1 must be a number")

    if not isinstance(num2, (int, float)):
        raise TypeError("(multiply) num2 must be a number")

    try:
        product = multiply_func(num1, num2)
    except Exception as e:
        # Log and rethrow the exact exception
        logging.error(f"Error occurred: {str(e)}")
        raise

    return product
