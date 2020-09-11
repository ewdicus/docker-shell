from typing import Optional
import docker


def get_docker_client_or_none() -> Optional[docker.DockerClient]:
    try:
        return docker.from_env()
    except Exception:
        return None
