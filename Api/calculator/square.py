
from typing import Union

def square(num: Union[int, float]) -> Union[int, float]:
    """
    This function calculates the square of a number.

    Raises a value error if the input is not a number.

    Parameters:
        num (Union[int, float]) : A number

    Returns:
        Union[int, float] : square of the number
    """

    # Validate input
    if not isinstance(num, (int, float)):
        raise ValueError(f"Input must be an integer or a float, not {type(num).__name__}")

    # Compute square
    return num * num


from square import square
