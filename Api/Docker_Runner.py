import docker
from language_mappings import LANGUAGE_MAPPINGS 
import Utils

class DockerRunner:
  def __init__(self):
    self.client = docker.from_env()

  def get_image(self, language: str) -> str:
    # Check if the language exists
    if language in LANGUAGE_MAPPINGS:
      return LANGUAGE_MAPPINGS[language]['image']
    else:
      raise KeyError(f"Language {language} not found in mappings")

  def get_command(self, language: str) -> str:
    # Check if the language exists
    if language in LANGUAGE_MAPPINGS:
      return LANGUAGE_MAPPINGS[language]['command']
    else:
      raise KeyError(f"Language {language} not found in mappings")

  def _get_container(self, image: str) -> docker.models.containers.Container:
    try:
      return self.client.containers.get(image)
    except docker.errors.NotFound:
      return None

  def create_container(self, image: str) -> docker.models.containers.Container:
    container = self._get_container(image)
    if not container:
      container = self.client.containers.run(image, detach=True)
    elif container.status != 'running':
      container.start()
    return container

  def install(self, container: docker.models.containers.Container, packages: list[str]) -> docker.models.execs.ExecResult:
    if packages:
      pkgs = ' '.join(packages)
      cmd = LANGUAGE_MAPPINGS[container.image.tags[0]]['packages'].format(pkgs)
      return container.exec_run(cmd)
    else:
      return None

  def run(self, container: docker.models.containers.Container, code: str) -> docker.models.execs.ExecResult:
    import shlex
    escaped_code = shlex.quote(code)
    cmd = self.get_command(container.image.tags[0]) + ' ' + escaped_code
    return container.exec_run(cmd)

  def handle_error(self, output: docker.models.execs.ExecResult) -> None:
    return Utils.handle_error(output)

if __name__ == "__main__":
  runner = DockerRunner()
  
  # Usage
  language = 'python'
  image = runner.get_image(language)
  command = runner.get_command(language)

  packages = ['numpy', 'pandas']
  code = 'print("Hello world")'

  container = runner.create_container(image)
  if packages:
    runner.install(container, packages)
  output = runner.run(container, code)

  if output.returncode != 0:
    runner.handle_error(output)
