from typing import Optional

import aiohttp
from ambient_backend_api_client import (
    ApiClient,
    Cluster,
    ClustersApi,
    Configuration,
    EventLabel,
)
from ambient_backend_api_client import NodeOutput as Node
from ambient_event_bus_client import Message

from ambient_edge_server import config
from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.repos.node_repo import NodeRepo
from ambient_edge_server.services.cluster_config_service import ClusterConfigService
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.utils import logger


class ClusterEventHandler(BaseHandler):
    def __init__(
        self,
        event_service: EventService,
        cluster_config_service: ClusterConfigService,
        node_repo: NodeRepo,
    ) -> None:
        super().__init__(event_service)
        self.cluster_config_service = cluster_config_service
        self.node_repo = node_repo
        self.api_config: Optional[Configuration] = None

    @property
    def label(self):
        return EventLabel.CLUSTER_EVENT

    async def start(self, api_config: Configuration) -> None:
        logger.debug("Cluster event handler started.")
        self.api_config = api_config

    async def handle(self, msg: Message) -> None:
        logger.info("Handling cluster event. [EventLabel: {}]", self.label)
        logger.debug(f"Handling cluster event: {msg.model_dump_json(indent=4)}")

        # fetch node from from backend
        try:
            current_node_data: Node = self.node_repo.get_node_data(strict=True)
            logger.info("retrieved node data from local repo")
            fetched_node_data = await fetch_node_data(
                current_node_data.id, self.api_config
            )
            logger.info("fetched node data from backend")
            self.node_repo.save_node_data(fetched_node_data)
            logger.debug(
                f"Fetched node data: {fetched_node_data.model_dump_json(indent=4)}"
            )
        except Exception as e:
            logger.error(f"Failed to fetch node data: {e}")
            return

        # create diff
        try:
            diff_result = await self.cluster_config_service.generate_diff(
                cluster_id=fetched_node_data.cluster_id
            )
            if diff_result.is_err():
                logger.error(f"Failed to generate diff: {diff_result.unwrap_err()}")
                return
            diff = diff_result.unwrap()
            logger.debug(f"Generated diff: {diff.model_dump_json(indent=4)}")

            # generate plan
            logger.debug("Generating reconciliation plan ...")
            plan_result = await self.cluster_config_service.plan_reconciliation(diff)
            if plan_result.is_err():
                logger.error(f"Failed to generate plan: {plan_result.unwrap_err()}")
                return
            plan = plan_result.unwrap()
            logger.debug(f"Generated plan: {plan}")

            # execute plan
            logger.debug("Executing reconciliation plan ...")
            await self.cluster_config_service.reconcile(plan=plan)
        except Exception as e:
            logger.error(f"Failed to reconcile cluster: {e}")
            return


async def fetch_node_data(node_id: int, api_config: Configuration) -> Node:
    logger.info("Fetching node data from backend [Node ID: {}]", node_id)
    logger.debug("api_config token: {}", api_config.access_token)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.settings.backend_api_url}/nodes/{node_id}",
            headers={
                "Authorization": f"Bearer {api_config.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        ) as response:
            response.raise_for_status()
            node_data = await response.json()
            return Node.model_validate(node_data)


async def fetch_cluster_data(cluster_id: str, api_config: Configuration) -> Cluster:
    async with ApiClient(api_config) as api_client:
        clusters_api = ClustersApi(api_client)
        cluster = await clusters_api.get_cluster_clusters_cluster_id_get(cluster_id)
        return cluster
