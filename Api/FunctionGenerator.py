import logging
import json
from Utils import get_gpt4_completion, code_extractor
import os
import warnings

# Suppress specific warning
warnings.filterwarnings('ignore', category=UserWarning,
                        message='.*Blowfish has been deprecated.*')

# Suppress ERROR logs from the root logger
logging.getLogger('root').setLevel(logging.CRITICAL)


FUNCTION_TEMPLATE = """Each function template MUST be in the following JSON parsable format - NO SINGLE QUOTES - NO EXPLAINATION OR NUMBERED STEPS - within a nameless list of dictionaries [{}] format:
language: [language],
file_name: [path_to_file/file.extension], FILE NAMES/PATHS MUST BE PRESENT/VALID (no placeholders allowed) - NO Unauthorized directories such as root to be used, always use relative paths.
function_name: [function_name],
function_description: [function_description],
parameters: [comma separated list],
dependencies: [comma separated list],
return_value: [return_value(s) in comma separated list].
Remember to avoid using single quotes in the function descriptions i.e user's should be users or calculator's should be calculators.
Do not write the content of the functions."""


def parse_functions_from_response(ai_response):
    try:
        ai_response = ai_response.replace('""""', '""').replace("'", '"').replace(
            '’', '"')  # Handle four consecutive quotes and replace single quotes and apostrophes with double quotes
        functions = json.loads(ai_response)
        print("converted to json")
    except json.JSONDecodeError as e:
        logging.error(
            f"Error converting AI response to JSON: {e}, ai_response: {ai_response}")
        functions = None
    return functions


def generate_initial_functions(code_requirements):
    ai_response = get_gpt4_completion(
        """Imagine three different programming experts are answering this question.
        All experts will write down 1 function of their thinking,
        then share it with the group.
        Then all experts will go on to the next function, etc.
        If any expert realises they're wrong at any point then they leave."""
        f"Please define a list of functions in a language of your choice that satisfies {code_requirements}. "
        f"function's should link together and use each others functionality"
        f"I want as many reusable, modular functions as possible with use of utility functions if applicable. "
        f"Code splitting should also be utilized, essential for frontend and backend programs, and correct file extensions must be used, e.g. .jsx for react. "
        f"{FUNCTION_TEMPLATE}"
    )
    functions = parse_functions_from_response(ai_response)
    return functions


def get_program_recommendations(initial_functions):
    ai_response = get_gpt4_completion(
        str(initial_functions) +
        f" Please provide additional functions: {FUNCTION_TEMPLATE} please create/update the main method as necessary."
    )
    print("Your Program currently has the following functionality:\n")

    for function in initial_functions:
        print(
            f"{function['function_name']}: {function['function_description']}")

    functions = parse_functions_from_response(ai_response)

    if functions is None:
        print("No additional functions to add.")
    elif functions:
        for function in functions:
            user_decision = input(
                f"Would you like to add the following function to your program: {function['function_name']} {function['function_description']}? y/n: ")
            if user_decision == "y":
                initial_functions.append(function)
                print(f"Function added: {function['function_name']}")

    return initial_functions


def remove_python_word(code):
    return code.replace('python', '')


def construct_filetree(functions):

    filetree = {function['file_name'] for function in functions}

    return filetree


def generate_code_for_function(function, functions, filetree):
    ai_response = get_gpt4_completion(
        f"Please write the code for the following function in {function['language']}:\n"
        f"Function name: {function['function_name']}\n"
        f"Description: {function['function_description']}\n"
        f"Parameters: {function['parameters']}\n"
        f"dependencies must be imported such as functions created in other files or libraries. "
        f"functions must be complete."
        f"boilerplate code must be included"
        f"All will be in the current directory. you can ONLY import these functions {functions} within these files {filetree} "
        f"Import statements must be CORRECT, CAREFULLY constructed, and relative to the filetree {filetree} you are currently in {function['file_name']}. we are already in the correct folder, we don't need to reference it in imports or we will get an error. No usage of '.' or './' in import paths, and all imports must follow established conventions without any weird or non-standard behavior."
        f"This function is part of the group of functions we have: {functions} within the filetree: {filetree}"
        f"YOU MUST reference and import functions relitave to all functions: {functions} within the filetree {filetree}"
        f"DO NOT write classes or OOP unless absolutely necessary!!!"
        f"You are currently only writing this function: {function['function_name']} do not generate any additional functions examples or ANYTHING else - 1 FUNCTION PER FILE - NO EXCEPTIONS"
        f"Ensure that the code follows best practices for the {function['language']} language, includes proper validation and error handling, and avoids redundancy. The code must be clear, well-commented, and maintainable, adhering to proper naming conventions and indentation. Do not use unconventional or 'hacky' solutions. If applicable, follow secure coding practices and consider the needs for testing. Respect dependencies and their versions, ensuring compatibility. Follow the {function['language']} specific directives related to import statements and file structure as previously detailed."
        f"If we are in the main method here are the appropriate functions {functions} and filetree {filetree} to be used in FLAWLESS {function['language']} import conventions NO WEIRD OR INCORRECT imports thinking step by step logically"

    )
    return ai_response


