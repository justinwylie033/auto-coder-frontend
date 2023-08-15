import docker
import uuid
from language_mappings import LANGUAGE_MAPPINGS

class DockerContainerManager:

    def __init__(self):
        self.client = docker.from_env()

    def generate_name(self):
        return str(uuid.uuid4())

    def create_container(self, language):
        if language not in LANGUAGE_MAPPINGS:
            raise ValueError(f"Unsupported language: {language}")

        image = LANGUAGE_MAPPINGS[language]['image']
        name = self.generate_name()
        try:
            container = self.client.containers.run(image, name=name, detach=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create container: {e}")

        return container

    def get_container(self, name):
        try:
            return self.client.containers.get(name)
        except Exception as e:
            raise RuntimeError(f"Failed to get container: {e}")

    def start_container(self, container):
      if container.status == 'exited':
          container.start()
      return container

    def remove_container(self, container):
        try:
            container.stop()
            container.remove()
        except Exception as e:
            raise RuntimeError(f"Failed to remove container: {e}")

    def install_packages(self, container, language, packages):
        if language not in LANGUAGE_MAPPINGS:
            raise ValueError(f"Unsupported language: {language}")

        command = LANGUAGE_MAPPINGS[language]['packages']
        pkgs = ' '.join(packages)
        try:
            exec_status, exec_output = container.exec_run(command.format(pkgs))
            if exec_status != 0:
                raise RuntimeError(f"Failed to install packages: {exec_output}")
        except Exception as e:
            raise RuntimeError(f"Failed to execute command: {e}")

    def execute_code(self, container, language, code):
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

    def stop_container(self, container):
        """
        Stop a running Docker container
        """
        try:
            if container.status == 'running':
                container.stop()
        except Exception as e:
            raise RuntimeError(f"Failed to stop container: {e}")

    def pause_container(self, container):
        """
        Pause a running Docker container
        """
        try:
            if container.status == 'running':
                container.pause()
        except Exception as e:
            raise RuntimeError(f"Failed to pause container: {e}")

    def resume_container(self, container):
        """
        Resume a paused Docker container
        """
        try:
            if container.status == 'paused':
                container.unpause()
        except Exception as e:
            raise RuntimeError(f"Failed to resume container: {e}")

    def restart_container(self, container):
        """
        Restart a Docker container
        """
        try:
            container.restart()
        except Exception as e:
            raise RuntimeError(f"Failed to restart container: {e}")