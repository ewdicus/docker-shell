from typing import Optional, List
import subprocess

from tabulate import tabulate
import typer
import docker
from .text_utils import error_text, info_text, dim_text, bold_text
from .docker_utils import get_docker_client_or_none

DEFAULT_SHELL_COMMAND = '/bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"'

app = typer.Typer()
docker_client = get_docker_client_or_none()


def display_error(text):
    """Display the text prefixed with "Error"""
    typer.echo(f"\n{error_text('Error:')} {text}\n", err=True)


def display_containers_table(containers: List[docker.models.containers.Container]):
    """Display a table of the ID, Name, and Image tags of the running containers"""
    headers = [bold_text("ID"), bold_text("Name"), dim_text("Image Tags")]
    table = [[c.short_id, c.name, dim_text(str(c.image.tags))] for c in containers]
    typer.echo(f"\n{tabulate(table, headers, tablefmt='github')}\n")


def suggest_containers(incomplete: str):
    """Provide suggestions for container names"""
    if not docker_client:
        return []
    containers = docker_client.containers.list()
    # If this returns an array of one item, that'll actually complete.
    return [c.name for c in containers if c.name.startswith(incomplete)]


@app.command()
def main(
    container: Optional[str] = typer.Argument(
        None, help="This can be a container name or ID.", autocompletion=suggest_containers
    ),
    command: str = typer.Option(
        DEFAULT_SHELL_COMMAND,
        "--command",
        "-c",
        envvar="DOCKER_SHELL_COMMAND",
        help="The shell command to run in the container.",
    ),
):
    """
    Shell into a running Docker container by name or ID.

    If run with no arguments, will display running containers. Change the shell command with
    --command, -c, or by setting an env var called DOCKER_SHELL_COMMAND.
    """
    if not docker_client:
        display_error("Could not connect to Docker. Is it running?")
        raise typer.Exit(1)

    if not container:
        containers = docker_client.containers.list()
        if not containers:
            typer.echo(info_text("\nNo containers running\n"))
        else:
            display_containers_table(containers)
        raise typer.Exit()

    try:
        docker_container = docker_client.containers.get(container)
    except docker.errors.NotFound:
        display_error(f"Could not find container {bold_text(container)}")
        raise typer.Exit(1)

    # Very fiddly to try to do this with the docker package. So, instead just run this as a
    # subprocess. We use shell and pass as a single string, because this means we don't need to
    # handle escaping the command.
    subprocess.run(f"docker exec -it {docker_container.name} {command}", shell=True)
    raise typer.Exit()


if __name__ == "__main__":
    app()
