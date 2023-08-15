
import logging
from addition import add
from division import divide

# Create a custom logger
logger = logging.getLogger(__name__)

def percentage(num, total):
    """
    This function computes the percentage of a given number.

    Parameters:
    num : This is the number of which to find the percentage.
    total : This is the total or whole amount against which the percentage is to be computed.

    Returns:
    percentage : This is the computed percentage of the given number against the total.
    """

    # Check if the inputs are numbers
    if not isinstance(num, (int, float)) or not isinstance(total, (int, float)):
        logger.error("Both the num and total should be numbers")
        raise TypeError("Both the num and total should be numbers")

    # Check if the total is greater than num
    if total < num:
        logger.error("The total should be greater than or equal to num")
        raise ValueError("The total should be greater than or equal to num")

    # Error check to validate that the total is not zero to avoid division by zero error.
    if total == 0:
        logger.error("The total cannot be zero!")
        raise ValueError("The total cannot be zero!")

    # Calculate the percentage of the given number against the total by dividing the number by the total and multiplying by 100.
    percentage = divide(num, total) * 100

    # Return the computed percentage.
    return percentage
