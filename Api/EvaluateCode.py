from Utils import get_gpt4_completion
import logging

def EvaluateCode(code:str, code_requirements:str, output:str):
    """
    Evaluate a piece of code against its requirements and output.

    Parameters:
    code (str): The code to evaluate.
    code_requirements (str): The requirements the code should meet.
    output (str): The output of the code.

    Returns:
    A dictionary with the evaluation result (as a boolean) or an error message.
    """
    try:
        # Validate inputs
        if not code or not isinstance(code, str):
            return {'error': 'Invalid code.'}
        if not code_requirements or not isinstance(code_requirements, str):
            return {'error': 'Invalid code requirements.'}
        if not output or not isinstance(output, str):
            return {'error': 'Invalid output.'}

        logging.info('Evaluating code...')
        prompt = (f"The following code: \n\n{code}\n\n was run and the output was: \n\n{output}\n\n"
                  f"The requirements for the code were: \n\n{code_requirements}\n\n"
                  "Does the code and output meet the requirements for a functional program to a high degree? Please answer 'yes' or 'no'.")
        evaluation = get_gpt4_completion(prompt)

        logging.info(f'Evaluation: {evaluation}')

        if "yes" in evaluation.lower():
            return {'evaluation': True}
        else:
            return {'evaluation': False}
    except Exception as e:
        logging.error(f'Error evaluating code: {str(e)}')
        return {'error': str(e)}
