from LanguageModels import get_gpt4_completion, get_gpt4_completion
from Utils import code_extractor
import logging

def GenerateCode(language, code_requirements):
    """
    Generate code based on the provided language and code requirements.
    """
    try:
        # Check if inputs are of the expected type and not empty
        if not isinstance(language, str) or not language:
            return {"error": "Invalid or missing language."}, 400
        if not isinstance(code_requirements, str) or not code_requirements:
            return {"error": "Invalid or missing code requirements."}, 400

        # Generate the prompt for the language model
        prompt = f"Programming Language: {language} \n Project Requirements: {code_requirements}\n only return code and code comments."
        
        # Get the code completion from the language model and extract the code
        code = code_extractor(get_gpt4_completion(prompt))

        return {'code': code.strip(), 'language': language, }, 200
    except Exception as e:
        # Log the error and return an error message
        logging.error(f"An error occurred in GenerateCode: {str(e)}")
        return {"error": str(e)}, 500
