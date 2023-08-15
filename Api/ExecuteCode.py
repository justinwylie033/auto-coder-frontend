from language_mappings import LANGUAGE_MAPPINGS

def execute_code( container, language, code):
    if language not in LANGUAGE_MAPPINGS:
        raise ValueError(f"Unsupported language: {language}")

    command = LANGUAGE_MAPPINGS[language]['command']
    escaped_code = code.replace("'", "\\'")
    cmd = f"{command} -c '{escaped_code}'"
    try:
        exec_status, exec_output = container.exec_run(cmd)
        if exec_status != 0:
            raise RuntimeError(f"Failed to execute code: {exec_output}")
    except Exception as e:
        raise RuntimeError(f"Failed to execute command: {e}")

    return exec_output.decode('utf-8')  # decode bytes object to string

execute_code( 'docker1', 'python', 'print("Hello, world!")')