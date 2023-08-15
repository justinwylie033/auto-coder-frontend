import logging
from DockerContainerManager import DockerContainerManager

def RunCode(language, code):
    """
    Run code in a specific language in a Docker container.
    """
    # Initialize DockerContainerManager
    manager = DockerContainerManager()

    # Create Docker container
    container = manager.create_container(language)

    try:
        # Check if inputs are of the expected type and not empty
        if not isinstance(language, str) or not language:
            return {"error": "Invalid or missing language."}, 400
        if not isinstance(code, str) or not code:
            return {"error": "Invalid or missing code."}, 400

        # Install packages required for code execution
        # In this case, we assume no additional packages are required
        # Modify as needed if your code requires certain packages
        # manager.install_packages(container, language, ["package1", "package2"])

        # Run the code in the Docker container
        exec_output = manager.execute_code(container, language, code)

        return {'output': exec_output, 'error': None}, 200

    except Exception as e:
        # Log the error and return an error message
        logging.error(f"An error occurred in RunCode: {str(e)}")
        return {'error': str(e)}, 500

    finally:
        # Ensure the Docker container is stopped and removed even if an error occurs
        try:
            manager.stop_container(container)
            manager.remove_container(container)
        except Exception as e:
            logging.error(f"Failed to clean up Docker container: {str(e)}")