def write_code_to_file(function, code):
    os.makedirs(os.path.dirname(function['file_name']), exist_ok=True)
    cleaned_code = remove_python_word(code)  # Removing the word "python"
    with open(function['file_name'], 'a') as f:
        f.write(cleaned_code)
        f.write("\n\n")  # add newlines to separate functions


def extract_file_names(functions):
    file_names = {function['file_name'] for function in functions}
    return file_names


def begin_working_on_code(functions):
    print("\nBeginning work on implementing functions...")
    for function in functions:
        print(f"Working on function: {function['function_name']}...")
        code = code_extractor(generate_code_for_function(
            function, functions, filetree))
        write_code_to_file(function, code)
        print(f"Successfully written code for {function['function_name']}.\n")


def improve_code(functions, filetree):
    print("\nImproving the code quality for each file...")
    file_names = extract_file_names(functions)
    for file in file_names:
        print(f"Improving code quality in file: {file}...")
        try:
            with open(file, 'r') as f:
                current_code = f.read()

                # Ask AI for a possible improvement
                improved_code = get_gpt4_completion(
                    f"Here is some code {current_code}, how could it be improved by an expert developer to be production-level code?"
                    f"dependencies must be imported such as functions created in other files or libraries. "
                    f"functions must be complete."
                    f"boilerplate code must be included"
                    f"All will be in the current directory. you can ONLY import these functions {functions} within these files {file_names} "
                    f"Import statements must be CORRECT, CAREFULLY constructed, and relative to the filetree {filetree} you are currently in {function['file_name']}. we are already in the correct folder, we don't need to reference it in imports or we will get an error. No usage of '.' or './' in import paths, and all imports must follow established conventions without any weird or non-standard behavior."
                    f"This function is part of the group of functions we have: {functions} within the filetree: {filetree}"
                    f"YOU MUST reference and import functions relitave to all functions: {functions} within the filetree {filetree}"
                    f"DO NOT write classes or OOP unless absolutely necessary!!!"
                    f"You are currently only improving this function: {current_code} do not generate any additional functions examples or ANYTHING else - 1 FUNCTION PER FILE - NO EXCEPTIONS"

                )

            improved_code = code_extractor(improved_code)
            if improved_code is not None:
                cleaned_code = remove_python_word(
                    improved_code)  # Removing the word "python"

                if cleaned_code:
                    with open(file, 'w') as f:
                        f.write(cleaned_code)
                    print(f"Successfully improved code in file {file}.\n")
                else:
                    print(f"Unable to extract improved code for file {file}\n")
            else:
                print(
                    f"Improvement extraction returned None for file {file}\n")
        except IOError as e:
            print(f"Error processing file {file}: {str(e)}\n")


def print_generated_files(filetree):
    print("\nHere are the contents of the generated files:")
    for file_name in filetree:
        print(f"\nFile: {file_name}")
        try:
            with open(file_name, 'r') as f:
                print(f.read())
        except IOError as e:
            print(f"Error reading file {file_name}: {str(e)}")


# Existing code
code_requirements = input("Please specify the program you require: ")
print("\nGenerating initial functions based on your requirements...")
initial_functions = generate_initial_functions(code_requirements)

print("\nHere are the initial functions generated:")
for function in initial_functions:
    print(f"- {function['function_name']}: {function['function_description']}")

print("\nGetting program recommendations...")
functions = get_program_recommendations(initial_functions)

filetree = construct_filetree(functions)
print("\nWorking on the implementation...")
begin_working_on_code(functions)

print("\nImproving the code quality...")
improve_code(functions, filetree)

print_generated_files(filetree)  # Calling the new function

print("\nDone! Your code has been generated and optimized.")
