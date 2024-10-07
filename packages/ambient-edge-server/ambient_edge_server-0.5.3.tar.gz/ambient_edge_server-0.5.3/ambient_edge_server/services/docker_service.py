import docker

from ambient_edge_server.models.docker_models import DockerRoleEnum
from ambient_edge_server.repos.docker_repo import DockerRepo


class DockerService:
    def __init__(self, client: docker.DockerClient, docker_repo: DockerRepo):
        self.client = client
        self.docker_repo = docker_repo

    def get_join_token(self, role: DockerRoleEnum) -> str:
        swarm_info = self.docker_repo.get_swarm_info()
        if role == DockerRoleEnum.Manager:
            return swarm_info.JoinTokens.Manager
        elif role == DockerRoleEnum.Worker:
            return swarm_info.JoinTokens.Worker
        else:
            raise ValueError("Role must be either MANAGER or WORKER")
