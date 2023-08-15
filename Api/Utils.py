import re
import ast
from LanguageModels import get_gpt4_completion, get_gpt_completion
import logging
import docker 

# Set up logging
logging.basicConfig(level=logging.INFO)

# FILE_INFO_MAPPING dictionary maps languages to their respective run commands and file extensions.
FILE_INFO_MAPPING = {
    'python': ('python', '.py'),
    'javascript': ('node', '.js'),
    'cpp': ('g++', '.cpp'),
    'java': ('java', '.java'),
    'jsx': ('node', '.jsx'),
    'php': ('php', '.php'),
    'swift': ('swift', '.swift'),
    'c#': ('dotnet', '.cs'),
    'go': ('go', '.go'),
}

# LANGUAGE_MAPPING dictionary maps languages to their respective docker image tags.
LANGUAGE_MAPPING = {
    'python': 'python:latest',
    'javascript': 'node:latest',
    'cpp': 'gcc:latest',
    'java': 'openjdk:latest',
    'jsx': 'node:latest',
    'php': 'php:latest',
    'swift': 'swift:latest',
    'c#': 'mcr.microsoft.com/dotnet/sdk:latest',
    'go': 'golang:latest',
}

# PACKAGE_INSTALLATION_COMMANDS dictionary maps languages to their respective package installation commands.
PACKAGE_INSTALLATION_COMMANDS = {
    "python": "pip install {}",
    "javascript": "npm install {}",
    "cpp": "apt-get install {}",
    "java": "apt-get install {}",
    "jsx": "npm install {}",
    "php": "composer require {}",
    "swift": "swift package add {}",
    "c#": "dotnet add package {}",
    "go": "go get {}",
}

def get_docker_image(language):
    try:
        docker_image = LANGUAGE_MAPPING.get(language.lower())
        if not docker_image:
            raise ValueError(f"Unsupported language: {language}")
        return docker_image
    except Exception as e:
        logging.error(f"Error in get_docker_image: {str(e)}")
        raise

def code_extractor(text):
    if not isinstance(text, str):
        raise TypeError("Input text must be string.")
    matches = re.findall(r'```(.*?)```', text, re.DOTALL)
    return '\n'.join(matches) if matches else None

def package_extractor(s):
    match = re.search(r'\[[^\]]*\]', s)
    return ast.literal_eval(match.group()) if match else []

def get_or_create_container(client, docker_image, container_name):
    try:
        return client.containers.get(container_name)
    except docker.errors.NotFound:
        logging.info(f"Container {container_name} does not exist. Creating a new one.")
        return client.containers.run(docker_image, detach=True, name=container_name)

def execute_command_in_container(container, command):
    exit_code, output = container.exec_run(command)
    if exit_code != 0:
        raise RuntimeError(f"Command execution failed with exit code: {exit_code}. Output: {output.decode('utf-8').strip()}")
    return output.decode('utf-8').strip()

def install_packages(language, code, container_name):
    if not language or not code:
        raise ValueError("Both language and code must be provided.")

    docker_image = get_docker_image(language)
    client = docker.from_env()
    container = get_or_create_container(client, docker_image, container_name)
    packages = package_extractor(get_gpt4_completion(f"please write an array of packages [] required for this script {code}."))
    logging.info(f"Installing packages: {packages}")

    installation_command = PACKAGE_INSTALLATION_COMMANDS.get(language.lower())
    if not installation_command:
        raise ValueError(f"Unsupported language: {language}")
    installation_command = installation_command.format(" ".join(packages))

    if not packages:
        return "No packages required"
    return execute_command_in_container(container, installation_command)

def run_code(language, code, container_name):
    try:
        docker_image = get_docker_image(language)
        client = docker.from_env()
        container = get_or_create_container(client, docker_image, container_name)
        
        command = FILE_INFO_MAPPING.get(language.lower())[0]
        if not command:
            raise ValueError(f"Unsupported language: {language}")
        
        command += " " + code  # Construct the full command
        
        output = execute_command_in_container(container, command)
        
        return True, output
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return False, str(e)
    

run_code("python", "print('hello world')", "test")