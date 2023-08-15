
import logging

def add(num1, num2):
    """
    This function adds two numbers.

    :param num1: First number
    :type num1: float
    :param num2: Second number
    :type num2: float
    :return: Sum of num1 and num2
    :rtype: float
    """
    try:
        # Check if the provided inputs are numbers
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            logging.error('Invalid inputs to the add function. Inputs must be int or float.')
            error_message = f"Provided inputs num1: {num1} of type: {type(num1)} and num2: {num2} of type: {type(num2)}. Both inputs to the add function must be int or float."
            raise ValueError(error_message)

        return num1 + num2

    except Exception as e:
        # Log the exception details and re-raise it
        logging.error(f"An unexpected error occurred while adding num1 and num2. Details: {str(e)}")
        raise
