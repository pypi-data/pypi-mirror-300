from typing import List

from ambient_backend_api_client import Configuration
from docker import DockerClient

from ambient_edge_server.event_handlers.authorize_to_registry_handler import (
    AuthorizeRegistryHandler,
)
from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.event_handlers.cluster_event_handler import ClusterEventHandler
from ambient_edge_server.event_handlers.deploy_service_handler import (
    DeployServiceHandler,
)
from ambient_edge_server.event_handlers.run_command_handler import RunCommandHandler
from ambient_edge_server.event_handlers.test_handler import TestHandler
from ambient_edge_server.repos.node_repo import NodeRepo
from ambient_edge_server.services.cluster_config_service import ClusterConfigService
from ambient_edge_server.services.command_service import CommandService
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.services.registry_service import RegistryServiceFactory


class HandlerService:
    def __init__(
        self,
        event_service: EventService,
        docker_client: DockerClient,
        registry_svc_factory: RegistryServiceFactory,
        cmd_svc: CommandService,
        cluster_config_service: ClusterConfigService,
        node_repo: NodeRepo,
    ) -> None:
        self._handlers: List[BaseHandler] = [
            TestHandler(event_service),
            DeployServiceHandler(event_service, docker_client=docker_client),
            AuthorizeRegistryHandler(
                event_svc=event_service, registry_svc_factory=registry_svc_factory
            ),
            RunCommandHandler(event_svc=event_service, cmd_svc=cmd_svc),
            ClusterEventHandler(
                event_service=event_service,
                cluster_config_service=cluster_config_service,
                node_repo=node_repo,
            ),
        ]

    async def start(self, api_config: Configuration):
        for handler in self._handlers:
            if hasattr(handler, "start"):
                await handler.start(api_config)
            await handler.subscribe()

    def get_handlers(self):
        return self._handlers
