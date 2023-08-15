from Utils import code_extractor, get_gpt4_completion
import logging

def ImproveCode(code:str, problem:str, code_output:str):
    """
    Improve a given piece of code.

    Parameters:
    code (str): The original code.
    problem (str): The problem with the original code.
    code_output (str): The output of the original code.

    Returns:
    A dictionary with the improved code or an error message.
    """
    try:
        # Validate inputs
        if not code or not isinstance(code, str):
            return {'error': 'Invalid code.'}
        if not problem or not isinstance(problem, str):
            return {'error': 'Invalid problem.'}
        if not code_output or not isinstance(code_output, str):
            return {'error': 'Invalid code output.'}

        logging.info('Improving code...')
        prompt = f"Please fix: {code} \n  Problem: {problem and code_output}\n only return code and code comments. no annotations, must compile and run. Code must be complete and correct. snippets will not be accepted. all input must be hardcoded. code must be efficient and readable."
        improved_code = code_extractor(get_gpt4_completion(prompt))

        return {'code': improved_code.strip()}
    except Exception as e:
        logging.error(f'Error improving code: {str(e)}')
        return {'error': str(e)}
